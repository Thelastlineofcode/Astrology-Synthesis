---
title: "Establish Typography System"
labels: ["component:design-system", "P0-Critical", "foundation"]
assignees: []
milestone: "Milestone 1: Foundation"
---

## 🎯 Objective

Define a complete typography system with font families, sizes, weights, and line heights that work harmoniously across all breakpoints.

## 📋 Description

Typography is fundamental to readability and hierarchy. Establish a type scale that provides clear visual hierarchy while maintaining accessibility and responsive behavior.

## 🔗 References

- **Design Artifact**: `COLOR_SCHEMES.md` (Typography section)
- **Guide**: `QUICK_REFERENCE.md` - Typography Scale
- **Guide**: `AI_COPILOT_GUIDE.md` - Accessibility Requirements

## ✅ Acceptance Criteria

- [ ] Font families defined (primary and monospace)
- [ ] Type scale established (h1, h2, h3, h4, body, small)
- [ ] Font weights defined (light, regular, medium, bold)
- [ ] Line heights optimized for readability
- [ ] Letter spacing applied where needed
- [ ] Responsive font sizes for mobile/tablet/desktop
- [ ] All text passes WCAG AA contrast ratios
- [ ] No FOUT (Flash of Unstyled Text) on page load

## 💻 Implementation Notes

### Typography CSS

```css
/* Add to /frontend/src/index.css or theme.css */

/* Import fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  /* Font Families */
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'Courier New', monospace;
  
  /* Type Scale - Desktop */
  --font-size-h1: 2.5rem;      /* 40px */
  --font-size-h2: 2rem;        /* 32px */
  --font-size-h3: 1.5rem;      /* 24px */
  --font-size-h4: 1.25rem;     /* 20px */
  --font-size-body: 1rem;      /* 16px */
  --font-size-small: 0.875rem; /* 14px */
  --font-size-tiny: 0.75rem;   /* 12px */
  
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
}

/* Base typography */
body {
  font-family: var(--font-primary);
  font-size: var(--font-size-body);
  font-weight: var(--font-weight-regular);
  line-height: var(--line-height-normal);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-tight);
  letter-spacing: var(--letter-spacing-tight);
  margin: 0 0 var(--space-4) 0;
}

h1 {
  font-size: var(--font-size-h1);
  font-weight: var(--font-weight-bold);
}

h2 {
  font-size: var(--font-size-h2);
}

h3 {
  font-size: var(--font-size-h3);
}

h4 {
  font-size: var(--font-size-h4);
}

/* Body text */
p {
  margin: 0 0 var(--space-4) 0;
  line-height: var(--line-height-normal);
}

/* Small text */
small, .text-small {
  font-size: var(--font-size-small);
}

.text-tiny {
  font-size: var(--font-size-tiny);
}

/* Monospace */
code, pre {
  font-family: var(--font-mono);
  font-size: 0.9em;
}

/* Responsive typography */
@media (max-width: 767px) {
  :root {
    --font-size-h1: 2rem;        /* 32px */
    --font-size-h2: 1.75rem;     /* 28px */
    --font-size-h3: 1.375rem;    /* 22px */
    --font-size-h4: 1.125rem;    /* 18px */
  }
}

@media (max-width: 480px) {
  :root {
    --font-size-h1: 1.75rem;     /* 28px */
    --font-size-h2: 1.5rem;      /* 24px */
    --font-size-h3: 1.25rem;     /* 20px */
  }
}
```

## 🧪 Testing Checklist

- [ ] All headings render with correct sizes
- [ ] Font weights visually distinct (light vs regular vs bold)
- [ ] Line heights provide good readability (not cramped)
- [ ] Responsive sizes adjust at mobile/tablet breakpoints
- [ ] Inter font loads correctly (no fallback flash)
- [ ] Monospace font renders in code blocks
- [ ] Text contrast meets WCAG AA (4.5:1 minimum)
- [ ] Long paragraphs remain readable (test with lorem ipsum)

## 🔍 Accessibility Requirements

- [ ] Minimum font size 14px for body text
- [ ] Line height at least 1.5 for body text
- [ ] Paragraph spacing at least 1.5x line height
- [ ] Text can be resized up to 200% without breaking layout

## 📦 Files to Create/Modify

- `frontend/src/index.css` (or `frontend/src/theme.css`)
- `frontend/public/index.html` (add font preconnect)

## 🔗 Dependencies

- Issue #1 (CSS Variables) - Typography variables build on theme system

## 📝 Additional Notes

- Consider adding `font-display: swap` to prevent FOIT
- Inter font is open source and highly readable
- Test on Windows/Mac for font rendering differences
- Ensure italic styles available if needed (e.g., for quotes)

---

**Priority**: P0 (Critical)  
**Estimated Effort**: 3 hours  
**Assignee**: TBD  
**Epic**: Epic 1 - Design System Foundation
