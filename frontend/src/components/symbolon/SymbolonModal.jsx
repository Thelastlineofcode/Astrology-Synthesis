"use client";

import React, { useEffect } from 'react';
import Badge from '../shared/Badge';
import Button from '../shared/Button';
import './SymbolonModal.css';

const SymbolonModal = ({ card, onClose }) => {
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleEscape);
    
    // Prevent body scroll when modal is open
    document.body.style.overflow = 'hidden';
    
    return () => {
      window.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [onClose]);
  
  return (
    <>
      <div className="modal-overlay" onClick={onClose} />
      <div className="symbolon-modal" role="dialog" aria-modal="true">
        <button
          className="symbolon-modal__close"
          onClick={onClose}
          aria-label="Close modal"
        >
          ×
        </button>
        
        <div className="symbolon-modal__content">
          <img
            src={`/content/symbolon/${card.image}`}
            alt={card.title}
            className="symbolon-modal__image"
          />
          
          <div className="symbolon-modal__text">
            <div className="symbolon-modal__header">
              <span className="symbolon-modal__number">Card {card.number}</span>
              <h2>{card.title}</h2>
            </div>
            
            {card.keywords && (
              <div className="symbolon-modal__keywords">
                {card.keywords.map((keyword, i) => (
                  <Badge key={i} variant="accent" size="medium">
                    {keyword}
                  </Badge>
                ))}
              </div>
            )}
            
            <div className="symbolon-modal__section">
              <h3>Core Meaning</h3>
              <p>{card.meaning}</p>
            </div>
            
            {card.interpretation && (
              <div className="symbolon-modal__section">
                <h3>Interpretation</h3>
                <p>{card.interpretation}</p>
              </div>
            )}
            
            {card.themes && (
              <div className="symbolon-modal__section">
                <h3>Themes & Archetypes</h3>
                <ul>
                  {card.themes.map((theme, i) => (
                    <li key={i}>{theme}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
        
        <div className="symbolon-modal__actions">
          <Button variant="secondary" onClick={onClose}>
            Close
          </Button>
        </div>
      </div>
    </>
  );
};

export default SymbolonModal;
