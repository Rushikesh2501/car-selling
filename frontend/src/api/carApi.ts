import type { Car, FilterState } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

export const fetchCars = async (filters: Partial<FilterState> = {}): Promise<Car[]> => {
  try {
    const params = new URLSearchParams();
    
    if (filters.brand) params.append('brand', filters.brand);
    if (filters.bodyType) params.append('body_type', filters.bodyType);
    if (filters.condition) params.append('condition', filters.condition);
    if (filters.minPrice) params.append('min_price', filters.minPrice);
    if (filters.maxPrice) params.append('max_price', filters.maxPrice);
    if (filters.minEngine) params.append('min_engine', filters.minEngine);
    if (filters.maxEngine) params.append('max_engine', filters.maxEngine);
    if (filters.minRating) params.append('min_rating', filters.minRating);
    if (filters.color) params.append('color', filters.color);
    if (filters.sortBy) params.append('sort_by', filters.sortBy);

    const response = await fetch(`${API_BASE_URL}/cars?${params.toString()}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch cars: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error in fetchCars:', error);
    throw error;
  }
};
