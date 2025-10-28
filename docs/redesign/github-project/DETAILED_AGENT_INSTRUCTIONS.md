# Agent Assignment Commands with Detailed Instructions

## 🤖 Phase 1: Foundation (Agent 1 - Design System Lead)

### Issue #10 - CSS Variables & Theme System ✅ ALREADY ASSIGNED

**Status:** Comment already posted, waiting for PR

---

### Issue #11 - Typography System
**Run after #10 is merged:**

```bash
gh issue comment 11 --body "# Agent 1: Typography System Implementation

## 🎯 Task Overview
Implement a complete typography system using the Inter font family with a responsive type scale. This builds on the CSS variables from Issue #10.

## 📋 Detailed Requirements

### 1. Font Loading
Create: \`/frontend/src/styles/fonts.css\`

\`\`\`css
/* Import Inter from Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Font stack with fallbacks */
:root {
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  --font-mono: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
}
\`\`\`

### 2. Type Scale (Major Third - 1.25 ratio)
Create: \`/frontend/src/styles/typography.css\`

\`\`\`css
:root {
  /* Base size */
  --text-base: 16px;
  
  /* Type scale */
  --text-xs: 0.64rem;   /* 10.24px */
  --text-sm: 0.8rem;    /* 12.8px */
  --text-md: 1rem;      /* 16px - base */
  --text-lg: 1.25rem;   /* 20px */
  --text-xl: 1.563rem;  /* 25px */
  --text-2xl: 1.953rem; /* 31.25px */
  --text-3xl: 2.441rem; /* 39px */
  --text-4xl: 3.052rem; /* 48.8px */
  
  /* Line heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
  
  /* Font weights */
  --font-light: 300;
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
  
  /* Letter spacing */
  --tracking-tight: -0.025em;
  --tracking-normal: 0em;
  --tracking-wide: 0.025em;
}

/* Apply to body */
body {
  font-family: var(--font-primary);
  font-size: var(--text-md);
  line-height: var(--leading-normal);
  color: var(--text-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Heading styles */
h1, .text-4xl { 
  font-size: var(--text-4xl); 
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tight);
  color: var(--text-primary);
  margin-bottom: var(--space-4);
}

h2, .text-3xl { 
  font-size: var(--text-3xl); 
  font-weight: var(--font-semibold);
  line-height: var(--leading-tight);
  color: var(--text-primary);
  margin-bottom: var(--space-3);
}

h3, .text-2xl { 
  font-size: var(--text-2xl); 
  font-weight: var(--font-semibold);
  line-height: var(--leading-normal);
  margin-bottom: var(--space-3);
}

h4, .text-xl { 
  font-size: var(--text-xl); 
  font-weight: var(--font-medium);
  line-height: var(--leading-normal);
}

/* Body text variants */
.text-lg { font-size: var(--text-lg); }
.text-md { font-size: var(--text-md); }
.text-sm { font-size: var(--text-sm); color: var(--text-secondary); }
.text-xs { font-size: var(--text-xs); color: var(--text-secondary); }

/* Utility classes */
.font-bold { font-weight: var(--font-bold); }
.font-semibold { font-weight: var(--font-semibold); }
.font-medium { font-weight: var(--font-medium); }
.font-normal { font-weight: var(--font-normal); }
.font-light { font-weight: var(--font-light); }

.leading-tight { line-height: var(--leading-tight); }
.leading-normal { line-height: var(--leading-normal); }
.leading-relaxed { line-height: var(--leading-relaxed); }

/* Responsive adjustments */
@media (max-width: 768px) {
  :root {
    --text-base: 14px;
  }
}
\`\`\`

### 3. Import Order
Modify: \`/frontend/src/index.js\`

Add these imports in ORDER:
\`\`\`javascript
import './styles/variables.css';  // From Issue #10
import './styles/fonts.css';      // NEW
import './styles/typography.css'; // NEW
\`\`\`

### 4. Typography Demo Component (for testing)
Create: \`/frontend/src/components/shared/TypographyDemo.jsx\`

\`\`\`javascript
import React from 'react';

const TypographyDemo = () => {
  return (
    <div style={{ padding: 'var(--space-5)' }}>
      <h1>Heading 1 - The Cosmic Blueprint</h1>
      <h2>Heading 2 - Birth Chart Analysis</h2>
      <h3>Heading 3 - Planetary Positions</h3>
      <h4>Heading 4 - House System</h4>
      
      <p className=\"text-lg\">
        Large body text - Primary content introduction with emphasis.
      </p>
      
      <p className=\"text-md\">
        Medium body text - Standard paragraph content for readability and comfortable reading.
      </p>
      
      <p className=\"text-sm\">
        Small text - Secondary information, captions, and metadata.
      </p>
      
      <p className=\"text-xs\">
        Extra small - Footnotes, legal text, minor details.
      </p>
      
      <div style={{ marginTop: 'var(--space-5)' }}>
        <p className=\"font-bold\">Bold weight example</p>
        <p className=\"font-semibold\">Semibold weight example</p>
        <p className=\"font-medium\">Medium weight example</p>
        <p className=\"font-normal\">Normal weight example</p>
        <p className=\"font-light\">Light weight example</p>
      </div>
    </div>
  );
};

export default TypographyDemo;
\`\`\`

## ✅ Acceptance Criteria Checklist

Test each item:
- [ ] Inter font loads from Google Fonts
- [ ] All heading sizes (h1-h4) render correctly
- [ ] Text utility classes (.text-lg, .text-md, etc.) work
- [ ] Font weights (light, normal, medium, semibold, bold) display properly
- [ ] Line heights are visually balanced
- [ ] Typography scales down on mobile (< 768px)
- [ ] All text uses CSS variables (no hardcoded values)
- [ ] Text colors respect theme (light/dark mode)
- [ ] Contrast ratios meet WCAG AA (4.5:1 for body, 3:1 for headings)

## 🧪 Testing Commands

\`\`\`bash
# Run dev server
cd frontend && npm start

# Check for hardcoded font values
grep -r \"font-family: \" frontend/src --exclude-dir=node_modules

# Verify no hardcoded font sizes outside typography.css
grep -r \"font-size: [0-9]\" frontend/src --exclude=\"typography.css\" --exclude-dir=node_modules
\`\`\`

## 📦 Files to Create
1. \`/frontend/src/styles/fonts.css\`
2. \`/frontend/src/styles/typography.css\`
3. \`/frontend/src/components/shared/TypographyDemo.jsx\`

## 📝 Files to Modify
1. \`/frontend/src/index.js\` - Add typography imports

## 🔗 Dependencies
- **Requires:** Issue #10 (CSS Variables) - MUST be merged first
- **Blocks:** All component issues (#12-25)

## 🎯 Success Criteria
- PR passes all tests
- No console errors or warnings
- Typography scales properly across devices
- Text is readable in both light and dark themes
- WCAG AA compliance verified

Please implement exactly as specified above and open a PR when complete."
```

