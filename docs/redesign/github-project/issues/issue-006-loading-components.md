---
title: "Create Loading & Skeleton Components"
labels: ["component:design-system", "P1-High", "ui-component"]
assignees: []
milestone: "Milestone 1: Foundation"
---

## 🎯 Objective

Build loading indicators (spinner, skeleton screens) for async operations to improve perceived performance and user experience.

## 📋 Description

Users should see visual feedback while charts calculate, data loads, or API calls process. Create reusable loading components with different sizes and skeleton variants for various content types.

## 🔗 References

- **Design Artifact**: `COMPONENT_STRUCTURE.md` (Shared Components)
- **Guide**: `AI_COPILOT_GUIDE.md` - Loading States

## ✅ Acceptance Criteria

- [ ] Spinner component with small, medium, large sizes
- [ ] Spinner color customizable
- [ ] Skeleton component for text (lines)
- [ ] Skeleton component for cards
- [ ] Skeleton component for tables
- [ ] Shimmer animation for skeleton
- [ ] `aria-live` announcements for loading states
- [ ] No layout shift when content replaces skeleton

## 💻 Implementation Notes

### Spinner Component

```jsx
// /frontend/src/components/shared/Spinner.jsx
import React from 'react';
import './Spinner.css';

const Spinner = ({ 
  size = 'medium', 
  color = 'primary',
  label = 'Loading...',
  className = '' 
}) => {
  return (
    <div 
      className={`spinner spinner--${size} spinner--${color} ${className}`}
      role="status"
      aria-label={label}
    >
      <svg className="spinner__svg" viewBox="0 0 50 50">
        <circle
          className="spinner__circle"
          cx="25"
          cy="25"
          r="20"
          fill="none"
          strokeWidth="4"
        />
      </svg>
      <span className="visually-hidden">{label}</span>
    </div>
  );
};

export default Spinner;
```

### Skeleton Component

```jsx
// /frontend/src/components/shared/Skeleton.jsx
import React from 'react';
import './Skeleton.css';

const Skeleton = ({ 
  variant = 'text', 
  width,
  height,
  count = 1,
  className = '' 
}) => {
  const skeletons = Array.from({ length: count }, (_, i) => (
    <div
      key={i}
      className={`skeleton skeleton--${variant} ${className}`}
      style={{ width, height }}
      aria-hidden="true"
    />
  ));
  
  return (
    <div className="skeleton-container" aria-busy="true" aria-live="polite">
      {skeletons}
    </div>
  );
};

// Preset skeleton patterns
export const SkeletonCard = () => (
  <div className="skeleton-card" aria-busy="true">
    <Skeleton variant="rect" height={200} />
    <div style={{ padding: 'var(--space-4)' }}>
      <Skeleton variant="text" width="60%" height={24} />
      <Skeleton variant="text" width="100%" count={3} />
    </div>
  </div>
);

export const SkeletonTable = ({ rows = 5 }) => (
  <div className="skeleton-table" aria-busy="true">
    {Array.from({ length: rows }, (_, i) => (
      <div key={i} className="skeleton-table__row">
        <Skeleton variant="text" width="30%" />
        <Skeleton variant="text" width="50%" />
        <Skeleton variant="text" width="20%" />
      </div>
    ))}
  </div>
);

export default Skeleton;
```

### Spinner Styles

```css
/* /frontend/src/components/shared/Spinner.css */
.spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Sizes */
.spinner--small {
  width: 20px;
  height: 20px;
}

.spinner--medium {
  width: 40px;
  height: 40px;
}

.spinner--large {
  width: 60px;
  height: 60px;
}

/* Colors */
.spinner--primary .spinner__circle {
  stroke: var(--color-primary);
}

.spinner--secondary .spinner__circle {
  stroke: var(--color-secondary);
}

.spinner--light .spinner__circle {
  stroke: var(--color-neutral-light);
}

/* Spinner animation */
.spinner__circle {
  stroke-dasharray: 90, 150;
  stroke-dashoffset: 0;
  stroke-linecap: round;
  animation: spinner-dash 1.5s ease-in-out infinite;
}

@keyframes spinner-dash {
  0% {
    stroke-dasharray: 1, 150;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -35;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -124;
  }
}

/* Visually hidden (for screen readers) */
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

### Skeleton Styles

```css
/* /frontend/src/components/shared/Skeleton.css */
.skeleton {
  background: linear-gradient(
    90deg,
    var(--bg-secondary) 0%,
    var(--bg-hover) 40%,
    var(--bg-secondary) 80%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: 4px;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* Variants */
.skeleton--text {
  height: 16px;
  margin-bottom: var(--space-2);
}

.skeleton--rect {
  width: 100%;
  height: 100px;
}

.skeleton--circle {
  border-radius: 50%;
}

/* Skeleton Card */
.skeleton-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--border-color);
}

/* Skeleton Table */
.skeleton-table__row {
  display: flex;
  gap: var(--space-4);
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--border-color);
}
```

## 🧪 Testing Checklist

- [ ] Spinner renders in all sizes (small, medium, large)
- [ ] Spinner colors customizable
- [ ] Spinner animates smoothly
- [ ] Skeleton shimmer animation works
- [ ] Skeleton text lines render correctly
- [ ] SkeletonCard matches actual card layout
- [ ] SkeletonTable matches actual table layout
- [ ] No layout shift when real content loads
- [ ] Screen reader announces loading state
- [ ] Spinner hidden from screen reader (decorative)
- [ ] Loading message announced via `aria-live`

## 🔍 Accessibility Requirements

- [ ] Spinner has `role="status"` and `aria-label`
- [ ] Skeleton has `aria-busy="true"`
- [ ] Loading text available to screen readers
- [ ] Loading state announced via `aria-live="polite"`
- [ ] Spinner not focusable (decorative)

## 📦 Files to Create/Modify

- `frontend/src/components/shared/Spinner.jsx` (create)
- `frontend/src/components/shared/Spinner.css` (create)
- `frontend/src/components/shared/Skeleton.jsx` (create)
- `frontend/src/components/shared/Skeleton.css` (create)
- `frontend/src/components/shared/Loading.test.jsx` (create)

## 🔗 Dependencies

- Issue #1 (CSS Variables)

## 📝 Additional Notes

- Use skeleton for content that takes >500ms to load
- Use spinner for quick actions (<500ms)
- Consider adding progress bar component (future)
- Test with slow 3G network throttling
- Ensure skeleton matches content structure exactly

---

**Priority**: P1 (High)  
**Estimated Effort**: 4 hours  
**Assignee**: TBD  
**Epic**: Epic 1 - Design System Foundation
