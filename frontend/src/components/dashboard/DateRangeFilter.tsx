'use client';

import React, { useState } from 'react';

interface DateRangeFilterProps {
  onFilterChange?: (startDate: string, endDate: string) => void;
}

export default function DateRangeFilter({ onFilterChange }: DateRangeFilterProps) {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [preset, setPreset] = useState('all');

  const presetRanges = [
    { id: 'all', label: 'All Time' },
    { id: 'today', label: 'Today' },
    { id: 'week', label: 'This Week' },
    { id: 'month', label: 'This Month' },
    { id: 'quarter', label: 'This Quarter' },
    { id: 'year', label: 'This Year' },
    { id: 'custom', label: 'Custom Range' },
  ];

  const handlePresetChange = (presetId: string) => {
    setPreset(presetId);
    const today = new Date();
    let start = new Date();
    let end = new Date();

    switch (presetId) {
      case 'today':
        start = today;
        end = today;
        break;
      case 'week':
        start = new Date(today.setDate(today.getDate() - 7));
        end = new Date();
        break;
      case 'month':
        start = new Date(today.getFullYear(), today.getMonth(), 1);
        end = new Date();
        break;
      case 'quarter':
        const quarter = Math.floor(today.getMonth() / 3);
        start = new Date(today.getFullYear(), quarter * 3, 1);
        end = new Date();
        break;
      case 'year':
        start = new Date(today.getFullYear(), 0, 1);
        end = new Date();
        break;
      case 'all':
      default:
        start = new Date(2020, 0, 1);
        end = new Date();
        break;
    }

    if (presetId !== 'custom') {
      const startStr = start.toISOString().split('T')[0];
      const endStr = end.toISOString().split('T')[0];
      setStartDate(startStr);
      setEndDate(endStr);
      if (onFilterChange) {
        onFilterChange(startStr, endStr);
      }
    }
  };

  const handleCustomDateChange = () => {
    if (onFilterChange && startDate && endDate) {
      onFilterChange(startDate, endDate);
    }
  };

  return (
    <div className="bg-white dark:bg-[var(--bg-secondary)] rounded-lg p-4 shadow-[var(--elevation-2)] border border-[var(--border-color)]">
      <h3 className="text-sm font-semibold text-[var(--text-primary)] mb-3">Filter by Date Range</h3>
      
      <div className="flex flex-wrap gap-2 mb-4">
        {presetRanges.map((range) => (
          <button
            key={range.id}
            onClick={() => handlePresetChange(range.id)}
            className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              preset === range.id
                ? 'bg-[var(--color-primary)] text-white'
                : 'bg-[var(--bg-primary)] text-[var(--text-primary)] border border-[var(--border-color)] hover:bg-[var(--bg-hover)]'
            }`}
          >
            {range.label}
          </button>
        ))}
      </div>

      {preset === 'custom' && (
        <div className="flex gap-3 items-end">
          <div className="flex-1">
            <label className="block text-sm font-medium text-[var(--text-secondary)] mb-1">
              Start Date
            </label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-[var(--border-color)] bg-white dark:bg-[var(--bg-secondary)] text-[var(--text-primary)]"
            />
          </div>
          <div className="flex-1">
            <label className="block text-sm font-medium text-[var(--text-secondary)] mb-1">
              End Date
            </label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-[var(--border-color)] bg-white dark:bg-[var(--bg-secondary)] text-[var(--text-primary)]"
            />
          </div>
          <button
            onClick={handleCustomDateChange}
            className="px-4 py-2 bg-[var(--color-primary)] text-white rounded-lg hover:opacity-90 transition-opacity"
          >
            Apply
          </button>
        </div>
      )}

      {preset !== 'custom' && startDate && endDate && (
        <div className="text-sm text-[var(--text-secondary)] mt-2">
          Showing data from {new Date(startDate).toLocaleDateString()} to {new Date(endDate).toLocaleDateString()}
        </div>
      )}
    </div>
  );
}
