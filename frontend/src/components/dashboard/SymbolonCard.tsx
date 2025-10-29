"use client";

import React from 'react';
import Card from '../shared/Card';
import './SymbolonCard.css';

const SymbolonCard = () => {
  return (
    <Card className="symbolon-card">
      <h3>Symbolon Cards</h3>
      <div className="symbolon-card__content">
        <p className="symbolon-description">
          Explore archetypal insights through Symbolon card readings
        </p>
        <div className="symbolon-cta">
          <button 
            className="symbolon-button"
            onClick={() => window.location.href = '/symbolon-demo'}
          >
            Draw a Card
          </button>
        </div>
      </div>
    </Card>
  );
};

export default SymbolonCard;
