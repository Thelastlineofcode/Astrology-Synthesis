'use client';

import React from 'react';
import WidgetCard from './WidgetCard';

interface StatCardProps {
  title: string;
  value: number | string;
  change?: number;
  trend?: 'up' | 'down' | 'neutral';
  unit?: string;
}

export default function StatCard({ title, value, change, trend, unit }: StatCardProps) {
  const getTrendIcon = () => {
    if (!trend || trend === 'neutral') return '→';
    return trend === 'up' ? '↑' : '↓';
  };

  const getTrendColor = () => {
    if (!trend || trend === 'neutral') return 'text-[var(--text-secondary)]';
    return trend === 'up' ? 'text-[var(--color-success)]' : 'text-[var(--color-error)]';
  };

  return (
    <div className="bg-white dark:bg-[var(--bg-secondary)] rounded-lg p-6 shadow-[var(--elevation-2)] border border-[var(--border-color)]">
      <h3 className="text-sm font-medium text-[var(--text-secondary)] mb-2">{title}</h3>
      <div className="flex items-baseline gap-2">
        <span className="text-3xl font-bold text-[var(--text-primary)]">
          {value}
        </span>
        {unit && <span className="text-lg text-[var(--text-secondary)]">{unit}</span>}
      </div>
      {change !== undefined && (
        <div className={`flex items-center gap-1 mt-2 text-sm ${getTrendColor()}`}>
          <span>{getTrendIcon()}</span>
          <span>{Math.abs(change)}%</span>
        </div>
      )}
    </div>
  );
}
