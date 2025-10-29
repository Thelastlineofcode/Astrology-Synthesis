'use client';

import React from 'react';
import WidgetCard from './WidgetCard';

interface WaitlistItem {
  id: string;
  name: string;
  code: string;
  status: string;
  position: number;
}

interface WaitlistWidgetProps {
  title: string;
  subtitle?: string;
  items: WaitlistItem[];
  viewMoreLink?: string;
}

export default function WaitlistWidget({ title, subtitle, items, viewMoreLink }: WaitlistWidgetProps) {
  const headerAction = viewMoreLink ? (
    <a href={viewMoreLink} className="text-sm text-[var(--color-primary)] hover:underline flex items-center gap-1">
      ↗️
    </a>
  ) : null;

  return (
    <WidgetCard title={title} headerAction={headerAction}>
      {subtitle && (
        <div className="mb-4 pb-4 border-b border-[var(--border-color)]">
          <p className="text-[var(--text-secondary)]">{subtitle}</p>
        </div>
      )}
      
      {items.length === 0 ? (
        <p className="text-[var(--text-secondary)] text-center py-8">No items in waitlist</p>
      ) : (
        <div className="space-y-4">
          {items.map((item) => (
            <div
              key={item.id}
              className="p-4 rounded-lg border border-[var(--border-color)] bg-white dark:bg-[var(--bg-secondary)]"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <h4 className="font-semibold text-[var(--text-primary)]">{item.name}</h4>
                  <p className="text-sm text-[var(--text-secondary)]">{item.code}</p>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-[var(--text-secondary)] mb-1">Status:</p>
                  <p className="text-sm font-medium text-[var(--text-primary)]">{item.status}</p>
                </div>
                <div className="text-right">
                  <p className="text-xs text-[var(--text-secondary)] mb-1">Position:</p>
                  <p className="text-2xl font-bold text-[var(--color-primary)]">{item.position}</p>
                </div>
              </div>
              
              <button className="w-full mt-3 py-2 px-4 text-sm border border-[var(--border-color)] rounded-lg hover:bg-[var(--bg-hover)] transition-colors text-[var(--text-primary)]">
                Open
              </button>
            </div>
          ))}
        </div>
      )}
    </WidgetCard>
  );
}
