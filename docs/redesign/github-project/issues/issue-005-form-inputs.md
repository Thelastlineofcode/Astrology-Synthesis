---
title: "Design Form Input Components (Text, Select, Checkbox)"
labels: ["component:design-system", "P0-Critical", "forms"]
assignees: []
milestone: "Milestone 1: Foundation"
---

## 🎯 Objective

Build accessible, reusable form input components (TextInput, Select, Checkbox, Radio) with validation states and proper labeling.

## 📋 Description

Forms are used for birth data entry, settings, and journal creation. Create consistent, accessible form components that handle validation, error states, and proper ARIA attributes.

## 🔗 References

- **Design Artifact**: `COMPONENT_STRUCTURE.md` (Shared Components - Forms)
- **Design Artifact**: `UX_COPY_GUIDE.md` (Form labels and validation messages)
- **Guide**: `AI_COPILOT_GUIDE.md` - Form Accessibility

## ✅ Acceptance Criteria

- [ ] TextInput component with label, placeholder, error state
- [ ] Select dropdown with label and error state
- [ ] Checkbox with label and indeterminate state
- [ ] Radio button group component
- [ ] All inputs have proper `<label>` associations
- [ ] Error messages displayed below inputs
- [ ] Required field indicator (asterisk)
- [ ] Disabled state styling
- [ ] Focus states clearly visible
- [ ] Validation states: default, valid, error
- [ ] Helper text support

## 💻 Implementation Notes

### TextInput Component

```jsx
// /frontend/src/components/shared/TextInput.jsx
import React, { useId } from 'react';
import './FormInputs.css';

const TextInput = ({
  label,
  type = 'text',
  value,
  onChange,
  placeholder,
  error,
  helperText,
  required = false,
  disabled = false,
  className = '',
  ...props
}) => {
  const id = useId();
  const errorId = `${id}-error`;
  const helperId = `${id}-helper`;
  
  return (
    <div className={`form-group ${error ? 'form-group--error' : ''} ${className}`}>
      <label htmlFor={id} className="form-label">
        {label}
        {required && <span className="form-label__required" aria-label="required">*</span>}
      </label>
      
      <input
        id={id}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        disabled={disabled}
        required={required}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={error ? errorId : helperText ? helperId : undefined}
        className="form-input"
        {...props}
      />
      
      {helperText && !error && (
        <p id={helperId} className="form-helper-text">{helperText}</p>
      )}
      
      {error && (
        <p id={errorId} className="form-error-text" role="alert">
          {error}
        </p>
      )}
    </div>
  );
};

export default TextInput;
```

### Select Component

```jsx
// /frontend/src/components/shared/Select.jsx
import React, { useId } from 'react';
import './FormInputs.css';

const Select = ({
  label,
  value,
  onChange,
  options = [],
  error,
  required = false,
  disabled = false,
  placeholder,
  className = '',
  ...props
}) => {
  const id = useId();
  const errorId = `${id}-error`;
  
  return (
    <div className={`form-group ${error ? 'form-group--error' : ''} ${className}`}>
      <label htmlFor={id} className="form-label">
        {label}
        {required && <span className="form-label__required" aria-label="required">*</span>}
      </label>
      
      <select
        id={id}
        value={value}
        onChange={onChange}
        disabled={disabled}
        required={required}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={error ? errorId : undefined}
        className="form-select"
        {...props}
      >
        {placeholder && <option value="">{placeholder}</option>}
        {options.map(option => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      
      {error && (
        <p id={errorId} className="form-error-text" role="alert">
          {error}
        </p>
      )}
    </div>
  );
};

export default Select;
```

### Checkbox Component

```jsx
// /frontend/src/components/shared/Checkbox.jsx
import React, { useId } from 'react';
import './FormInputs.css';

const Checkbox = ({
  label,
  checked,
  onChange,
  disabled = false,
  indeterminate = false,
  className = '',
  ...props
}) => {
  const id = useId();
  const ref = React.useRef(null);
  
  React.useEffect(() => {
    if (ref.current) {
      ref.current.indeterminate = indeterminate;
    }
  }, [indeterminate]);
  
  return (
    <div className={`form-checkbox ${className}`}>
      <input
        ref={ref}
        id={id}
        type="checkbox"
        checked={checked}
        onChange={onChange}
        disabled={disabled}
        className="form-checkbox__input"
        {...props}
      />
      <label htmlFor={id} className="form-checkbox__label">
        {label}
      </label>
    </div>
  );
};

export default Checkbox;
```

