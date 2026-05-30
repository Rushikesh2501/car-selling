from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn

from app.config import settings
from app.models import Car, ChatRequest, ChatResponse
from app.database import get_all_cars
from app.rag import rag_engine

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for high-end car selling catalog with embedded multi-language RAG chatbot",
    version="1.0.0"
)

# Set up CORS for React frontend (development and production hosts)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production readiness and easy deployment, we allow all or configure specifically
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/cars", response_model=List[Car])
def read_cars(
    brand: Optional[str] = None,
    body_type: Optional[str] = None,
    condition: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_engine: Optional[float] = None,
    max_engine: Optional[float] = None,
    min_rating: Optional[float] = None,
    color: Optional[str] = None,
    sort_by: Optional[str] = None  # price_asc, price_desc, rating_desc, engine_asc, engine_desc, year_desc
):
    cars = get_all_cars()
    
    # 1. Filter results
    filtered_cars = []
    for car in cars:
        if brand and car.brand.lower() != brand.lower():
            continue
        if body_type and car.body_type.lower() != body_type.lower():
            continue
        if condition and car.condition.lower() != condition.lower():
            continue
        if min_price is not None and car.price < min_price:
            continue
        if max_price is not None and car.price > max_price:
            continue
        if min_engine is not None and car.engine_capacity < min_engine:
            continue
        if max_engine is not None and car.engine_capacity > max_engine:
            continue
        if min_rating is not None and car.rating < min_rating:
            continue
        if color and car.color.lower() != color.lower():
            continue
        filtered_cars.append(car)
        
    # 2. Sort results
    if sort_by:
        if sort_by == "price_asc":
            filtered_cars.sort(key=lambda x: x.price)
        elif sort_by == "price_desc":
            filtered_cars.sort(key=lambda x: x.price, reverse=True)
        elif sort_by == "rating_desc":
            filtered_cars.sort(key=lambda x: x.rating, reverse=True)
        elif sort_by == "engine_asc":
            filtered_cars.sort(key=lambda x: x.engine_capacity)
        elif sort_by == "engine_desc":
            filtered_cars.sort(key=lambda x: x.engine_capacity, reverse=True)
        elif sort_by == "year_desc":
            filtered_cars.sort(key=lambda x: x.year, reverse=True)
            
    return filtered_cars

@app.post("/api/chat", response_model=ChatResponse)
def chatbot_chat(request: ChatRequest):
    return rag_engine.chat_query(request.message, request.history)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "rag_initialized": rag_engine.initialized,
        "api_key_configured": bool(settings.GEMINI_API_KEY)
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
