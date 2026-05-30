import json
import logging
import re
from typing import List, Dict, Any, Tuple
import google.generativeai as genai
import chromadb
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings

from app.config import settings
from app.database import get_all_cars
from app.models import Car, ChatMessage, ChatResponse

logger = logging.getLogger("rag")
logging.basicConfig(level=logging.INFO)

# Define custom Gemini Embedding Function for ChromaDB
class GeminiEmbeddingFunction(EmbeddingFunction):
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)

    def __call__(self, input: Documents) -> Embeddings:
        # Generate embeddings using the standard and widely supported embedding-001 model
        response = genai.embed_content(
            model="models/embedding-001",
            content=input,
            task_type="retrieval_document"
        )
        return response['embedding']

# Fallback basic text search in case ChromaDB or Gemini is not fully configured
def keyword_search(query: str, cars: List[Car]) -> List[int]:
    query_lower = query.lower()
    matches = []
    
    # 1. Map color synonyms for Marathi, Hindi, Spanish, English
    color_map = {
        "white": ["white", "pandhri", "pandhra", "safed", "shweta", "blanco", "blanc"],
        "black": ["black", "kali", "kala", "kalyat", "negro", "noir"],
        "red": ["red", "lal", "tambada", "tambadi", "rojo", "rouge"],
        "blue": ["blue", "nila", "nili", "azura", "azul", "bleu"],
        "silver": ["silver", "chandni", "plata", "argent"],
        "grey": ["grey", "gray", "rakhadi", "gris"],
        "bronze": ["bronze", "bronz", "tambya"]
    }
    
    # Check if a specific color is explicitly requested
    requested_color = None
    for color, synonyms in color_map.items():
        if any(syn in query_lower for syn in synonyms):
            requested_color = color
            break

    # Check if a specific body type is requested
    requested_body = None
    if "sedan" in query_lower or "seadan" in query_lower:
        requested_body = "sedan"
    elif "hatchback" in query_lower or "hatch" in query_lower:
        requested_body = "hatchback"
    elif "mpv" in query_lower or "mvp" in query_lower or "minivan" in query_lower:
        requested_body = "mpv"

    # Check if a specific engine size is requested (e.g. "1 lit", "1.5L", "2.0")
    requested_engine = None
    # Regex to find numbers like "1 lit", "1.5 l", "2.5 lit", "1.2 lit"
    engine_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:lit|l(?:iter)?|cc)?", query_lower)
    if engine_match:
        try:
            val = float(engine_match.group(1))
            # Only match realistic small capacities (1.0 to 4.0) to avoid catching prices/years
            if 0.8 <= val <= 5.0:
                requested_engine = val
        except ValueError:
            pass

    for car in cars:
        score = 0
        
        # STRICT FILTERS: If the user asked for a specific criteria, we MUST filter out non-matching options!
        if requested_color and car.color.lower() != requested_color:
            continue
        if requested_body and car.body_type.lower() != requested_body:
            continue
        if requested_engine:
            # Tolerant match within 0.1L (e.g., "1 lit" matches 1.0L, "2 lit" matches 2.0L)
            if abs(car.engine_capacity - requested_engine) > 0.15:
                continue

        # Criteria boosts
        if car.brand.lower() in query_lower:
            score += 15
        if car.model.lower() in query_lower:
            score += 15
        if requested_color and car.color.lower() == requested_color:
            score += 20
        if requested_body and car.body_type.lower() == requested_body:
            score += 20
        if requested_engine and abs(car.engine_capacity - requested_engine) <= 0.1:
            score += 20
            
        if "cheap" in query_lower or "budget" in query_lower or "sasta" in query_lower or "affordable" in query_lower:
            if car.price < 1500000: # under 15 Lakhs
                score += 10
        if "luxury" in query_lower or "premium" in query_lower or "rich" in query_lower:
            if car.price > 4000000: # over 40 Lakhs
                score += 10
                
        # Base semantic boost
        if any(word in car.description.lower() for word in query_lower.split() if len(word) > 3):
            score += 3
            
        if score > 0 or (requested_color or requested_body or requested_engine):
            # Include in results if it matches our strict filter conditions
            matches.append((car.id, score))
            
    # Sort by score descending
    matches.sort(key=lambda x: x[1], reverse=True)
    return [m[0] for m in matches]


