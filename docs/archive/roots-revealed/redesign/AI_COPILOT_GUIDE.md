# AI Copilot Contributor Guide - BMAD Astrology App

## 🤖 Welcome, AI Agent!

This guide is specifically written for AI coding agents (like GitHub Copilot, cursor, or other LLM-based assistants) working on the BMAD Astrology App redesign. Follow these guidelines to ensure consistency, quality, and maintainability.

---

## 📚 **CRITICAL: Read These First**

Before implementing ANY feature, you MUST review these design artifacts:

1. **[Component Structure](../../../attachments/bmad_component_structure.txt)** - Complete UI component hierarchy and organization
2. **[Color Schemes](../../../attachments/bmad_color_schemes.txt)** - "Healing Cosmos" palette with hex codes and usage guidelines
3. **[UX Copy Guide](../../../attachments/bmad_ux_copy_guide.txt)** - ALL text content, error messages, CTAs, microcopy
4. **[Design Inspiration](../../../attachments/bmad_design_inspiration.txt)** - Visual references, typography, spacing, accessibility standards

**Never guess at design decisions. Always reference the artifacts.**

---

## 🎨 Design System Rules

### Colors - Use CSS Variables ONLY

```css
/* ✅ CORRECT */
.button-primary {
  background: var(--color-primary);
  color: var(--color-neutral-light);
}

/* ❌ WRONG - Never hardcode colors */
.button-primary {
  background: #3E4B6E;
  color: #F5F3EE;
}
```

**Reference**: `COLOR_SCHEMES.md` for complete palette

### Spacing - Use 8pt Grid

```css
/* ✅ CORRECT */
.card {
  padding: var(--space-4);  /* 24px */
  margin-bottom: var(--space-6);  /* 48px */
}

/* ❌ WRONG - Arbitrary values */
.card {
  padding: 22px;
  margin-bottom: 45px;
}
```

**Available spacing**: 4px, 8px, 16px, 24px, 32px, 48px, 64px

### Typography - Use Predefined Scales

```css
/* ✅ CORRECT */
.heading {
  font-size: var(--font-size-h2);
  line-height: var(--line-height-heading);
}

/* ❌ WRONG */
.heading {
  font-size: 23px;
  line-height: 1.3;
}
```

---

## 📝 Copy & Content Rules

### **NEVER Write Your Own Copy**

All UI text MUST come from `UX_COPY_GUIDE.md`. Copy it verbatim.

```jsx
/* ✅ CORRECT - From UX_COPY_GUIDE.md */
<Button>Generate Chart</Button>
<EmptyState>
  <h3>Your cosmic story awaits</h3>
  <p>Generate your natal chart to unlock personalized insights</p>
</EmptyState>

/* ❌ WRONG - Made up copy */
<Button>Create a Chart</Button>
<EmptyState>
  <h3>No chart yet</h3>
  <p>Click here to make one</p>
</EmptyState>
```

### Text Patterns

- **Buttons**: Action verbs, title case ("Generate Chart", "Save Entry")
- **Headings**: Sentence case ("Your natal chart", not "Your Natal Chart")
- **Empty states**: Encouraging, warm ("Your cosmic story awaits")
- **Errors**: Clear, actionable ("We couldn't find that location. Try again?")
- **Success**: Celebratory with emoji ("✨ Your chart is ready!")

**Reference**: `UX_COPY_GUIDE.md` sections 1-14

---

## ♿ Accessibility - Non-Negotiable

Every component MUST be accessible. No exceptions.

### Checklist for Every Component

```jsx
/* ✅ Complete Accessibility Example */
<button
  onClick={handleClick}
  aria-label="Close modal"
  aria-pressed={isActive}
  disabled={isDisabled}
>
  <CloseIcon aria-hidden="true" />
  <span className="sr-only">Close</span>
</button>

<img 
  src={cardImage} 
  alt="The Sovereign archetype card showing a crowned figure"
/>

<input
  id="birth-year"
  type="number"
  aria-label="Birth year"
  aria-describedby="year-error"
  aria-invalid={!!errors.year}
  required
/>
{errors.year && (
  <span id="year-error" role="alert">
    {errors.year}
  </span>
)}
```

### Required for All Interactive Elements

