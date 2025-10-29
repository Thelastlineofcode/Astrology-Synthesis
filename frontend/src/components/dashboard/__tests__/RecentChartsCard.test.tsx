import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import RecentChartsCard from '../RecentChartsCard';

describe('RecentChartsCard', () => {
  const mockCharts = [
    { id: '1', name: 'Chart 1', date: '2025-10-01T10:00:00Z' },
    { id: '2', name: 'Chart 2', date: '2025-10-02T10:00:00Z' },
    { id: '3', date: '2025-10-03T10:00:00Z' }, // No name
  ];

  test('renders loading state', () => {
    const { container } = render(<RecentChartsCard charts={[]} loading={true} />);
    
    expect(screen.getByText('Recent Charts')).toBeInTheDocument();
    expect(container.querySelector('.loading-skeleton')).toBeInTheDocument();
  });

  test('renders empty state when no charts', () => {
    render(<RecentChartsCard charts={[]} loading={false} />);
    
    expect(screen.getByText('Recent Charts')).toBeInTheDocument();
    expect(screen.getByText(/No charts yet/)).toBeInTheDocument();
  });

  test('renders chart list with data', () => {
    render(<RecentChartsCard charts={mockCharts} loading={false} />);
    
    expect(screen.getByText('Recent Charts')).toBeInTheDocument();
    expect(screen.getByText('Chart 1')).toBeInTheDocument();
    expect(screen.getByText('Chart 2')).toBeInTheDocument();
    expect(screen.getByText('Unnamed Chart')).toBeInTheDocument(); // For chart without name
    expect(screen.getByText('View All')).toBeInTheDocument();
  });

  test('displays formatted dates', () => {
    render(<RecentChartsCard charts={mockCharts} loading={false} />);
    
    // Check that dates are rendered (format may vary by locale)
    const dates = screen.getAllByText(/\d+\/\d+\/\d+/);
    expect(dates.length).toBeGreaterThan(0);
  });

  test('renders View buttons for each chart', () => {
    render(<RecentChartsCard charts={mockCharts} loading={false} />);
    
    const viewButtons = screen.getAllByText('View');
    expect(viewButtons).toHaveLength(mockCharts.length);
  });
});
