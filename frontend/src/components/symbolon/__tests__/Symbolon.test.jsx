import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import SymbolonCard from '../SymbolonCard';
import SymbolonGrid from '../SymbolonGrid';
import SymbolonModal from '../SymbolonModal';

// Mock card data
const mockCard = {
  id: 1,
  number: 1,
  title: 'The Warrior',
  image: 'symbolon-01.jpg',
  keywords: ['Aggression', 'Conquest', 'Energy'],
  meaning: 'Underlying the problem is the anger and aggression you have not yet perceived and acknowledged.',
  interpretation: 'The task ahead of you involved becoming more instigative.',
  themes: ['Mars energy', 'New beginnings', 'Action']
};

const mockCards = [
  mockCard,
  {
    id: 2,
    number: 2,
    title: 'The Lover',
    image: 'symbolon-02.jpg',
    keywords: ['Worth', 'Attraction', 'Possession'],
    meaning: 'You are a prisoner of your own feelings of worthlessness.'
  }
];

describe('SymbolonCard', () => {
  it('renders card with image, title, and keywords', () => {
    render(<SymbolonCard card={mockCard} onClick={() => {}} />);
    
    expect(screen.getByText('The Warrior')).toBeInTheDocument();
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('Aggression')).toBeInTheDocument();
    expect(screen.getByText('Conquest')).toBeInTheDocument();
    expect(screen.getByText('Energy')).toBeInTheDocument();
    
    const img = screen.getByAltText('The Warrior');
    expect(img).toHaveAttribute('src', '/content/symbolon/symbolon-01.jpg');
    expect(img).toHaveAttribute('loading', 'lazy');
  });

  it('truncates excerpt text to 120 characters', () => {
    render(<SymbolonCard card={mockCard} onClick={() => {}} />);
    
    const excerpt = screen.getByText(/Underlying the problem/);
    expect(excerpt.textContent.length).toBeLessThanOrEqual(124); // 120 + "..."
  });

  it('calls onClick when card is clicked', () => {
    const handleClick = jest.fn();
    render(<SymbolonCard card={mockCard} onClick={handleClick} />);
    
    fireEvent.click(screen.getByText('The Warrior'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('shows only first 3 keywords', () => {
    const cardWithManyKeywords = {
      ...mockCard,
      keywords: ['Keyword1', 'Keyword2', 'Keyword3', 'Keyword4', 'Keyword5']
    };
    
    render(<SymbolonCard card={cardWithManyKeywords} onClick={() => {}} />);
    
    expect(screen.getByText('Keyword1')).toBeInTheDocument();
    expect(screen.getByText('Keyword2')).toBeInTheDocument();
    expect(screen.getByText('Keyword3')).toBeInTheDocument();
    expect(screen.queryByText('Keyword4')).not.toBeInTheDocument();
    expect(screen.queryByText('Keyword5')).not.toBeInTheDocument();
  });
});

describe('SymbolonGrid', () => {
  it('renders multiple cards in grid', () => {
    render(<SymbolonGrid cards={mockCards} loading={false} />);
    
    expect(screen.getByText('The Warrior')).toBeInTheDocument();
    expect(screen.getByText('The Lover')).toBeInTheDocument();
  });

  it('shows skeleton loaders when loading', () => {
    const { container } = render(<SymbolonGrid cards={[]} loading={true} />);
    
    const skeletons = container.querySelectorAll('.symbolon-grid__skeleton');
    expect(skeletons.length).toBe(6);
  });

  it('opens modal when card is clicked', () => {
    render(<SymbolonGrid cards={mockCards} loading={false} />);
    
    fireEvent.click(screen.getByText('The Warrior'));
    
    // Modal should appear
    expect(screen.getByRole('dialog')).toBeInTheDocument();
    expect(screen.getByText('Card 1')).toBeInTheDocument();
  });

  it('closes modal when close button is clicked', () => {
    render(<SymbolonGrid cards={mockCards} loading={false} />);
    
    // Open modal
    fireEvent.click(screen.getByText('The Warrior'));
    expect(screen.getByRole('dialog')).toBeInTheDocument();
    
    // Close modal
    fireEvent.click(screen.getByLabelText('Close modal'));
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });
});

describe('SymbolonModal', () => {
  it('renders modal with card details', () => {
    render(<SymbolonModal card={mockCard} onClose={() => {}} />);
    
    expect(screen.getByRole('dialog')).toBeInTheDocument();
    expect(screen.getByText('The Warrior')).toBeInTheDocument();
    expect(screen.getByText('Card 1')).toBeInTheDocument();
    expect(screen.getByText('Core Meaning')).toBeInTheDocument();
    expect(screen.getByText('Interpretation')).toBeInTheDocument();
    expect(screen.getByText('Themes & Archetypes')).toBeInTheDocument();
  });

  it('displays all keywords in modal', () => {
    render(<SymbolonModal card={mockCard} onClose={() => {}} />);
    
    expect(screen.getByText('Aggression')).toBeInTheDocument();
    expect(screen.getByText('Conquest')).toBeInTheDocument();
    expect(screen.getByText('Energy')).toBeInTheDocument();
  });

  it('displays themes as list items', () => {
    render(<SymbolonModal card={mockCard} onClose={() => {}} />);
    
    expect(screen.getByText('Mars energy')).toBeInTheDocument();
    expect(screen.getByText('New beginnings')).toBeInTheDocument();
    expect(screen.getByText('Action')).toBeInTheDocument();
  });

  it('calls onClose when close button is clicked', () => {
    const handleClose = jest.fn();
    render(<SymbolonModal card={mockCard} onClose={handleClose} />);
    
    fireEvent.click(screen.getByLabelText('Close modal'));
    expect(handleClose).toHaveBeenCalledTimes(1);
  });

  it('calls onClose when overlay is clicked', () => {
    const handleClose = jest.fn();
    render(<SymbolonModal card={mockCard} onClose={handleClose} />);
    
    const overlay = document.querySelector('.modal-overlay');
    fireEvent.click(overlay);
    expect(handleClose).toHaveBeenCalledTimes(1);
  });

  it('calls onClose when Escape key is pressed', () => {
    const handleClose = jest.fn();
    render(<SymbolonModal card={mockCard} onClose={handleClose} />);
    
    fireEvent.keyDown(window, { key: 'Escape' });
    expect(handleClose).toHaveBeenCalledTimes(1);
  });

  it('prevents body scroll when modal is open', () => {
    const { unmount } = render(<SymbolonModal card={mockCard} onClose={() => {}} />);
    
    expect(document.body.style.overflow).toBe('hidden');
    
    unmount();
    expect(document.body.style.overflow).toBe('unset');
  });

  it('renders Close button in actions', () => {
    const handleClose = jest.fn();
    render(<SymbolonModal card={mockCard} onClose={handleClose} />);
    
    const closeButtons = screen.getAllByRole('button', { name: /close/i });
    // The second button is in the actions section
    const actionButton = closeButtons[1];
    fireEvent.click(actionButton);
    expect(handleClose).toHaveBeenCalledTimes(1);
  });

  it('handles card without interpretation section', () => {
    const cardWithoutInterpretation = {
      ...mockCard,
      interpretation: undefined
    };
    
    render(<SymbolonModal card={cardWithoutInterpretation} onClose={() => {}} />);
    
    expect(screen.getByText('Core Meaning')).toBeInTheDocument();
    expect(screen.queryByText('Interpretation')).not.toBeInTheDocument();
  });

  it('handles card without themes section', () => {
    const cardWithoutThemes = {
      ...mockCard,
      themes: undefined
    };
    
    render(<SymbolonModal card={cardWithoutThemes} onClose={() => {}} />);
    
    expect(screen.getByText('Core Meaning')).toBeInTheDocument();
    expect(screen.queryByText('Themes & Archetypes')).not.toBeInTheDocument();
  });
});

describe('Accessibility', () => {
  it('modal has proper ARIA attributes', () => {
    render(<SymbolonModal card={mockCard} onClose={() => {}} />);
    
    const modal = screen.getByRole('dialog');
    expect(modal).toHaveAttribute('aria-modal', 'true');
  });

  it('close button has aria-label', () => {
    render(<SymbolonModal card={mockCard} onClose={() => {}} />);
    
    const closeButton = screen.getByLabelText('Close modal');
    expect(closeButton).toBeInTheDocument();
  });

  it('images have descriptive alt text', () => {
    render(<SymbolonCard card={mockCard} onClick={() => {}} />);
    
    const img = screen.getByAltText('The Warrior');
    expect(img).toBeInTheDocument();
  });
});