---

### Issue #12 - Button Component
**Run after #11 is merged:**

```bash
gh issue comment 12 --body "# Agent 1: Button Component Implementation

## 🎯 Task Overview
Create a comprehensive button component system with multiple variants (primary, secondary, outline, text) and states (default, hover, active, disabled, loading).

## 📋 Detailed Requirements

### 1. Button Component
Create: \`/frontend/src/components/shared/Button.jsx\`

\`\`\`javascript
import React from 'react';
import './Button.css';

const Button = ({ 
  children,
  variant = 'primary',  // primary | secondary | outline | text | danger
  size = 'md',          // sm | md | lg
  disabled = false,
  loading = false,
  fullWidth = false,
  leftIcon = null,
  rightIcon = null,
  onClick,
  type = 'button',
  className = '',
  ...props 
}) => {
  const buttonClass = [
    'btn',
    \`btn--\${variant}\`,
    \`btn--\${size}\`,
    fullWidth && 'btn--full-width',
    loading && 'btn--loading',
    className
  ].filter(Boolean).join(' ');

  return (
    <button
      type={type}
      className={buttonClass}
      disabled={disabled || loading}
      onClick={onClick}
      {...props}
    >
      {loading && <span className=\"btn__spinner\" aria-hidden=\"true\"></span>}
      {!loading && leftIcon && <span className=\"btn__icon btn__icon--left\">{leftIcon}</span>}
      <span className=\"btn__text\">{children}</span>
      {!loading && rightIcon && <span className=\"btn__icon btn__icon--right\">{rightIcon}</span>}
    </button>
  );
};

export default Button;
\`\`\`

### 2. Button Styles
Create: \`/frontend/src/components/shared/Button.css\`

\`\`\`css
/* Base button styles */
.btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  
  font-family: var(--font-primary);
  font-weight: var(--font-medium);
  text-align: center;
  text-decoration: none;
  white-space: nowrap;
  
  border: 2px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  
  transition: all 0.2s ease-in-out;
  user-select: none;
  
  /* Remove default button styles */
  background: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

.btn:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Sizes */
.btn--sm {
  padding: var(--space-1) var(--space-3);
  font-size: var(--text-sm);
  min-height: 32px;
}

.btn--md {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-md);
  min-height: 40px;
}

.btn--lg {
  padding: var(--space-3) var(--space-5);
  font-size: var(--text-lg);
  min-height: 48px;
}

/* Primary variant */
.btn--primary {
  background-color: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.btn--primary:hover:not(:disabled) {
  background-color: var(--color-primary-dark);
  border-color: var(--color-primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(62, 75, 110, 0.3);
}

.btn--primary:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(62, 75, 110, 0.2);
}

/* Secondary variant */
.btn--secondary {
  background-color: var(--color-secondary);
  color: var(--color-neutral-900);
  border-color: var(--color-secondary);
}

.btn--secondary:hover:not(:disabled) {
  background-color: var(--color-secondary-dark);
  border-color: var(--color-secondary-dark);
  transform: translateY(-1px);
}

/* Outline variant */
.btn--outline {
  background-color: transparent;
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.btn--outline:hover:not(:disabled) {
  background-color: var(--color-primary);
  color: white;
}

/* Text variant */
.btn--text {
  background-color: transparent;
  color: var(--color-primary);
  border-color: transparent;
  padding: var(--space-2);
}

.btn--text:hover:not(:disabled) {
  background-color: rgba(62, 75, 110, 0.1);
}

/* Danger variant */
.btn--danger {
  background-color: var(--color-error);
  color: white;
  border-color: var(--color-error);
}

.btn--danger:hover:not(:disabled) {
  background-color: #A6654A;
  border-color: #A6654A;
}

/* Disabled state */
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

/* Loading state */
.btn--loading {
  pointer-events: none;
}

.btn--loading .btn__text {
  opacity: 0.6;
}

.btn__spinner {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: btn-spin 0.6s linear infinite;
}

@keyframes btn-spin {
  to { transform: translateX(-50%) rotate(360deg); }
}

/* Full width */
.btn--full-width {
  width: 100%;
}

/* Icons */
.btn__icon {
  display: inline-flex;
  align-items: center;
}

.btn__icon svg {
  width: 16px;
  height: 16px;
}

.btn--lg .btn__icon svg {
  width: 20px;
  height: 20px;
}
\`\`\`

### 3. Button Demo/Test Component
Create: \`/frontend/src/components/shared/ButtonDemo.jsx\`

\`\`\`javascript
import React, { useState } from 'react';
import Button from './Button';

const ButtonDemo = () => {
  const [loading, setLoading] = useState(false);

  const handleClick = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 2000);
  };

  return (
    <div style={{ padding: 'var(--space-5)', display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
      <div>
        <h3>Variants</h3>
        <div style={{ display: 'flex', gap: 'var(--space-3)', flexWrap: 'wrap' }}>
          <Button variant=\"primary\">Primary</Button>
          <Button variant=\"secondary\">Secondary</Button>
          <Button variant=\"outline\">Outline</Button>
          <Button variant=\"text\">Text</Button>
          <Button variant=\"danger\">Danger</Button>
        </div>
      </div>

      <div>
        <h3>Sizes</h3>
        <div style={{ display: 'flex', gap: 'var(--space-3)', alignItems: 'center' }}>
          <Button size=\"sm\">Small</Button>
          <Button size=\"md\">Medium</Button>
          <Button size=\"lg\">Large</Button>
        </div>
      </div>

      <div>
        <h3>States</h3>
        <div style={{ display: 'flex', gap: 'var(--space-3)', flexWrap: 'wrap' }}>
          <Button>Default</Button>
          <Button disabled>Disabled</Button>
          <Button loading={loading} onClick={handleClick}>
            {loading ? 'Loading...' : 'Click to Load'}
          </Button>
        </div>
      </div>

      <div>
        <h3>With Icons</h3>
        <div style={{ display: 'flex', gap: 'var(--space-3)' }}>
          <Button leftIcon=\"⭐\">Favorite</Button>
          <Button rightIcon=\"→\">Next</Button>
        </div>
      </div>

      <div>
        <h3>Full Width</h3>
        <Button fullWidth>Full Width Button</Button>
      </div>
    </div>
  );
};

export default ButtonDemo;
\`\`\`

## ✅ Acceptance Criteria Checklist

- [ ] All 5 button variants render correctly (primary, secondary, outline, text, danger)
- [ ] All 3 sizes work (sm, md, lg)
- [ ] Disabled state prevents clicks and shows visual feedback
- [ ] Loading state shows spinner and prevents interaction
- [ ] Icons (left and right) display properly
- [ ] Full width option stretches button to container width
- [ ] Hover effects work on all variants (except disabled)
- [ ] Focus indicators visible (WCAG 2.1)
- [ ] Keyboard accessible (Enter and Space trigger onClick)
- [ ] No console errors
- [ ] Works in light and dark themes

## 🧪 Testing Checklist

Manual tests:
- [ ] Click each button variant
- [ ] Tab through buttons (focus visible)
- [ ] Press Enter and Space on focused buttons
- [ ] Test in light mode
- [ ] Test in dark mode
- [ ] Test on mobile (< 768px)
- [ ] Verify hover states
- [ ] Verify loading state (2s delay)

## 📦 Files to Create
1. \`/frontend/src/components/shared/Button.jsx\`
2. \`/frontend/src/components/shared/Button.css\`
3. \`/frontend/src/components/shared/ButtonDemo.jsx\`

## 🔗 Dependencies
- **Requires:** Issues #10 (CSS Variables) + #11 (Typography) - MUST be merged
- **Blocks:** All form components (#14, #20) and UI components

## 🎯 Success Criteria
- All button variants functional
- Fully accessible (keyboard + screen reader)
- WCAG AA compliant
- No layout shifts or console errors
- Passes manual testing in 3+ browsers

Please implement exactly as specified and open a PR when complete."
```

