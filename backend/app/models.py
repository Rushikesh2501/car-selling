from pydantic import BaseModel, Field
from typing import List, Optional

class Car(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    price: float
    condition: str
    engine_capacity: float  # e.g. 1.5, 2.0, 3.0
    body_type: str  # sedan, hatchback, mpv
    rating: float  # calculated based on condition and age (1-5)
    image_url: str
    description: str
    mileage: int
    fuel_type: str
    color: str

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    response: str
    suggested_car_ids: List[int]
    language: str