- ✅ Keyboard accessible (Tab, Enter, Space, Arrow keys)
- ✅ Focus indicator visible (2px outline, 2px offset)
- ✅ ARIA labels on all buttons/links
- ✅ alt text on all images
- ✅ Form labels associated with inputs
- ✅ Error messages announced (role="alert")
- ✅ Loading states announced (aria-live="polite")

### ARIA Patterns Reference

```jsx
/* Accordion */
<button
  aria-expanded={isOpen}
  aria-controls="panel-1"
  onClick={toggle}
>
  Expand Section
</button>
<div id="panel-1" role="region" aria-labelledby="heading-1">
  Content
</div>

/* Modal */
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
>
  <h2 id="modal-title">Modal Heading</h2>
  {/* Content */}
</div>

/* Loading */
<div aria-live="polite" aria-busy="true">
  Calculating chart...
</div>
```

**Reference**: `DESIGN_INSPIRATION.md` (Accessibility Requirements)

---

## 🧩 Component Development

### Component Structure

```jsx
// ✅ CORRECT Structure
// /frontend/src/components/shared/Button.jsx

import React from 'react';
import './Button.css';

/**
 * Button component with multiple variants
 * 
 * @param {string} variant - 'primary' | 'secondary' | 'tertiary' | 'icon'
 * @param {string} size - 'small' | 'medium' | 'large'
 * @param {boolean} disabled - Disabled state
 * @param {boolean} loading - Loading state
 * @param {string} ariaLabel - Accessible label (required for icon buttons)
 * @param {function} onClick - Click handler
 * 
 * @accessibility
 * - Keyboard accessible (Enter/Space)
 * - Focus indicator visible
 * - Loading state announced
 */
const Button = ({ 
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  ariaLabel,
  onClick,
  children 
}) => {
  return (
    <button
      className={`btn btn--${variant} btn--${size}`}
      onClick={onClick}
      disabled={disabled || loading}
      aria-label={ariaLabel}
      aria-busy={loading}
    >
      {loading ? <Spinner /> : children}
    </button>
  );
};

export default Button;
```

### CSS Modules or BEM

```css
/* ✅ CORRECT - BEM naming */
.btn {
  padding: var(--space-3) var(--space-4);
  border-radius: 8px;
  font-weight: 600;
  transition: all 150ms ease;
  cursor: pointer;
}

.btn--primary {
  background: var(--color-primary);
  color: var(--color-neutral-light);
}

.btn--primary:hover:not(:disabled) {
  background: var(--color-primary-light);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(62, 75, 110, 0.4);
}

.btn--primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
```

---

## 📱 Responsive Design

### Mobile-First Approach

```css
/* ✅ CORRECT - Mobile first */
.card {
  width: 100%;
  padding: var(--space-3);
}

@media (min-width: 768px) {
  .card {
    width: 320px;
    padding: var(--space-4);
  }
}

@media (min-width: 1024px) {
  .card {
    width: 400px;
  }
}

/* ❌ WRONG - Desktop first */
.card {
  width: 400px;
}

@media (max-width: 768px) {
  .card {
    width: 100%;
  }
}
```

### Breakpoints

```css
--breakpoint-mobile: 320px - 767px;
--breakpoint-tablet: 768px - 1023px;
--breakpoint-desktop: 1024px - 1439px;
--breakpoint-large: 1440px+;
```

### Touch Targets

```css
/* ✅ Minimum 44px × 44px on mobile */
@media (max-width: 767px) {
  .btn {
    min-height: 44px;
    min-width: 44px;
  }
}
```

---

## 🎭 Theme Support (Light/Dark Mode)

### Using Theme Variables

```css
/* variables.css */
:root {
  --bg-primary: var(--color-neutral-light);
  --text-primary: var(--color-neutral-dark);
}

[data-theme="dark"] {
  --bg-primary: var(--color-neutral-dark);
  --text-primary: var(--color-neutral-light);
}
```

```jsx
/* Theme Toggle Component */
const ThemeToggle = () => {
  const [theme, setTheme] = useState('light');
  
  useEffect(() => {
    const saved = localStorage.getItem('theme') || 'light';
    setTheme(saved);
    document.documentElement.setAttribute('data-theme', saved);
  }, []);
  
  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
  };
  
  return (
    <Toggle
      checked={theme === 'dark'}
      onChange={toggleTheme}
      label="Dark Mode"
    />
  );
};
```