---

---

### Issue #13 - Card Component
**Run after #12 is merged:**

```bash
gh issue comment 13 --body "# Agent 1: Card Component Implementation

## 🎯 Task Overview
Create a flexible card component system for displaying content sections with consistent styling, elevation, and interactive states.

## 📋 Detailed Requirements

### 1. Card Component
Create: \`/frontend/src/components/shared/Card.jsx\`

\`\`\`javascript
import React from 'react';
import './Card.css';

const Card = ({ 
  children,
  variant = 'default',  // default | elevated | outlined | interactive
  padding = 'md',       // sm | md | lg | none
  onClick,
  className = '',
  as = 'div',
  ...props 
}) => {
  const Component = as;
  const isClickable = !!onClick;
  
  const cardClass = [
    'card',
    \`card--\${variant}\`,
    \`card--padding-\${padding}\`,
    isClickable && 'card--clickable',
    className
  ].filter(Boolean).join(' ');

  return (
    <Component
      className={cardClass}
      onClick={onClick}
      role={isClickable ? 'button' : undefined}
      tabIndex={isClickable ? 0 : undefined}
      onKeyDown={isClickable ? (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onClick?.(e);
        }
      } : undefined}
      {...props}
    >
      {children}
    </Component>
  );
};

// Sub-components for structured content
Card.Header = ({ children, className = '', ...props }) => (
  <div className={\`card__header \${className}\`} {...props}>
    {children}
  </div>
);

Card.Body = ({ children, className = '', ...props }) => (
  <div className={\`card__body \${className}\`} {...props}>
    {children}
  </div>
);

Card.Footer = ({ children, className = '', ...props }) => (
  <div className={\`card__footer \${className}\`} {...props}>
    {children}
  </div>
);

export default Card;
\`\`\`

### 2. Card Styles
Create: \`/frontend/src/components/shared/Card.css\`

\`\`\`css
.card {
  background-color: var(--bg-secondary);
  border-radius: 12px;
  transition: all 0.2s ease-in-out;
  position: relative;
  overflow: hidden;
}

/* Variants */
.card--default {
  border: 1px solid var(--border-color);
}

.card--elevated {
  border: none;
  box-shadow: 0 2px 8px rgba(45, 49, 66, 0.1);
}

[data-theme=\"dark\"] .card--elevated {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.card--outlined {
  border: 2px solid var(--color-primary);
  background-color: transparent;
}

.card--interactive {
  border: 1px solid var(--border-color);
  cursor: pointer;
}

/* Padding variants */
.card--padding-none {
  padding: 0;
}

.card--padding-sm {
  padding: var(--space-3);
}

.card--padding-md {
  padding: var(--space-4);
}

.card--padding-lg {
  padding: var(--space-5);
}

/* Clickable state */
.card--clickable {
  cursor: pointer;
}

.card--clickable:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(45, 49, 66, 0.15);
}

[data-theme=\"dark\"] .card--clickable:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
}

.card--clickable:active {
  transform: translateY(0);
}

.card--clickable:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Sub-components */
.card__header {
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--border-color);
  margin-bottom: var(--space-3);
}

.card__body {
  flex: 1;
}

.card__footer {
  padding-top: var(--space-3);
  border-top: 1px solid var(--border-color);
  margin-top: var(--space-3);
  display: flex;
  gap: var(--space-2);
  align-items: center;
}

/* Responsive */
@media (max-width: 768px) {
  .card--padding-md {
    padding: var(--space-3);
  }
  
  .card--padding-lg {
    padding: var(--space-4);
  }
}
\`\`\`

### 3. Card Demo Component
Create: \`/frontend/src/components/shared/CardDemo.jsx\`

\`\`\`javascript
import React from 'react';
import Card from './Card';
import Button from './Button';

const CardDemo = () => {
  return (
    <div style={{ padding: 'var(--space-5)', display: 'grid', gap: 'var(--space-4)', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))' }}>
      
      <Card variant=\"default\">
        <h3>Default Card</h3>
        <p>Basic card with border and padding.</p>
      </Card>

      <Card variant=\"elevated\">
        <h3>Elevated Card</h3>
        <p>Card with shadow elevation.</p>
      </Card>

      <Card variant=\"outlined\">
        <h3>Outlined Card</h3>
        <p>Card with prominent border.</p>
      </Card>

      <Card variant=\"interactive\" onClick={() => alert('Card clicked!')}>
        <h3>Interactive Card</h3>
        <p>Click me! I'm interactive and keyboard accessible.</p>
      </Card>

      <Card variant=\"elevated\" padding=\"lg\">
        <Card.Header>
          <h3 style={{ margin: 0 }}>Structured Card</h3>
          <p style={{ margin: 0, fontSize: 'var(--text-sm)' }}>With header, body, and footer</p>
        </Card.Header>
        <Card.Body>
          <p>This card uses the structured layout with separate header, body, and footer sections.</p>
        </Card.Body>
        <Card.Footer>
          <Button size=\"sm\" variant=\"outline\">Cancel</Button>
          <Button size=\"sm\">Confirm</Button>
        </Card.Footer>
      </Card>

      <Card variant=\"default\" padding=\"none\">
        <img 
          src=\"https://via.placeholder.com/400x200/3E4B6E/FFFFFF?text=Card+Image\" 
          alt=\"Placeholder\"
          style={{ width: '100%', display: 'block' }}
        />
        <div style={{ padding: 'var(--space-4)' }}>
          <h3>Card with Image</h3>
          <p>No padding on card, padding on content div.</p>
        </div>
      </Card>

    </div>
  );
};

export default CardDemo;
\`\`\`

## ✅ Acceptance Criteria
- [ ] All 4 card variants render correctly
- [ ] Padding options work (none, sm, md, lg)
- [ ] Interactive cards respond to clicks
- [ ] Interactive cards keyboard accessible (Enter/Space)
- [ ] Hover effects work on interactive cards
- [ ] Sub-components (Header, Body, Footer) render correctly
- [ ] Cards work in light and dark themes
- [ ] Focus indicators visible

## 📦 Files to Create
1. \`/frontend/src/components/shared/Card.jsx\`
2. \`/frontend/src/components/shared/Card.css\`
3. \`/frontend/src/components/shared/CardDemo.jsx\`

## 🔗 Dependencies
- **Requires:** #10, #11, #12 merged
- **Blocks:** Dashboard (#17), BMAD (#22), Symbolon (#25)

Please implement and open PR."
```

