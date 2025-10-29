---
title: "Build Symbolon Card Display Component"
labels: ["component:symbolon", "P1-High", "feature", "visualization"]
assignees: []
milestone: "Milestone 3: Advanced Features"
---

## 🎯 Objective

Create a component to display Symbolon cards with images, titles, meanings, and interpretations in a visually appealing card layout.

## 📋 Description

Symbolon cards are archetypal images used for deeper psychological and spiritual insights. Build a component that displays card images, titles, keywords, and detailed interpretations from the content files.

## 🔗 References

- **Design Artifact**: `COMPONENT_STRUCTURE.md` (Symbolon Cards Section)
- **Design Artifact**: `UX_COPY_GUIDE.md` (Symbolon copy)
- **Content**: `/backend/content/symbolon_universal_v1.json`
- **Images**: `/backend/content/symbolon/` (card images)

## ✅ Acceptance Criteria

- [ ] Display single card with image, title, number
- [ ] Show card keywords/themes
- [ ] Display detailed interpretation text
- [ ] Flip animation (front/back) for card reveal (bonus)
- [ ] Grid view for multiple cards (spread layout)
- [ ] Responsive card sizing (mobile/tablet/desktop)
- [ ] Loading state while fetching card data
- [ ] Modal/expanded view for full interpretation
- [ ] Print-friendly layout
- [ ] Image lazy loading for performance

## 💻 Implementation Notes

### Symbolon Card Component

```jsx
// /frontend/src/components/symbolon/SymbolonCard.jsx
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
          {card.meaning.substring(0, 120)}...
        </p>
      </div>
    </Card>
  );
};

export default SymbolonCard;
```

### Symbolon Grid Component

```jsx
// /frontend/src/components/symbolon/SymbolonGrid.jsx
import React, { useState, useEffect } from 'react';
import SymbolonCard from './SymbolonCard';
import SymbolonModal from './SymbolonModal';
import './SymbolonGrid.css';

const SymbolonGrid = ({ cards = [], loading }) => {
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
```

### Symbolon Modal (Detail View)

```jsx
// /frontend/src/components/symbolon/SymbolonModal.jsx
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
    return () => window.removeEventListener('keydown', handleEscape);
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
```

### Symbolon Styles

```css
/* /frontend/src/components/symbolon/SymbolonCard.css */
.symbolon-card {
  overflow: hidden;
  transition: transform 200ms ease, box-shadow 200ms ease;
}

.symbolon-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.symbolon-card__image-container {
  position: relative;
  width: 100%;
  aspect-ratio: 2/3;
  background: var(--bg-hover);
}

.symbolon-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.symbolon-card__skeleton {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, var(--bg-secondary), var(--bg-hover), var(--bg-secondary));
  animation: shimmer 1.5s infinite;
}

.symbolon-card__number {
  position: absolute;
  top: var(--space-3);
  right: var(--space-3);
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
  color: var(--color-primary);
  font-weight: var(--font-weight-bold);
  border-radius: 50%;
  font-size: var(--font-size-small);
}

.symbolon-card__content {
  padding: var(--space-4);
}

.symbolon-card__title {
  font-size: var(--font-size-h4);
  margin-bottom: var(--space-3);
  color: var(--color-primary);
}

.symbolon-card__keywords {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-bottom: var(--space-3);
}

.symbolon-card__excerpt {
  font-size: var(--font-size-small);
  color: var(--text-secondary);
  line-height: var(--line-height-normal);
}

/* Grid Layout */
.symbolon-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-5);
}

@media (min-width: 640px) {
  .symbolon-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .symbolon-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  z-index: 500;
}

.symbolon-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  background: var(--bg-secondary);
  border-radius: 12px;
  overflow-y: auto;
  z-index: 600;
  animation: fadeIn 200ms ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translate(-50%, -48%); }
  to { opacity: 1; transform: translate(-50%, -50%); }
}

.symbolon-modal__close {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  font-size: 32px;
  line-height: 1;
  cursor: pointer;
  z-index: 10;
}

.symbolon-modal__content {
  display: grid;
  gap: var(--space-6);
  padding: var(--space-6);
}

@media (min-width: 768px) {
  .symbolon-modal__content {
    grid-template-columns: 1fr 1.5fr;
  }
}

.symbolon-modal__image {
  width: 100%;
  border-radius: 8px;
}

.symbolon-modal__number {
  font-size: var(--font-size-small);
  color: var(--text-secondary);
  font-weight: var(--font-weight-medium);
}

.symbolon-modal__keywords {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin: var(--space-4) 0;
}

.symbolon-modal__section {
  margin-bottom: var(--space-5);
}

.symbolon-modal__section h3 {
  color: var(--color-primary);
  margin-bottom: var(--space-3);
}

.symbolon-modal__actions {
  padding: var(--space-5);
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
}
```

## 🧪 Testing Checklist

- [ ] Single card renders with image, title, keywords
- [ ] Card grid displays multiple cards correctly
- [ ] Card click opens modal with full interpretation
- [ ] Modal closes on overlay click, close button, and Escape key
- [ ] Image lazy loading works (network tab)
- [ ] Loading skeleton shows while images load
- [ ] Responsive grid: 1 col (mobile), 2 col (tablet), 3 col (desktop)
- [ ] Modal scrolls when content overflows
- [ ] No layout shift when images load
- [ ] Print layout readable

## 🔍 Accessibility Requirements

- [ ] Card images have descriptive `alt` text
- [ ] Cards keyboard focusable (tab)
- [ ] Modal has `role="dialog"` and `aria-modal="true"`
- [ ] Modal close button has `aria-label`
- [ ] Modal focus trapped when open (bonus)
- [ ] Escape key closes modal
- [ ] Screen reader announces card count

## 📦 Files to Create/Modify

- `frontend/src/components/symbolon/SymbolonCard.jsx` (create)
- `frontend/src/components/symbolon/SymbolonCard.css` (create)
- `frontend/src/components/symbolon/SymbolonGrid.jsx` (create)
- `frontend/src/components/symbolon/SymbolonGrid.css` (create)
- `frontend/src/components/symbolon/SymbolonModal.jsx` (create)
- `frontend/src/components/symbolon/SymbolonModal.css` (create)
- `frontend/src/components/symbolon/Symbolon.test.jsx` (create)

## 🔗 Dependencies

- Issue #4 (Card Component)
- Issue #3 (Button Component)
- Symbolon content JSON (`/backend/content/symbolon_universal_v1.json`)
- Symbolon images (`/backend/content/symbolon/`)

## 📝 Additional Notes

- Symbolon content already exists in `/backend/content/`
- Card images should be optimized (WebP format)
- Consider adding card flip animation (CSS transform)
- Consider adding "Shuffle" and "Draw Card" features (future)
- Test with all 78 Symbolon cards
- Modal should support navigation (prev/next card)

---

**Priority**: P1 (High)  
**Estimated Effort**: 10 hours  
**Assignee**: TBD  
**Epic**: Epic 6 - Symbolon Card System
