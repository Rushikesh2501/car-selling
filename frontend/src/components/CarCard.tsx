import React from 'react';
import type { Car } from '../types';
import { RatingStars } from './RatingStars';

interface CarCardProps {
  car: Car;
  isSuggested?: boolean;
}

export const CarCard: React.FC<CarCardProps> = ({ car, isSuggested = false }) => {
  // Format price beautifully in Indian Rupees (INR)
  const formattedPrice = new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(car.price);

  // Format engine capacity
  const formattedEngine = car.engine_capacity === 0 ? 'Electric' : `${car.engine_capacity}L`;

  // Format mileage
  const formattedMileage = new Intl.NumberFormat('en-IN').format(car.mileage) + ' km';

  return (
    <div className={`car-card glass-panel ${isSuggested ? 'suggested' : ''}`}>
      <div className="car-image-container">
        <img
          className="car-image"
          src={car.image_url}
          alt={`${car.brand} ${car.model}`}
          loading="lazy"
        />
        <div className="car-badge">{car.year}</div>
      </div>

      <div className="car-info">
        <div className="car-header">
          <div className="car-title-group">
            <h3 className="car-title">{car.model}</h3>
            <span className="car-brand">{car.brand} • {car.color}</span>
          </div>
          <span className="car-price">{formattedPrice}</span>
        </div>

        <div className="car-specs">
          <div className="spec-item">
            <span className="spec-label">Engine</span>
            <span className="spec-value">{formattedEngine}</span>
          </div>
          <div className="spec-item">
            <span className="spec-label">Body Type</span>
            <span className="spec-value" style={{ textTransform: 'capitalize' }}>
              {car.body_type}
            </span>
          </div>
          <div className="spec-item">
            <span className="spec-label">Condition</span>
            <span className="spec-value">{car.condition}</span>
          </div>
          <div className="spec-item">
            <span className="spec-label">Mileage</span>
            <span className="spec-value">{formattedMileage}</span>
          </div>
          <div className="spec-item">
            <span className="spec-label">Color</span>
            <span className="spec-value">{car.color}</span>
          </div>
          <div className="spec-item">
            <span className="spec-label">Fuel Type</span>
            <span className="spec-value">{car.fuel_type}</span>
          </div>
        </div>

        <p className="car-desc" title={car.description}>
          {car.description}
        </p>

        <div className="car-rating-container">
          <RatingStars rating={car.rating} />
          <span className="rating-value">{car.rating.toFixed(1)} / 5.0</span>
        </div>
      </div>
    </div>
  );
};