---

## 🧪 Testing Checklist

Before marking an issue as complete, verify:

### Functionality
- [ ] All acceptance criteria met
- [ ] No console errors
- [ ] Works on latest Chrome, Firefox, Safari
- [ ] API calls handle errors gracefully
- [ ] Loading states display correctly
- [ ] Empty states display when appropriate

### Accessibility
- [ ] Keyboard navigation works (Tab, Enter, Space, Arrows, Esc)
- [ ] Focus visible on all interactive elements
- [ ] Screen reader announces content (test with browser extension)
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] All images have alt text
- [ ] Form validation errors announced

### Responsive
- [ ] Mobile (375px width) - works and readable
- [ ] Tablet (768px width) - layout adapts correctly
- [ ] Desktop (1440px width) - uses space effectively
- [ ] No horizontal scroll at any breakpoint
- [ ] Touch targets 44px+ on mobile

### Design Consistency
- [ ] Colors match design system (CSS variables used)
- [ ] Spacing uses 8pt grid
- [ ] Typography matches scale
- [ ] Matches Figma designs (if available)
- [ ] Animations smooth (150-250ms transitions)

### Code Quality
- [ ] Component documented (props, usage, accessibility)
- [ ] CSS classes follow BEM or modules
- [ ] No hardcoded values (use CSS variables)
- [ ] Code commented where complex
- [ ] PropTypes or TypeScript types defined

---

## 🚫 Common Mistakes to Avoid

### ❌ DON'T: Hardcode Colors
```jsx
/* WRONG */
<div style={{ color: '#3E4B6E', background: '#F5F3EE' }}>
```

### ✅ DO: Use CSS Variables
```jsx
/* CORRECT */
<div className="card-primary">
```

---

### ❌ DON'T: Make Up Copy
```jsx
/* WRONG */
<Button>Submit Form</Button>
```

### ✅ DO: Use Copy from Guide
```jsx
/* CORRECT - from UX_COPY_GUIDE.md */
<Button>Calculate Chart</Button>
```

---

### ❌ DON'T: Skip Accessibility
```jsx
/* WRONG */
<button onClick={handleClose}>
  <XIcon />
</button>
```

### ✅ DO: Include ARIA Labels
```jsx
/* CORRECT */
<button onClick={handleClose} aria-label="Close modal">
  <XIcon aria-hidden="true" />
</button>
```

---

### ❌ DON'T: Use Arbitrary Spacing
```css
/* WRONG */
.card {
  margin: 22px 15px;
  padding: 18px;
}
```

### ✅ DO: Use Spacing Scale
```css
/* CORRECT */
.card {
  margin: var(--space-4) var(--space-3);
  padding: var(--space-3);
}
```

---

### ❌ DON'T: Desktop-First Responsive
```css
/* WRONG */
.grid {
  grid-template-columns: repeat(3, 1fr);
}
@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
```

