import { useState, useEffect } from 'react';
import type { Car, FilterState } from './types';
import { fetchCars } from './api/carApi';
import { Navbar } from './components/Navbar';
import { FilterSidebar } from './components/FilterSidebar';
import { CarCard } from './components/CarCard';
import { Chatbot } from './components/Chatbot';

const DEFAULT_FILTERS: FilterState = {
  brand: '',
  bodyType: '',
  condition: '',
  minPrice: '',
  maxPrice: '',
  minEngine: '',
  maxEngine: '',
  minRating: '',
  color: '',
  sortBy: '',
};

function App() {
  const [cars, setCars] = useState<Car[]>([]);
  const [filters, setFilters] = useState<FilterState>(DEFAULT_FILTERS);
  const [suggestedCarIds, setSuggestedCarIds] = useState<number[]>([]);
  const [isChatOpen, setIsChatOpen] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch cars when manual filters are modified
  useEffect(() => {
    const getCars = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await fetchCars(filters);
        setCars(data);
      } catch (err) {
        setError('Failed to retrieve vehicle listings. Please ensure the backend is running.');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    getCars();
  }, [filters]);

  const handleFilterChange = (updates: Partial<FilterState>) => {
    setFilters((prev) => ({ ...prev, ...updates }));
  };

  const handleClearFilters = () => {
    setFilters(DEFAULT_FILTERS);
    setSuggestedCarIds([]);
  };

  const handleSuggestedCarsReceived = (carIds: number[]) => {
    setSuggestedCarIds(carIds);
  };

  const handleClearSuggestions = () => {
    setSuggestedCarIds([]);
  };

  // Perform AI custom sorting: show ONLY recommended cars
  let displayedCars = [...cars];
  if (suggestedCarIds.length > 0) {
    displayedCars = cars.filter((car) => suggestedCarIds.includes(car.id));
    // Sort suggestions strictly in the order of relevance returned by the AI
    displayedCars.sort((a, b) => suggestedCarIds.indexOf(a.id) - suggestedCarIds.indexOf(b.id));
  }

  return (
    <div className="app-container">
      <Navbar
        isChatOpen={isChatOpen}
        onToggleChat={() => setIsChatOpen((prev) => !prev)}
        suggestedCount={suggestedCarIds.length}
      />

      <div className="content-wrapper">
        <FilterSidebar
          filters={filters}
          onChange={handleFilterChange}
          onClear={handleClearFilters}
        />

        <main className="main-content">
          <div className="listing-header">
            <div>
              <h2 style={{ fontSize: '24px', fontWeight: 800 }}>Premium Vehicle Fleet</h2>
              <span className="cars-count">
                Displaying {displayedCars.length} of {cars.length} active listings
              </span>
            </div>
          </div>

          {/* AI Recommendations active banner */}
          {suggestedCarIds.length > 0 && (
            <div className="highlight-banner">
              <span>
                ✨ <strong>AI Search Filter Active:</strong> Displaying only the recommended matching vehicles suggested by the AI.
              </span>
              <button onClick={handleClearSuggestions}>
                Show Full Fleet ×
              </button>
            </div>
          )}

          {isLoading ? (
            <div className="loading-container">
              <div className="spinner" />
              <span>Updating active vehicle fleet...</span>
            </div>
          ) : error ? (
            <div className="empty-state">
              <span className="empty-state-icon">⚠️</span>
              <span className="empty-state-title">Connection Error</span>
              <p>{error}</p>
            </div>
          ) : displayedCars.length === 0 ? (
            <div className="empty-state glass-panel">
              <span className="empty-state-icon">🔍</span>
              <span className="empty-state-title">No cars match your search filters</span>
              <p>Try resetting the filters or tweaking your criteria in the sidebar.</p>
              <button
                className="chat-toggle-btn"
                style={{ marginTop: '12px' }}
                onClick={handleClearFilters}
              >
                Reset All Filters
              </button>
            </div>
          ) : (
            <div className="cars-grid">
              {displayedCars.map((car) => (
                <CarCard
                  key={car.id}
                  car={car}
                  isSuggested={suggestedCarIds.includes(car.id)}
                />
              ))}
            </div>
          )}
        </main>

        <Chatbot
          isOpen={isChatOpen}
          onClose={() => setIsChatOpen(false)}
          onSuggestedCarsReceived={handleSuggestedCarsReceived}
        />
      </div>
    </div>
  );
}

export default App;
