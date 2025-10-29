"use client";

import React, { useState } from 'react';
import './AdminSidebar.css';

interface NavItem {
  id: string;
  label: string;
  icon?: string;
  hasDropdown?: boolean;
  isActive?: boolean;
}

const navItems: NavItem[] = [
  { id: 'dashboard', label: 'Dashboard', icon: '🏠', isActive: true },
  { id: 'admissions', label: 'Admissions', icon: '📋', hasDropdown: true },
  { id: 'financials', label: 'Financials', icon: '💰', hasDropdown: true },
  { id: 'schedule', label: 'Schedule', icon: '📅' },
  { id: 'academics', label: 'Academics', icon: '📚', hasDropdown: true },
  { id: 'edit-widgets', label: 'Edit My Widgets', icon: '⚙️', hasDropdown: true },
  { id: 'enrollment', label: 'Enrollment', icon: '👥' },
  { id: 'notifications', label: 'Notifications', icon: '🔔' },
  { id: 'messages', label: 'Messages', icon: '✉️' },
  { id: 'global-links', label: 'Global Links', icon: '🌐', hasDropdown: true },
];

interface AdminSidebarProps {
  userName?: string;
  userAvatar?: string;
}

const AdminSidebar: React.FC<AdminSidebarProps> = ({ 
  userName = 'Admin User',
  userAvatar
}) => {
  const [expandedItems, setExpandedItems] = useState<string[]>([]);

  const toggleItem = (itemId: string) => {
    setExpandedItems(prev => 
      prev.includes(itemId) 
        ? prev.filter(id => id !== itemId)
        : [...prev, itemId]
    );
  };

  return (
    <div className="admin-sidebar">
      <div className="admin-sidebar-header">
        <div className="admin-sidebar-logo">
          <span className="logo-icon">🏔️</span>
          <span className="logo-text">HighPoint</span>
        </div>
        <button className="menu-toggle" aria-label="Toggle menu">
          ☰
        </button>
      </div>

      <nav className="admin-sidebar-nav">
        {navItems.map((item) => (
          <div key={item.id} className="nav-item-container">
            <button
              className={`nav-item ${item.isActive ? 'nav-item--active' : ''}`}
              onClick={() => item.hasDropdown && toggleItem(item.id)}
            >
              <span className="nav-item-icon">{item.icon}</span>
              <span className="nav-item-label">{item.label}</span>
              {item.hasDropdown && (
                <span className="nav-item-arrow">
                  {expandedItems.includes(item.id) ? '▼' : '▶'}
                </span>
              )}
            </button>
            {item.hasDropdown && expandedItems.includes(item.id) && (
              <div className="nav-item-dropdown">
                <button className="nav-item-sub">Submenu 1</button>
                <button className="nav-item-sub">Submenu 2</button>
              </div>
            )}
          </div>
        ))}
      </nav>

      <div className="admin-sidebar-footer">
        <div className="user-profile">
          <div className="user-avatar">
            {userAvatar ? (
              <img src={userAvatar} alt={userName} />
            ) : (
              <div className="user-avatar-placeholder">
                {userName.charAt(0).toUpperCase()}
              </div>
            )}
          </div>
          <span className="user-name">{userName}</span>
          <button className="user-menu-toggle" aria-label="User menu">
            ▼
          </button>
        </div>
      </div>
    </div>
  );
};

export default AdminSidebar;
