---
title: "Set Up CSS Variables & Theme System"
labels: ["component:design-system", "P0-Critical", "epic", "feature"]
assignees: []
milestone: "Milestone 1: Foundation"
---

## 🎯 Objective

Implement the "Healing Cosmos" color palette and spacing system using CSS custom properties. Include light/dark mode support with theme toggle functionality.

## 📋 Description

This is the foundation of our design system. All colors, spacing values, and theme-specific styles must be defined as CSS variables to ensure consistency across the entire application and enable easy theme switching.

## 🔗 References

- **Design Artifact**: `COLOR_SCHEMES.md` (CSS Variables Structure section)
- **Guide**: `AI_COPILOT_GUIDE.md` - Design System Rules
- **Epic**: #1 (Design System & Component Library)

## ✅ Acceptance Criteria

- [ ] All colors from `COLOR_SCHEMES.md` defined as CSS variables in `/frontend/src/styles/variables.css`
- [ ] Spacing scale (4px, 8px, 16px, 24px, 32px, 48px, 64px) implemented as CSS variables
- [ ] Light theme variant created in `:root` selector
- [ ] Dark theme variant created in `[data-theme="dark"]` selector
- [ ] Theme persists in `localStorage` between sessions
- [ ] Theme toggle component functional (switch between light/dark)
- [ ] `prefers-color-scheme` media query respected for auto theme detection
- [ ] All color contrast ratios meet WCAG AA standards (tested)

## 💻 Implementation Notes

### CSS Variables Structure

```css
/* /frontend/src/styles/variables.css */
:root {
  /* Colors - Healing Cosmos Palette */
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
  
  /* Spacing Scale (8pt grid) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 16px;
  --space-4: 24px;
  --space-5: 32px;
  --space-6: 48px;
  --space-7: 64px;
  
  /* Theme Variables (reassignable) */
  --bg-primary: var(--color-neutral-50);
  --bg-secondary: #FFFFFF;
  --text-primary: var(--color-neutral-900);
  --text-secondary: rgba(62, 75, 110, 0.7);
  --border-color: rgba(165, 184, 164, 0.3);
}

[data-theme="dark"] {
  --bg-primary: var(--color-neutral-900);
  --bg-secondary: #3A4257;
  --text-primary: var(--color-neutral-50);
  --text-secondary: var(--color-secondary);
  --border-color: rgba(62, 75, 110, 0.4);
}

/* Auto theme detection */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg-primary: var(--color-neutral-900);
    --bg-secondary: #3A4257;
    --text-primary: var(--color-neutral-50);
    --text-secondary: var(--color-secondary);
  }
}
```

### Theme Toggle Component

```jsx
// /frontend/src/components/shared/ThemeToggle.jsx
import React, { useState, useEffect } from 'react';

const ThemeToggle = () => {
  const [theme, setTheme] = useState('light');
  
  useEffect(() => {
    // Check localStorage or system preference
    const savedTheme = localStorage.getItem('theme');
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    const initialTheme = savedTheme || systemTheme;
    
    setTheme(initialTheme);
    document.documentElement.setAttribute('data-theme', initialTheme);
  }, []);
  
  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  };
  
  return (
    <button
      onClick={toggleTheme}
      aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      className="theme-toggle"
    >
      {theme === 'light' ? '🌙' : '☀️'}
    </button>
  );
};

export default ThemeToggle;
```

## 🧪 Testing Checklist

- [ ] All CSS variables load without errors
- [ ] Theme toggle switches between light and dark modes instantly
- [ ] Theme persists after page refresh
- [ ] System preference is respected when no saved theme
- [ ] Color contrast ratios verified with browser DevTools:
  - [ ] Primary on light background: 4.5:1+
  - [ ] Text on all backgrounds: 4.5:1+
  - [ ] Interactive elements: 3:1+
- [ ] No hardcoded colors found in codebase (audit with search)
- [ ] Dark mode readable and visually consistent

## 🔍 Accessibility Requirements

- [ ] Theme toggle has `aria-label` describing current/next state
- [ ] Color is not the only means of conveying information
- [ ] Focus indicators visible in both themes
- [ ] All text meets WCAG AA contrast requirements

## 📦 Files to Create/Modify

- `frontend/src/styles/variables.css` (create)
- `frontend/src/styles/themes.css` (create)
- `frontend/src/components/shared/ThemeToggle.jsx` (create)
- `frontend/src/components/shared/ThemeToggle.css` (create)
- `frontend/src/App.jsx` (modify to include ThemeToggle)

## 🔗 Dependencies

- None (foundational issue)

## 🚫 Blocked By

- None

## 📝 Additional Notes

- All future components MUST use these CSS variables
- Never hardcode color values
- See `AI_COPILOT_GUIDE.md` for enforcement examples
- Test in Chrome, Firefox, and Safari

---

**Priority**: P0 (Blocking)  
**Estimated Effort**: 4 hours  
**Assignee**: TBD  
**Epic**: Epic 1 - Design System