---

### Issue #14 - Form Input Components
**Run after #13 is merged:**

```bash
gh issue comment 14 --body "# Agent 2: Form Input Components Implementation

## 🎯 Task Overview
Create comprehensive form input components: TextInput, Select, Checkbox, Radio, and DateInput with validation states and accessibility.

## 📋 Detailed Implementation

### 1. TextInput Component
Create: \`/frontend/src/components/shared/TextInput.jsx\`

\`\`\`javascript
import React, { forwardRef } from 'react';
import './FormInputs.css';

const TextInput = forwardRef(({ 
  label,
  id,
  name,
  type = 'text',
  placeholder,
  value,
  onChange,
  error,
  helperText,
  required = false,
  disabled = false,
  fullWidth = false,
  leftIcon,
  rightIcon,
  ...props 
}, ref) => {
  const inputId = id || name;
  
  return (
    <div className={\`form-field \${fullWidth ? 'form-field--full-width' : ''}\`}>
      {label && (
        <label htmlFor={inputId} className=\"form-label\">
          {label}
          {required && <span className=\"form-label__required\" aria-label=\"required\">*</span>}
        </label>
      )}
      
      <div className={\`input-wrapper \${error ? 'input-wrapper--error' : ''} \${disabled ? 'input-wrapper--disabled' : ''}\`}>
        {leftIcon && <span className=\"input-icon input-icon--left\">{leftIcon}</span>}
        
        <input
          ref={ref}
          id={inputId}
          name={name}
          type={type}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          required={required}
          disabled={disabled}
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={error ? \`\${inputId}-error\` : helperText ? \`\${inputId}-helper\` : undefined}
          className=\"form-input\"
          {...props}
        />
        
        {rightIcon && <span className=\"input-icon input-icon--right\">{rightIcon}</span>}
      </div>
      
      {error && (
        <span id={\`\${inputId}-error\`} className=\"form-error\" role=\"alert\">
          {error}
        </span>
      )}
      
      {helperText && !error && (
        <span id={\`\${inputId}-helper\`} className=\"form-helper\">
          {helperText}
        </span>
      )}
    </div>
  );
});

TextInput.displayName = 'TextInput';

export default TextInput;
\`\`\`

### 2. Select Component
Create: \`/frontend/src/components/shared/Select.jsx\`

\`\`\`javascript
import React, { forwardRef } from 'react';
import './FormInputs.css';

const Select = forwardRef(({ 
  label,
  id,
  name,
  value,
  onChange,
  options = [],
  placeholder = 'Select an option',
  error,
  helperText,
  required = false,
  disabled = false,
  fullWidth = false,
  ...props 
}, ref) => {
  const selectId = id || name;
  
  return (
    <div className={\`form-field \${fullWidth ? 'form-field--full-width' : ''}\`}>
      {label && (
        <label htmlFor={selectId} className=\"form-label\">
          {label}
          {required && <span className=\"form-label__required\">*</span>}
        </label>
      )}
      
      <div className={\`select-wrapper \${error ? 'select-wrapper--error' : ''} \${disabled ? 'select-wrapper--disabled' : ''}\`}>
        <select
          ref={ref}
          id={selectId}
          name={name}
          value={value}
          onChange={onChange}
          required={required}
          disabled={disabled}
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={error ? \`\${selectId}-error\` : helperText ? \`\${selectId}-helper\` : undefined}
          className=\"form-select\"
          {...props}
        >
          <option value=\"\" disabled>{placeholder}</option>
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        <span className=\"select-arrow\" aria-hidden=\"true\">▼</span>
      </div>
      
      {error && (
        <span id={\`\${selectId}-error\`} className=\"form-error\" role=\"alert\">
          {error}
        </span>
      )}
      
      {helperText && !error && (
        <span id={\`\${selectId}-helper\`} className=\"form-helper\">
          {helperText}
        </span>
      )}
    </div>
  );
});

Select.displayName = 'Select';

export default Select;
\`\`\`

### 3. Checkbox Component
Create: \`/frontend/src/components/shared/Checkbox.jsx\`

\`\`\`javascript
import React, { forwardRef } from 'react';
import './FormInputs.css';

const Checkbox = forwardRef(({ 
  label,
  id,
  name,
  checked,
  onChange,
  disabled = false,
  error,
  ...props 
}, ref) => {
  const checkboxId = id || name;
  
  return (
    <div className=\"form-field\">
      <label className={\`checkbox-label \${disabled ? 'checkbox-label--disabled' : ''} \${error ? 'checkbox-label--error' : ''}\`}>
        <input
          ref={ref}
          id={checkboxId}
          name={name}
          type=\"checkbox\"
          checked={checked}
          onChange={onChange}
          disabled={disabled}
          className=\"checkbox-input\"
          aria-invalid={error ? 'true' : 'false'}
          {...props}
        />
        <span className=\"checkbox-custom\"></span>
        <span className=\"checkbox-text\">{label}</span>
      </label>
      
      {error && (
        <span className=\"form-error\" role=\"alert\">
          {error}
        </span>
      )}
    </div>
  );
});

Checkbox.displayName = 'Checkbox';

export default Checkbox;
\`\`\`

### 4. Form Inputs Styles
Create: \`/frontend/src/components/shared/FormInputs.css\`

\`\`\`css
/* Form field container */
.form-field {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
}

.form-field--full-width {
  width: 100%;
}

/* Labels */
.form-label {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--text-primary);
  display: flex;
  gap: var(--space-1);
}

.form-label__required {
  color: var(--color-error);
}

/* Text Input */
.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background-color: var(--bg-secondary);
  border: 2px solid var(--border-color);
  border-radius: 8px;
  transition: all 0.2s ease-in-out;
}

.input-wrapper:focus-within {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(62, 75, 110, 0.1);
}

.input-wrapper--error {
  border-color: var(--color-error);
}

.input-wrapper--error:focus-within {
  box-shadow: 0 0 0 3px rgba(193, 123, 92, 0.1);
}

.input-wrapper--disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-input {
  flex: 1;
  padding: var(--space-3);
  border: none;
  background: transparent;
  font-family: var(--font-primary);
  font-size: var(--text-md);
  color: var(--text-primary);
  outline: none;
}

.form-input::placeholder {
  color: var(--text-secondary);
}

.form-input:disabled {
  cursor: not-allowed;
}

.input-icon {
  padding: 0 var(--space-3);
  color: var(--text-secondary);
  display: flex;
  align-items: center;
}

/* Select */
.select-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background-color: var(--bg-secondary);
  border: 2px solid var(--border-color);
  border-radius: 8px;
  transition: all 0.2s ease-in-out;
}

.select-wrapper:focus-within {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(62, 75, 110, 0.1);
}

.select-wrapper--error {
  border-color: var(--color-error);
}

.select-wrapper--disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-select {
  flex: 1;
  padding: var(--space-3);
  padding-right: var(--space-6);
  border: none;
  background: transparent;
  font-family: var(--font-primary);
  font-size: var(--text-md);
  color: var(--text-primary);
  outline: none;
  cursor: pointer;
  appearance: none;
}

.form-select:disabled {
  cursor: not-allowed;
}

.select-arrow {
  position: absolute;
  right: var(--space-3);
  pointer-events: none;
  color: var(--text-secondary);
  font-size: var(--text-xs);
}

/* Checkbox */
.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
  user-select: none;
}

.checkbox-label--disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.checkbox-label--error .checkbox-custom {
  border-color: var(--color-error);
}

.checkbox-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.checkbox-custom {
  width: 20px;
  height: 20px;
  border: 2px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease-in-out;
}

.checkbox-input:checked + .checkbox-custom {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
}

.checkbox-input:checked + .checkbox-custom::after {
  content: '✓';
  color: white;
  font-size: 14px;
  font-weight: bold;
}

.checkbox-input:focus-visible + .checkbox-custom {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.checkbox-text {
  font-size: var(--text-md);
  color: var(--text-primary);
}

/* Helper text and errors */
.form-helper {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}

.form-error {
  font-size: var(--text-sm);
  color: var(--color-error);
  font-weight: var(--font-medium);
}
\`\`\`

### 5. Form Demo
Create: \`/frontend/src/components/shared/FormDemo.jsx\`

\`\`\`javascript
import React, { useState } from 'react';
import TextInput from './TextInput';
import Select from './Select';
import Checkbox from './Checkbox';
import Button from './Button';

const FormDemo = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    country: '',
    subscribe: false
  });
  
  const [errors, setErrors] = useState({});

  const handleSubmit = (e) => {
    e.preventDefault();
    const newErrors = {};
    
    if (!formData.name) newErrors.name = 'Name is required';
    if (!formData.email) newErrors.email = 'Email is required';
    if (!formData.country) newErrors.country = 'Please select a country';
    
    setErrors(newErrors);
    
    if (Object.keys(newErrors).length === 0) {
      alert('Form submitted successfully!');
      console.log(formData);
    }
  };

  return (
    <div style={{ padding: 'var(--space-5)', maxWidth: '500px' }}>
      <h2>Form Components Demo</h2>
      
      <form onSubmit={handleSubmit}>
        <TextInput
          label=\"Name\"
          name=\"name\"
          placeholder=\"Enter your name\"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          error={errors.name}
          required
          fullWidth
        />

        <TextInput
          label=\"Email\"
          name=\"email\"
          type=\"email\"
          placeholder=\"your@email.com\"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          error={errors.email}
          helperText=\"We'll never share your email\"
          required
          fullWidth
        />

        <Select
          label=\"Country\"
          name=\"country\"
          value={formData.country}
          onChange={(e) => setFormData({ ...formData, country: e.target.value })}
          options={[
            { value: 'us', label: 'United States' },
            { value: 'uk', label: 'United Kingdom' },
            { value: 'ca', label: 'Canada' },
            { value: 'au', label: 'Australia' }
          ]}
          error={errors.country}
          required
          fullWidth
        />

        <Checkbox
          label=\"Subscribe to newsletter\"
          name=\"subscribe\"
          checked={formData.subscribe}
          onChange={(e) => setFormData({ ...formData, subscribe: e.target.checked })}
        />

        <div style={{ display: 'flex', gap: 'var(--space-3)', marginTop: 'var(--space-4)' }}>
          <Button type=\"submit\" variant=\"primary\">Submit</Button>
          <Button type=\"button\" variant=\"outline\" onClick={() => setFormData({ name: '', email: '', country: '', subscribe: false })}>
            Reset
          </Button>
        </div>
      </form>
    </div>
  );
};

export default FormDemo;
\`\`\`

## ✅ Acceptance Criteria
- [ ] TextInput handles all input types (text, email, password, number)
- [ ] Select dropdown works with options array
- [ ] Checkbox toggles correctly
- [ ] All components show error states
- [ ] All components are keyboard accessible
- [ ] Focus indicators visible
- [ ] Labels properly associated with inputs
- [ ] Helper text and errors announced by screen readers
- [ ] Required fields marked visually and for assistive tech
- [ ] Disabled states prevent interaction

## 📦 Files to Create
1. \`/frontend/src/components/shared/TextInput.jsx\`
2. \`/frontend/src/components/shared/Select.jsx\`
3. \`/frontend/src/components/shared/Checkbox.jsx\`
4. \`/frontend/src/components/shared/FormInputs.css\`
5. \`/frontend/src/components/shared/FormDemo.jsx\`

## 🔗 Dependencies
- **Requires:** #10-13 merged
- **Blocks:** #20 (Birth Data Form)

Please implement and open PR."
```

