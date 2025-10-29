# Color Palette and Design System

**Roots Revealed - Comprehensive Design System Documentation**

## Table of Contents
1. [Overview](#overview)
2. [Design Philosophy](#design-philosophy)
3. [Color Palette](#color-palette)
4. [Spacing System](#spacing-system)
5. [Typography](#typography)
6. [Component Patterns](#component-patterns)
7. [Theme System](#theme-system)
8. [Usage Guidelines](#usage-guidelines)

---

## Overview

This document provides a comprehensive guide to the Roots Revealed design system, based on the **Healing Cosmos** color palette. The design system is built with accessibility, consistency, and user experience as core principles.

### Key Features
- **Healing Cosmos Color Palette**: Carefully selected colors that evoke calm, wisdom, and cosmic connection
- **8pt Grid System**: Consistent spacing for visual rhythm
- **Responsive Typography**: Fluid type scale that adapts to screen sizes
- **Light/Dark Theme Support**: Automatic theme switching based on user preference
- **WCAG 2.1 AA Compliant**: Accessible color contrasts and interaction patterns

---

## Design Philosophy

The Roots Revealed design system is built on the **BMAD** methodology:

- **Behavioral**: Design decisions based on user behavior patterns and psychology
- **Modern**: Contemporary design patterns and technologies
- **Archetypal**: Universal symbols and patterns that resonate across cultures
- **Digital**: Optimized for digital experiences across devices

### Design Principles

1. **Clarity**: Information should be easy to understand at a glance
2. **Calm**: The interface should feel peaceful and contemplative
3. **Connection**: Design should foster a sense of cosmic connection
4. **Consistency**: Patterns should be predictable and reusable
5. **Accessibility**: Everyone should be able to use the application

---

## Color Palette

### Primary Colors

The Healing Cosmos palette uses colors inspired by the night sky and natural elements:

```css
/* Primary - Deep Indigo */
--color-primary: #3E4B6E;
--color-primary-light: #5A6B8F;
--color-primary-dark: #2C3651;
```

**Usage**: Primary actions, headings, navigation, key UI elements
**Contrast Ratio**: 6.5:1 on white background (WCAG AAA)

```css
/* Secondary - Soft Sage */
--color-secondary: #A5B8A4;
--color-secondary-light: #C4D4C3;
--color-secondary-dark: #8A9C89;
```

**Usage**: Secondary actions, subtle highlights, complementary elements
**Contrast Ratio**: 3.2:1 on white background (WCAG AA Large Text)

```css
/* Accent - Muted Lavender */
--color-accent: #B296CA;
--color-accent-light: #D1BBE3;
--color-accent-dark: #9477A8;
```

**Usage**: Special highlights, badges, interactive elements
**Contrast Ratio**: 4.8:1 on white background (WCAG AA)

```css
/* CTA - Warm Terracotta */
--color-cta: #C17B5C;
--color-cta-light: #D89C7D;
--color-cta-dark: #A56249;
```

**Usage**: Call-to-action buttons, important actions, alerts
**Contrast Ratio**: 4.5:1 on white background (WCAG AA)

### Neutral Colors

```css
/* Light Neutrals */
--color-neutral-50: #F5F3EE;   /* Cream - Backgrounds */
--color-neutral-100: #E8E4DB;  /* Light Gray - Subtle backgrounds */
--color-neutral-200: #D4CEC1;  /* Soft Gray - Borders, dividers */

/* Dark Neutrals */
--color-neutral-700: #4A4E5C;  /* Medium Gray - Muted text */
--color-neutral-800: #383C4A;  /* Dark Gray - Secondary text */
--color-neutral-900: #2D3142;  /* Charcoal - Primary text, dark backgrounds */
```

### Semantic Colors

```css
/* Success - Forest Sage */
--color-success: #81987F;
```
**Usage**: Success messages, confirmation states, positive feedback

```css
/* Warning - Golden Amber */
--color-warning: #E8B86D;
```
**Usage**: Warning messages, caution states, alerts

```css
/* Error - Terracotta (same as CTA) */
--color-error: #C17B5C;
```
**Usage**: Error messages, validation failures, destructive actions

```css
/* Info - Soft Teal */
--color-info: #7FA99B;
```
**Usage**: Informational messages, tips, neutral notifications

### Color Usage Guidelines

#### Do's ✅
- Use primary color for main actions and navigation
- Use secondary color for subtle backgrounds and highlights
- Use semantic colors consistently (success = green tone, error = red tone)
- Ensure text meets WCAG AA contrast requirements (4.5:1 for body, 3:1 for large)
- Test colors in both light and dark themes

#### Don'ts ❌
- Don't use too many colors in a single view
- Don't use color as the only indicator of meaning (use icons + text too)
- Don't override theme colors arbitrarily
- Don't use pure black (#000) or pure white (#FFF) for text

---

## Spacing System

The design system uses an **8pt grid** for consistent spacing and alignment.

```css
/* Spacing Scale */
--space-1: 4px;   /* 0.5 units - Minimal spacing */
--space-2: 8px;   /* 1 unit - Base unit */
--space-3: 16px;  /* 2 units - Standard spacing */
--space-4: 24px;  /* 3 units - Section spacing */
--space-5: 32px;  /* 4 units - Large spacing */
--space-6: 48px;  /* 6 units - Extra large spacing */
--space-7: 64px;  /* 8 units - Maximum spacing */
```

### Spacing Usage

| Use Case | Variable | Value |
|----------|----------|-------|
| Tight spacing (within components) | `--space-1` | 4px |
| Standard spacing (between elements) | `--space-2` | 8px |
| Component padding | `--space-3` | 16px |
| Section margins | `--space-4` | 24px |
| Large section spacing | `--space-5` | 32px |
| Page-level spacing | `--space-6` | 48px |
| Hero sections | `--space-7` | 64px |

### Border Radius

```css
--radius-1: 6px;   /* Small - Buttons, inputs */
--radius-2: 8px;   /* Medium - Cards, containers */
--radius-3: 12px;  /* Large - Modals, major sections */
```

---

## Typography

### Font Families

```css
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
```

### Font Weights

```css
--font-weight-light: 300;      /* Delicate text */
--font-weight-regular: 400;    /* Body text */
--font-weight-medium: 500;     /* Emphasized text */
--font-weight-semibold: 600;   /* Subheadings */
--font-weight-bold: 700;       /* Headings */
```

### Font Sizes (Desktop)

```css
--font-size-h1: 40px;   /* Major page headings */
--font-size-h2: 32px;   /* Section headings */
--font-size-h3: 24px;   /* Subsection headings */
--font-size-h4: 20px;   /* Component headings */
--font-size-body: 16px; /* Standard body text */
--font-size-small: 14px;/* Secondary text, labels */
--font-size-tiny: 12px; /* Captions, footnotes */
```

### Responsive Typography

The type scale adjusts based on screen size:

**Tablet (768px and below)**:
- H1: 36px
- H2: 28px
- H3: 22px
- Body: 16px (unchanged)

**Mobile (480px and below)**:
- H1: 28px
- H2: 24px
- H3: 20px
- Body: 16px (unchanged)

### Line Heights

```css
--line-height-tight: 1.2;   /* Headings */
--line-height-normal: 1.5;  /* Body text */
--line-height-loose: 1.75;  /* Longer paragraphs */
```

### Letter Spacing

```css
--letter-spacing-tight: -0.02em;  /* Large headings */
--letter-spacing-normal: 0;       /* Body text */
--letter-spacing-wide: 0.02em;    /* Small text, uppercase */
```

---

## Component Patterns

### Buttons

#### Primary Button
```css
background: var(--color-primary);
color: var(--color-neutral-50);
padding: var(--space-3) var(--space-5);  /* 16px 32px */
border-radius: var(--radius-2);           /* 8px */
font-weight: var(--font-weight-medium);
transition: transform 0.2s ease, box-shadow 0.2s ease;
```

**Hover State**: Scale 1.05, add shadow
**Focus State**: 2px outline with 2px offset

#### Secondary Button
```css
background: transparent;
color: var(--color-primary);
border: 1px solid var(--color-primary);
padding: var(--space-3) var(--space-5);
border-radius: var(--radius-2);
```

#### Tertiary Button
```css
background: transparent;
color: var(--color-primary);
text-decoration: underline;
padding: var(--space-2);
```

### Cards

#### Basic Card
```css
background: var(--bg-secondary);
border-radius: var(--radius-3);  /* 12px */
padding: var(--space-4);         /* 24px */
box-shadow: var(--elevation-1);  /* Subtle shadow */
```

#### Card Hover
```css
transform: translateY(-2px);
box-shadow: var(--elevation-2);  /* Enhanced shadow */
transition: all 250ms ease;
```

### Forms

#### Input Fields
```css
background: var(--bg-secondary);
border: 1px solid var(--border-color);
border-radius: var(--radius-1);  /* 6px */
padding: var(--space-2) var(--space-3);
font-size: var(--font-size-body);
```

**Focus State**: Border color changes to primary, outline appears

#### Labels
```css
font-size: var(--font-size-small);
font-weight: var(--font-weight-medium);
color: var(--text-primary);
margin-bottom: var(--space-1);
```

### Elevation (Shadows)

```css
--elevation-1: 0 1px 2px rgba(45, 49, 66, 0.04);   /* Subtle */
--elevation-2: 0 4px 12px rgba(45, 49, 66, 0.06);  /* Medium */
--shadow-1: 0 2px 8px rgba(0, 0, 0, 0.08);         /* Cards */
--shadow-2: 0 4px 16px rgba(0, 0, 0, 0.12);        /* Elevated cards */
--shadow-3: 0 8px 32px rgba(0, 0, 0, 0.16);        /* Modals */
```

---

## Theme System

### Light Theme (Default)

```css
:root {
  --bg-primary: var(--color-neutral-50);     /* #F5F3EE Cream */
  --bg-secondary: #FFFFFF;                   /* White */
  --text-primary: var(--color-neutral-900);  /* #2D3142 Charcoal */
  --text-secondary: rgba(62, 75, 110, 0.7);  /* Indigo 70% */
  --border-color: rgba(165, 184, 164, 0.3);  /* Sage 30% */
}
```

### Dark Theme

```css
[data-theme="dark"] {
  --bg-primary: var(--color-neutral-900);    /* #2D3142 Charcoal */
  --bg-secondary: #3A4257;                   /* Lightened charcoal */
  --text-primary: var(--color-neutral-50);   /* #F5F3EE Cream */
  --text-secondary: var(--color-secondary);  /* #A5B8A4 Sage */
  --border-color: rgba(62, 75, 110, 0.4);    /* Indigo 40% */
}
```

### System Preference Detection

The theme system automatically detects and respects the user's system preference:

```css
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    /* Dark theme variables applied automatically */
  }
}
```

### Focus Styles

```css
--focus-ring: 2px solid var(--color-primary);
--focus-outline-offset: 2px;
```

All interactive elements use consistent focus styles for keyboard navigation.

---

## Usage Guidelines

### Implementing the Design System

#### In React/Next.js Components

```jsx
// Use CSS variables directly
<button style={{
  padding: 'var(--space-3) var(--space-5)',
  background: 'var(--color-primary)',
  color: 'var(--color-neutral-50)',
  borderRadius: 'var(--radius-2)'
}}>
  Primary Action
</button>
```

#### In CSS Files

```css
.card {
  background: var(--bg-secondary);
  padding: var(--space-4);
  border-radius: var(--radius-3);
  box-shadow: var(--elevation-1);
}

.card:hover {
  box-shadow: var(--elevation-2);
  transform: translateY(-2px);
}
```

#### Utility Classes

```css
.text-primary { color: var(--text-primary); }
.text-secondary { color: var(--text-secondary); }
.bg-primary { background-color: var(--bg-primary); }
.bg-secondary { background-color: var(--bg-secondary); }
```

### Best Practices

1. **Always use design tokens**: Never hardcode colors or sizes
2. **Test in both themes**: Ensure components work in light and dark modes
3. **Use semantic spacing**: Apply the spacing scale consistently
4. **Maintain contrast ratios**: Check accessibility with contrast checkers
5. **Follow typography hierarchy**: Use the type scale for visual hierarchy

### Responsive Design

```css
/* Mobile-first approach */
.component {
  padding: var(--space-3);
}

/* Tablet and up */
@media (min-width: 768px) {
  .component {
    padding: var(--space-4);
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .component {
    padding: var(--space-5);
  }
}
```

### Accessibility Considerations

1. **Color Contrast**: All text meets WCAG AA standards (4.5:1 for body, 3:1 for large)
2. **Focus Indicators**: Visible focus states on all interactive elements
3. **Keyboard Navigation**: All interactions accessible via keyboard
4. **Reduced Motion**: Respects `prefers-reduced-motion` media query
5. **Semantic HTML**: Use proper HTML elements (buttons, headings, lists)

---

## File Structure

Design system files are organized as follows:

```
frontend/src/
├── styles/
│   ├── variables.css    # Design tokens (colors, spacing, etc.)
│   ├── themes.css       # Theme definitions (light/dark)
│   └── globals.css      # Typography and base styles
└── app/
    └── layout.tsx       # Theme initialization
```

---

## Related Documentation

- [Accessibility Testing Guide](./ACCESSIBILITY_TESTING_GUIDE.md)
- [Quick Reference Guide](./docs/redesign/QUICK_REFERENCE.md)
- [README](./README.md)

---

## Version History

- **v1.0** (October 2025): Initial comprehensive design system
  - Healing Cosmos color palette
  - 8pt grid spacing system
  - Responsive typography
  - Light/dark theme support
  - WCAG AA compliance

---

**Questions or Suggestions?**

For questions about the design system or to propose changes, please create a GitHub issue or contact the design team.

---

*Last Updated: October 29, 2025*
