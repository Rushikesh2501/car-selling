import type { ChatMessage } from '../types';

const API_BASE_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000') + '/api';

export interface ChatResponseData {
  response: string;
  suggested_car_ids: number[];
  language: string;
}

export const sendChatMessage = async (
  message: string,
  history: ChatMessage[]
): Promise<ChatResponseData> => {
  try {
    // Format frontend history to match FastAPI backend schema
    const formattedHistory = history.map((msg) => ({
      role: msg.role,
      content: msg.content,
    }));

    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        history: formattedHistory,
      }),
    });

    if (!response.ok) {
      throw new Error(`Failed to send message: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error in sendChatMessage:', error);
    throw error;
  }
};
