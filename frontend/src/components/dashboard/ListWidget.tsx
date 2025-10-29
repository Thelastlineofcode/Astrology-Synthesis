'use client';

import React from 'react';
import WidgetCard from './WidgetCard';

interface ListItem {
  id: string;
  title: string;
  subtitle?: string;
  status?: string;
}

interface ListWidgetProps {
  title: string;
  items: ListItem[];
  viewMoreLink?: string;
  emptyMessage?: string;
}

export default function ListWidget({ title, items, viewMoreLink, emptyMessage = 'No items' }: ListWidgetProps) {
  const viewMoreAction = viewMoreLink ? (
    <a href={viewMoreLink} className="text-sm text-[var(--color-primary)] hover:underline flex items-center gap-1">
      ↗️
    </a>
  ) : null;

  return (
    <WidgetCard title={title} headerAction={viewMoreAction}>
      {items.length === 0 ? (
        <p className="text-[var(--text-secondary)] text-center py-8">{emptyMessage}</p>
      ) : (
        <div className="space-y-3">
          {items.map((item) => (
            <div
              key={item.id}
              className="flex items-center justify-between p-3 rounded-lg hover:bg-[var(--bg-hover)] transition-colors border border-[var(--border-color)]"
            >
              <div className="flex-1">
                <h4 className="font-medium text-[var(--text-primary)]">{item.title}</h4>
                {item.subtitle && (
                  <p className="text-sm text-[var(--text-secondary)] mt-1">{item.subtitle}</p>
                )}
              </div>
              {item.status && (
                <span className="text-xs px-2 py-1 rounded bg-[var(--color-secondary-light)] text-[var(--color-primary-dark)]">
                  {item.status}
                </span>
              )}
              <button className="ml-2 text-[var(--text-secondary)] hover:text-[var(--text-primary)]">
                →
              </button>
            </div>
          ))}
          {viewMoreLink && items.length > 5 && (
            <button className="w-full py-2 text-[var(--color-primary)] hover:underline text-sm">
              View {items.length - 5} More
            </button>
          )}
        </div>
      )}
    </WidgetCard>
  );
}
