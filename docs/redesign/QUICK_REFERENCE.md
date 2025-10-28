# BMAD Astrology App - Quick Reference Guide

## 🎨 Color Palette (Healing Cosmos)

```css
/* Primary Colors */
--color-primary: #3E4B6E;        /* Deep Indigo */
--color-secondary: #A5B8A4;      /* Soft Sage */
--color-accent: #B296CA;         /* Muted Lavender */
--color-cta: #C17B5C;            /* Warm Terracotta */

/* Neutrals */
--color-neutral-light: #F5F3EE;  /* Cream */
--color-neutral-dark: #2D3142;   /* Charcoal */

/* Semantic */
--color-success: #81987F;        /* Forest Sage */
--color-warning: #E8B86D;        /* Golden Amber */
--color-error: #C17B5C;          /* Terracotta */
--color-info: #7FA99B;           /* Soft Teal */
```

## 📏 Spacing Scale (8pt Grid)

```css
--space-1: 4px;
--space-2: 8px;
--space-3: 16px;
--space-4: 24px;
--space-5: 32px;
--space-6: 48px;
--space-7: 64px;
```

## 📱 Breakpoints

```css
--breakpoint-mobile: 320px - 767px;
--breakpoint-tablet: 768px - 1023px;
--breakpoint-desktop: 1024px - 1439px;
--breakpoint-large: 1440px+;
```

## 🔤 Typography Scale

```css
/* Desktop */
--font-size-h1: 32px;
--font-size-h2: 24px;
--font-size-h3: 20px;
--font-size-body: 16px;
--font-size-small: 14px;
--font-size-tiny: 12px;

/* Mobile */
--font-size-h1-mobile: 28px;
--font-size-h2-mobile: 22px;
--font-size-h3-mobile: 18px;
```

## 🎭 Button Styles

### Primary Button
- Background: `var(--color-primary)`
- Text: `var(--color-neutral-light)`
- Padding: `12px 24px`
- Border radius: `8px`

### Secondary Button
- Border: `1px solid var(--color-primary)`
- Text: `var(--color-primary)`
- Background: `transparent`

### Tertiary Button
- Text: `var(--color-primary)`
- Background: `transparent`
- Hover: underline

## �� Card Styles

### Basic Card
- Background: `var(--color-neutral-light)`
- Border radius: `12px`
- Shadow: `0 2px 8px rgba(0,0,0,0.08)`
- Padding: `24px` (medium)

### Card Hover
- Shadow: `0 4px 16px rgba(0,0,0,0.12)`
- Transform: `translateY(-2px)`
- Transition: `250ms ease`

## ♿ Accessibility Checklist

- [ ] Color contrast 4.5:1 (text), 3:1 (UI)
- [ ] Focus indicator visible (2px outline, 2px offset)
- [ ] Keyboard navigation (Tab, Enter, Space, Arrows, Esc)
- [ ] ARIA labels on buttons/links
- [ ] Alt text on images
- [ ] Form labels associated
- [ ] Error messages announced (role="alert")
- [ ] Loading states announced (aria-live="polite")
- [ ] Touch targets 44px × 44px (mobile)

## 📝 Common Copy Patterns

### Buttons
- "Generate Chart"
- "Calculate Chart"
- "Start Analysis"
- "Save Entry"
- "Load Sample"

### Empty States
- "Your cosmic story awaits"
- "Start capturing your inner world"
- "Discover your behavioral blueprint"

### Success Messages
- "✨ Your chart is ready!"
- "Entry saved ✓"
- "Workflow activated 🎉"

### Loading States
- "Calculating planetary positions..."
- "Analyzing patterns..."
- "Loading chart..."

## 🧩 Component Usage

### Button
```jsx
<Button 
  variant="primary" 
  size="medium"
  onClick={handleClick}
  ariaLabel="Calculate chart"
>
  Calculate Chart
</Button>
```

### Card
```jsx
<Card variant="stat" padding="medium">
  <Card.Icon><CalendarIcon /></Card.Icon>
  <Card.Metric>7 days</Card.Metric>
  <Card.Label>Journal Streak</Card.Label>
</Card>
```

### Input
```jsx
<Input
  type="number"
  name="year"
  label="Birth Year"
  value={year}
  onChange={handleChange}
  error={errors.year}
  required
/>
```

### Modal
```jsx
<Modal
  isOpen={isOpen}
  onClose={handleClose}
  title="Card Details"
  ariaLabel="Card detail modal"
>
  {/* Content */}
</Modal>
```

## 🎯 File Naming Conventions

### Components
- PascalCase for files: `Button.jsx`
- CSS file matches: `Button.css`
- Test file: `Button.test.jsx`

### Folders
- lowercase with hyphens: `natal-chart/`
- grouped by feature: `components/chart/`

### CSS Classes
- BEM naming: `.card`, `.card--primary`, `.card__icon`
- Lowercase with hyphens

## 📦 Import Order

```jsx
// 1. React
import React, { useState, useEffect } from 'react';

// 2. External libraries
import { useRouter } from 'react-router-dom';

// 3. Internal components
import Button from '../shared/Button';
import Card from '../shared/Card';

// 4. Hooks and utilities
import { useAuth } from '../../hooks/useAuth';
import { formatDate } from '../../utils/date';

// 5. Styles
import './ComponentName.css';
```

## 🧪 Testing Commands

```bash
# Run all tests
npm test

# Run specific test file
npm test Button.test.jsx

# Run with coverage
npm test -- --coverage

# Lighthouse audit
npm run build && npx lighthouse http://localhost:3000
```

## 🚀 Development Commands

```bash
# Start dev server
npm start

# Build for production
npm run build

# Run linter
npm run lint

# Format code
npm run format
```

## �� Reference Documents

1. [Project Overview](./PROJECT_OVERVIEW.md)
2. [Epics and Issues](./EPICS_AND_ISSUES.md)
3. [AI Copilot Guide](./AI_COPILOT_GUIDE.md)
4. Component Structure (see attachments)
5. Color Schemes (see attachments)
6. UX Copy Guide (see attachments)
7. Design Inspiration (see attachments)

---

**Keep this guide handy while coding!**