### ✅ DO: Mobile-First Responsive
```css
/* CORRECT */
.grid {
  grid-template-columns: 1fr;
}
@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

---

## 🔍 Issue Implementation Workflow

### Step 1: Read the Issue
- Review title, description, acceptance criteria
- Check dependencies (are blocking issues complete?)
- Note priority level
- Read linked reference documents

### Step 2: Review Design Artifacts
- Check `COMPONENT_STRUCTURE.md` for component hierarchy
- Check `COLOR_SCHEMES.md` for colors to use
- Check `UX_COPY_GUIDE.md` for exact text content
- Check `DESIGN_INSPIRATION.md` for patterns and styles

### Step 3: Plan Implementation
- Identify reusable components needed
- Determine CSS variables to use
- List accessibility requirements
- Note responsive breakpoints needed

### Step 4: Implement
- Write semantic HTML
- Use CSS variables for colors/spacing
- Copy text from UX guide verbatim
- Add ARIA attributes
- Include keyboard navigation
- Make mobile-first responsive

### Step 5: Test
- Run through testing checklist (above)
- Test keyboard navigation
- Test on mobile, tablet, desktop
- Verify color contrast
- Check console for errors

### Step 6: Document
- Add JSDoc comments to component
- Include accessibility notes
- Provide usage examples
- Update component README if needed

### Step 7: Mark Complete
- All acceptance criteria met ✅
- All tests passing ✅
- Code reviewed (if human team) ✅
- Documentation updated ✅

---

## 📦 File Organization

```
/frontend/src/
├── components/
│   ├── layout/
│   │   ├── Header/
│   │   │   ├── Header.jsx
│   │   │   ├── Header.css
│   │   │   └── Header.test.jsx
│   │   ├── Sidebar/
│   │   └── Footer/
│   ├── shared/
│   │   ├── Button/
│   │   │   ├── Button.jsx
│   │   │   ├── Button.css
│   │   │   └── Button.test.jsx
│   │   ├── Card/
│   │   └── Input/
│   ├── dashboard/
│   ├── chart/
│   ├── bmad/
│   ├── symbolon/
│   ├── journal/
│   └── settings/
├── styles/
│   ├── variables.css    ← Define all CSS custom properties here
│   ├── typography.css   ← Font scales and styles
│   ├── themes.css       ← Light/dark mode overrides
│   └── reset.css        ← CSS reset/normalize
├── hooks/
├── contexts/
├── services/
└── utils/
```

---

## 🎯 Example: Implementing a Card Component

Let's walk through implementing Issue 1.4 (Card Component) step-by-step:

### 1. Read Issue & References
- **Issue**: Create Card component with 6 variants
- **Reference**: `COMPONENT_STRUCTURE.md` (Card Variants section)
- **Reference**: `DESIGN_INSPIRATION.md` (Card Dimensions, Shadow)

### 2. Check Design Specs
- Border radius: 12px
- Shadow: `0 2px 8px rgba(0,0,0,0.08)`
- Hover shadow: `0 4px 16px rgba(0,0,0,0.12)`
- Padding options: small (12px), medium (24px), large (32px)

### 3. Implement Component

```jsx
// /frontend/src/components/shared/Card/Card.jsx

import React from 'react';
import './Card.css';

/**
 * Card component - base container for content
 * 
 * @param {string} variant - 'basic' | 'stat' | 'image' | 'action' | 'expansion' | 'highlight'
 * @param {string} padding - 'small' | 'medium' | 'large'
 * @param {boolean} elevated - Adds hover shadow effect
 * @param {function} onClick - Optional click handler
 * @param {object} children - Card content
 * 
 * @example
 * <Card variant="stat" padding="medium">
 *   <Card.Icon><CalendarIcon /></Card.Icon>
 *   <Card.Metric>7 days</Card.Metric>
 *   <Card.Label>Journal Streak</Card.Label>
 * </Card>
 */
const Card = ({ 
  variant = 'basic',
  padding = 'medium',
  elevated = false,
  onClick,
  children,
  ...props
}) => {
  const Tag = onClick ? 'button' : 'article';
  
  return (
    <Tag
      className={`card card--${variant} card--padding-${padding} ${elevated ? 'card--elevated' : ''}`}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyPress={onClick ? (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onClick(e);
        }
      } : undefined}
      {...props}
    >
      {children}
    </Tag>
  );
};

// Sub-components for structured cards
Card.Icon = ({ children }) => (
  <div className="card__icon">{children}</div>
);

Card.Metric = ({ children }) => (
  <div className="card__metric">{children}</div>
);

Card.Label = ({ children }) => (
  <div className="card__label">{children}</div>
);

export default Card;
```

### 4. Style Component

```css
/* /frontend/src/components/shared/Card/Card.css */

.card {
  background: var(--color-neutral-light);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: box-shadow 250ms ease, transform 250ms ease;
}

/* Padding variants */
.card--padding-small {
  padding: var(--space-3); /* 16px */
}

.card--padding-medium {
  padding: var(--space-4); /* 24px */
}

.card--padding-large {
  padding: var(--space-6); /* 48px */
}

/* Elevated hover effect */
.card--elevated:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

/* Clickable cards */
.card[role="button"] {
  cursor: pointer;
  border: none;
  text-align: left;
  width: 100%;
}

.card[role="button"]:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Stat Card Variant */
.card--stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.card__icon {
  font-size: 32px;
  margin-bottom: var(--space-2);
  color: var(--color-primary);
}

