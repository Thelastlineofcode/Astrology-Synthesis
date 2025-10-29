---
title: "Create Reusable Button Component"
labels: ["component:design-system", "P0-Critical", "ui-component"]
assignees: []
milestone: "Milestone 1: Foundation"
---

## 🎯 Objective

Build a flexible, accessible Button component with variants (primary, secondary, ghost), sizes, and states (loading, disabled).

## 📋 Description

Buttons are the most frequently used interactive element. Create a component that handles all use cases: CTAs, form submissions, icon buttons, and navigation links styled as buttons.

## 🔗 References

- **Design Artifact**: `COMPONENT_STRUCTURE.md` (Shared Components)
- **Design Artifact**: `COLOR_SCHEMES.md` (Button colors)
- **Guide**: `AI_COPILOT_GUIDE.md` - Accessibility Requirements

## ✅ Acceptance Criteria

- [ ] Three variants: `primary`, `secondary`, `ghost`
- [ ] Three sizes: `small`, `medium`, `large`
- [ ] Disabled state with reduced opacity
- [ ] Loading state with spinner animation
- [ ] Icon support (left/right/only)
- [ ] Full-width option
- [ ] Keyboard accessible (Enter/Space to activate)
- [ ] Hover, focus, active states clearly visible
- [ ] Works as `<button>` or `<a>` (link styled as button)
- [ ] Passes WCAG 2.1 AA contrast requirements

## 💻 Implementation Notes

### Button Component

```jsx
// /frontend/src/components/shared/Button.jsx
import React from 'react';
import './Button.css';

const Button = ({
  children,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  fullWidth = false,
  iconLeft,
  iconRight,
  onClick,
  type = 'button',
  href,
  className = '',
  ...props
}) => {
  const classNames = [
    'btn',
    `btn--${variant}`,
    `btn--${size}`,
    fullWidth && 'btn--full-width',
    loading && 'btn--loading',
    disabled && 'btn--disabled',
    className
  ].filter(Boolean).join(' ');
  
  const content = (
    <>
      {loading && <span className="btn__spinner" aria-hidden="true" />}
      {!loading && iconLeft && <span className="btn__icon btn__icon--left">{iconLeft}</span>}
      <span className="btn__text">{children}</span>
      {!loading && iconRight && <span className="btn__icon btn__icon--right">{iconRight}</span>}
    </>
  );
  
  if (href && !disabled) {
    return (
      <a
        href={href}
        className={classNames}
        aria-disabled={disabled}
        {...props}
      >
        {content}
      </a>
    );
  }
  
  return (
    <button
      type={type}
      className={classNames}
      onClick={onClick}
      disabled={disabled || loading}
      aria-busy={loading}
      {...props}
    >
      {content}
    </button>
  );
};

export default Button;
```

### Button Styles

```css
/* /frontend/src/components/shared/Button.css */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  font-family: var(--font-primary);
  font-weight: var(--font-weight-medium);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 150ms ease;
  text-decoration: none;
  position: relative;
}

.btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Sizes */
.btn--small {
  padding: var(--space-2) var(--space-3);
  font-size: var(--font-size-small);
}

.btn--medium {
  padding: var(--space-3) var(--space-5);
  font-size: var(--font-size-body);
}

.btn--large {
  padding: var(--space-4) var(--space-6);
  font-size: var(--font-size-h4);
}

/* Variants */
.btn--primary {
  background: var(--color-primary);
  color: var(--color-neutral-light);
}

.btn--primary:hover:not(:disabled) {
  background: var(--color-primary-dark);
  transform: translateY(-1px);
}

.btn--primary:active:not(:disabled) {
  transform: translateY(0);
}

.btn--secondary {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn--secondary:hover:not(:disabled) {
  background: var(--bg-hover);
  border-color: var(--color-primary);
}

.btn--ghost {
  background: transparent;
  color: var(--color-primary);
}

.btn--ghost:hover:not(:disabled) {
  background: var(--bg-hover);
}

/* States */
.btn--disabled,
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.btn--loading {
  pointer-events: none;
}

.btn--full-width {
  width: 100%;
}

/* Spinner */
.btn__spinner {
  width: 16px;
  height: 16px;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 600ms linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Icons */
.btn__icon {
  display: inline-flex;
  align-items: center;
}

.btn__icon svg {
  width: 20px;
  height: 20px;
}
```

## 🧪 Testing Checklist

- [ ] All three variants render correctly
- [ ] All three sizes display distinct sizing
- [ ] Disabled button not clickable
- [ ] Loading spinner appears when `loading={true}`
- [ ] Icons render on left/right correctly
- [ ] Full-width button spans container width
- [ ] Hover states visible
- [ ] Focus ring visible on keyboard focus (Tab key)
- [ ] Enter/Space triggers onClick
- [ ] Works as link (`<a>`) when href provided
- [ ] No console errors when rendering
- [ ] Contrast ratios pass WCAG AA for all variants

## 🔍 Accessibility Requirements

- [ ] Focus indicator clearly visible (2px outline, 2px offset)
- [ ] `aria-busy="true"` when loading
- [ ] `aria-disabled="true"` when disabled
- [ ] Button text descriptive (not just "Click here")
- [ ] Icon-only buttons have `aria-label`
- [ ] Works with keyboard only (no mouse needed)

## 📦 Files to Create/Modify

- `frontend/src/components/shared/Button.jsx` (create)
- `frontend/src/components/shared/Button.css` (create)
- `frontend/src/components/shared/Button.test.jsx` (create)

## 🔗 Dependencies

- Issue #1 (CSS Variables)
- Issue #2 (Typography System)

## 📝 Additional Notes

- Consider adding `ripple` effect on click (optional)
- Add `danger` variant for destructive actions (future)
- Test on touch devices for 44px minimum tap target
- Ensure spinner color contrasts with button background

---

**Priority**: P0 (Critical)  
**Estimated Effort**: 4 hours  
**Assignee**: TBD  
**Epic**: Epic 1 - Design System Foundation
