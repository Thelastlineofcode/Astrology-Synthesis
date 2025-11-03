"use client";

import React from 'react';
import Card from '../shared/Card';
import Button from '../shared/Button';
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
          <Button variant="primary" className="bmad-button" href="/bmad">
            View Analysis
          </Button>
        </div>
      </div>
    </Card>
  );
};

export default BMADSummaryCard;
