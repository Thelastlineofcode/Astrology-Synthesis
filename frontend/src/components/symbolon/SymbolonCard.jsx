"use client";

import React, { useState } from 'react';
import Card from '../shared/Card';
import Badge from '../shared/Badge';
import './SymbolonCard.css';

const SymbolonCard = ({ card, onClick }) => {
  const [imageLoaded, setImageLoaded] = useState(false);
  
  return (
    <Card 
      className="symbolon-card"
      hoverable
      onClick={onClick}
      padding="none"
    >
      <div className="symbolon-card__image-container">
        {!imageLoaded && <div className="symbolon-card__skeleton" />}
        <img
          src={`/content/symbolon/${card.image}`}
          alt={card.title}
          className="symbolon-card__image"
          loading="lazy"
          onLoad={() => setImageLoaded(true)}
        />
        <div className="symbolon-card__number">{card.number}</div>
      </div>
      
      <div className="symbolon-card__content">
        <h3 className="symbolon-card__title">{card.title}</h3>
        
        {card.keywords && (
          <div className="symbolon-card__keywords">
            {card.keywords.slice(0, 3).map((keyword, i) => (
              <Badge key={i} variant="neutral" size="small">
                {keyword}
              </Badge>
            ))}
          </div>
        )}
        
        <p className="symbolon-card__excerpt">
          {card.meaning?.substring(0, 120)}...
        </p>
      </div>
    </Card>
  );
};

export default SymbolonCard;
