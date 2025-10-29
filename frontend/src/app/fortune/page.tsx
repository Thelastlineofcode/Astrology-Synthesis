"use client";

import React, { useState } from 'react';
import './fortune.css';

interface FortuneData {
  dailyReading: string;
  weeklyReading: string;
  monthlyReading: string;
}

export default function FortunePage() {
  const [selectedReading, setSelectedReading] = useState<'daily' | 'weekly' | 'monthly'>('daily');
  
  const fortuneData: FortuneData = {
    dailyReading: "Today's energies align perfectly for new beginnings. The stars suggest taking bold action in your creative pursuits. Trust your intuition and embrace opportunities that come your way.",
    weeklyReading: "This week brings transformative energy into your relationships. Focus on communication and understanding. A significant opportunity for personal growth emerges mid-week.",
    monthlyReading: "This month marks a powerful cycle of manifestation. Your goals and dreams are within reach. Stay focused on your intentions and maintain balance between work and personal life."
  };

  const getCurrentReading = () => {
    switch(selectedReading) {
      case 'daily': return fortuneData.dailyReading;
      case 'weekly': return fortuneData.weeklyReading;
      case 'monthly': return fortuneData.monthlyReading;
    }
  };

  return (
    <div className="fortune-page">
      {/* Header with currency */}
      <div className="fortune-header">
        <button className="add-button">
          <span className="plus-icon">+</span>
        </button>
        <div className="currency-display">
          <span className="currency-amount">37,484</span>
          <span className="star-icon">✨</span>
        </div>
        <button className="notification-button">
          <span className="bell-icon">🔔</span>
          <span className="notification-badge">5</span>
        </button>
      </div>

      {/* Profile Section */}
      <div className="profile-section">
        <div className="profile-avatar">
          <div className="avatar-circle">
            <span className="avatar-placeholder">ES</span>
          </div>
        </div>
        <h1 className="profile-name">Emma Smith</h1>
        <div className="profile-zodiac">
          <span className="zodiac-icon">♊</span>
          <span className="zodiac-name">Gemini</span>
        </div>
      </div>

      {/* Get Premium Card */}
      <div className="premium-card">
        <div className="moon-decoration moon-left"></div>
        <div className="moon-decoration moon-right"></div>
        <h2 className="premium-title">Get Premium</h2>
        <p className="premium-description">
          Get Unlimited Tarot Reading, No Adds<br />and Other Advantages
        </p>
      </div>

      {/* Stats Section */}
      <div className="stats-section">
        {/* Invite Friends Card */}
        <div className="invite-card">
          <div className="moon-phases">
            <span className="phase-icon">🌑</span>
            <span className="phase-icon">🌓</span>
            <span className="phase-icon">🌕</span>
            <span className="phase-icon">🌗</span>
          </div>
          <h3 className="invite-title">Invite Friends</h3>
          <p className="invite-description">Earn a 5% discount<br />progression</p>
        </div>

        {/* Progress Card */}
        <div className="progress-card">
          <div className="progress-main">
            <span className="progress-value">75%</span>
            <span className="progress-change">+15%</span>
            <span className="arrow-icon">›</span>
          </div>
          <div className="progress-bars">
            <div className="bar bar-active"></div>
            <div className="bar bar-active"></div>
            <div className="bar bar-active"></div>
            <div className="bar bar-active"></div>
            <div className="bar bar-active"></div>
            <div className="bar bar-inactive"></div>
          </div>
        </div>
      </div>

      {/* Reference Code Section */}
      <div className="reference-section">
        <span className="reference-label">Reference Code</span>
        <button className="reference-button">
          <span className="arrow-icon">→</span>
        </button>
      </div>

      {/* Fortune Readings Section */}
      <div className="fortune-readings">
        <h2 className="readings-title">Your Fortune</h2>
        
        {/* Reading Type Selector */}
        <div className="reading-selector">
          <button 
            className={`selector-button ${selectedReading === 'daily' ? 'active' : ''}`}
            onClick={() => setSelectedReading('daily')}
          >
            Daily
          </button>
          <button 
            className={`selector-button ${selectedReading === 'weekly' ? 'active' : ''}`}
            onClick={() => setSelectedReading('weekly')}
          >
            Weekly
          </button>
          <button 
            className={`selector-button ${selectedReading === 'monthly' ? 'active' : ''}`}
            onClick={() => setSelectedReading('monthly')}
          >
            Monthly
          </button>
        </div>

        {/* Reading Content */}
        <div className="reading-content">
          <div className="reading-card">
            <div className="zodiac-symbol">♊</div>
            <p className="reading-text">{getCurrentReading()}</p>
            <div className="reading-actions">
              <button className="action-button">
                <span>💾</span> Save
              </button>
              <button className="action-button">
                <span>📤</span> Share
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Navigation */}
      <nav className="bottom-nav">
        <button className="nav-item">
          <span className="nav-icon">🔍</span>
          <span className="nav-label">Discover</span>
        </button>
        <button className="nav-item">
          <span className="nav-icon">🌙</span>
          <span className="nav-label">Astrolocers</span>
        </button>
        <button className="nav-item">
          <span className="nav-icon">🪐</span>
          <span className="nav-label">Starbase</span>
        </button>
        <button className="nav-item">
          <span className="nav-icon">💬</span>
          <span className="nav-label">Consultant</span>
        </button>
        <button className="nav-item active">
          <span className="nav-icon">👤</span>
          <span className="nav-label">Profile</span>
          <span className="nav-badge">5</span>
        </button>
      </nav>
    </div>
  );
}
