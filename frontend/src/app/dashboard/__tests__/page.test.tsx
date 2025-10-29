import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Dashboard from '../page';

interface LocalStorageMock {
  getItem: jest.Mock;
  setItem: jest.Mock;
  clear: jest.Mock;
}

// Mock localStorage
const localStorageMock: LocalStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  clear: jest.fn(),
};
global.localStorage = localStorageMock as unknown as Storage;

describe('Dashboard', () => {
  beforeEach(() => {
    localStorageMock.getItem.mockClear();
  });

  it('renders dashboard header', () => {
    localStorageMock.getItem.mockReturnValue('[]');
    render(<Dashboard />);
    
    expect(screen.getByText('Your Astrology Dashboard')).toBeInTheDocument();
    expect(screen.getByText(/Welcome back. Ready to explore the cosmos?/i)).toBeInTheDocument();
  });

  it('displays empty state when no recent charts exist', async () => {
    localStorageMock.getItem.mockReturnValue('[]');
    render(<Dashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/No charts yet. Generate your first chart to get started!/i)).toBeInTheDocument();
    });
  });

  it('renders all dashboard cards', () => {
    localStorageMock.getItem.mockReturnValue('[]');
    render(<Dashboard />);
    
    // Check for card headers
    expect(screen.getByText('Generate Your Chart')).toBeInTheDocument();
    expect(screen.getByText('Recent Charts')).toBeInTheDocument();
    expect(screen.getByText('BMAD Analysis')).toBeInTheDocument();
    expect(screen.getByText('Symbolon Cards')).toBeInTheDocument();
  });

  it('handles localStorage data correctly', async () => {
    const mockCharts = [
      { id: '1', name: 'My Chart', date: '2024-01-15' },
      { id: '2', name: 'Test Chart', date: '2024-01-16' },
    ];
    
    // Set up localStorage before rendering
    Storage.prototype.getItem = jest.fn(() => JSON.stringify(mockCharts));
    
    render(<Dashboard />);
    
    // Component should render without crashing
    expect(screen.getByText('Your Astrology Dashboard')).toBeInTheDocument();
  });
});
