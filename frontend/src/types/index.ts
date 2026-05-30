export interface Car {
  id: number;
  brand: string;
  model: string;
  year: number;
  price: number;
  condition: string;
  engine_capacity: number;
  body_type: string;
  rating: number;
  image_url: string;
  description: string;
  mileage: number;
  fuel_type: string;
  color: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  suggestedCarIds?: number[];
  timestamp: Date;
}

export interface FilterState {
  brand: string;
  bodyType: string;
  condition: string;
  minPrice: string;
  maxPrice: string;
  minEngine: string;
  maxEngine: string;
  minRating: string;
  color: string;
  sortBy: string;
}
