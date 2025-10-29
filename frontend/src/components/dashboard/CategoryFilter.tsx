'use client';

import React, { useState } from 'react';

interface CategoryFilterProps {
  categories: string[];
  selectedCategories?: string[];
  onFilterChange?: (selected: string[]) => void;
}

export default function CategoryFilter({ 
  categories, 
  selectedCategories = [], 
  onFilterChange 
}: CategoryFilterProps) {
  const [selected, setSelected] = useState<string[]>(selectedCategories);

  const handleToggle = (category: string) => {
    const newSelected = selected.includes(category)
      ? selected.filter(c => c !== category)
      : [...selected, category];
    
    setSelected(newSelected);
    if (onFilterChange) {
      onFilterChange(newSelected);
    }
  };

  const handleSelectAll = () => {
    setSelected(categories);
    if (onFilterChange) {
      onFilterChange(categories);
    }
  };

  const handleClearAll = () => {
    setSelected([]);
    if (onFilterChange) {
      onFilterChange([]);
    }
  };

  return (
    <div className="bg-white dark:bg-[var(--bg-secondary)] rounded-lg p-4 shadow-[var(--elevation-2)] border border-[var(--border-color)]">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-[var(--text-primary)]">Filter by Category</h3>
        <div className="flex gap-2">
          <button
            onClick={handleSelectAll}
            className="text-xs text-[var(--color-primary)] hover:underline"
          >
            Select All
          </button>
          <span className="text-xs text-[var(--text-secondary)]">|</span>
          <button
            onClick={handleClearAll}
            className="text-xs text-[var(--color-primary)] hover:underline"
          >
            Clear
          </button>
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        {categories.map((category) => {
          const isSelected = selected.includes(category);
          return (
            <button
              key={category}
              onClick={() => handleToggle(category)}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                isSelected
                  ? 'bg-[var(--color-primary)] text-white'
                  : 'bg-[var(--bg-primary)] text-[var(--text-primary)] border border-[var(--border-color)] hover:bg-[var(--bg-hover)]'
              }`}
            >
              {isSelected && '✓ '}
              {category}
            </button>
          );
        })}
      </div>

      {selected.length > 0 && (
        <div className="mt-3 text-sm text-[var(--text-secondary)]">
          {selected.length} {selected.length === 1 ? 'category' : 'categories'} selected
        </div>
      )}
    </div>
  );
}
