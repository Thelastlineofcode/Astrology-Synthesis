'use client';

import React from 'react';

interface WidgetCardProps {
  title: string;
  children: React.ReactNode;
  headerAction?: React.ReactNode;
  className?: string;
}

export default function WidgetCard({ title, children, headerAction, className = '' }: WidgetCardProps) {
  return (
    <div className={`bg-white dark:bg-[var(--bg-secondary)] rounded-lg shadow-[var(--elevation-2)] border border-[var(--border-color)] ${className}`}>
      <div className="flex items-center justify-between p-4 border-b border-[var(--border-color)]">
        <h2 className="text-lg font-semibold text-[var(--text-primary)]">{title}</h2>
        {headerAction && <div>{headerAction}</div>}
      </div>
      <div className="p-4">
        {children}
      </div>
    </div>
  );
}