.card__metric {
  font-size: var(--font-size-h2);
  font-weight: 700;
  color: var(--color-primary);
  margin-bottom: var(--space-1);
}

.card__label {
  font-size: var(--font-size-small);
  color: var(--text-secondary);
}

/* Dark mode */
[data-theme="dark"] .card {
  background: #3A4257;
}

/* Responsive */
@media (max-width: 767px) {
  .card {
    border-radius: 8px;
  }
  
  .card--padding-large {
    padding: var(--space-4);
  }
}
```

### 5. Test Component

```jsx
// /frontend/src/components/shared/Card/Card.test.jsx

import { render, screen, fireEvent } from '@testing-library/react';
import Card from './Card';

describe('Card Component', () => {
  test('renders basic card', () => {
    render(<Card>Test Content</Card>);
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });
  
  test('handles click events', () => {
    const handleClick = jest.fn();
    render(<Card onClick={handleClick}>Clickable</Card>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalled();
  });
  
  test('keyboard accessible', () => {
    const handleClick = jest.fn();
    render(<Card onClick={handleClick}>Press Enter</Card>);
    const card = screen.getByRole('button');
    fireEvent.keyPress(card, { key: 'Enter' });
    expect(handleClick).toHaveBeenCalled();
  });
});
```

### 6. Document Component

```markdown
# Card Component

Reusable card container with multiple variants.

## Variants

- **basic**: Simple container
- **stat**: Icon + metric + label (centered)
- **image**: Image header with content
- **action**: Includes CTA button
- **expansion**: Collapsible accordion
- **highlight**: Featured content with gradient border

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | string | 'basic' | Card style variant |
| padding | string | 'medium' | Padding size |
| elevated | boolean | false | Adds hover shadow |
| onClick | function | - | Click handler (makes clickable) |

## Usage

\`\`\`jsx
// Basic card
<Card padding="medium">
  <h3>Title</h3>
  <p>Content</p>
</Card>

// Stat card
<Card variant="stat" padding="medium">
  <Card.Icon><CalendarIcon /></Card.Icon>
  <Card.Metric>7 days</Card.Metric>
  <Card.Label>Journal Streak</Card.Label>
</Card>

// Clickable card
<Card elevated onClick={handleClick}>
  Click me
</Card>
\`\`\`

## Accessibility

- Clickable cards use button role
- Keyboard accessible (Enter/Space)
- Focus indicator visible (2px outline)
- Semantic HTML (article for static, button for clickable)

## Responsive

- Border radius reduces on mobile (12px → 8px)
- Large padding reduces on mobile (48px → 24px)
```

### 7. Mark Issue Complete ✅

All acceptance criteria met:
- ✅ Card base component with 12px border radius
- ✅ Shadow system implemented
- ✅ 6+ variants (basic, stat, image, action, expansion, highlight)
- ✅ Expansion cards animate smoothly
- ✅ Cards responsive
- ✅ Semantic HTML

---

## 🤝 Working with Human Developers

If you're collaborating with human developers:

1. **Comment your code** - Explain complex logic
2. **Document decisions** - Why you chose a particular approach
3. **Ask questions** - If design specs are unclear, ask before guessing
4. **Suggest improvements** - If you see a better way, propose it
5. **Follow PRs** - Learn from code reviews

---

## 📞 Need Help?

If you encounter issues:

1. **Re-read the design artifacts** - Answer is probably there
2. **Check component structure** - Are you organizing files correctly?
3. **Review similar components** - How did others solve this?
4. **Test incrementally** - Don't build everything then test
5. **Ask for clarification** - Better to ask than guess wrong

---

## 🎉 You're Ready!

You now have everything you need to contribute high-quality, accessible, design-consistent components to the BMAD Astrology App.

**Key Reminders**:
- ✅ Always reference design artifacts
- ✅ Never hardcode colors or spacing
- ✅ Copy text from UX guide verbatim
- ✅ Make everything keyboard accessible
- ✅ Test on mobile, tablet, desktop
- ✅ Document your components

**Happy coding! 🚀**

---

**Document Version**: 1.0  
**Last Updated**: October 28, 2025  
**Maintained By**: BMAD Astrology App Team
