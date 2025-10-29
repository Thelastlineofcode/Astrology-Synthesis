import React from 'react';
import { render, screen } from '@testing-library/react';
import WidgetCard from '../WidgetCard';

describe('WidgetCard', () => {
  it('renders title and children', () => {
    render(
      <WidgetCard title="Test Widget">
        <div>Test Content</div>
      </WidgetCard>
    );
    
    expect(screen.getByText('Test Widget')).toBeInTheDocument();
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('renders header action when provided', () => {
    render(
      <WidgetCard 
        title="Test Widget"
        headerAction={<button>Action</button>}
      >
        <div>Content</div>
      </WidgetCard>
    );
    
    expect(screen.getByText('Action')).toBeInTheDocument();
  });

  it('applies custom className', () => {
    const { container } = render(
      <WidgetCard 
        title="Test Widget"
        className="custom-class"
      >
        <div>Content</div>
      </WidgetCard>
    );
    
    const widget = container.firstChild;
    expect(widget).toHaveClass('custom-class');
  });
});
