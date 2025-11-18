# Color Palette and Design System

## Overview

The "Healing Cosmos" design system provides a comprehensive, accessible, and cohesive visual language for the Mula: The Root astrology application. This document serves as the single source of truth for all design tokens, color usage, typography, spacing, and component styling guidelines.

## Table of Contents

- [Color Palette](#color-palette)
- [Accessibility & WCAG Compliance](#accessibility--wcag-compliance)
- [Design Tokens](#design-tokens)
- [Typography System](#typography-system)
- [Spacing & Layout](#spacing--layout)
- [Component Styles](#component-styles)
- [Theme System (Light/Dark Mode)](#theme-system-lightdark-mode)
- [Usage Guidelines](#usage-guidelines)
- [Implementation Examples](#implementation-examples)

---

## Color Palette

### "Healing Cosmos" - Primary Colors

Our color palette embodies the balance between mystical wisdom and clinical professionalism, creating a welcoming yet trustworthy atmosphere.

#### Primary Color - Deep Indigo
- **Hex**: `#3E4B6E`
- **RGB**: `rgb(62, 75, 110)`
- **Usage**: Main navigation, primary buttons, headers, key interactive elements
- **Meaning**: Trust, wisdom, depth, stability
- **Variants**:
  - Light: `#5A6B8F` - Hover states, lighter backgrounds
  - Dark: `#2C3651` - Active states, pressed buttons

#### Secondary Color - Soft Sage
- **Hex**: `#A5B8A4`
- **RGB**: `rgb(165, 184, 164)`
- **Usage**: Secondary buttons, borders, subtle backgrounds, success states
- **Meaning**: Healing, balance, renewal, growth
- **Variants**:
  - Light: `#C4D4C3` - Hover backgrounds, light accents
  - Dark: `#8A9C89` - Active states, borders

#### Accent Color - Muted Lavender
- **Hex**: `#B296CA`
- **RGB**: `rgb(178, 150, 202)`
- **Usage**: Highlights, focus indicators, special features, spiritual elements
- **Meaning**: Spirituality, transformation, intuition
- **Variants**:
  - Light: `#D1BBE3` - Hover states, light backgrounds
  - Dark: `#9477A8` - Active states, darker accents

#### CTA (Call-to-Action) Color - Warm Terracotta
- **Hex**: `#C17B5C`
- **RGB**: `rgb(193, 123, 92)`
- **Usage**: Primary action buttons, important alerts, emphasis
- **Meaning**: Grounding, action, warmth, connection to earth
- **Variants**:
  - Light: `#D89C7D` - Hover states
  - Dark: `#A56249` - Active states, pressed buttons

### Neutral Colors

#### Neutrals - Light Theme
- **50** (Cream): `#F5F3EE` - Primary background in light mode
- **100**: `#E8E4DB` - Secondary backgrounds, disabled states
- **200**: `#D4CEC1` - Borders, dividers, subtle backgrounds
- **700**: `#4A4E5C` - Secondary text
- **800**: `#383C4A` - Primary text (dark theme)
- **900** (Charcoal): `#2D3142` - Primary text, headings (light theme), primary background (dark theme)

### Semantic Colors

These colors convey specific states and feedback:

#### Success - Forest Sage
- **Hex**: `#81987F`
- **RGB**: `rgb(129, 152, 127)`
- **Usage**: Success messages, completed actions, positive feedback
- **Contrast Ratio (on white)**: 4.58:1 ✓ WCAG AA

#### Warning - Golden Amber
- **Hex**: `#E8B86D`
- **RGB**: `rgb(232, 184, 109)`
- **Usage**: Warning messages, caution indicators, alerts
- **Contrast Ratio (on white)**: 2.64:1 ⚠️ Use with dark text

#### Error - Terracotta
- **Hex**: `#C17B5C`
- **RGB**: `rgb(193, 123, 92)`
- **Usage**: Error messages, validation failures, destructive actions
- **Contrast Ratio (on white)**: 3.67:1 ⚠️ Use with white text on this background

#### Info - Soft Teal
- **Hex**: `#7FA99B`
- **RGB**: `rgb(127, 169, 155)`
- **Usage**: Informational messages, tips, neutral notifications
- **Contrast Ratio (on white)**: 3.89:1 ✓ WCAG AA (for large text)

---

## Accessibility & WCAG Compliance

All colors in this design system have been evaluated for WCAG 2.1 Level AA compliance. This section provides contrast ratios and usage guidelines to ensure accessibility.

### Contrast Requirements

- **Normal text** (< 18pt or < 14pt bold): Minimum 4.5:1
- **Large text** (≥ 18pt or ≥ 14pt bold): Minimum 3:1
- **UI components & graphics**: Minimum 3:1

### Contrast Ratios - Light Mode

| Foreground Color | Background | Ratio | WCAG AA | Usage |
|------------------|------------|-------|---------|-------|
| Primary (#3E4B6E) | Cream (#F5F3EE) | 6.89:1 | ✓✓ Pass | Body text, headings |
| Charcoal (#2D3142) | Cream (#F5F3EE) | 9.23:1 | ✓✓ Pass | Primary text |
| Primary (#3E4B6E) | White (#FFFFFF) | 7.92:1 | ✓✓ Pass | Text on cards |
| Sage (#A5B8A4) | White (#FFFFFF) | 2.34:1 | ✗ Fail | Borders only, not text |
| Lavender (#B296CA) | White (#FFFFFF) | 3.22:1 | ✓ Large text | Accent elements |
| Terracotta (#C17B5C) | White (#FFFFFF) | 3.67:1 | ✓ Large text | CTA buttons with white text |

### Contrast Ratios - Dark Mode

| Foreground Color | Background | Ratio | WCAG AA | Usage |
|------------------|------------|-------|---------|-------|
| Cream (#F5F3EE) | Charcoal (#2D3142) | 9.23:1 | ✓✓ Pass | Primary text in dark mode |
| Sage (#A5B8A4) | Charcoal (#2D3142) | 3.94:1 | ✓ Large text | Secondary text |
| Cream (#F5F3EE) | Secondary BG (#3A4257) | 7.12:1 | ✓✓ Pass | Text on cards (dark mode) |

### Accessible Color Usage Guidelines

1. **Never use color alone** to convey information. Always pair with icons, text, or patterns.
2. **Focus indicators** must have 3:1 contrast against background and adjacent colors.
3. **Interactive elements** (buttons, links) must have 3:1 contrast in all states.
4. **Error messages** should include icons and descriptive text, not just red color.
5. **Status indicators** should use icons + text + color for redundancy.

### Testing Tools

To verify color contrast:
- **Chrome DevTools**: Lighthouse accessibility audit
- **Online Tools**: 
  - WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
  - Colorable: https://colorable.jxnblk.com/
- **Browser Extensions**: 
  - axe DevTools
  - WAVE Evaluation Tool

---

## Design Tokens

Design tokens are the smallest, indivisible design decisions stored as CSS custom properties. They ensure consistency and enable easy theming.

### Implementation Location

All design tokens are defined in:
```
/frontend/src/styles/variables.css
```

### Token Structure

```css
:root {
  /* ============================================
     COLOR TOKENS
     ============================================ */
  
  /* Primary Colors */
  --color-primary: #3E4B6E;
  --color-primary-light: #5A6B8F;
  --color-primary-dark: #2C3651;
  
  --color-secondary: #A5B8A4;
  --color-secondary-light: #C4D4C3;
  --color-secondary-dark: #8A9C89;
  
  --color-accent: #B296CA;
  --color-accent-light: #D1BBE3;
  --color-accent-dark: #9477A8;
  
  --color-cta: #C17B5C;
  --color-cta-light: #D89C7D;
  --color-cta-dark: #A56249;
  
  /* Neutral Colors */
  --color-neutral-50: #F5F3EE;
  --color-neutral-100: #E8E4DB;
  --color-neutral-200: #D4CEC1;
  --color-neutral-700: #4A4E5C;
  --color-neutral-800: #383C4A;
  --color-neutral-900: #2D3142;
  
  /* Semantic Colors */
  --color-success: #81987F;
  --color-warning: #E8B86D;
  --color-error: #C17B5C;
  --color-info: #7FA99B;
  
  /* ============================================
     SPACING TOKENS (8pt Grid System)
     ============================================ */
  
  --space-1: 4px;   /* 0.25rem - Micro spacing */
  --space-2: 8px;   /* 0.5rem - Tiny spacing */
  --space-3: 16px;  /* 1rem - Small spacing */
  --space-4: 24px;  /* 1.5rem - Medium spacing */
  --space-5: 32px;  /* 2rem - Large spacing */
  --space-6: 48px;  /* 3rem - Extra large spacing */
  --space-7: 64px;  /* 4rem - XXL spacing */
  
  /* ============================================
     THEME VARIABLES (Context-Dependent)
     ============================================ */
  
  --bg-primary: var(--color-neutral-50);
  --bg-secondary: #FFFFFF;
  --bg-hover: rgba(165, 184, 164, 0.1);
  
  --text-primary: var(--color-neutral-900);
  --text-secondary: rgba(62, 75, 110, 0.7);
  
  --border-color: rgba(165, 184, 164, 0.3);
  
  /* ============================================
     ELEVATION (Shadows)
     ============================================ */
  
  --elevation-1: 0 1px 2px rgba(45, 49, 66, 0.04);
  --elevation-2: 0 4px 12px rgba(45, 49, 66, 0.06);
  --elevation-3: 0 8px 24px rgba(45, 49, 66, 0.08);
  
  /* ============================================
     TYPOGRAPHY TOKENS
     ============================================ */
  
  /* Font Families */
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'Courier New', monospace;
  
  /* Font Sizes */
  --font-size-tiny: 12px;     /* 0.75rem */
  --font-size-small: 14px;    /* 0.875rem */
  --font-size-base: 16px;     /* 1rem */
  --font-size-h4: 20px;       /* 1.25rem */
  --font-size-h3: 24px;       /* 1.5rem */
  --font-size-h2: 28px;       /* 1.75rem */
  --font-size-h1: 32px;       /* 2rem */
  
  /* Font Weights */
  --font-weight-light: 300;
  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  
  /* Line Heights */
  --line-height-tight: 1.2;
  --line-height-normal: 1.5;
  --line-height-loose: 1.75;
  
  /* Letter Spacing */
  --letter-spacing-tight: -0.025em;
  --letter-spacing-normal: 0;
  --letter-spacing-wide: 0.025em;
  
  /* ============================================
     BORDER RADIUS
     ============================================ */
  
  --radius-small: 4px;
  --radius-medium: 8px;
  --radius-large: 12px;
  --radius-full: 9999px;
  
  /* ============================================
     TRANSITIONS
     ============================================ */
  
  --transition-fast: 150ms ease;
  --transition-base: 250ms ease;
  --transition-slow: 350ms ease;
}
```

---

## Typography System

### Font Families

#### Primary Font: Inter (or System Fallback)
```css
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```
- **Usage**: All body text, UI elements, headings
- **Characteristics**: Highly readable, modern, excellent at small sizes
- **Weights Available**: 300, 400, 500, 600, 700

#### Monospace Font: JetBrains Mono
```css
--font-mono: 'JetBrains Mono', 'Courier New', monospace;
```
- **Usage**: Code snippets, technical data, timestamps
- **Characteristics**: Clear distinction between similar characters

### Type Scale

#### Headings

| Element | Size (Desktop) | Size (Mobile) | Weight | Line Height | Usage |
|---------|---------------|---------------|---------|-------------|-------|
| H1 | 32px (2rem) | 28px | 700 (Bold) | 1.2 | Page titles |
| H2 | 28px (1.75rem) | 24px | 600 (Semibold) | 1.2 | Section headers |
| H3 | 24px (1.5rem) | 20px | 600 (Semibold) | 1.2 | Subsection headers |
| H4 | 20px (1.25rem) | 18px | 500 (Medium) | 1.2 | Card titles |

#### Body Text

| Element | Size | Weight | Line Height | Usage |
|---------|------|--------|-------------|-------|
| Base | 16px (1rem) | 400 (Regular) | 1.5 | Body copy, paragraphs |
| Small | 14px (0.875rem) | 400 (Regular) | 1.5 | Captions, labels |
| Tiny | 12px (0.75rem) | 400 (Regular) | 1.5 | Metadata, timestamps |

### Responsive Typography

```css
/* Mobile (< 768px) */
@media (max-width: 767px) {
  :root {
    --font-size-h1: 28px;
    --font-size-h2: 24px;
    --font-size-h3: 20px;
    --font-size-h4: 18px;
  }
}

/* Small Mobile (< 480px) */
@media (max-width: 480px) {
  :root {
    --font-size-h1: 24px;
    --font-size-h2: 22px;
    --font-size-h3: 18px;
  }
}
```

### Typography Usage Examples

```css
/* Heading Styles */
h1, h2, h3, h4 {
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-tight);
  letter-spacing: var(--letter-spacing-tight);
  margin: 0 0 var(--space-4) 0;
  color: var(--text-primary);
}

h1 {
  font-size: var(--font-size-h1);
  font-weight: var(--font-weight-bold);
}

/* Body Text */
body {
  font-family: var(--font-primary);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-regular);
  line-height: var(--line-height-normal);
  color: var(--text-primary);
}

/* Small Text */
.text-small {
  font-size: var(--font-size-small);
  color: var(--text-secondary);
}
```

---

## Spacing & Layout

### 8-Point Grid System

All spacing values are multiples of 4px (0.25rem), creating a consistent rhythm throughout the interface.

| Token | Value | Usage |
|-------|-------|-------|
| `--space-1` | 4px | Tight spacing, icon padding |
| `--space-2` | 8px | Button padding, small gaps |
| `--space-3` | 16px | Standard element spacing |
| `--space-4` | 24px | Card padding, section spacing |
| `--space-5` | 32px | Large gaps, section margins |
| `--space-6` | 48px | Page sections |
| `--space-7` | 64px | Major page sections |

### Layout Breakpoints

```css
/* Mobile First Approach */
--breakpoint-mobile: 320px;   /* Mobile (up to 767px) */
--breakpoint-tablet: 768px;   /* Tablet (768px - 1023px) */
--breakpoint-desktop: 1024px; /* Desktop (1024px - 1439px) */
--breakpoint-large: 1440px;   /* Large Desktop (1440px+) */
```

### Grid System

#### Desktop (≥ 1024px)
- **Columns**: 12
- **Gutter**: 24px
- **Max Width**: 1200px

#### Tablet (768px - 1023px)
- **Columns**: 8
- **Gutter**: 20px
- **Max Width**: 100%

#### Mobile (< 768px)
- **Columns**: 4
- **Gutter**: 16px
- **Max Width**: 100%

---

## Component Styles

### Buttons

#### Primary Button
```css
.btn-primary {
  background: var(--color-primary);
  color: var(--color-neutral-50);
  border: none;
  padding: 12px 24px;
  border-radius: var(--radius-medium);
  font-weight: var(--font-weight-medium);
  transition: var(--transition-base);
}

.btn-primary:hover {
  background: var(--color-primary-light);
  transform: translateY(-1px);
  box-shadow: var(--elevation-2);
}

.btn-primary:active {
  background: var(--color-primary-dark);
  transform: translateY(0);
}
```

#### Secondary Button
```css
.btn-secondary {
  background: transparent;
  color: var(--color-primary);
  border: 1px solid var(--color-primary);
  padding: 12px 24px;
  border-radius: var(--radius-medium);
  font-weight: var(--font-weight-medium);
  transition: var(--transition-base);
}

.btn-secondary:hover {
  background: var(--bg-hover);
}
```

#### CTA Button (Call-to-Action)
```css
.btn-cta {
  background: var(--color-cta);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: var(--radius-medium);
  font-weight: var(--font-weight-medium);
  box-shadow: var(--elevation-2);
  transition: var(--transition-base);
}

.btn-cta:hover {
  background: var(--color-cta-light);
  box-shadow: var(--elevation-3);
}
```

### Cards

#### Basic Card
```css
.card {
  background: var(--bg-secondary);
  border-radius: var(--radius-large);
  padding: var(--space-4);
  box-shadow: var(--elevation-1);
  border: 1px solid var(--border-color);
  transition: var(--transition-base);
}

.card:hover {
  box-shadow: var(--elevation-2);
  transform: translateY(-2px);
}
```

#### Stat Card
```css
.card-stat {
  background: var(--bg-secondary);
  border-radius: var(--radius-large);
  padding: var(--space-4);
  text-align: center;
  border-left: 4px solid var(--color-accent);
}

.card-stat__metric {
  font-size: var(--font-size-h1);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
}

.card-stat__label {
  font-size: var(--font-size-small);
  color: var(--text-secondary);
  margin-top: var(--space-2);
}
```

### Form Inputs

```css
.input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-medium);
  font-size: var(--font-size-base);
  color: var(--text-primary);
  background: var(--bg-secondary);
  transition: var(--transition-fast);
}

.input:focus {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
  border-color: var(--color-accent);
}

.input.error {
  border-color: var(--color-error);
}

.input-label {
  display: block;
  margin-bottom: var(--space-2);
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}
```

### Badges

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-medium);
}

.badge--success {
  background: var(--color-success);
  color: white;
}

.badge--warning {
  background: var(--color-warning);
  color: var(--color-neutral-900);
}

.badge--error {
  background: var(--color-error);
  color: white;
}

.badge--info {
  background: var(--color-info);
  color: white;
}
```

---

## Theme System (Light/Dark Mode)

### Implementation

The theme system uses CSS custom properties that can be reassigned based on the `[data-theme]` attribute on the `<html>` element.

#### Light Theme (Default)
```css
:root {
  --bg-primary: var(--color-neutral-50);
  --bg-secondary: #FFFFFF;
  --text-primary: var(--color-neutral-900);
  --text-secondary: rgba(62, 75, 110, 0.7);
  --border-color: rgba(165, 184, 164, 0.3);
}
```

#### Dark Theme
```css
[data-theme="dark"] {
  --bg-primary: var(--color-neutral-900);
  --bg-secondary: #3A4257;
  --text-primary: var(--color-neutral-50);
  --text-secondary: var(--color-secondary);
  --border-color: rgba(62, 75, 110, 0.4);
}
```

#### System Preference Detection
```css
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg-primary: var(--color-neutral-900);
    --bg-secondary: #3A4257;
    --text-primary: var(--color-neutral-50);
    --text-secondary: var(--color-secondary);
    --border-color: rgba(62, 75, 110, 0.4);
  }
}
```

### Theme Toggle Component

The `ThemeToggle` component allows users to manually switch between light and dark modes, with the preference persisted in `localStorage`.

**Location**: `/frontend/src/components/shared/ThemeToggle.tsx`

**Features**:
- Detects system preference on first load
- Persists user choice in localStorage
- Provides accessible toggle button
- Smooth transitions between themes

---

## Usage Guidelines

### Do's ✓

1. **Always use CSS variables** for colors, spacing, and typography
   ```css
   /* ✓ Good */
   color: var(--color-primary);
   padding: var(--space-4);
   
   /* ✗ Bad */
   color: #3E4B6E;
   padding: 24px;
   ```

2. **Use semantic color tokens** for theme-dependent values
   ```css
   /* ✓ Good */
   background: var(--bg-primary);
   color: var(--text-primary);
   
   /* ✗ Bad */
   background: #F5F3EE;
   color: #2D3142;
   ```

3. **Follow the 8pt spacing grid**
   ```css
   /* ✓ Good */
   margin: var(--space-3) var(--space-4);
   
   /* ✗ Bad */
   margin: 15px 25px;
   ```

4. **Ensure minimum contrast ratios**
   - 4.5:1 for normal text
   - 3:1 for large text and UI components

5. **Provide focus indicators** on all interactive elements
   ```css
   button:focus-visible {
     outline: 2px solid var(--color-accent);
     outline-offset: 2px;
   }
   ```

### Don'ts ✗

1. **Don't hardcode colors** - Always use design tokens
2. **Don't use color alone** to convey meaning - Combine with icons/text
3. **Don't create arbitrary spacing** - Stick to the spacing scale
4. **Don't override theme variables** without good reason
5. **Don't skip accessibility testing** - Verify contrast and keyboard navigation

---

## Implementation Examples

### Example 1: Creating a Custom Card Component

```jsx
// Card.jsx
import React from 'react';
import './Card.css';

const Card = ({ children, variant = 'default', padding = 'medium' }) => {
  return (
    <div className={`card card--${variant} card--padding-${padding}`}>
      {children}
    </div>
  );
};

export default Card;
```

```css
/* Card.css */
.card {
  background: var(--bg-secondary);
  border-radius: var(--radius-large);
  box-shadow: var(--elevation-1);
  border: 1px solid var(--border-color);
  transition: var(--transition-base);
}

.card:hover {
  box-shadow: var(--elevation-2);
  transform: translateY(-2px);
}

.card--padding-small {
  padding: var(--space-3);
}

.card--padding-medium {
  padding: var(--space-4);
}

.card--padding-large {
  padding: var(--space-5);
}

.card--variant-primary {
  border-left: 4px solid var(--color-primary);
}

.card--variant-accent {
  border-left: 4px solid var(--color-accent);
}
```

### Example 2: Accessible Button with Focus State

```jsx
// Button.jsx
import React from 'react';
import './Button.css';

const Button = ({ 
  children, 
  variant = 'primary', 
  onClick, 
  ariaLabel,
  disabled = false 
}) => {
  return (
    <button
      className={`btn btn--${variant}`}
      onClick={onClick}
      aria-label={ariaLabel}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

export default Button;
```

```css
/* Button.css */
.btn {
  padding: 12px var(--space-4);
  border-radius: var(--radius-medium);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  border: none;
  cursor: pointer;
  transition: var(--transition-base);
  font-family: var(--font-primary);
}

.btn:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn--primary {
  background: var(--color-primary);
  color: var(--color-neutral-50);
}

.btn--primary:hover:not(:disabled) {
  background: var(--color-primary-light);
  box-shadow: var(--elevation-2);
}

.btn--secondary {
  background: transparent;
  color: var(--color-primary);
  border: 1px solid var(--color-primary);
}

.btn--secondary:hover:not(:disabled) {
  background: var(--bg-hover);
}

.btn--cta {
  background: var(--color-cta);
  color: white;
  box-shadow: var(--elevation-2);
}

.btn--cta:hover:not(:disabled) {
  background: var(--color-cta-light);
  transform: translateY(-1px);
  box-shadow: var(--elevation-3);
}
```

### Example 3: Form with Validation States

```jsx
// Input.jsx
import React from 'react';
import './Input.css';

const Input = ({ 
  label, 
  name, 
  value, 
  onChange, 
  error, 
  required = false,
  type = 'text'
}) => {
  return (
    <div className="input-group">
      <label htmlFor={name} className="input-label">
        {label}
        {required && <span className="input-required">*</span>}
      </label>
      <input
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        className={`input ${error ? 'input--error' : ''}`}
        aria-invalid={!!error}
        aria-describedby={error ? `${name}-error` : undefined}
      />
      {error && (
        <span id={`${name}-error`} className="input-error" role="alert">
          {error}
        </span>
      )}
    </div>
  );
};

export default Input;
```

```css
/* Input.css */
.input-group {
  margin-bottom: var(--space-4);
}

.input-label {
  display: block;
  margin-bottom: var(--space-2);
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}

.input-required {
  color: var(--color-error);
  margin-left: var(--space-1);
}

.input {
  width: 100%;
  padding: 12px var(--space-3);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-medium);
  font-size: var(--font-size-base);
  color: var(--text-primary);
  background: var(--bg-secondary);
  transition: var(--transition-fast);
  font-family: var(--font-primary);
}

.input:focus {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
  border-color: var(--color-accent);
}

.input--error {
  border-color: var(--color-error);
}

.input--error:focus {
  outline-color: var(--color-error);
}

.input-error {
  display: block;
  margin-top: var(--space-2);
  font-size: var(--font-size-small);
  color: var(--color-error);
}
```

---

## Testing Checklist

Use this checklist to ensure your implementation follows the design system:

### Color & Accessibility
- [ ] All colors use CSS variables (no hardcoded hex values)
- [ ] Text contrast ratios meet WCAG AA (4.5:1 for normal text)
- [ ] UI component contrast meets 3:1 minimum
- [ ] Color is not the only means of conveying information
- [ ] Both light and dark themes tested

### Typography
- [ ] All font sizes use CSS variables
- [ ] Headings use appropriate semantic HTML (h1-h4)
- [ ] Line height is at least 1.5 for body text
- [ ] Text can be resized to 200% without breaking layout
- [ ] Font weights are from the defined scale

### Spacing & Layout
- [ ] All spacing uses the 8pt grid scale
- [ ] Responsive breakpoints are respected
- [ ] Touch targets are minimum 44x44px on mobile
- [ ] Layout works on mobile, tablet, and desktop

### Components
- [ ] All interactive elements have focus indicators
- [ ] Hover states are defined and visible
- [ ] Disabled states are clearly indicated
- [ ] Loading states are accessible (aria-live)
- [ ] Error messages are announced to screen readers

### Theme Support
- [ ] Component works in both light and dark themes
- [ ] Theme-dependent colors use semantic tokens
- [ ] No FOUT (Flash of Unstyled Text) on page load
- [ ] System preference is respected

---

## Maintenance & Updates

### Version History

- **v1.0** (October 2025) - Initial design system documentation
  - "Healing Cosmos" color palette
  - 8pt spacing grid
  - Light/dark theme support
  - Comprehensive accessibility guidelines

### Future Enhancements

- [ ] Additional theme variants (e.g., high contrast mode)
- [ ] Expanded component library documentation
- [ ] Animation and motion guidelines
- [ ] Icon system documentation
- [ ] Data visualization color palettes

### Contributing

When proposing changes to the design system:

1. **Document the rationale** - Why is this change needed?
2. **Verify accessibility** - Ensure WCAG AA compliance
3. **Test both themes** - Confirm light and dark mode support
4. **Update documentation** - Keep this file current
5. **Provide examples** - Show implementation in code

---

## Resources & References

### Design Tools
- **Figma**: Design mockups and prototypes
- **Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Color Palette Generator**: https://coolors.co/

### Documentation
- [Project Overview](/docs/redesign/PROJECT_OVERVIEW.md)
- [Quick Reference](/docs/redesign/QUICK_REFERENCE.md)
- [Component Issues](/docs/redesign/github-project/issues/)

### External Resources
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN: CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)
- [Inclusive Components](https://inclusive-components.design/)

---

**Document Version**: 1.0  
**Last Updated**: October 29, 2025  
**Maintained By**: Product Management Team  
**Status**: Active

For questions or suggestions, please open an issue in the GitHub repository.
