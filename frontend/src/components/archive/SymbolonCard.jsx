"use client";

import React from 'react';
import Card from '@/components/shared/Card';
import Button from '@/components/shared/Button';
import './SymbolonCard.css';

const SymbolonCard = () => {
  // In a real implementation, this would fetch saved readings
  const hasSavedReadings = false;
  
  if (!hasSavedReadings) {
    return (
      <Card className="symbolon-card">
        <h3>Symbolon Readings</h3>
        <div className="empty-state">
          <p className="empty-state__text">
            Your cosmic story awaits. Create your first Symbolon reading to explore archetypal patterns.
          </p>
          <Button 
            variant="primary" 
            size="medium"
            onClick={() => window.location.href = '/symbolon'}
            className="empty-state__cta"
          >
            Start Reading
          </Button>
        </div>
      </Card>
    );
  }
  
  // When data exists, show saved readings
  return (
    <Card className="symbolon-card">
      <div className="card-header">
        <h3>Symbolon Readings</h3>
        <Button 
          variant="secondary" 
          size="small"
          onClick={() => window.location.href = '/symbolon/saved'}
        >
          View All
        </Button>
      </div>
      
      <div className="symbolon-preview">
        <div className="symbolon-preview__item">
          <div className="symbolon-preview__card">
            <div className="symbolon-preview__image">🌟</div>
          </div>
          <span className="symbolon-preview__label">Latest Reading</span>
        </div>
      </div>
    </Card>
  );
};

export default SymbolonCard;
