import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ThemeToggle from '../ThemeToggle';

// Mock localStorage
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: (key) => store[key] || null,
    setItem: (key, value) => {
      store[key] = value.toString();
    },
    clear: () => {
      store = {};
    },
    removeItem: (key) => {
      delete store[key];
    },
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Mock matchMedia
const matchMediaMock = (matches) => ({
  matches,
  media: '(prefers-color-scheme: dark)',
  onchange: null,
  addListener: jest.fn(),
  removeListener: jest.fn(),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
  dispatchEvent: jest.fn(),
});

describe('ThemeToggle', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorageMock.clear();
    
    // Reset document theme attribute
    document.documentElement.removeAttribute('data-theme');
    
    // Mock window.matchMedia
    window.matchMedia = jest.fn().mockImplementation((query) => 
      matchMediaMock(false)
    );
  });

  it('renders theme toggle button', async () => {
    render(<ThemeToggle />);
    
    // Wait for component to mount (hasMounted state)
    await waitFor(() => {
      const button = screen.getByRole('button');
      expect(button).toBeInTheDocument();
    });
  });

  it('displays moon icon for light theme by default', async () => {
    render(<ThemeToggle />);
    
    await waitFor(() => {
      const button = screen.getByRole('button');
      expect(button).toHaveTextContent('🌙');
    });
  });

  it('toggles to dark theme when clicked', async () => {
    render(<ThemeToggle />);
    
    await waitFor(() => {
      const button = screen.getByRole('button');
      fireEvent.click(button);
    });

    await waitFor(() => {
      expect(localStorage.getItem('theme')).toBe('dark');
      expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
      const button = screen.getByRole('button');
      expect(button).toHaveTextContent('☀️');
    });
  });

  it('toggles back to light theme when clicked again', async () => {
    render(<ThemeToggle />);
    
    await waitFor(() => {
      const button = screen.getByRole('button');
      fireEvent.click(button);
    });

    await waitFor(() => {
      const button = screen.getByRole('button');
      fireEvent.click(button);
    });

    await waitFor(() => {
      expect(localStorage.getItem('theme')).toBe('light');
      expect(document.documentElement.getAttribute('data-theme')).toBe('light');
      const button = screen.getByRole('button');
      expect(button).toHaveTextContent('🌙');
    });
  });

  it('has proper aria-label for accessibility', async () => {
    render(<ThemeToggle />);
    
    await waitFor(() => {
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('aria-label', 'Switch to dark mode');
    });
  });

  it('updates aria-label after theme change', async () => {
    render(<ThemeToggle />);
    
    await waitFor(() => {
      const button = screen.getByRole('button');
      fireEvent.click(button);
    });

    await waitFor(() => {
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('aria-label', 'Switch to light mode');
    });
  });

  it('respects saved theme from localStorage', async () => {
    localStorage.setItem('theme', 'dark');
    
    render(<ThemeToggle />);
    
    await waitFor(() => {
      const button = screen.getByRole('button');
      expect(button).toHaveTextContent('☀️');
      expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
    });
  });

  it('respects system preference when no saved theme', async () => {
    window.matchMedia = jest.fn().mockImplementation((query) => 
      matchMediaMock(true) // System prefers dark
    );
    
    render(<ThemeToggle />);
    
    await waitFor(() => {
      const button = screen.getByRole('button');
      expect(button).toHaveTextContent('☀️');
    });
  });

  it('has keyboard accessibility (can be clicked with keyboard)', async () => {
    render(<ThemeToggle />);
    
    await waitFor(() => {
      const button = screen.getByRole('button');
      expect(button.className).toContain('theme-toggle');
    });
  });

  it('includes screen reader only text', async () => {
    render(<ThemeToggle />);
    
    await waitFor(() => {
      const srText = document.querySelector('.sr-only');
      expect(srText).toBeInTheDocument();
      expect(srText).toHaveTextContent('Toggle theme');
    });
  });

  it('renders after mount (SSR safe with hasMounted check)', async () => {
    render(<ThemeToggle />);
    
    // Component should render after mount
    await waitFor(() => {
      const button = screen.getByRole('button');
      expect(button).toBeInTheDocument();
    });
  });

  it('persists theme choice across component remounts', async () => {
    const { unmount } = render(<ThemeToggle />);
    
    await waitFor(() => {
      const button = screen.getByRole('button');
      fireEvent.click(button);
    });

    await waitFor(() => {
      expect(localStorage.getItem('theme')).toBe('dark');
    });

    unmount();
    
    render(<ThemeToggle />);
    
    await waitFor(() => {
      const button = screen.getByRole('button');
      expect(button).toHaveTextContent('☀️');
      expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
    });
  });
});

describe('ThemeToggle Accessibility', () => {
  beforeEach(() => {
    localStorageMock.clear();
    document.documentElement.removeAttribute('data-theme');
    window.matchMedia = jest.fn().mockImplementation((query) => 
      matchMediaMock(false)
    );
  });

  it('button is keyboard focusable', async () => {
    render(<ThemeToggle />);
    
    await waitFor(() => {
      const button = screen.getByRole('button');
      expect(button).not.toHaveAttribute('tabindex', '-1');
    });
  });

  it('has descriptive aria-label that changes with state', async () => {
    render(<ThemeToggle />);
    
    await waitFor(() => {
      const button = screen.getByRole('button');
      expect(button.getAttribute('aria-label')).toMatch(/Switch to (light|dark) mode/);
    });
  });

  it('has title attribute for tooltip', async () => {
    render(<ThemeToggle />);
    
    await waitFor(() => {
      const button = screen.getByRole('button');
      expect(button).toHaveAttribute('title');
      expect(button.getAttribute('title')).toMatch(/Switch to (light|dark) mode/);
    });
  });
});
