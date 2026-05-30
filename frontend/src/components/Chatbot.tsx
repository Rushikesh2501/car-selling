import React, { useState, useRef, useEffect } from 'react';
import type { ChatMessage } from '../types';
import { sendChatMessage } from '../api/chatApi';

interface ChatbotProps {
  isOpen: boolean;
  onClose: () => void;
  onSuggestedCarsReceived: (carIds: number[]) => void;
}

const QUICK_PROMPTS = [
  { label: '🇬🇧 Hatchbacks under ₹10 Lakhs', text: 'Show me fuel efficient hatchbacks under 10 Lakhs' },
  { label: '🇪🇸 Sedanes familiares (Spanish)', text: '¿Cuáles son los mejores sedanes de lujo en excelente estado?' },
  { label: '🇮🇳 1.5L इंजन वाली MPV (Hindi)', text: 'मुझे 1.5L इंजन क्षमता वाली आरामदायक MPV कारें दिखाएं' }
];

export const Chatbot: React.FC<ChatbotProps> = ({
  isOpen,
  onClose,
  onSuggestedCarsReceived,
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content:
        "Hello! I am your Dream cars Assistant. 🚗\n" +
        "You can ask me anything about our inventory in **any language** (English, Hindi, Spanish, Marathi, etc.).\n" +
        "I will reply in that language and dynamically find/sort the perfect cars on your screen!",
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll messages to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMessage: ChatMessage = {
      id: Math.random().toString(36).substr(2, 9),
      role: 'user',
      content: text,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // API call to backend RAG
      const result = await sendChatMessage(text, [...messages, userMessage]);

      const assistantMessage: ChatMessage = {
        id: Math.random().toString(36).substr(2, 9),
        role: 'assistant',
        content: result.response,
        suggestedCarIds: result.suggested_car_ids,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);

      // Notify parent to highlight and sort these cars
      if (result.suggested_car_ids && result.suggested_car_ids.length > 0) {
        onSuggestedCarsReceived(result.suggested_car_ids);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage: ChatMessage = {
        id: Math.random().toString(36).substr(2, 9),
        role: 'assistant',
        content:
          "⚠️ Apologies! I had trouble connecting to the service. Please make sure the backend is running, and that you have configured your GEMINI_API_KEY in your backend's `.env` file.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSendMessage(inputValue);
  };

  return (
    <div className={`chatbot-drawer glass-panel ${isOpen ? 'open' : ''}`}>
      <div className="chat-header">
        <div className="chat-agent-info">
          <div className="chat-avatar">CAR</div>
          <div className="chat-details">
            <span className="chat-name">Car buying assistant</span>
          </div>
        </div>
        <button className="chat-close-btn" onClick={onClose} aria-label="Close Chat">
          ×
        </button>
      </div>

      <div className="chat-messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`message-bubble ${msg.role}`}>
            <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>
            <div className="message-meta">
              <span>
                {msg.timestamp.toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </span>
              {msg.role === 'assistant' && msg.suggestedCarIds && msg.suggestedCarIds.length > 0 && (
                <span style={{ color: 'var(--accent)', fontWeight: 'bold' }}>
                  • Sorted {msg.suggestedCarIds.length} cars
                </span>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="typing-indicator message-bubble assistant">
            <div className="typing-dot" />
            <div className="typing-dot" />
            <div className="typing-dot" />
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompts Container if history is short */}
      {messages.length <= 2 && !isLoading && (
        <div
          style={{
            padding: '0 16px 12px 16px',
            display: 'flex',
            flexDirection: 'column',
            gap: '8px',
          }}
        >
          <span style={{ fontSize: '11px', color: 'var(--text-dark)', fontWeight: '700', textTransform: 'uppercase' }}>
            Try Multi-Language RAG:
          </span>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            {QUICK_PROMPTS.map((qp, idx) => (
              <button
                key={idx}
                onClick={() => handleSendMessage(qp.text)}
                style={{
                  background: 'rgba(255, 255, 255, 0.03)',
                  border: '1px solid var(--border-glass)',
                  borderRadius: '8px',
                  color: 'var(--text-primary)',
                  fontSize: '12px',
                  padding: '8px 12px',
                  cursor: 'pointer',
                  textAlign: 'left',
                  transition: 'var(--transition-fast)',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = 'rgba(138, 63, 252, 0.1)';
                  e.currentTarget.style.borderColor = 'rgba(138, 63, 252, 0.3)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'rgba(255, 255, 255, 0.03)';
                  e.currentTarget.style.borderColor = 'var(--border-glass)';
                }}
              >
                {qp.label}
              </button>
            ))}
          </div>
        </div>
      )}

      <form className="chat-input-form" onSubmit={handleFormSubmit}>
        <div className="chat-input-container">
          <input
            type="text"
            className="chat-text-input"
            placeholder="Type in any language..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={isLoading}
          />
        </div>
        <button
          type="submit"
          className="chat-send-btn"
          disabled={!inputValue.trim() || isLoading}
          aria-label="Send Message"
        >
          <svg className="chat-send-icon" viewBox="0 0 20 20">
            <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.43a1 1 0 001.17-1.408l-7-14z" />
          </svg>
        </button>
      </form>
    </div>
  );
};
