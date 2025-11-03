"use client";

import React from 'react';
import Card from '@/components/shared/Card';
import Button from '@/components/shared/Button';
import './BMADSummaryCard.css';

const BMADSummaryCard = () => {
  // In a real implementation, this would fetch BMAD data
  const hasBMADData = false;
  
  if (!hasBMADData) {
    return (
      <Card className="bmad-summary-card">
        <h3>BMAD Insights</h3>
        <div className="empty-state">
          <p className="empty-state__text">
            Generate a chart to unlock Birth Matrix Analysis Dashboard insights.
          </p>
        </div>
      </Card>
    );
  }
  
  // When data exists, show summary
  return (
    <Card className="bmad-summary-card">
      <div className="card-header">
        <h3>BMAD Insights</h3>
        <Button 
          variant="secondary" 
          size="small"
          onClick={() => window.location.href = '/bmad'}
        >
          View Details
        </Button>
      </div>
      
      <div className="bmad-summary">
        <div className="bmad-metric">
          <span className="bmad-metric__value">4</span>
          <span className="bmad-metric__label">Life Path</span>
        </div>
        <div className="bmad-metric">
          <span className="bmad-metric__value">7</span>
          <span className="bmad-metric__label">Soul Number</span>
        </div>
        <div className="bmad-metric">
          <span className="bmad-metric__value">11</span>
          <span className="bmad-metric__label">Destiny</span>
        </div>
      </div>
    </Card>
  );
};

export default BMADSummaryCard;