### Form Styles

```css
/* /frontend/src/components/shared/FormInputs.css */
.form-group {
  margin-bottom: var(--space-5);
}

.form-label {
  display: block;
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.form-label__required {
  color: var(--color-error);
  margin-left: var(--space-1);
}

/* Text Input */
.form-input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  font-size: var(--font-size-body);
  font-family: var(--font-primary);
  color: var(--text-primary);
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  transition: all 150ms ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(62, 75, 110, 0.1);
}

.form-input:disabled {
  background: var(--bg-disabled);
  cursor: not-allowed;
  opacity: 0.6;
}

.form-input::placeholder {
  color: var(--text-tertiary);
}

/* Error state */
.form-group--error .form-input,
.form-group--error .form-select {
  border-color: var(--color-error);
}

.form-group--error .form-input:focus,
.form-group--error .form-select:focus {
  box-shadow: 0 0 0 3px rgba(193, 123, 92, 0.1);
}

/* Helper/Error text */
.form-helper-text,
.form-error-text {
  margin-top: var(--space-2);
  font-size: var(--font-size-small);
}

.form-helper-text {
  color: var(--text-secondary);
}

.form-error-text {
  color: var(--color-error);
}

/* Select */
.form-select {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  font-size: var(--font-size-body);
  font-family: var(--font-primary);
  color: var(--text-primary);
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 150ms ease;
}

.form-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(62, 75, 110, 0.1);
}

/* Checkbox */
.form-checkbox {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.form-checkbox__input {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: var(--color-primary);
}

.form-checkbox__label {
  font-size: var(--font-size-body);
  color: var(--text-primary);
  cursor: pointer;
  user-select: none;
}

.form-checkbox__input:disabled {
  cursor: not-allowed;
}

.form-checkbox__input:disabled + .form-checkbox__label {
  opacity: 0.6;
  cursor: not-allowed;
}
```

## 🧪 Testing Checklist

- [ ] All inputs render with labels
- [ ] Required asterisk appears when `required={true}`
- [ ] Error messages display correctly
- [ ] Helper text shows when provided
- [ ] Focus states clearly visible
- [ ] Disabled state prevents interaction
- [ ] Validation states work (default, error)
- [ ] Checkbox indeterminate state works
- [ ] Select dropdown opens/closes correctly
- [ ] Keyboard navigation works (tab, arrow keys for select)
- [ ] Screen reader announces labels and errors

## 🔍 Accessibility Requirements

- [ ] All inputs have associated `<label>` (not placeholder-only)
- [ ] Required fields have `required` attribute and visual indicator
- [ ] Error messages have `role="alert"` for live announcement
- [ ] Inputs have `aria-invalid` when error state
- [ ] Error/helper text linked via `aria-describedby`
- [ ] Focus indicators visible (not suppressed)
- [ ] Color not sole indicator of validation state (icons + text)

## 📦 Files to Create/Modify

- `frontend/src/components/shared/TextInput.jsx` (create)
- `frontend/src/components/shared/Select.jsx` (create)
- `frontend/src/components/shared/Checkbox.jsx` (create)
- `frontend/src/components/shared/Radio.jsx` (create - similar to Checkbox)
- `frontend/src/components/shared/FormInputs.css` (create)
- `frontend/src/components/shared/FormInputs.test.jsx` (create)

## 🔗 Dependencies

- Issue #1 (CSS Variables)
- Issue #2 (Typography System)

## 📝 Additional Notes

- Use `useId()` hook for unique IDs (React 18+)
- Consider adding DatePicker component (future)
- Consider adding TimePicker component (future)
- Test with browser autofill
- Ensure native HTML5 validation works

---

**Priority**: P0 (Critical)  
**Estimated Effort**: 6 hours  
**Assignee**: TBD  
**Epic**: Epic 1 - Design System Foundation
