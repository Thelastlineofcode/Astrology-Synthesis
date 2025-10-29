'use client';

import React from 'react';
import WidgetCard from './WidgetCard';

interface ChartDataPoint {
  label: string;
  value: number;
  color?: string;
}

interface ChartWidgetProps {
  title: string;
  data: ChartDataPoint[];
  type?: 'bar' | 'line';
}

export default function ChartWidget({ title, data, type = 'bar' }: ChartWidgetProps) {
  const maxValue = Math.max(...data.map(d => d.value), 1);
  
  const colors = [
    'var(--color-primary)',
    'var(--color-secondary)',
    'var(--color-accent)',
    'var(--color-cta)',
    'var(--color-info)',
  ];

  return (
    <WidgetCard title={title}>
      <div className="space-y-4">
        {data.map((point, index) => {
          const percentage = (point.value / maxValue) * 100;
          const barColor = point.color || colors[index % colors.length];
          
          return (
            <div key={point.label} className="space-y-2">
              <div className="flex justify-between items-baseline">
                <span className="text-sm font-medium text-[var(--text-primary)]">{point.label}</span>
                <span className="text-sm text-[var(--text-secondary)]">{point.value}</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                <div
                  className="h-3 rounded-full transition-all duration-500"
                  style={{
                    width: `${percentage}%`,
                    backgroundColor: barColor,
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
      
      {data.length === 0 && (
        <p className="text-[var(--text-secondary)] text-center py-8">No data available</p>
      )}
    </WidgetCard>
  );
}
