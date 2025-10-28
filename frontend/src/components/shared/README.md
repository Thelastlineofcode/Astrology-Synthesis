# Button Component

A flexible, accessible Button component with multiple variants, sizes, and states.

## Usage

```jsx
import Button from './components/shared/Button';

// Basic usage
<Button>Click me</Button>

// Different variants
<Button variant="primary">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="ghost">Ghost</Button>

// Different sizes
<Button size="small">Small</Button>
<Button size="medium">Medium</Button>
<Button size="large">Large</Button>

// States
<Button disabled>Disabled</Button>
<Button loading>Loading...</Button>

// With icons
<Button iconLeft={<PlusIcon />}>Add Item</Button>
<Button iconRight={<ArrowIcon />}>Next</Button>

// Full width
<Button fullWidth>Full Width Button</Button>

// As a link
<Button href="/path">Link Button</Button>

// Custom className
<Button className="custom-class">Custom</Button>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | - | Button text content |
| `variant` | `'primary' \| 'secondary' \| 'ghost'` | `'primary'` | Visual style variant |
| `size` | `'small' \| 'medium' \| 'large'` | `'medium'` | Button size |
| `disabled` | `boolean` | `false` | Disables the button |
| `loading` | `boolean` | `false` | Shows loading spinner |
| `fullWidth` | `boolean` | `false` | Makes button full width |
| `iconLeft` | `ReactNode` | - | Icon to display on the left |
| `iconRight` | `ReactNode` | - | Icon to display on the right |
| `onClick` | `function` | - | Click handler |
| `type` | `'button' \| 'submit' \| 'reset'` | `'button'` | Button type |
| `href` | `string` | - | If provided, renders as anchor tag |
| `className` | `string` | `''` | Additional CSS classes |

## Accessibility

- ✅ Keyboard accessible (Tab, Enter, Space)
- ✅ Clear focus indicator (2px outline, 2px offset)
- ✅ ARIA attributes (`aria-busy`, `aria-disabled`)
- ✅ WCAG 2.1 AA contrast compliant
- ✅ Minimum 44px touch target

## Examples

### Icon-only button
```jsx
<Button aria-label="Add new item" iconLeft={<PlusIcon />} />
```

### Form submit button
```jsx
<Button type="submit" variant="primary">
  Submit Form
</Button>
```

### Loading button
```jsx
const [isLoading, setIsLoading] = useState(false);

<Button loading={isLoading} onClick={handleSubmit}>
  {isLoading ? 'Submitting...' : 'Submit'}
</Button>
```

## CSS Variables

The component uses CSS variables with fallbacks:

- `--color-primary` (default: #667eea)
- `--color-primary-dark` (default: #5568d3)
- `--color-neutral-light` (default: #ffffff)
- `--bg-secondary` (default: #f7fafc)
- `--bg-hover` (default: #edf2f7)
- `--text-primary` (default: #2d3748)
- `--border-color` (default: #cbd5e0)
- `--space-2` through `--space-6` (default: 8px, 16px, 24px, 32px, 48px)
- `--font-primary` (default: system fonts)
- `--font-weight-medium` (default: 500)
- `--font-size-small`, `--font-size-body`, `--font-size-h4`

## Testing

Run tests with:
```bash
npm test -- Button.test.jsx
```

30 comprehensive tests covering:
- All variants and sizes
- Disabled and loading states
- Icon rendering
- Button vs anchor rendering
- Keyboard accessibility
- ARIA attributes
- Click handlers

## Demo

View the interactive demo:
```jsx
import ButtonDemo from './components/shared/ButtonDemo';
```
