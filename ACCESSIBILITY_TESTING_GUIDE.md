# Accessibility Testing Guide

**Roots Revealed - WCAG 2.1 Compliance and Accessibility Testing**

## Table of Contents
1. [Overview](#overview)
2. [WCAG 2.1 Standards](#wcag-21-standards)
3. [Testing Checklist](#testing-checklist)
4. [Manual Testing](#manual-testing)
5. [Automated Testing](#automated-testing)
6. [Common Issues and Fixes](#common-issues-and-fixes)
7. [Testing Tools](#testing-tools)
8. [Accessibility Workflow](#accessibility-workflow)

---

## Overview

This guide provides comprehensive instructions for testing and ensuring accessibility compliance for the Roots Revealed application. We target **WCAG 2.1 Level AA** compliance as our baseline, with AAA standards where feasible.

### Why Accessibility Matters

- **Inclusive Design**: Everyone should be able to use astrology tools, regardless of ability
- **Legal Compliance**: Many jurisdictions require digital accessibility
- **Better UX**: Accessible design improves usability for all users
- **SEO Benefits**: Accessible sites rank better in search engines
- **Market Reach**: 15%+ of the global population has some form of disability

### Our Accessibility Commitment

✅ **WCAG 2.1 Level AA Compliance**  
✅ **Keyboard Navigation Support**  
✅ **Screen Reader Compatibility**  
✅ **Color Contrast Standards**  
✅ **Responsive and Mobile Accessible**  
✅ **Reduced Motion Support**

---

## WCAG 2.1 Standards

### Four Principles (POUR)

#### 1. Perceivable
Information and UI components must be presentable to users in ways they can perceive.

- **Text Alternatives**: Provide alt text for images
- **Time-based Media**: Captions and transcripts
- **Adaptable**: Content can be presented in different ways
- **Distinguishable**: Make it easy to see and hear content

#### 2. Operable
User interface components and navigation must be operable.

- **Keyboard Accessible**: All functionality available from keyboard
- **Enough Time**: Users have adequate time to read and use content
- **Seizures**: Don't design content that causes seizures
- **Navigable**: Help users navigate and find content

#### 3. Understandable
Information and the operation of the user interface must be understandable.

- **Readable**: Make text content readable and understandable
- **Predictable**: Make pages appear and operate in predictable ways
- **Input Assistance**: Help users avoid and correct mistakes

#### 4. Robust
Content must be robust enough to be interpreted by a wide variety of user agents, including assistive technologies.

- **Compatible**: Maximize compatibility with current and future tools

### Conformance Levels

- **Level A**: Basic accessibility (minimum requirement)
- **Level AA**: Addresses major barriers (our target)
- **Level AAA**: Highest level (apply where possible)

---

## Testing Checklist

### ✅ Color and Contrast

- [ ] Text contrast ratio ≥ 4.5:1 (body text, WCAG AA)
- [ ] Large text contrast ratio ≥ 3:1 (18pt+ or 14pt+ bold, WCAG AA)
- [ ] UI component contrast ratio ≥ 3:1 (buttons, borders, icons)
- [ ] Color is not the only means of conveying information
- [ ] Link text is distinguishable from surrounding text
- [ ] Focus indicators have sufficient contrast (≥ 3:1)

**Testing Tools**: Chrome DevTools, WebAIM Contrast Checker, Colour Contrast Analyser

### ✅ Keyboard Navigation

- [ ] All interactive elements are keyboard accessible (Tab navigation)
- [ ] Focus order is logical and intuitive
- [ ] Focus indicators are clearly visible
- [ ] No keyboard traps (users can navigate away from elements)
- [ ] Skip links available to bypass repetitive content
- [ ] Keyboard shortcuts don't conflict with assistive technologies
- [ ] Enter/Space activate buttons and links
- [ ] Escape closes modals and dropdowns
- [ ] Arrow keys navigate within components (menus, tabs, etc.)

**Testing Method**: Unplug mouse, navigate site using Tab, Shift+Tab, Enter, Space, Arrow keys, Escape

### ✅ Screen Reader Support

- [ ] All images have appropriate alt text
- [ ] Decorative images have empty alt attributes (alt="")
- [ ] Form inputs have associated labels
- [ ] Buttons have descriptive text or aria-labels
- [ ] Landmark regions are properly defined (header, nav, main, footer)
- [ ] Heading hierarchy is logical (h1 → h2 → h3, no skips)
- [ ] Links have descriptive text (not "click here")
- [ ] ARIA attributes used correctly and sparingly
- [ ] Live regions announce dynamic content (aria-live)
- [ ] Error messages are announced (role="alert")
- [ ] Loading states are communicated (aria-busy, aria-live)

**Testing Tools**: NVDA (Windows), JAWS (Windows), VoiceOver (macOS/iOS), TalkBack (Android)

### ✅ Forms and Input

- [ ] All form fields have visible labels
- [ ] Labels are programmatically associated (for/id or aria-labelledby)
- [ ] Required fields are indicated (both visually and programmatically)
- [ ] Error messages are clear and specific
- [ ] Errors are announced to screen readers (aria-describedby, role="alert")
- [ ] Input fields have appropriate type and autocomplete attributes
- [ ] Field constraints are clearly communicated
- [ ] Success messages are announced

### ✅ Responsive and Mobile

- [ ] Touch targets are at least 44×44px
- [ ] Content is readable without horizontal scrolling
- [ ] Text can be zoomed to 200% without loss of functionality
- [ ] Content reflows at different viewport sizes
- [ ] Pinch-to-zoom is not disabled
- [ ] Orientation (portrait/landscape) doesn't break functionality

### ✅ Multimedia and Animation

- [ ] Videos have captions and transcripts
- [ ] Audio content has transcripts
- [ ] Auto-playing media can be paused
- [ ] Animations respect prefers-reduced-motion
- [ ] No flashing content (≥3 flashes per second)

### ✅ Semantic HTML

- [ ] Proper use of semantic elements (nav, main, article, section)
- [ ] Buttons use `<button>` elements (not divs with click handlers)
- [ ] Links use `<a>` elements with href attributes
- [ ] Lists use `<ul>`, `<ol>`, `<li>` elements
- [ ] Tables use proper structure (thead, tbody, th, td)
- [ ] Form controls use native elements (input, select, textarea)

---

## Manual Testing

### Keyboard-Only Navigation Test

**Duration**: 15-30 minutes per page

1. **Disconnect or hide your mouse**
2. **Start at the top of the page**
3. **Press Tab repeatedly**
   - Note: Does focus move in logical order?
   - Note: Is focus clearly visible?
4. **Try Shift+Tab** to move backwards
5. **Test interactive elements**:
   - Press Enter on links and buttons
   - Use Space to activate buttons
   - Use Arrow keys in dropdowns and menus
   - Use Escape to close modals
6. **Check for keyboard traps**
   - Can you Tab away from every element?
7. **Document any issues**

### Screen Reader Testing

**Tools**: NVDA (free), JAWS (paid), VoiceOver (built-in on Mac)

#### NVDA Quick Start (Windows)

1. Download and install NVDA from nvaccess.org
2. Start NVDA (Insert key becomes NVDA modifier)
3. Navigate with:
   - **Tab/Shift+Tab**: Move between interactive elements
   - **Arrow Keys**: Read line by line
   - **NVDA+Down Arrow**: Read all from cursor
   - **H**: Jump to next heading
   - **D**: Jump to next landmark
4. Listen for:
   - Are all elements announced correctly?
   - Is the content understandable?
   - Are instructions clear?

#### VoiceOver Quick Start (macOS)

1. Enable VoiceOver: Cmd+F5 or System Preferences → Accessibility
2. Navigate with:
   - **Control+Option+Arrow Keys**: Move through elements
   - **Control+Option+Space**: Activate elements
   - **Control+Option+H**: Next heading
   - **Control+Option+U**: Open rotor (navigation menu)
3. Listen for proper announcements

### Color Contrast Testing

**Tool**: WebAIM Contrast Checker (webaim.org/resources/contrastchecker/)

1. **Identify text elements** in your design
2. **Get foreground color** (text color)
3. **Get background color**
4. **Enter values into contrast checker**
5. **Verify**:
   - Body text: ≥ 4.5:1 (AA) or ≥ 7:1 (AAA)
   - Large text (18pt+): ≥ 3:1 (AA) or ≥ 4.5:1 (AAA)
   - UI components: ≥ 3:1
6. **Document and fix failures**

### Mobile/Touch Testing

1. **Test on real devices** (iPhone, Android)
2. **Check touch target sizes** (≥44×44px)
3. **Test landscape and portrait orientations**
4. **Zoom to 200%** and verify usability
5. **Test with VoiceOver/TalkBack** enabled

---

## Automated Testing

### Browser DevTools

#### Chrome DevTools Lighthouse

1. Open DevTools (F12)
2. Go to Lighthouse tab
3. Select "Accessibility" category
4. Click "Generate report"
5. Review issues and scores
6. Aim for 90+ score

#### Chrome DevTools Accessibility Pane

1. Open DevTools
2. Go to Elements tab
3. Select Accessibility pane
4. Review Accessibility Tree
5. Check ARIA attributes
6. Verify computed properties

### axe DevTools Extension

**Installation**: Chrome Web Store → "axe DevTools"

1. Install extension
2. Open DevTools → axe DevTools tab
3. Click "Scan ALL of my page"
4. Review issues by severity:
   - **Critical**: Fix immediately
   - **Serious**: Fix before release
   - **Moderate**: Fix soon
   - **Minor**: Fix when possible
5. Click on issues for detailed guidance

### Automated Testing in CI/CD

#### Jest + jest-axe

```javascript
// Example test
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import MyComponent from './MyComponent';

expect.extend(toHaveNoViolations);

test('should not have accessibility violations', async () => {
  const { container } = render(<MyComponent />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

#### Pa11y (Command Line Tool)

```bash
# Install globally
npm install -g pa11y

# Test a page
pa11y http://localhost:3000

# Test with standard
pa11y --standard WCAG2AA http://localhost:3000

# Generate report
pa11y --reporter html http://localhost:3000 > report.html
```

---

## Common Issues and Fixes

### Issue: Missing Alt Text

**Problem**: Images without alt attributes
```html
<!-- ❌ Bad -->
<img src="chart.png">
```

**Fix**: Add descriptive alt text
```html
<!-- ✅ Good -->
<img src="chart.png" alt="Natal chart showing planetary positions">

<!-- ✅ Good - Decorative image -->
<img src="decoration.png" alt="">
```

### Issue: Low Color Contrast

**Problem**: Text color doesn't have sufficient contrast
```css
/* ❌ Bad - Contrast ratio 2.5:1 */
color: #999999;
background: #FFFFFF;
```

**Fix**: Use darker color for sufficient contrast
```css
/* ✅ Good - Contrast ratio 4.8:1 */
color: #666666;
background: #FFFFFF;
```

### Issue: Missing Form Labels

**Problem**: Input fields without labels
```html
<!-- ❌ Bad -->
<input type="text" placeholder="Enter name">
```

**Fix**: Add proper label
```html
<!-- ✅ Good -->
<label for="userName">Name:</label>
<input type="text" id="userName" placeholder="Enter name">
```

### Issue: Keyboard Trap

**Problem**: Users can't Tab out of modal
```javascript
// ❌ Bad - No escape handler
<Modal>Content</Modal>
```

**Fix**: Add keyboard handlers
```javascript
// ✅ Good
<Modal onEscape={closeModal}>
  Content
  <button onClick={closeModal}>Close</button>
</Modal>
```

### Issue: Non-Semantic Buttons

**Problem**: Using div as button
```html
<!-- ❌ Bad -->
<div onclick="submit()">Submit</div>
```

**Fix**: Use proper button element
```html
<!-- ✅ Good -->
<button type="submit" onClick={submit}>Submit</button>
```

### Issue: Missing Focus Indicators

**Problem**: No visible focus state
```css
/* ❌ Bad */
button:focus {
  outline: none;
}
```

**Fix**: Maintain or enhance focus indicators
```css
/* ✅ Good */
button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

---

## Testing Tools

### Browser Extensions

| Tool | Platform | Purpose |
|------|----------|---------|
| **axe DevTools** | Chrome, Firefox | Automated accessibility testing |
| **WAVE** | Chrome, Firefox | Visual feedback on accessibility |
| **Lighthouse** | Chrome (built-in) | Performance and accessibility audits |
| **Accessibility Insights** | Chrome, Edge | Guided accessibility testing |

### Screen Readers

| Tool | Platform | Cost |
|------|----------|------|
| **NVDA** | Windows | Free |
| **JAWS** | Windows | Paid |
| **VoiceOver** | macOS, iOS | Free (built-in) |
| **TalkBack** | Android | Free (built-in) |
| **Narrator** | Windows | Free (built-in) |

### Color Contrast Checkers

- **WebAIM Contrast Checker**: webaim.org/resources/contrastchecker/
- **Colour Contrast Analyser**: tpgi.com/color-contrast-checker/
- **Contrast Ratio**: contrast-ratio.com

### Command Line Tools

```bash
# Pa11y - Accessibility testing
npm install -g pa11y
pa11y --standard WCAG2AA http://localhost:3000

# Lighthouse CLI
npm install -g lighthouse
lighthouse http://localhost:3000 --only-categories=accessibility

# axe-cli
npm install -g axe-cli
axe http://localhost:3000
```

---

## Accessibility Workflow

### During Development

1. **Use semantic HTML** from the start
2. **Test with keyboard** as you build
3. **Check color contrast** before finalizing designs
4. **Add ARIA only when needed** (HTML first)
5. **Test with screen reader** regularly

### Before Pull Request

1. **Run automated tests** (jest-axe, Lighthouse)
2. **Manual keyboard test** (5 min per component)
3. **Check color contrast** for new colors
4. **Review ARIA attributes** for correctness
5. **Test focus indicators** are visible

### During Code Review

- [ ] Semantic HTML used correctly
- [ ] ARIA attributes are necessary and correct
- [ ] Keyboard navigation works
- [ ] Color contrast meets standards
- [ ] Focus indicators are visible
- [ ] Alt text is descriptive

### Before Release

1. **Full accessibility audit** with axe DevTools
2. **Screen reader testing** (NVDA or VoiceOver)
3. **Keyboard-only navigation** of all pages
4. **Mobile accessibility testing**
5. **Lighthouse accessibility score** ≥ 90
6. **User testing** with people who use assistive tech

### Post-Release

- Monitor accessibility issues in bug reports
- Conduct periodic accessibility audits (quarterly)
- Stay updated on WCAG guidelines
- Collect feedback from users with disabilities

---

## Quick Reference

### WCAG 2.1 AA Requirements

| Requirement | Minimum Standard |
|-------------|------------------|
| Text Contrast | 4.5:1 (body), 3:1 (large text) |
| UI Component Contrast | 3:1 |
| Keyboard Access | All functionality accessible |
| Focus Indicator | Visible and distinct |
| Touch Target Size | 44×44px (mobile) |
| Heading Hierarchy | Logical (no skips) |
| Form Labels | All inputs labeled |
| Alt Text | All images (or alt="") |
| ARIA | Used correctly, sparingly |
| Color Information | Not sole indicator |

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Tab** | Move to next focusable element |
| **Shift+Tab** | Move to previous focusable element |
| **Enter** | Activate link or button |
| **Space** | Activate button, check checkbox |
| **Arrow Keys** | Navigate within components |
| **Escape** | Close modal or dropdown |
| **Home/End** | Move to start/end of list |

### ARIA Quick Guide

```html
<!-- Button with icon (no visible text) -->
<button aria-label="Close modal">
  <span aria-hidden="true">×</span>
</button>

<!-- Error message -->
<div role="alert">Please enter a valid email</div>

<!-- Loading state -->
<div aria-live="polite" aria-busy="true">Loading...</div>

<!-- Expandable section -->
<button aria-expanded="false" aria-controls="content">
  Show Details
</button>
<div id="content" hidden>Content here</div>

<!-- Required field -->
<input type="text" aria-required="true" required>
```

---

## Resources

### Official Documentation

- **WCAG 2.1 Guidelines**: w3.org/WAI/WCAG21/quickref/
- **ARIA Authoring Practices**: w3.org/WAI/ARIA/apg/
- **MDN Accessibility**: developer.mozilla.org/en-US/docs/Web/Accessibility

### Learning Resources

- **WebAIM**: webaim.org (tutorials, articles)
- **A11y Project**: a11yproject.com (checklist, patterns)
- **Deque University**: dequeuniversity.com (courses)

### Communities

- **WebAIM Discussion List**: webaim.org/discussion/
- **A11y Slack**: web-a11y.slack.com
- **Reddit r/accessibility**: reddit.com/r/accessibility

---

## Support and Questions

For questions about accessibility or to report accessibility issues:

1. Create a GitHub issue with the "accessibility" label
2. Include:
   - Description of the issue
   - Steps to reproduce
   - Expected vs. actual behavior
   - Assistive technology used (if applicable)

We are committed to making Roots Revealed accessible to everyone. Thank you for helping us improve!

---

*Last Updated: October 29, 2025*
*WCAG Version: 2.1 Level AA*
