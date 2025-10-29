'use client';

import React from 'react';
import Link from 'next/link';

interface SidebarProps {
  currentPath?: string;
}

const navigationItems = [
  { id: 'dashboard', label: 'Dashboard', icon: '🏠', href: '/dashboard' },
  { id: 'admissions', label: 'Admissions', icon: '📋', href: '/dashboard/admissions' },
  { id: 'financials', label: 'Financials', icon: '💰', href: '/dashboard/financials' },
  { id: 'schedule', label: 'Schedule', icon: '📅', href: '/dashboard/schedule' },
  { id: 'academics', label: 'Academics', icon: '📚', href: '/dashboard/academics' },
  { id: 'widgets', label: 'Edit My Widgets', icon: '⚙️', href: '/dashboard/widgets' },
  { id: 'enrollment', label: 'Enrollment', icon: '📝', href: '/dashboard/enrollment' },
  { id: 'notifications', label: 'Notifications', icon: '🔔', href: '/dashboard/notifications' },
  { id: 'messages', label: 'Messages', icon: '💬', href: '/dashboard/messages' },
  { id: 'links', label: 'Global Links', icon: '🌐', href: '/dashboard/links' },
];

export default function DashboardSidebar({ currentPath }: SidebarProps) {
  return (
    <aside className="w-80 bg-[var(--color-primary)] text-white min-h-screen flex flex-col">
      {/* Logo Section */}
      <div className="p-6 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="text-2xl">🔮</div>
          <h1 className="text-xl font-bold">Roots Revealed</h1>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4">
        {navigationItems.map((item) => {
          const isActive = currentPath === item.href;
          return (
            <Link
              key={item.id}
              href={item.href}
              className={`flex items-center gap-3 px-6 py-3 transition-colors ${
                isActive
                  ? 'bg-white/10 text-white border-l-4 border-white'
                  : 'text-white/80 hover:bg-white/5 hover:text-white'
              }`}
            >
              <span className="text-xl">{item.icon}</span>
              <span className="font-medium">{item.label}</span>
              {item.id === 'admissions' || item.id === 'financials' || item.id === 'academics' || item.id === 'links' ? (
                <span className="ml-auto text-white/60">▼</span>
              ) : null}
            </Link>
          );
        })}
      </nav>

      {/* User Profile Section */}
      <div className="p-6 border-t border-white/10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center">
            <span className="text-lg">👤</span>
          </div>
          <div className="flex-1">
            <p className="font-medium">User Name</p>
            <button className="text-sm text-white/70 hover:text-white">▼</button>
          </div>
        </div>
      </div>
    </aside>
  );
}
