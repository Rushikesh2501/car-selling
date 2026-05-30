import React from 'react';
import type { FilterState } from '../types';

interface FilterSidebarProps {
  filters: FilterState;
  onChange: (updates: Partial<FilterState>) => void;
  onClear: () => void;
}

const BRANDS = ['Toyota', 'Honda', 'BMW', 'Tesla', 'Suzuki', 'Hyundai', 'Ford', 'Mercedes-Benz'];
const BODY_TYPES = ['sedan', 'hatchback', 'mpv'];
const CONDITIONS = ['Excellent', 'Very Good', 'Good', 'Fair', 'Poor'];
const COLORS = ['White', 'Black', 'Silver', 'Red', 'Blue', 'Grey', 'Bronze'];

export const FilterSidebar: React.FC<FilterSidebarProps> = ({
  filters,
  onChange,
  onClear,
}) => {
  const handleSelectChange = (
    e: React.ChangeEvent<HTMLSelectElement | HTMLInputElement>
  ) => {
    const { name, value } = e.target;
    onChange({ [name]: value });
  };

  return (
    <aside className="sidebar glass-panel">
      <div className="sidebar-title">
        <span>Filters & Sort</span>
        <button className="clear-btn" onClick={onClear}>
          Reset All
        </button>
      </div>

      {/* Sorting Group */}
      <div className="filter-group">
        <label className="filter-label" htmlFor="sortBy">
          Sort Catalog By
        </label>
        <select
          className="filter-input"
          id="sortBy"
          name="sortBy"
          value={filters.sortBy}
          onChange={handleSelectChange}
        >
          <option value="">Default Sorting</option>
          <option value="price_asc">Price: Low to High</option>
          <option value="price_desc">Price: High to Low</option>
          <option value="rating_desc">Rating: High to Low</option>
          <option value="engine_asc">Engine: Small to Large</option>
          <option value="engine_desc">Engine: Large to Small</option>
          <option value="year_desc">Year: Newest to Oldest</option>
        </select>
      </div>

      {/* Body Type & Company Group */}
      <div className="filter-group">
        <label className="filter-label" htmlFor="bodyType">
          Body Type
        </label>
        <select
          className="filter-input"
          id="bodyType"
          name="bodyType"
          value={filters.bodyType}
          onChange={handleSelectChange}
          style={{ marginBottom: '12px' }}
        >
          <option value="">All Body Types</option>
          {BODY_TYPES.map((bt) => (
            <option key={bt} value={bt} style={{ textTransform: 'capitalize' }}>
              {bt}
            </option>
          ))}
        </select>

        <label className="filter-label" htmlFor="brand" style={{ marginTop: '8px' }}>
          Company / Brand
        </label>
        <select
          className="filter-input"
          id="brand"
          name="brand"
          value={filters.brand}
          onChange={handleSelectChange}
          style={{ marginBottom: '12px' }}
        >
          <option value="">All Companies</option>
          {BRANDS.map((b) => (
            <option key={b} value={b}>
              {b}
            </option>
          ))}
        </select>

        <label className="filter-label" htmlFor="color" style={{ marginTop: '8px' }}>
          Color of Car
        </label>
        <select
          className="filter-input"
          id="color"
          name="color"
          value={filters.color}
          onChange={handleSelectChange}
        >
          <option value="">All Colors</option>
          {COLORS.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>

      {/* Condition Group */}
      <div className="filter-group">
        <label className="filter-label" htmlFor="condition">
          Car Condition
        </label>
        <select
          className="filter-input"
          id="condition"
          name="condition"
          value={filters.condition}
          onChange={handleSelectChange}
        >
          <option value="">Any Condition</option>
          {CONDITIONS.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>

      {/* Price Range */}
      <div className="filter-group">
        <label className="filter-label">Price Range (₹)</label>
        <div className="price-range-inputs">
          <input
            type="number"
            className="filter-input"
            name="minPrice"
            placeholder="Min"
            value={filters.minPrice}
            onChange={handleSelectChange}
            min="0"
          />
          <input
            type="number"
            className="filter-input"
            name="maxPrice"
            placeholder="Max"
            value={filters.maxPrice}
            onChange={handleSelectChange}
            min="0"
          />
        </div>
      </div>

      {/* Engine Capacity Range */}
      <div className="filter-group">
        <label className="filter-label">Engine Capacity (L)</label>
        <div className="price-range-inputs">
          <input
            type="number"
            step="0.1"
            className="filter-input"
            name="minEngine"
            placeholder="Min"
            value={filters.minEngine}
            onChange={handleSelectChange}
            min="0"
          />
          <input
            type="number"
            step="0.1"
            className="filter-input"
            name="maxEngine"
            placeholder="Max"
            value={filters.maxEngine}
            onChange={handleSelectChange}
            min="0"
          />
        </div>
      </div>

      {/* Star Rating Group */}
      <div className="filter-group">
        <label className="filter-label" htmlFor="minRating">
          Minimum Stars
        </label>
        <select
          className="filter-input"
          id="minRating"
          name="minRating"
          value={filters.minRating}
          onChange={handleSelectChange}
        >
          <option value="">Any Rating</option>
          <option value="4.5">4.5+ Stars</option>
          <option value="4.0">4.0+ Stars</option>
          <option value="3.5">3.5+ Stars</option>
          <option value="3.0">3.0+ Stars</option>
          <option value="2.0">2.0+ Stars</option>
        </select>
      </div>
    </aside>
  );
};
