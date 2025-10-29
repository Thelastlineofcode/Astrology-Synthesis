'use client';

import React from 'react';

interface DashboardHeaderProps {
  userName?: string;
  title?: string;
}

export default function DashboardHeader({ userName = 'User', title = 'Dashboard' }: DashboardHeaderProps) {
  return (
    <header className="bg-white dark:bg-[var(--bg-secondary)] border-b border-[var(--border-color)]">
      <div className="flex items-center justify-between p-6">
        <div>
          <h1 className="text-3xl font-bold text-[var(--text-primary)] mb-2">{title}</h1>
          <p className="text-xl text-[var(--text-secondary)]">
            Hello {userName}! 👋
          </p>
        </div>
        
        <div className="flex items-center gap-4">
          <button className="p-2 rounded-lg hover:bg-[var(--bg-hover)] transition-colors">
            <span className="text-2xl">⚙️</span>
          </button>
        </div>
      </div>
    </header>
  );
}
