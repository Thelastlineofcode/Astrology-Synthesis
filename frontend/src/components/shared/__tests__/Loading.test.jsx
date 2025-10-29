import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Spinner from '../Spinner';
import Skeleton, { SkeletonCard, SkeletonTable } from '../Skeleton';

describe('Spinner', () => {
  it('renders spinner with default props', () => {
    const { container } = render(<Spinner />);
    
    const spinner = container.querySelector('.spinner');
    expect(spinner).toBeInTheDocument();
    expect(spinner).toHaveClass('spinner--medium');
    expect(spinner).toHaveClass('spinner--primary');
  });

  it('renders spinner in small size', () => {
    const { container } = render(<Spinner size="small" />);
    
    const spinner = container.querySelector('.spinner');
    expect(spinner).toHaveClass('spinner--small');
  });

  it('renders spinner in large size', () => {
    const { container } = render(<Spinner size="large" />);
    
    const spinner = container.querySelector('.spinner');
    expect(spinner).toHaveClass('spinner--large');
  });

  it('renders spinner with custom color', () => {
    const { container } = render(<Spinner color="secondary" />);
    
    const spinner = container.querySelector('.spinner');
    expect(spinner).toHaveClass('spinner--secondary');
  });

  it('renders spinner with light color', () => {
    const { container } = render(<Spinner color="light" />);
    
    const spinner = container.querySelector('.spinner');
    expect(spinner).toHaveClass('spinner--light');
  });

  it('has role="status" for accessibility', () => {
    const { container } = render(<Spinner />);
    
    const spinner = container.querySelector('.spinner');
    expect(spinner).toHaveAttribute('role', 'status');
  });

  it('has aria-label with default loading text', () => {
    const { container } = render(<Spinner />);
    
    const spinner = container.querySelector('.spinner');
    expect(spinner).toHaveAttribute('aria-label', 'Loading...');
  });

  it('has custom aria-label when provided', () => {
    const { container } = render(<Spinner label="Loading data..." />);
    
    const spinner = container.querySelector('.spinner');
    expect(spinner).toHaveAttribute('aria-label', 'Loading data...');
  });

  it('includes visually hidden text for screen readers', () => {
    const { container } = render(<Spinner label="Loading..." />);
    
    const hiddenText = container.querySelector('.visually-hidden');
    expect(hiddenText).toBeInTheDocument();
    expect(hiddenText).toHaveTextContent('Loading...');
  });

  it('applies custom className', () => {
    const { container } = render(<Spinner className="custom-spinner" />);
    
    const spinner = container.querySelector('.spinner');
    expect(spinner).toHaveClass('custom-spinner');
  });

  it('renders SVG with correct viewBox', () => {
    const { container } = render(<Spinner />);
    
    const svg = container.querySelector('.spinner__svg');
    expect(svg).toBeInTheDocument();
    expect(svg).toHaveAttribute('viewBox', '0 0 50 50');
  });

  it('renders circle with correct attributes', () => {
    const { container } = render(<Spinner />);
    
    const circle = container.querySelector('.spinner__circle');
    expect(circle).toBeInTheDocument();
    expect(circle).toHaveAttribute('cx', '25');
    expect(circle).toHaveAttribute('cy', '25');
    expect(circle).toHaveAttribute('r', '20');
    expect(circle).toHaveAttribute('fill', 'none');
    expect(circle).toHaveAttribute('stroke-width', '4');
  });
});

describe('Skeleton', () => {
  it('renders skeleton with default props', () => {
    const { container } = render(<Skeleton />);
    
    const skeleton = container.querySelector('.skeleton');
    expect(skeleton).toBeInTheDocument();
    expect(skeleton).toHaveClass('skeleton--text');
  });

  it('renders skeleton with rect variant', () => {
    const { container } = render(<Skeleton variant="rect" />);
    
    const skeleton = container.querySelector('.skeleton');
    expect(skeleton).toHaveClass('skeleton--rect');
  });

  it('renders skeleton with circle variant', () => {
    const { container } = render(<Skeleton variant="circle" />);
    
    const skeleton = container.querySelector('.skeleton');
    expect(skeleton).toHaveClass('skeleton--circle');
  });

  it('renders skeleton with custom width', () => {
    const { container } = render(<Skeleton width="200px" />);
    
    const skeleton = container.querySelector('.skeleton');
    expect(skeleton).toHaveStyle({ width: '200px' });
  });

  it('renders skeleton with custom height', () => {
    const { container } = render(<Skeleton height="50px" />);
    
    const skeleton = container.querySelector('.skeleton');
    expect(skeleton).toHaveStyle({ height: '50px' });
  });

  it('renders multiple skeleton elements when count is provided', () => {
    const { container } = render(<Skeleton count={3} />);
    
    const skeletons = container.querySelectorAll('.skeleton');
    expect(skeletons).toHaveLength(3);
  });

  it('applies custom className', () => {
    const { container } = render(<Skeleton className="custom-skeleton" />);
    
    const skeleton = container.querySelector('.skeleton');
    expect(skeleton).toHaveClass('custom-skeleton');
  });

  it('has aria-busy="true" on container', () => {
    const { container } = render(<Skeleton />);
    
    const skeletonContainer = container.querySelector('.skeleton-container');
    expect(skeletonContainer).toHaveAttribute('aria-busy', 'true');
  });

  it('has aria-live="polite" on container', () => {
    const { container } = render(<Skeleton />);
    
    const skeletonContainer = container.querySelector('.skeleton-container');
    expect(skeletonContainer).toHaveAttribute('aria-live', 'polite');
  });

  it('has aria-hidden="true" on skeleton elements', () => {
    const { container } = render(<Skeleton />);
    
    const skeleton = container.querySelector('.skeleton');
    expect(skeleton).toHaveAttribute('aria-hidden', 'true');
  });
});