class RageEngine:
    def __init__(self):
        self.cars = get_all_cars()
        self.initialized = False
        self.chroma_client = None
        self.collection = None
        self.api_key = settings.GEMINI_API_KEY
        
        if not self.api_key:
            logger.warning("GEMINI_API_KEY is not set in environment! RAG will run in simulation/fallback mode.")
            return
            
        try:
            # Initialize ChromaDB client (using persistent directory)
            self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
            self.emb_fn = GeminiEmbeddingFunction(api_key=self.api_key)
            
            # Get or create collection
            # To ensure clean database on server restart, we delete and recreate or just reset the collection
            try:
                self.chroma_client.delete_collection("cars_collection")
            except Exception:
                pass # Collection did not exist
                
            # Test the embedding function to ensure it works, otherwise trigger fallback immediately
            self.emb_fn(["test"])
            
            self.collection = self.chroma_client.create_collection(
                name="cars_collection",
                embedding_function=self.emb_fn
            )
            
            # Load cars into Chroma
            self._load_cars_into_vector_db()
            self.initialized = True
            logger.info("ChromaDB and RAG Engine initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB/Gemini: {e}. Fallback mode active.")
            self.initialized = False

    def _load_cars_into_vector_db(self):
        documents = []
        ids = []
        metadatas = []
        
        for car in self.cars:
            # Build semantic description document
            doc_text = (
                f"ID: {car.id}. Brand: {car.brand}. Model: {car.model}. Year: {car.year}. Color: {car.color}. "
                f"Price: ₹{car.price:.2f}. Condition: {car.condition}. Engine Capacity: {car.engine_capacity}L. "
                f"Body Type: {car.body_type}. Fuel Type: {car.fuel_type}. Rating: {car.rating} stars. "
                f"Mileage: {car.mileage} kilometers. Description: {car.description}"
            )
            documents.append(doc_text)
            ids.append(str(car.id))
            metadatas.append({
                "id": car.id,
                "brand": car.brand,
                "model": car.model,
                "price": car.price,
                "body_type": car.body_type,
                "condition": car.condition,
                "year": car.year,
                "color": car.color
            })
            
        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        logger.info(f"Loaded {len(documents)} cars into ChromaDB.")

    def search_semantic_cars(self, query: str, limit: int = 5) -> List[Car]:
        if not self.initialized or not self.collection:
            logger.info("RAG not initialized. Performing keyword fallback search.")
            matched_ids = keyword_search(query, self.cars)
            return [car for car in self.cars if car.id in matched_ids][:limit]
            
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=limit
            )
            
            matched_ids = []
            if results and 'ids' in results and len(results['ids']) > 0:
                matched_ids = [int(x) for x in results['ids'][0]]
                
            # Fetch full car details maintaining Chroma relevance order
            matched_cars = []
            car_dict = {car.id: car for car in self.cars}
            for cid in matched_ids:
                if cid in car_dict:
                    matched_cars.append(car_dict[cid])
            return matched_cars
        except Exception as e:
            logger.error(f"Semantic search failed: {e}. Falling back to keywords.")
            matched_ids = keyword_search(query, self.cars)
            return [car for car in self.cars if car.id in matched_ids][:limit]

    def chat_query(self, user_msg: str, chat_history: List[ChatMessage]) -> ChatResponse:
        # Detect simple language indicator or rely on Gemini
        # Search Chroma for top 6 matching cars to feed context
        relevant_cars = self.search_semantic_cars(user_msg, limit=6)
        
        # Format context
        context_str = ""
        for i, car in enumerate(relevant_cars):
            context_str += (
                f"- [CAR ID {car.id}] {car.brand} {car.model} ({car.year})\n"
                f"  Price: ₹{car.price:.2f}, Condition: {car.condition}, Engine: {car.engine_capacity}L, Body: {car.body_type}, Color: {car.color}\n"
                f"  Rating: {car.rating}/5 stars, Fuel: {car.fuel_type}, Mileage: {car.mileage} kilometers\n"
                f"  Description: {car.description}\n\n"
            )
            
        if not self.api_key:
            # Simulating response if no Gemini API Key exists
            lang = "English"
            if any(word in user_msg.lower() for word in ["hola", "como", "carro", "barato"]):
                lang = "Spanish"
                msg = (
                    "¡Hola! (Simulado: Falta GEMINI_API_KEY en .env)\n"
                    "Para activar el chatbot de IA premium con Gemini, por favor agrega tu `GEMINI_API_KEY` "
                    "en el archivo `.env` en la carpeta `backend/`.\n\n"
                    "Aquí están los autos recomendados según tu búsqueda:\n"
                )
            elif any(word in user_msg.lower() for word in ["मुझे", "कार", "सस्ता", "नमस्ते"]):
                lang = "Hindi"
                msg = (
                    "नमस्ते! (सिम्युलेटेड: .env में GEMINI_API_KEY गायब है)\n"
                    "जेमिनी के साथ प्रीमियम AI चैटबॉट को सक्षम करने के लिए, कृपया `backend/` फ़ोल्डर में "
                    "`.env` फ़ाइल में अपना `GEMINI_API_KEY` जोड़ें।\n\n"
                    "यहाँ आपकी खोज के आधार पर अनुशंसित कारें हैं:\n"
                )
            else:
                msg = (
                    "Hello! (Simulated: GEMINI_API_KEY is missing from .env)\n"
                    "To enable the premium Gemini LLM RAG chatbot, please configure a valid `GEMINI_API_KEY` "
                    "in your `backend/.env` file.\n\n"
                    "Here are the recommended cars matching your query:\n"
                )
            
            for car in relevant_cars:
                msg += f"- **{car.brand} {car.model}** ({car.year}) - ₹{car.price:.2f} ({car.rating} Stars)\n"
                
            return ChatResponse(
                response=msg,
                suggested_car_ids=[c.id for c in relevant_cars],
                language=lang
            )

        try:
            # Set up Gemini generative model
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            
            # Format chat history for context
            history_str = ""
            for h in chat_history[-6:]:  # include last 6 messages
                role_name = "User" if h.role == "user" else "Assistant"
                history_str += f"{role_name}: {h.content}\n"
                
            system_prompt = (
                "You are Dream cars Assistant, an extremely premium and helpful AI car sales specialist.\n"
                "Your goal is to guide the user in selecting the perfect car from our fleet.\n\n"
                "RULES:\n"
                "1. ALWAYS respond in the EXACT language used by the user. If the user writes in Hindi, reply in Hindi. If Marathi (e.g. 'mala white car pahijel'), reply in Marathi. If English, reply in English. (This is critical!).\n"
                "2. Base your recommendations strictly on the provided context cars.\n"
                "3. In your response, give a beautiful and convincing comparison or sales pitch highlighting the features (price, condition, engine, age, rating, color).\n"
                "4. CRITICAL FILTER REQUIREMENT: Your returned 'suggested_car_ids' list MUST contain ONLY the car IDs that directly and strictly match the user's explicit filter requests. Do NOT include any extra, loose, or non-matching options! For example:\n"
                "   - If the user asks for a 'white' car (e.g., 'safed', 'pandhri', 'white'), you MUST ONLY include IDs of cars whose Color is 'White'.\n"
                "   - If the user asks for '1.0L' engine capacity (e.g. '1 lit', '1.0 liter', '1000 cc'), you MUST ONLY include IDs of cars whose Engine Capacity is exactly 1.0.\n"
                "   - If the user asks for 'sedan', you MUST ONLY include sedans. Do NOT show hatchbacks or MPVs. if they ask for 'hatchback', ONLY include hatchbacks. If they ask for 'MPV', ONLY include MPVs.\n"
                "   - If no cars match their filters exactly, return an empty array [] for 'suggested_car_ids' and politely explain that we don't have that specific match in our active fleet.\n"
                "5. You MUST structure your output as a VALID JSON object. Do not include any markdown backticks around the JSON. The response must contain exactly two fields:\n"
                "   - 'response': A string containing your conversational reply in the user's language.\n"
                "   - 'suggested_car_ids': An array of integers representing the IDs of the cars you are recommending/talking about in order of relevance to the query, adhering strictly to Rule 4.\n\n"
                f"CHAT HISTORY FOR CONTEXT:\n{history_str}\n"
                f"RELEVANT CARS IN INVENTORY:\n{context_str}\n"
                f"USER'S QUERY: {user_msg}"
            )
            
            # Request JSON from Gemini
            response = model.generate_content(
                system_prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            
            response_text = response.text.strip()
            # In case Gemini adds markdown blocks despite our prompt, clean them
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            data = json.loads(response_text)
            
            # Detect language using a simple heuristic or prompt summary
            # We can ask Gemini or use a light regex check to determine language
            detected_lang = "English"
            if any(ord(char) > 255 for char in user_msg):
                # likely Hindi, Devanagari, or other non-latin character set
                detected_lang = "Hindi/Non-English"
            elif any(word in user_msg.lower() for word in ["hola", "que", "buenos", "carro"]):
                detected_lang = "Spanish"
                
            return ChatResponse(
                response=data.get("response", "Here are some cars for you!"),
                suggested_car_ids=data.get("suggested_car_ids", [c.id for c in relevant_cars]),
                language=detected_lang
            )
            
        except Exception as e:
            logger.error(f"Gemini API generation failed: {e}. Returning safe fallback.")
            return ChatResponse(
                response=f"I found some great options for you in our collection! (Fallback: {e})",
                suggested_car_ids=[c.id for c in relevant_cars],
                language="English"
            )

# Create single instance to be used across endpoints
rag_engine = RageEngine()
