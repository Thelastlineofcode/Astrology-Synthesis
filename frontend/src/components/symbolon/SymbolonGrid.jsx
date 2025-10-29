"use client";

import React, { useState } from 'react';
import SymbolonCard from './SymbolonCard';
import SymbolonModal from './SymbolonModal';
import './SymbolonGrid.css';

const SkeletonCard = () => (
  <div className="symbolon-grid__skeleton">
    <div className="skeleton-image" />
    <div className="skeleton-content">
      <div className="skeleton-title" />
      <div className="skeleton-badges" />
      <div className="skeleton-text" />
    </div>
  </div>
);

const SymbolonGrid = ({ cards = [], loading = false }) => {
  const [selectedCard, setSelectedCard] = useState(null);
  
  if (loading) {
    return (
      <div className="symbolon-grid">
        {Array.from({ length: 6 }).map((_, i) => (
          <SkeletonCard key={i} />
        ))}
      </div>
    );
  }
  
  return (
    <>
      <div className="symbolon-grid">
        {cards.map((card) => (
          <SymbolonCard
            key={card.id}
            card={card}
            onClick={() => setSelectedCard(card)}
          />
        ))}
      </div>
      
      {selectedCard && (
        <SymbolonModal
          card={selectedCard}
          onClose={() => setSelectedCard(null)}
        />
      )}
    </>
  );
};

export default SymbolonGrid;
