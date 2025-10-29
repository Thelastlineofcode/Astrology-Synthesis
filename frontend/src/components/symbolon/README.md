# Symbolon Card Components

A collection of React components for displaying and interacting with Symbolon archetypal cards in the Astrology Synthesis application.

## Components

### SymbolonCard

Displays a single Symbolon card with image, title, number, and keywords.

**Props:**
- `card` (object): Card data containing:
  - `id`: Unique identifier
  - `number`: Card number (1-78)
  - `title`: Card title (e.g., "The Warrior")
  - `image`: Image filename (e.g., "symbolon-01.jpg")
  - `keywords`: Array of keyword strings
  - `meaning`: Core meaning text
- `onClick` (function): Handler called when card is clicked

**Features:**
- Lazy image loading with skeleton placeholder
- Displays first 3 keywords as badges
- Truncates meaning text to 120 characters
- Hover effect with elevation
- Responsive card sizing

**Example:**
```jsx
import { SymbolonCard } from '@/components/symbolon';

<SymbolonCard 
  card={cardData}
  onClick={() => handleCardClick(cardData)}
/>
```

### SymbolonGrid

Displays multiple Symbolon cards in a responsive grid layout.

**Props:**
- `cards` (array): Array of card objects
- `loading` (boolean): If true, shows skeleton loading states

**Features:**
- Responsive grid: 1 column (mobile), 2 columns (tablet), 3 columns (desktop)
- Skeleton loading states (6 placeholders)
- Automatic modal opening on card click
- Modal management built-in

**Example:**
```jsx
import { SymbolonGrid } from '@/components/symbolon';

<SymbolonGrid 
  cards={symbolonCards}
  loading={isLoading}
/>
```

### SymbolonModal

Full-screen modal displaying complete card details and interpretation.

**Props:**
- `card` (object): Card data (same structure as SymbolonCard)
- `onClose` (function): Handler called when modal is closed

**Features:**
- Overlay click closes modal
- Escape key closes modal
- Close button (× and "Close" button)
- Prevents body scroll when open
- Full card interpretation with sections:
  - Core Meaning
  - Interpretation
  - Themes & Archetypes
- All keywords displayed
- Print-friendly layout
- Responsive: single column (mobile), 2-column (desktop)

**Example:**
```jsx
import { SymbolonModal } from '@/components/symbolon';

{selectedCard && (
  <SymbolonModal
    card={selectedCard}
    onClose={() => setSelectedCard(null)}
  />
)}
```

## Card Data Structure

```javascript
{
  id: 1,
  number: 1,
  title: 'The Warrior',
  image: 'symbolon-01.jpg',
  keywords: ['Aggression', 'Conquest', 'Energy'],
  meaning: 'Core meaning text...',
  interpretation: 'Detailed interpretation...',
  themes: ['Theme 1', 'Theme 2', 'Theme 3']
}
```

## Styling

All components use CSS variables from the design system:
- `--color-primary`: Primary theme color
- `--color-accent`: Accent color for badges
- `--bg-primary`: Background color
- `--bg-secondary`: Card background
- `--text-primary`: Primary text color
- `--text-secondary`: Secondary text color
- `--space-*`: Spacing scale (1-7)
- `--elevation-*`: Shadow levels

Components automatically adapt to light/dark themes via CSS variables.

## Accessibility

- All images have descriptive `alt` attributes
- Modal has `role="dialog"` and `aria-modal="true"`
- Close button has `aria-label="Close modal"`
- Keyboard navigation: Escape key closes modal
- Focus management: body scroll prevented when modal open

## Testing

Comprehensive test suite covers:
- Component rendering
- User interactions (clicks, keyboard)
- Loading states
- Edge cases (missing data)
- Accessibility requirements

Run tests:
```bash
npm test Symbolon.test.jsx
```

## Demo

Visit `/symbolon-demo` to see all components in action with sample data.

## Dependencies

### Shared Components
- `Card`: Base card component
- `Button`: Button component  
- `Badge`: Badge/pill component

### External Dependencies
- React 19
- Next.js 16

## File Structure

```
frontend/src/components/symbolon/
├── SymbolonCard.jsx       # Individual card component
├── SymbolonCard.css       # Card styles
├── SymbolonGrid.jsx       # Grid layout component
├── SymbolonGrid.css       # Grid styles
├── SymbolonModal.jsx      # Modal component
├── SymbolonModal.css      # Modal styles
├── index.js               # Component exports
└── __tests__/
    └── Symbolon.test.jsx  # Test suite
```

## Images

Card images are stored in `/frontend/public/content/symbolon/` and named as `symbolon-XX.jpg` where XX is the card number (01-78).

## Performance

- Images use lazy loading (`loading="lazy"`)
- Skeleton loading states for better perceived performance
- CSS animations for smooth transitions
- Optimized grid layout with CSS Grid
