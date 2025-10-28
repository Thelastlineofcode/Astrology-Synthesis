# Form Input Components

Accessible, reusable form input components with validation states and proper ARIA attributes.

## Components

### TextInput
Text input field with label, validation, and helper text support.

**Props:**
- `label` (string, required) - Label text for the input
- `type` (string, default: 'text') - HTML input type (text, email, password, etc.)
- `value` (string, required) - Input value
- `onChange` (function, required) - Change handler
- `placeholder` (string) - Placeholder text
- `error` (string) - Error message to display
- `helperText` (string) - Helper text to display below input
- `required` (boolean, default: false) - Mark field as required
- `disabled` (boolean, default: false) - Disable the input
- `className` (string) - Additional CSS classes

**Example:**
```jsx
import { TextInput } from './components/shared';

<TextInput
  label="Email Address"
  type="email"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  placeholder="you@example.com"
  error={emailError}
  helperText="We'll never share your email"
  required
/>
```

### Select
Dropdown select component with label and validation.

**Props:**
- `label` (string, required) - Label text for the select
- `value` (string, required) - Selected value
- `onChange` (function, required) - Change handler
- `options` (array, required) - Array of { value, label } objects
- `placeholder` (string) - Placeholder option text
- `error` (string) - Error message to display
- `required` (boolean, default: false) - Mark field as required
- `disabled` (boolean, default: false) - Disable the select
- `className` (string) - Additional CSS classes

**Example:**
```jsx
import { Select } from './components/shared';

const countries = [
  { value: 'us', label: 'United States' },
  { value: 'uk', label: 'United Kingdom' },
  { value: 'ca', label: 'Canada' },
];

<Select
  label="Country"
  value={country}
  onChange={(e) => setCountry(e.target.value)}
  options={countries}
  placeholder="Select your country"
  error={countryError}
  required
/>
```

### Checkbox
Checkbox input with label and indeterminate state support.

**Props:**
- `label` (string, required) - Label text for the checkbox
- `checked` (boolean, required) - Checked state
- `onChange` (function, required) - Change handler
- `disabled` (boolean, default: false) - Disable the checkbox
- `indeterminate` (boolean, default: false) - Set indeterminate state
- `className` (string) - Additional CSS classes

**Example:**
```jsx
import { Checkbox } from './components/shared';

<Checkbox
  label="I accept the terms and conditions"
  checked={acceptTerms}
  onChange={(e) => setAcceptTerms(e.target.checked)}
/>
```

### Radio
Individual radio button with label.

**Props:**
- `label` (string, required) - Label text for the radio button
- `name` (string, required) - Radio group name
- `value` (string, required) - Radio button value
- `checked` (boolean, required) - Checked state
- `onChange` (function, required) - Change handler
- `disabled` (boolean, default: false) - Disable the radio button
- `className` (string) - Additional CSS classes

### RadioGroup
Radio button group component with label and validation.

**Props:**
- `label` (string, required) - Label text for the radio group
- `name` (string, required) - Radio group name
- `options` (array, required) - Array of { value, label, disabled? } objects
- `value` (string, required) - Selected value
- `onChange` (function, required) - Change handler
- `error` (string) - Error message to display
- `required` (boolean, default: false) - Mark field as required
- `className` (string) - Additional CSS classes

**Example:**
```jsx
import { RadioGroup } from './components/shared';

const genderOptions = [
  { value: 'male', label: 'Male' },
  { value: 'female', label: 'Female' },
  { value: 'other', label: 'Other' },
];

<RadioGroup
  label="Gender"
  name="gender"
  options={genderOptions}
  value={gender}
  onChange={(e) => setGender(e.target.value)}
  error={genderError}
  required
/>
```

## Accessibility Features

All components include proper accessibility support:

- ✅ Associated labels using unique IDs (via `useId()` hook)
- ✅ `aria-invalid` attribute for error states
- ✅ `aria-describedby` linking to error/helper text
- ✅ `role="alert"` on error messages for screen reader announcements
- ✅ Required field indicators with `aria-label="required"`
- ✅ Keyboard navigation support
- ✅ Clear focus states
- ✅ Proper semantic HTML

## Validation States

Components support three validation states:

1. **Default** - Normal state, no validation feedback
2. **Error** - Red border, error message displayed with `role="alert"`
3. **Valid** - Can be implemented by checking if value is present and no error

## CSS Variables

Components use CSS variables for theming. Default values are provided as fallbacks:

```css
--color-primary: #3E4B6E
--color-error: #C17B5C
--text-primary: #2D3142
--text-secondary: rgba(62, 75, 110, 0.7)
--bg-primary: #F5F3EE
--bg-disabled: #E8E4DB
--border-color: rgba(165, 184, 164, 0.3)
--space-1: 4px
--space-2: 8px
--space-3: 16px
--space-4: 24px
--space-5: 32px
--font-size-small: 14px
--font-size-body: 16px
--font-weight-medium: 500
```

## BEM Naming Convention

All CSS classes follow BEM (Block Element Modifier) naming:

- **Block**: `.form-group`, `.form-checkbox`, `.form-radio-group`
- **Element**: `.form-label__required`, `.form-checkbox__input`
- **Modifier**: `.form-group--error`, `.form-radio-group--error`

## Testing

All components have comprehensive test coverage including:

- Rendering with proper labels
- Required field indicators
- Error and helper text display
- User interactions (onChange handlers)
- Disabled states
- ARIA attributes
- Accessibility features

Run tests with:
```bash
npm test FormInputs.test.jsx
```

## Example Usage

See `FormInputsExample.jsx` for a complete example demonstrating all components with state management and validation.

## Dependencies

- React 18+ (uses `useId()` hook)
- No external UI libraries required
- Works with CSS custom properties

## Browser Support

Compatible with all modern browsers that support:
- CSS custom properties (CSS variables)
- React 18+ features
- HTML5 form elements
