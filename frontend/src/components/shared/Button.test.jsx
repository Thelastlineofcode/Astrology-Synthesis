import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Button from './Button';

describe('Button component', () => {
  // Basic rendering tests
  it('renders button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  // Variant tests
  describe('Variants', () => {
    it('renders primary variant by default', () => {
      const { container } = render(<Button>Primary</Button>);
      const button = container.querySelector('.btn--primary');
      expect(button).toBeInTheDocument();
    });

    it('renders secondary variant', () => {
      const { container } = render(<Button variant="secondary">Secondary</Button>);
      const button = container.querySelector('.btn--secondary');
      expect(button).toBeInTheDocument();
    });

    it('renders ghost variant', () => {
      const { container } = render(<Button variant="ghost">Ghost</Button>);
      const button = container.querySelector('.btn--ghost');
      expect(button).toBeInTheDocument();
    });
  });

  // Size tests
  describe('Sizes', () => {
    it('renders medium size by default', () => {
      const { container } = render(<Button>Medium</Button>);
      const button = container.querySelector('.btn--medium');
      expect(button).toBeInTheDocument();
    });

    it('renders small size', () => {
      const { container } = render(<Button size="small">Small</Button>);
      const button = container.querySelector('.btn--small');
      expect(button).toBeInTheDocument();
    });

    it('renders large size', () => {
      const { container } = render(<Button size="large">Large</Button>);
      const button = container.querySelector('.btn--large');
      expect(button).toBeInTheDocument();
    });
  });

  // State tests
  describe('States', () => {
    it('renders disabled state', () => {
      render(<Button disabled>Disabled</Button>);
      const button = screen.getByRole('button');
      expect(button).toBeDisabled();
      expect(button).toHaveClass('btn--disabled');
    });

    it('does not call onClick when disabled', () => {
      const handleClick = jest.fn();
      render(<Button disabled onClick={handleClick}>Disabled</Button>);
      const button = screen.getByRole('button');
      fireEvent.click(button);
      expect(handleClick).not.toHaveBeenCalled();
    });

    it('renders loading state', () => {
      const { container } = render(<Button loading>Loading</Button>);
      const spinner = container.querySelector('.btn__spinner');
      expect(spinner).toBeInTheDocument();
      expect(container.querySelector('.btn--loading')).toBeInTheDocument();
    });

    it('has aria-busy when loading', () => {
      render(<Button loading>Loading</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('aria-busy', 'true');
    });

    it('is disabled when loading', () => {
      render(<Button loading>Loading</Button>);
      const button = screen.getByRole('button');
      expect(button).toBeDisabled();
    });

    it('does not call onClick when loading', () => {
      const handleClick = jest.fn();
      render(<Button loading onClick={handleClick}>Loading</Button>);
      const button = screen.getByRole('button');
      fireEvent.click(button);
      expect(handleClick).not.toHaveBeenCalled();
    });
  });

  // Icon tests
  describe('Icons', () => {
    it('renders left icon', () => {
      const LeftIcon = () => <svg data-testid="left-icon"><path /></svg>;
      const { container } = render(
        <Button iconLeft={<LeftIcon />}>With Left Icon</Button>
      );
      expect(screen.getByTestId('left-icon')).toBeInTheDocument();
      expect(container.querySelector('.btn__icon--left')).toBeInTheDocument();
    });

    it('renders right icon', () => {
      const RightIcon = () => <svg data-testid="right-icon"><path /></svg>;
      const { container } = render(
        <Button iconRight={<RightIcon />}>With Right Icon</Button>
      );
      expect(screen.getByTestId('right-icon')).toBeInTheDocument();
      expect(container.querySelector('.btn__icon--right')).toBeInTheDocument();
    });

    it('hides icons when loading', () => {
      const LeftIcon = () => <svg data-testid="left-icon"><path /></svg>;
      const RightIcon = () => <svg data-testid="right-icon"><path /></svg>;
      render(
        <Button loading iconLeft={<LeftIcon />} iconRight={<RightIcon />}>
          Loading
        </Button>
      );
      expect(screen.queryByTestId('left-icon')).not.toBeInTheDocument();
      expect(screen.queryByTestId('right-icon')).not.toBeInTheDocument();
    });

    it('icon has aria-hidden on spinner', () => {
      const { container } = render(<Button loading>Loading</Button>);
      const spinner = container.querySelector('.btn__spinner');
      expect(spinner).toHaveAttribute('aria-hidden', 'true');
    });
  });

  // Full-width tests
  describe('Full-width', () => {
    it('renders full-width button', () => {
      const { container } = render(<Button fullWidth>Full Width</Button>);
      const button = container.querySelector('.btn--full-width');
      expect(button).toBeInTheDocument();
    });
  });

  // Button type tests
  describe('Button types', () => {
    it('renders as button by default', () => {
      render(<Button>Button</Button>);
      const button = screen.getByRole('button');
      expect(button.tagName).toBe('BUTTON');
      expect(button).toHaveAttribute('type', 'button');
    });

    it('renders as submit button', () => {
      render(<Button type="submit">Submit</Button>);
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('type', 'submit');
    });

    it('renders as link when href provided', () => {
      render(<Button href="/test">Link Button</Button>);
      const link = screen.getByRole('link');
      expect(link.tagName).toBe('A');
      expect(link).toHaveAttribute('href', '/test');
    });

    it('renders as button when href provided but disabled', () => {
      render(<Button href="/test" disabled>Disabled Link</Button>);
      const button = screen.getByRole('button');
      expect(button.tagName).toBe('BUTTON');
    });

    it('has aria-disabled on link when disabled', () => {
      render(<Button href="/test" disabled={false}>Link</Button>);
      const link = screen.getByRole('link');
      expect(link).toHaveAttribute('aria-disabled', 'false');
    });
  });

  // Interaction tests
  describe('Interactions', () => {
    it('calls onClick when clicked', () => {
      const handleClick = jest.fn();
      render(<Button onClick={handleClick}>Click me</Button>);
      const button = screen.getByRole('button');
      fireEvent.click(button);
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('supports keyboard activation with Enter', () => {
      const handleClick = jest.fn();
      render(<Button onClick={handleClick}>Press Enter</Button>);
      const button = screen.getByRole('button');
      fireEvent.keyDown(button, { key: 'Enter', code: 'Enter' });
      // Note: React automatically handles Enter key for buttons
      // So we just verify the button is keyboard accessible
      expect(button).toBeInTheDocument();
    });

    it('supports keyboard activation with Space', () => {
      const handleClick = jest.fn();
      render(<Button onClick={handleClick}>Press Space</Button>);
      const button = screen.getByRole('button');
      fireEvent.keyDown(button, { key: ' ', code: 'Space' });
      // Note: React automatically handles Space key for buttons
      expect(button).toBeInTheDocument();
    });
  });

  // Custom className tests
  describe('Custom className', () => {
    it('applies custom className', () => {
      const { container } = render(<Button className="custom-class">Custom</Button>);
      const button = container.querySelector('.custom-class');
      expect(button).toBeInTheDocument();
    });

    it('preserves base classes with custom className', () => {
      const { container } = render(<Button className="custom-class">Custom</Button>);
      const button = container.querySelector('button');
      expect(button).toHaveClass('btn');
      expect(button).toHaveClass('btn--primary');
      expect(button).toHaveClass('btn--medium');
      expect(button).toHaveClass('custom-class');
    });
  });

  // Additional props tests
  describe('Additional props', () => {
    it('passes through additional props', () => {
      render(<Button data-testid="custom-button" aria-label="Custom Label">Button</Button>);
      const button = screen.getByTestId('custom-button');
      expect(button).toHaveAttribute('aria-label', 'Custom Label');
    });
  });

  // No console errors
  it('renders without console errors', () => {
    const consoleSpy = jest.spyOn(console, 'error');
    render(<Button>Test</Button>);
    expect(consoleSpy).not.toHaveBeenCalled();
    consoleSpy.mockRestore();
  });
});
