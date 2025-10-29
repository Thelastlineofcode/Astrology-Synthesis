"use client";

import React from 'react';
import Card from '../shared/Card';
import './BMADSummaryCard.css';

const BMADSummaryCard = () => {
  return (
    <Card className="bmad-summary-card">
      <h3>BMAD Analysis</h3>
      <div className="bmad-summary-card__content">
        <p className="bmad-description">
          Discover insights from your Birth Matrix Analysis Dashboard
        </p>
        <div className="bmad-cta">
          <button 
            className="bmad-button"
            onClick={() => window.location.href = '/bmad'}
          >
            View Analysis
          </button>
        </div>
      </div>
    </Card>
  );
};

export default BMADSummaryCard;
