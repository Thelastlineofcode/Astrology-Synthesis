"use client";

import React, { useState } from 'react';
import './CardDraw.css';

interface Card {
  id: string;
  name: string;
  subtitle: string;
  symbol: string;
  meaning: string;
  advice: string;
}

// Sample Vodou Oracle cards (will be replaced with API data)
const SAMPLE_CARDS: Card[] = [
  {
    id: 'papa-legba',
    name: 'Papa Legba',
    subtitle: 'The Crossroads',
    symbol: '🗝️',
    meaning: 'Papa Legba stands at the crossroads of destiny. New opportunities await you, but decisive action is required.',
    advice: 'Open doors are meant to be walked through. Trust your intuition and take the first step into the unknown.'
  },
  {
    id: 'erzulie-freda',
    name: 'Erzulie Freda',
    subtitle: 'Love & Beauty',
    symbol: '💝',
    meaning: 'The Lwa of love and beauty blesses your path. Emotional fulfillment and deep connections are approaching.',
    advice: 'Open your heart to receive love. Self-care and appreciation of beauty will attract positive energy.'
  },
  {
    id: 'baron-samedi',
    name: 'Baron Samedi',
    subtitle: 'Death & Rebirth',
    symbol: '💀',
    meaning: 'The Baron teaches that endings are new beginnings. A transformation is underway in your life.',
    advice: 'Release what no longer serves you. Embrace change fearlessly, for rebirth follows death.'
  },
  {
    id: 'ogoun',
    name: 'Ogoun',
    subtitle: 'Strength & War',
    symbol: '⚔️',
    meaning: 'Ogoun brings the fire of determination. Your strength and courage will overcome obstacles.',
    advice: 'Stand firm in your convictions. Victory comes to those who fight with honor and persistence.'
  },
  {
    id: 'damballah',
    name: 'Damballah',
    subtitle: 'Wisdom & Purity',
    symbol: '🐍',
    meaning: 'The Serpent Lwa offers ancient wisdom and spiritual clarity. Truth is revealing itself to you.',
    advice: 'Seek inner peace through meditation and reflection. Wisdom comes from stillness.'
  }
];

interface CardDrawProps {
  onCardDrawn?: (card: Card) => void;
}

export default function CardDraw({ onCardDrawn }: CardDrawProps) {
  const [isShuffling, setIsShuffling] = useState(false);
  const [isFlipping, setIsFlipping] = useState(false);
  const [isRevealed, setIsRevealed] = useState(false);
  const [drawnCard, setDrawnCard] = useState<Card | null>(null);

  const handleDrawCard = () => {
    if (isShuffling || isFlipping) return;

    // Start shuffle animation
    setIsShuffling(true);

    // After shuffle, flip the card
    setTimeout(() => {
      setIsShuffling(false);
      setIsFlipping(true);

      // Select random card
      const randomCard = SAMPLE_CARDS[Math.floor(Math.random() * SAMPLE_CARDS.length)];
      setDrawnCard(randomCard);

      // After flip animation, reveal the reading
      setTimeout(() => {
        setIsFlipping(false);
        setIsRevealed(true);
        if (onCardDrawn) {
          onCardDrawn(randomCard);
        }
      }, 800);
    }, 600);
  };

  const handleReset = () => {
    setIsRevealed(false);
    setDrawnCard(null);
  };

  return (
    <div className="card-draw">
      <div className="card-draw__deck">
        {/* Stack of cards */}
        <div 
          className={`card-draw__card ${
            isShuffling ? 'card-draw__card--shuffling' : ''
          } ${
            isFlipping ? 'card-draw__card--flipping' : ''
          } ${
            isRevealed ? 'card-draw__card--revealed' : ''
          }`}
          onClick={!isRevealed ? handleDrawCard : undefined}
          role="button"
          aria-label={isRevealed ? "Card revealed" : "Click to draw a card"}
          tabIndex={0}
        >
          {/* Card Back */}
          <div className="card-draw__card-back">
            <div className="card-draw__card-pattern">🌙</div>
          </div>

          {/* Card Front */}
          {drawnCard && (
            <div className="card-draw__card-front">
              <div className="card-draw__card-image">
                {drawnCard.symbol}
              </div>
              <div>
                <h3 className="card-draw__card-name">{drawnCard.name}</h3>
                <p className="card-draw__card-subtitle">{drawnCard.subtitle}</p>
              </div>
            </div>
          )}
        </div>

        {/* Background cards for depth */}
        <div className="card-draw__card">
          <div className="card-draw__card-back">
            <div className="card-draw__card-pattern">🌙</div>
          </div>
        </div>
        <div className="card-draw__card">
          <div className="card-draw__card-back">
            <div className="card-draw__card-pattern">🌙</div>
          </div>
        </div>
      </div>

      {/* Draw button */}
      {!isRevealed && (
        <button 
          className="card-draw__button"
          onClick={handleDrawCard}
          disabled={isShuffling || isFlipping}
          aria-label="Draw a card"
        >
          {isShuffling ? 'Shuffling...' : isFlipping ? 'Drawing...' : 'Draw Your Card'}
        </button>
      )}

      {/* Reset button */}
      {isRevealed && (
        <button 
          className="card-draw__button"
          onClick={handleReset}
          aria-label="Draw another card"
        >
          Draw Another Card
        </button>
      )}

      {/* Card reading */}
      {isRevealed && drawnCard && (
        <div className="card-draw__reading">
          <h3 className="card-draw__reading-title">Your Reading</h3>
          <p className="card-draw__reading-text">
            <strong>Meaning:</strong> {drawnCard.meaning}
          </p>
          <p className="card-draw__reading-text">
            <strong>Advice:</strong> {drawnCard.advice}
          </p>
          <div className="card-draw__reading-actions">
            <button className="card-draw__action-button" aria-label="Save reading">
              💾 Save
            </button>
            <button className="card-draw__action-button" aria-label="Share reading">
              📤 Share
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