---

## 📋 Remaining Issues (15-25)

I'll continue generating the complete detailed instructions for all remaining issues. This will take a moment...

---

### Issue #15 - Loading Components
**Run after foundation complete (parallel with other agents):**

```bash
gh issue comment 15 --body "# Agent 3: Loading Components Implementation

## 🎯 Task Overview
Create loading indicators: Spinner, Skeleton loaders, and Progress bars for various loading states.

## 📋 Detailed Implementation

### 1. Spinner Component
Create: \`/frontend/src/components/shared/Spinner.jsx\`

\`\`\`javascript
import React from 'react';
import './Loading.css';

const Spinner = ({ size = 'md', color = 'primary', className = '' }) => {
  return (
    <div 
      className={\`spinner spinner--\${size} spinner--\${color} \${className}\`}
      role=\"status\"
      aria-label=\"Loading\"
    >
      <div className=\"spinner__circle\"></div>
      <span className=\"sr-only\">Loading...</span>
    </div>
  );
};

export default Spinner;
\`\`\`

### 2. Skeleton Component
Create: \`/frontend/src/components/shared/Skeleton.jsx\`

\`\`\`javascript
import React from 'react';
import './Loading.css';

const Skeleton = ({ 
  width = '100%',
  height = '20px',
  variant = 'text', // text | circular | rectangular
  className = '',
  ...props 
}) => {
  return (
    <div
      className={\`skeleton skeleton--\${variant} \${className}\`}
      style={{ width, height }}
      aria-busy=\"true\"
      aria-label=\"Loading content\"
      {...props}
    />
  );
};

export default Skeleton;
\`\`\`

### 3. Loading Styles
Create: \`/frontend/src/components/shared/Loading.css\`

\`\`\`css
/* Spinner */
.spinner {
  display: inline-block;
  position: relative;
}

.spinner--sm {
  width: 16px;
  height: 16px;
}

.spinner--md {
  width: 32px;
  height: 32px;
}

.spinner--lg {
  width: 48px;
  height: 48px;
}

.spinner__circle {
  width: 100%;
  height: 100%;
  border: 3px solid transparent;
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.spinner--primary .spinner__circle {
  border-top-color: var(--color-primary);
}

.spinner--secondary .spinner__circle {
  border-top-color: var(--color-secondary);
}

.spinner--white .spinner__circle {
  border-top-color: white;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Skeleton */
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-neutral-200) 0%,
    var(--color-neutral-100) 50%,
    var(--color-neutral-200) 100%
  );
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  border-radius: 4px;
}

[data-theme=\"dark\"] .skeleton {
  background: linear-gradient(
    90deg,
    var(--color-neutral-800) 0%,
    var(--color-neutral-700) 50%,
    var(--color-neutral-800) 100%
  );
}

.skeleton--circular {
  border-radius: 50%;
}

.skeleton--rectangular {
  border-radius: 8px;
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Screen reader only */
.sr-only {
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
\`\`\`

## ✅ Acceptance Criteria
- [ ] Spinner renders in 3 sizes (sm, md, lg)
- [ ] Spinner has color variants
- [ ] Skeleton supports text, circular, rectangular variants
- [ ] Animations are smooth (60fps)
- [ ] Loading states announced to screen readers
- [ ] Respects prefers-reduced-motion

## 📦 Files
1. \`/frontend/src/components/shared/Spinner.jsx\`
2. \`/frontend/src/components/shared/Skeleton.jsx\`
3. \`/frontend/src/components/shared/Loading.css\`

## 🔗 Dependencies
Requires: #10-13 merged

Please implement and open PR."
```

