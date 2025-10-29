import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Dashboard from '../page';

// Mock the dashboard card components
jest.mock('@/components/dashboard/QuickChartCard', () => {
  return function MockQuickChartCard() {
    return <div data-testid="quick-chart-card">Quick Chart Card</div>;
  };
});

jest.mock('@/components/dashboard/RecentChartsCard', () => {
  return function MockRecentChartsCard({ charts, loading }: { charts: any[], loading: boolean }) {
    return (
      <div data-testid="recent-charts-card">
        {loading ? 'Loading...' : `${charts.length} charts`}
      </div>
    );
  };
});

jest.mock('@/components/dashboard/BMADSummaryCard', () => {
  return function MockBMADSummaryCard() {
    return <div data-testid="bmad-summary-card">BMAD Summary Card</div>;
  };
});

jest.mock('@/components/dashboard/SymbolonCard', () => {
  return function MockSymbolonCard() {
    return <div data-testid="symbolon-card">Symbolon Card</div>;
  };
});

describe('Dashboard', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
  });

  test('renders dashboard header', () => {
    render(<Dashboard />);
    expect(screen.getByText('Your Astrology Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Welcome back. Ready to explore the cosmos?')).toBeInTheDocument();
  });

  test('renders all dashboard cards', () => {
    render(<Dashboard />);
    expect(screen.getByTestId('quick-chart-card')).toBeInTheDocument();
    expect(screen.getByTestId('recent-charts-card')).toBeInTheDocument();
    expect(screen.getByTestId('bmad-summary-card')).toBeInTheDocument();
    expect(screen.getByTestId('symbolon-card')).toBeInTheDocument();
  });

  test('loads recent charts from localStorage', async () => {
    const mockCharts = [
      { id: '1', name: 'Chart 1', date: '2025-10-01' },
      { id: '2', name: 'Chart 2', date: '2025-10-02' },
    ];
    localStorage.setItem('recentCharts', JSON.stringify(mockCharts));

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText('2 charts')).toBeInTheDocument();
    });
  });

  test('handles empty localStorage gracefully', async () => {
    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText('0 charts')).toBeInTheDocument();
    });
  });

  test('limits recent charts to 3', async () => {
    const mockCharts = [
      { id: '1', name: 'Chart 1', date: '2025-10-01' },
      { id: '2', name: 'Chart 2', date: '2025-10-02' },
      { id: '3', name: 'Chart 3', date: '2025-10-03' },
      { id: '4', name: 'Chart 4', date: '2025-10-04' },
      { id: '5', name: 'Chart 5', date: '2025-10-05' },
    ];
    localStorage.setItem('recentCharts', JSON.stringify(mockCharts));

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText('3 charts')).toBeInTheDocument();
    });
  });

  test('dashboard renders without errors', () => {
    render(<Dashboard />);
    expect(screen.getByText('Your Astrology Dashboard')).toBeInTheDocument();
  });
});