describe('SkeletonCard', () => {
  it('renders skeleton card component', () => {
    const { container } = render(<SkeletonCard />);
    
    const skeletonCard = container.querySelector('.skeleton-card');
    expect(skeletonCard).toBeInTheDocument();
  });

  it('has aria-busy="true"', () => {
    const { container } = render(<SkeletonCard />);
    
    const skeletonCard = container.querySelector('.skeleton-card');
    expect(skeletonCard).toHaveAttribute('aria-busy', 'true');
  });

  it('renders rect skeleton for image', () => {
    const { container } = render(<SkeletonCard />);
    
    const rectSkeleton = container.querySelector('.skeleton--rect');
    expect(rectSkeleton).toBeInTheDocument();
  });

  it('renders text skeletons for content', () => {
    const { container } = render(<SkeletonCard />);
    
    const textSkeletons = container.querySelectorAll('.skeleton--text');
    expect(textSkeletons.length).toBeGreaterThan(0);
  });
});

describe('SkeletonTable', () => {
  it('renders skeleton table with default 5 rows', () => {
    const { container } = render(<SkeletonTable />);
    
    const rows = container.querySelectorAll('.skeleton-table__row');
    expect(rows).toHaveLength(5);
  });

  it('renders skeleton table with custom number of rows', () => {
    const { container } = render(<SkeletonTable rows={3} />);
    
    const rows = container.querySelectorAll('.skeleton-table__row');
    expect(rows).toHaveLength(3);
  });

  it('has aria-busy="true"', () => {
    const { container } = render(<SkeletonTable />);
    
    const skeletonTable = container.querySelector('.skeleton-table');
    expect(skeletonTable).toHaveAttribute('aria-busy', 'true');
  });

  it('renders 3 skeleton cells per row', () => {
    const { container } = render(<SkeletonTable rows={1} />);
    
    const row = container.querySelector('.skeleton-table__row');
    const skeletons = row.querySelectorAll('.skeleton-container');
    expect(skeletons).toHaveLength(3);
  });
});

describe('Accessibility', () => {
  it('spinner is announced to screen readers with role="status"', () => {
    const { container } = render(<Spinner />);
    
    const spinner = container.querySelector('[role="status"]');
    expect(spinner).toBeInTheDocument();
  });

  it('spinner has descriptive aria-label', () => {
    const { container } = render(<Spinner label="Processing request..." />);
    
    const spinner = container.querySelector('[role="status"]');
    expect(spinner).toHaveAttribute('aria-label', 'Processing request...');
  });

  it('skeleton container announces loading state', () => {
    const { container } = render(<Skeleton />);
    
    const skeletonContainer = container.querySelector('[aria-busy="true"]');
    expect(skeletonContainer).toBeInTheDocument();
    expect(skeletonContainer).toHaveAttribute('aria-live', 'polite');
  });

  it('skeleton elements are hidden from screen readers', () => {
    const { container } = render(<Skeleton count={3} />);
    
    const skeletons = container.querySelectorAll('.skeleton');
    skeletons.forEach(skeleton => {
      expect(skeleton).toHaveAttribute('aria-hidden', 'true');
    });
  });

  it('spinner text is visually hidden but available to screen readers', () => {
    const { container } = render(<Spinner label="Loading data..." />);
    
    const hiddenText = container.querySelector('.visually-hidden');
    expect(hiddenText).toBeInTheDocument();
    expect(hiddenText).toHaveTextContent('Loading data...');
    
    // Check that visually-hidden class is applied
    expect(hiddenText).toHaveClass('visually-hidden');
  });
});

describe('Layout Stability', () => {
  it('skeleton maintains consistent dimensions', () => {
    const { container } = render(<Skeleton width="300px" height="50px" />);
    
    const skeleton = container.querySelector('.skeleton');
    expect(skeleton).toHaveStyle({ width: '300px', height: '50px' });
  });

  it('skeleton card maintains consistent structure', () => {
    const { container } = render(<SkeletonCard />);
    
    const skeletonCard = container.querySelector('.skeleton-card');
    expect(skeletonCard).toBeInTheDocument();
    
    // Verify structure matches expected card layout
    const rectSkeleton = container.querySelector('.skeleton--rect');
    expect(rectSkeleton).toBeInTheDocument();
  });

  it('skeleton table rows maintain consistent structure', () => {
    const { container } = render(<SkeletonTable rows={2} />);
    
    const rows = container.querySelectorAll('.skeleton-table__row');
    rows.forEach(row => {
      const cells = row.querySelectorAll('.skeleton-container');
      expect(cells).toHaveLength(3);
    });
  });
});
