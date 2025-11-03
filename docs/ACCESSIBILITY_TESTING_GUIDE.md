# Accessibility Testing Guide

## Overview

This guide provides comprehensive instructions for testing the accessibility of the Mula: The Root astrology application. All features must meet WCAG 2.1 Level AA standards.

## Quick Reference

### WCAG 2.1 Level AA Requirements

| Category | Requirement | Standard |
|----------|------------|----------|
| **Color Contrast** | Text < 18pt or < 14pt bold | 4.5:1 minimum |
| **Color Contrast** | Text ≥ 18pt or ≥ 14pt bold | 3:1 minimum |
| **Color Contrast** | UI components & graphics | 3:1 minimum |
| **Touch Targets** | Interactive elements (mobile) | 44px × 44px minimum |
| **Focus Indicators** | Visible focus on all interactive elements | 2px minimum, 3:1 contrast |

---

## Color Contrast Testing

### Automated Testing Tools

#### 1. Chrome DevTools Lighthouse
```bash
# Run Lighthouse audit
1. Open Chrome DevTools (F12)
2. Navigate to "Lighthouse" tab
3. Select "Accessibility" category
4. Click "Analyze page load"
5. Review contrast issues in report
```

#### 2. axe DevTools Extension
- Install: [Chrome](https://chrome.google.com/webstore/detail/axe-devtools) | [Firefox](https://addons.mozilla.org/en-US/firefox/addon/axe-devtools/)
- Run automated scan on every page
- Fix all "Critical" and "Serious" issues

#### 3. WAVE Browser Extension
- Install: [WAVE Extension](https://wave.webaim.org/extension/)
- Provides visual feedback on page
- Highlights contrast errors inline

### Manual Contrast Verification

Use the WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/

#### Light Mode Tests

| Element | Foreground | Background | Required | Actual | Pass? |
|---------|-----------|------------|----------|--------|-------|
| Body Text | #2D3142 | #F5F3EE | 4.5:1 | 9.23:1 | ✓ |
| Primary Button Text | #F5F3EE | #3E4B6E | 4.5:1 | 6.89:1 | ✓ |
| Secondary Text | #3E4B6E | #F5F3EE | 4.5:1 | 6.89:1 | ✓ |
| CTA Button Text | #FFFFFF | #C17B5C | 4.5:1 | 4.21:1 | ⚠️ (Use larger text) |
| Border (UI Component) | #A5B8A4 | #FFFFFF | 3:1 | 2.34:1 | ✗ (Decorative only) |

#### Dark Mode Tests

| Element | Foreground | Background | Required | Actual | Pass? |
|---------|-----------|------------|----------|--------|-------|
| Body Text | #F5F3EE | #2D3142 | 4.5:1 | 9.23:1 | ✓ |
| Card Text | #F5F3EE | #3A4257 | 4.5:1 | 7.12:1 | ✓ |
| Secondary Text | #A5B8A4 | #2D3142 | 4.5:1 | 3.94:1 | ⚠️ (Large text only) |

---

## Keyboard Navigation Testing

### Test Scenarios

#### 1. Tab Order
- [ ] Press `Tab` to navigate forward through all interactive elements
- [ ] Press `Shift+Tab` to navigate backward
- [ ] Tab order is logical (follows visual order)
- [ ] No keyboard traps (can escape all UI components)
- [ ] Hidden elements are not focusable

#### 2. Focus Indicators
- [ ] Focus outline visible on ALL interactive elements
- [ ] Focus outline has minimum 2px width
- [ ] Focus outline has 3:1 contrast against background
- [ ] Focus outline doesn't clip or get hidden by overflow

#### 3. Keyboard Shortcuts

| Action | Key | Expected Behavior |
|--------|-----|-------------------|
| Navigate forward | `Tab` | Move to next interactive element |
| Navigate backward | `Shift+Tab` | Move to previous element |
| Activate button | `Enter` or `Space` | Trigger button action |
| Close modal | `Esc` | Close modal, return focus |
| Navigate dropdown | `Arrow keys` | Move through options |
| Select dropdown option | `Enter` | Select and close dropdown |

#### 4. Modal/Dialog Testing
- [ ] Modal traps focus (can't tab outside modal)
- [ ] `Esc` key closes modal
- [ ] Focus returns to trigger element on close
- [ ] First focusable element receives focus on open
- [ ] Background content is inert (can't interact)

#### 5. Form Navigation
- [ ] Can navigate between form fields with `Tab`
- [ ] Error messages are announced when shown
- [ ] Required fields are indicated (not by color alone)
- [ ] Can submit form with `Enter` key

---

## Screen Reader Testing

### Recommended Screen Readers

| Platform | Screen Reader | Download |
|----------|--------------|----------|
| Windows | NVDA (free) | https://www.nvaccess.org/ |
| Windows | JAWS (paid) | https://www.freedomscientific.com/products/software/jaws/ |
| macOS | VoiceOver (built-in) | Cmd+F5 to enable |
| iOS | VoiceOver (built-in) | Settings → Accessibility |
| Android | TalkBack (built-in) | Settings → Accessibility |

### Testing Checklist

#### General
- [ ] All images have descriptive `alt` text
- [ ] Decorative images have `alt=""` or `role="presentation"`
- [ ] Page has descriptive `<title>` element
- [ ] Main content landmark exists (`<main>` or `role="main"`)
- [ ] Navigation landmark exists (`<nav>` or `role="navigation"`)

#### Semantic HTML
- [ ] Headings use proper hierarchy (h1 → h2 → h3)
- [ ] Lists use `<ul>`, `<ol>`, `<li>` elements
- [ ] Forms use `<label>` elements associated with inputs
- [ ] Buttons use `<button>` (not `<div>` with click handlers)
- [ ] Links use `<a>` with `href` attribute

#### ARIA Labels
- [ ] Icon buttons have `aria-label`
- [ ] Form inputs without visible labels have `aria-label`
- [ ] Error messages use `aria-describedby` or `role="alert"`
- [ ] Loading indicators use `aria-live="polite"`
- [ ] Tabs have proper `role="tablist"`, `role="tab"`, `role="tabpanel"`

#### Dynamic Content
- [ ] Loading states announced with `aria-live="polite"`
- [ ] Error messages announced with `role="alert"`
- [ ] Success messages announced to screen reader
- [ ] Content changes are announced appropriately

---

## Mobile Accessibility Testing

### Touch Target Size

All interactive elements must be at least 44px × 44px.

```css
/* Ensure minimum touch target size */
button, a, input, select, textarea {
  min-height: 44px;
  min-width: 44px;
  /* Or use padding to achieve size */
}
```

#### Test Cases
- [ ] All buttons are 44px × 44px or larger
- [ ] Links have sufficient padding
- [ ] Form inputs are easily tappable
- [ ] Spacing between adjacent tap targets is adequate (8px minimum)

### Mobile Screen Reader Testing

#### iOS VoiceOver
1. Enable: Settings → Accessibility → VoiceOver
2. Navigate with swipe gestures
3. Double-tap to activate elements
4. Test all interactive elements

#### Android TalkBack
1. Enable: Settings → Accessibility → TalkBack
2. Navigate with swipe gestures
3. Double-tap to activate elements
4. Test all interactive elements

---

## Reduced Motion Support

Users with vestibular disorders may need reduced motion.

### Implementation

```css
/* Respect user's motion preferences */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Test Cases
- [ ] Set OS to "Reduce motion" preference
- [ ] Animations are disabled or significantly reduced
- [ ] Parallax effects are disabled
- [ ] Auto-playing videos are paused
- [ ] Transitions still provide visual feedback (without motion)

---

## Zoom and Text Scaling

### Browser Zoom Testing

Test at these zoom levels:
- [ ] 100% (baseline)
- [ ] 125%
- [ ] 150%
- [ ] 200%
- [ ] 400% (extreme case)

#### Test Criteria
- [ ] Content remains readable and accessible
- [ ] No horizontal scrolling (except data tables)
- [ ] No content is cut off or hidden
- [ ] Interactive elements remain clickable
- [ ] Layout doesn't break

### Text Scaling (Browser Settings)

Some users increase text size without zooming the entire page.

- [ ] Set browser to "Very Large" text size
- [ ] Content remains readable
- [ ] Text doesn't overlap
- [ ] Containers expand to accommodate larger text

---

## Color Blindness Testing

### Types of Color Blindness

1. **Protanopia** (Red-blind) - 1% of males
2. **Deuteranopia** (Green-blind) - 1% of males
3. **Tritanopia** (Blue-blind) - Rare
4. **Achromatopsia** (Complete color blindness) - Very rare

### Testing Tools

#### Browser Extensions
- **Colorblinding** (Chrome): Simulates different types of color blindness
- **NoCoffee Vision Simulator** (Chrome/Firefox): Multiple vision simulations

#### Manual Testing
- [ ] Information is not conveyed by color alone
- [ ] Status indicators use icons + text + color
- [ ] Links are distinguishable without color (underline, bold, etc.)
- [ ] Charts and graphs use patterns or labels, not just color
- [ ] Form validation errors use icons + text, not just red borders

---

## Testing Workflow

### For Every New Component

1. **Build the Component**
   ```bash
   npm run dev
   ```

2. **Automated Testing**
   - Run Lighthouse accessibility audit
   - Run axe DevTools scan
   - Fix all issues before manual testing

3. **Manual Keyboard Testing**
   - Test complete keyboard navigation
   - Verify focus indicators
   - Test with screen reader (NVDA/VoiceOver)

4. **Visual Contrast Testing**
   - Verify all text contrast ratios
   - Test in both light and dark modes
   - Use browser DevTools color picker

5. **Mobile Testing**
   - Test on actual mobile device
   - Verify touch target sizes
   - Test with mobile screen reader

6. **Document Results**
   - Add test results to component documentation
   - Create GitHub issue for any accessibility bugs
   - Update this guide if new patterns emerge

### Pre-Release Checklist

Before merging to main:

- [ ] All Lighthouse accessibility scores 95+
- [ ] Zero critical/serious axe violations
- [ ] All pages keyboard navigable
- [ ] All interactive elements have focus indicators
- [ ] All images have alt text
- [ ] All forms have associated labels
- [ ] Color contrast meets WCAG AA
- [ ] Touch targets meet 44px minimum (mobile)
- [ ] Tested with screen reader
- [ ] Tested with keyboard only
- [ ] Tested at 200% zoom
- [ ] Reduced motion preference respected

---

## Common Issues and Fixes

### Issue 1: Missing Focus Indicator

**Problem**: Focus indicator not visible or missing

**Fix**:
```css
:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* Never do this: */
*:focus {
  outline: none; /* ❌ BAD */
}
```

### Issue 2: Low Contrast Text

**Problem**: Text doesn't meet 4.5:1 contrast ratio

**Fix**:
```css
/* ❌ Bad - Low contrast */
.text-secondary {
  color: #A5B8A4; /* 2.34:1 on white */
}

/* ✅ Good - Sufficient contrast */
.text-secondary {
  color: rgba(62, 75, 110, 0.7); /* 5.2:1 on white */
}
```

### Issue 3: Div Click Handlers

**Problem**: Using `<div onClick={...}>` instead of button

**Fix**:
```jsx
/* ❌ Bad - Not keyboard accessible */
<div onClick={handleClick}>Click me</div>

/* ✅ Good - Keyboard accessible */
<button onClick={handleClick}>Click me</button>
```

### Issue 4: Missing Alt Text

**Problem**: Images without alt attributes

**Fix**:
```jsx
/* ❌ Bad */
<img src="chart.png" />

/* ✅ Good - Descriptive */
<img src="chart.png" alt="Natal chart showing planetary positions" />

/* ✅ Good - Decorative */
<img src="decorative.png" alt="" role="presentation" />
```

### Issue 5: Color-Only Indicators

**Problem**: Status conveyed by color alone

**Fix**:
```jsx
/* ❌ Bad - Color only */
<span style={{ color: 'green' }}>Success</span>

/* ✅ Good - Icon + text + color */
<span className="status-success">
  <CheckIcon aria-hidden="true" />
  <span>Success</span>
</span>
```

---

## Resources

### Testing Tools

- **Lighthouse**: Built into Chrome DevTools
- **axe DevTools**: https://www.deque.com/axe/devtools/
- **WAVE**: https://wave.webaim.org/extension/
- **Color Contrast Analyzer**: https://www.tpgi.com/color-contrast-checker/
- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/

### Screen Readers

- **NVDA** (Windows, free): https://www.nvaccess.org/
- **JAWS** (Windows, paid): https://www.freedomscientific.com/products/software/jaws/
- **VoiceOver** (macOS/iOS, built-in): Cmd+F5
- **TalkBack** (Android, built-in): Settings → Accessibility

### Learning Resources

- **WCAG 2.1 Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **A11y Project**: https://www.a11yproject.com/
- **MDN Accessibility**: https://developer.mozilla.org/en-US/docs/Web/Accessibility
- **WebAIM**: https://webaim.org/
- **Inclusive Components**: https://inclusive-components.design/

### Documentation

- [Color Palette and Design System](/docs/COLOR_PALETTE_AND_DESIGN_SYSTEM.md)
- [Project Overview](/docs/redesign/PROJECT_OVERVIEW.md)
- [Quick Reference](/docs/redesign/QUICK_REFERENCE.md)

---

**Document Version**: 1.0  
**Last Updated**: October 29, 2025  
**Maintained By**: QA & Product Management Team  
**Status**: Active

For questions or to report accessibility issues, please open a GitHub issue with the label `accessibility`.
