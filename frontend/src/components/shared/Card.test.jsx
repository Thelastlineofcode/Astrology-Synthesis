import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Card from './Card';

describe('Card component', () => {
  it('renders children content', () => {
    render(<Card>Test Content</Card>);
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  describe('Variants', () => {
    it('renders default variant', () => {
      const { container } = render(<Card variant="default">Content</Card>);
      expect(container.firstChild).toHaveClass('card--default');
    });

    it('renders elevated variant', () => {
      const { container } = render(<Card variant="elevated">Content</Card>);
      expect(container.firstChild).toHaveClass('card--elevated');
    });

    it('renders outlined variant', () => {
      const { container } = render(<Card variant="outlined">Content</Card>);
      expect(container.firstChild).toHaveClass('card--outlined');
    });

    it('uses default variant when no variant specified', () => {
      const { container } = render(<Card>Content</Card>);
      expect(container.firstChild).toHaveClass('card--default');
    });
  });

  describe('Padding Options', () => {
    it('applies none padding', () => {
      const { container } = render(<Card padding="none">Content</Card>);
      expect(container.firstChild).toHaveClass('card--padding-none');
    });

    it('applies small padding', () => {
      const { container } = render(<Card padding="small">Content</Card>);
      expect(container.firstChild).toHaveClass('card--padding-small');
    });

    it('applies medium padding', () => {
      const { container } = render(<Card padding="medium">Content</Card>);
      expect(container.firstChild).toHaveClass('card--padding-medium');
    });

    it('applies large padding', () => {
      const { container } = render(<Card padding="large">Content</Card>);
      expect(container.firstChild).toHaveClass('card--padding-large');
    });

    it('uses medium padding as default', () => {
      const { container } = render(<Card>Content</Card>);
      expect(container.firstChild).toHaveClass('card--padding-medium');
    });
  });

  describe('Header and Footer', () => {
    it('renders header when provided', () => {
      render(<Card header={<span>Header Content</span>}>Body</Card>);
      expect(screen.getByText('Header Content')).toBeInTheDocument();
    });

    it('renders footer when provided', () => {
      render(<Card footer={<span>Footer Content</span>}>Body</Card>);
      expect(screen.getByText('Footer Content')).toBeInTheDocument();
    });

    it('renders both header and footer', () => {
      render(
        <Card 
          header={<span>Header</span>} 
          footer={<span>Footer</span>}
        >
          Body
        </Card>
      );
      expect(screen.getByText('Header')).toBeInTheDocument();
      expect(screen.getByText('Footer')).toBeInTheDocument();
      expect(screen.getByText('Body')).toBeInTheDocument();
    });

    it('does not render header div when header not provided', () => {
      const { container } = render(<Card>Content</Card>);
      expect(container.querySelector('.card__header')).not.toBeInTheDocument();
    });

    it('does not render footer div when footer not provided', () => {
      const { container } = render(<Card>Content</Card>);
      expect(container.querySelector('.card__footer')).not.toBeInTheDocument();
    });
  });

  describe('Interactive States', () => {
    it('applies hoverable class when hoverable prop is true', () => {
      const { container } = render(<Card hoverable>Content</Card>);
      expect(container.firstChild).toHaveClass('card--hoverable');
    });

    it('does not apply hoverable class by default', () => {
      const { container } = render(<Card>Content</Card>);
      expect(container.firstChild).not.toHaveClass('card--hoverable');
    });

    it('applies clickable class when onClick is provided', () => {
      const handleClick = jest.fn();
      const { container } = render(<Card onClick={handleClick}>Content</Card>);
      expect(container.firstChild).toHaveClass('card--clickable');
    });

    it('calls onClick when card is clicked', () => {
      const handleClick = jest.fn();
      const { container } = render(<Card onClick={handleClick}>Content</Card>);
      fireEvent.click(container.firstChild);
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('does not call onClick when card is not clickable', () => {
      const handleClick = jest.fn();
      const { container } = render(<Card>Content</Card>);
      fireEvent.click(container.firstChild);
      expect(handleClick).not.toHaveBeenCalled();
    });
  });

  describe('Accessibility', () => {
    it('has role="button" when clickable', () => {
      const handleClick = jest.fn();
      const { container } = render(<Card onClick={handleClick}>Content</Card>);
      expect(container.firstChild).toHaveAttribute('role', 'button');
    });

    it('does not have role="button" when not clickable', () => {
      const { container } = render(<Card>Content</Card>);
      expect(container.firstChild).not.toHaveAttribute('role', 'button');
    });

    it('has tabIndex="0" when clickable', () => {
      const handleClick = jest.fn();
      const { container } = render(<Card onClick={handleClick}>Content</Card>);
      expect(container.firstChild).toHaveAttribute('tabindex', '0');
    });

    it('does not have tabIndex when not clickable', () => {
      const { container } = render(<Card>Content</Card>);
      expect(container.firstChild).not.toHaveAttribute('tabindex');
    });

    it('triggers onClick on Enter key press', () => {
      const handleClick = jest.fn();
      const { container } = render(<Card onClick={handleClick}>Content</Card>);
      fireEvent.keyDown(container.firstChild, { key: 'Enter' });
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('triggers onClick on Space key press', () => {
      const handleClick = jest.fn();
      const { container } = render(<Card onClick={handleClick}>Content</Card>);
      fireEvent.keyDown(container.firstChild, { key: ' ' });
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('does not trigger onClick on other key presses', () => {
      const handleClick = jest.fn();
      const { container } = render(<Card onClick={handleClick}>Content</Card>);
      fireEvent.keyDown(container.firstChild, { key: 'a' });
      expect(handleClick).not.toHaveBeenCalled();
    });

    it('prevents default on Space key to avoid page scroll', () => {
      const handleClick = jest.fn();
      const { container } = render(<Card onClick={handleClick}>Content</Card>);
      const event = new KeyboardEvent('keydown', { key: ' ', bubbles: true });
      const preventDefaultSpy = jest.spyOn(event, 'preventDefault');
      fireEvent(container.firstChild, event);
      expect(preventDefaultSpy).toHaveBeenCalled();
    });

    it('does not trigger keyboard events when not clickable', () => {
      const handleClick = jest.fn();
      const { container } = render(<Card>Content</Card>);
      fireEvent.keyDown(container.firstChild, { key: 'Enter' });
      fireEvent.keyDown(container.firstChild, { key: ' ' });
      expect(handleClick).not.toHaveBeenCalled();
    });
  });

  describe('Custom Props', () => {
    it('applies custom className', () => {
      const { container } = render(<Card className="custom-class">Content</Card>);
      expect(container.firstChild).toHaveClass('custom-class');
      expect(container.firstChild).toHaveClass('card');
    });

    it('passes through additional props', () => {
      const { container } = render(
        <Card data-testid="custom-card" aria-label="Custom Card">
          Content
        </Card>
      );
      expect(container.firstChild).toHaveAttribute('data-testid', 'custom-card');
      expect(container.firstChild).toHaveAttribute('aria-label', 'Custom Card');
    });
  });

  describe('Complex Content', () => {
    it('renders nested components', () => {
      render(
        <Card>
          <h2>Title</h2>
          <p>Description</p>
          <button>Action</button>
        </Card>
      );
      expect(screen.getByText('Title')).toBeInTheDocument();
      expect(screen.getByText('Description')).toBeInTheDocument();
      expect(screen.getByText('Action')).toBeInTheDocument();
    });

    it('renders with long content without layout issues', () => {
      const longContent = 'A'.repeat(1000);
      const { container } = render(<Card>{longContent}</Card>);
      expect(container.firstChild).toBeInTheDocument();
      expect(screen.getByText(longContent)).toBeInTheDocument();
    });
  });
});