---

### Issue #16 - Navigation Bar
**Run after foundation complete:**

```bash
gh issue comment 16 --body "# Agent 4: Navigation Bar Implementation

## 🎯 Task Overview
Create responsive navigation bar with mobile menu, logo, and theme toggle integration.

## 📋 Implementation

### 1. Navigation Component
Create: \`/frontend/src/components/layout/Navigation.jsx\`

\`\`\`javascript
import React, { useState } from 'react';
import ThemeToggle from '../shared/ThemeToggle';
import './Navigation.css';

const Navigation = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { label: 'Dashboard', path: '/' },
    { label: 'Chart', path: '/chart' },
    { label: 'BMAD', path: '/bmad' },
    { label: 'Symbolon', path: '/symbolon' }
  ];

  return (
    <nav className=\"nav\" role=\"navigation\" aria-label=\"Main navigation\">
      <div className=\"nav__container\">
        <div className=\"nav__brand\">
          <span className=\"nav__logo\">✨ Astrology Synthesis</span>
        </div>

        <button
          className=\"nav__toggle\"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-expanded={mobileMenuOpen}
          aria-label=\"Toggle navigation menu\"
        >
          <span className=\"nav__toggle-icon\">{mobileMenuOpen ? '✕' : '☰'}</span>
        </button>

        <div className={\`nav__menu \${mobileMenuOpen ? 'nav__menu--open' : ''}\`}>
          <ul className=\"nav__list\">
            {navLinks.map((link) => (
              <li key={link.path} className=\"nav__item\">
                <a 
                  href={link.path} 
                  className=\"nav__link\"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
          
          <div className=\"nav__actions\">
            <ThemeToggle />
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
\`\`\`

### 2. Navigation Styles
Create: \`/frontend/src/components/layout/Navigation.css\`

\`\`\`css
.nav {
  background-color: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav__container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-3) var(--space-4);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav__brand {
  display: flex;
  align-items: center;
}

.nav__logo {
  font-size: var(--text-xl);
  font-weight: var(--font-bold);
  color: var(--color-primary);
}

.nav__toggle {
  display: none;
  background: none;
  border: none;
  font-size: var(--text-2xl);
  color: var(--text-primary);
  cursor: pointer;
  padding: var(--space-2);
}

.nav__menu {
  display: flex;
  align-items: center;
  gap: var(--space-5);
}

.nav__list {
  display: flex;
  gap: var(--space-4);
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav__link {
  color: var(--text-primary);
  text-decoration: none;
  font-weight: var(--font-medium);
  padding: var(--space-2) var(--space-3);
  border-radius: 6px;
  transition: all 0.2s ease-in-out;
}

.nav__link:hover {
  background-color: var(--color-primary);
  color: white;
}

.nav__link:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.nav__actions {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

/* Mobile */
@media (max-width: 768px) {
  .nav__toggle {
    display: block;
  }

  .nav__menu {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background-color: var(--bg-secondary);
    border-bottom: 1px solid var(--border-color);
    flex-direction: column;
    align-items: stretch;
    gap: 0;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease-in-out;
  }

  .nav__menu--open {
    max-height: 400px;
  }

  .nav__list {
    flex-direction: column;
    gap: 0;
    width: 100%;
  }

  .nav__link {
    display: block;
    padding: var(--space-3) var(--space-4);
    border-radius: 0;
  }

  .nav__actions {
    padding: var(--space-3) var(--space-4);
    border-top: 1px solid var(--border-color);
  }
}
\`\`\`

## ✅ Acceptance Criteria
- [ ] Navigation renders on all pages
- [ ] Mobile menu toggles correctly
- [ ] Theme toggle integrated
- [ ] All links keyboard accessible
- [ ] Focus indicators visible
- [ ] Sticky positioning works
- [ ] Responsive (mobile/desktop)

## 📦 Files
1. \`/frontend/src/components/layout/Navigation.jsx\`
2. \`/frontend/src/components/layout/Navigation.css\`

## 🔗 Dependencies
Requires: #10 (ThemeToggle)

Please implement and open PR."
```

