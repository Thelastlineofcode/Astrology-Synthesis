---
title: "Build Card Component System"
labels: ["component:design-system", "P0-Critical", "ui-component"]
assignees: []
milestone: "Milestone 1: Foundation"
---

## 🎯 Objective

Create a flexible Card component for grouping related content with variants (default, elevated, outlined) and proper spacing.

## 📋 Description

Cards are used throughout the app to group information (dashboard widgets, chart sections, BMAD analysis blocks). Build a reusable component with consistent styling.

## 🔗 References

- **Design Artifact**: `COMPONENT_STRUCTURE.md` (Shared Components)
- **Design Artifact**: `COLOR_SCHEMES.md` (Surface colors)
- **Guide**: `QUICK_REFERENCE.md` - Spacing system

## ✅ Acceptance Criteria

- [ ] Three variants: `default`, `elevated`, `outlined`
- [ ] Padding options: `none`, `small`, `medium`, `large`
- [ ] Optional header/footer sections
- [ ] Hover state for interactive cards
- [ ] Click handler support
- [ ] Responsive padding at mobile/desktop breakpoints
- [ ] Works with any child content
- [ ] Shadow elevation consistent with design system

## 💻 Implementation Notes

### Card Component

```jsx
// /frontend/src/components/shared/Card.jsx
import React from 'react';
import './Card.css';

const Card = ({
  children,
  variant = 'default',
  padding = 'medium',
  hoverable = false,
  onClick,
  className = '',
  header,
  footer,
  ...props
}) => {
  const classNames = [
    'card',
    `card--${variant}`,
    `card--padding-${padding}`,
    hoverable && 'card--hoverable',
    onClick && 'card--clickable',
    className
  ].filter(Boolean).join(' ');
  
  const handleClick = () => {
    if (onClick) onClick();
  };
  
  const handleKeyDown = (e) => {
    if (onClick && (e.key === 'Enter' || e.key === ' ')) {
      e.preventDefault();
      onClick();
    }
  };
  
  return (
    <div
      className={classNames}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      tabIndex={onClick ? 0 : undefined}
      role={onClick ? 'button' : undefined}
      {...props}
    >
      {header && <div className="card__header">{header}</div>}
      <div className="card__content">{children}</div>
      {footer && <div className="card__footer">{footer}</div>}
    </div>
  );
};

export default Card;
```

### Card Styles

```css
/* /frontend/src/components/shared/Card.css */
.card {
  background: var(--bg-secondary);
  border-radius: 12px;
  transition: all 200ms ease;
}

/* Variants */
.card--default {
  border: 1px solid var(--border-color);
}

.card--elevated {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: none;
}

.card--outlined {
  border: 2px solid var(--color-primary);
  background: transparent;
}

/* Padding */
.card--padding-none .card__content {
  padding: 0;
}

.card--padding-small .card__content {
  padding: var(--space-3);
}

.card--padding-medium .card__content {
  padding: var(--space-5);
}

.card--padding-large .card__content {
  padding: var(--space-7);
}

/* Header/Footer */
.card__header,
.card__footer {
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--border-color);
}

.card__footer {
  border-top: 1px solid var(--border-color);
  border-bottom: none;
}

/* Interactive states */
.card--hoverable:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.card--clickable {
  cursor: pointer;
}

.card--clickable:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Responsive */
@media (max-width: 767px) {
  .card--padding-large .card__content {
    padding: var(--space-5);
  }
}
```

## 🧪 Testing Checklist

- [ ] All three variants render correctly
- [ ] Padding options apply correct spacing
- [ ] Header/footer sections display when provided
- [ ] Hoverable cards animate on hover
- [ ] Clickable cards trigger onClick
- [ ] Keyboard accessible (Enter/Space for clickable cards)
- [ ] Focus ring visible on keyboard focus
- [ ] Responsive padding adjusts on mobile
- [ ] No layout breaks with long content
- [ ] Shadow elevations distinct between variants

## 🔍 Accessibility Requirements

- [ ] Clickable cards have `role="button"`
- [ ] Clickable cards keyboard accessible (tab, enter, space)
- [ ] Focus indicator clearly visible
- [ ] Content within card accessible to screen readers
- [ ] No nested interactive elements (avoid card button with button inside)

## 📦 Files to Create/Modify

- `frontend/src/components/shared/Card.jsx` (create)
- `frontend/src/components/shared/Card.css` (create)
- `frontend/src/components/shared/Card.test.jsx` (create)

## 🔗 Dependencies

- Issue #1 (CSS Variables)

## 📝 Additional Notes

- Cards used extensively in Dashboard, Chart Sections, BMAD Analysis
- Consider adding `loading` prop with skeleton state (future)
- Test with nested content (tables, forms, images)
- Ensure sufficient contrast in outlined variant

---

**Priority**: P0 (Critical)  
**Estimated Effort**: 3 hours  
**Assignee**: TBD  
**Epic**: Epic 1 - Design System Foundation
