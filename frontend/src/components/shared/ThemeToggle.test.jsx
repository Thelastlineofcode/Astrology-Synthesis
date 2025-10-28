// /frontend/src/components/shared/ThemeToggle.test.jsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ThemeToggle from './ThemeToggle';

describe('ThemeToggle', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
    // Reset data-theme attribute
    document.documentElement.removeAttribute('data-theme');
  });

  it('renders theme toggle button', () => {
    render(<ThemeToggle />);
    const button = screen.getByRole('button');
    expect(button).toBeInTheDocument();
  });

  it('has proper aria-label', () => {
    render(<ThemeToggle />);
    const button = screen.getByRole('button');
    expect(button).toHaveAttribute('aria-label');
  });

  it('toggles theme on click', () => {
    render(<ThemeToggle />);
    const button = screen.getByRole('button');
    
    // Initial state should be light or system preference
    const initialTheme = document.documentElement.getAttribute('data-theme');
    
    // Click to toggle
    fireEvent.click(button);
    
    const newTheme = document.documentElement.getAttribute('data-theme');
    expect(newTheme).not.toBe(initialTheme);
  });

  it('persists theme to localStorage', () => {
    render(<ThemeToggle />);
    const button = screen.getByRole('button');
    
    // Click to toggle
    fireEvent.click(button);
    
    // Check if theme is saved in localStorage
    const savedTheme = localStorage.getItem('theme');
    expect(savedTheme).toBeTruthy();
    expect(['light', 'dark']).toContain(savedTheme);
  });

  it('loads saved theme from localStorage', () => {
    // Set a theme in localStorage
    localStorage.setItem('theme', 'dark');
    
    render(<ThemeToggle />);
    
    // Check if the theme is applied
    const theme = document.documentElement.getAttribute('data-theme');
    expect(theme).toBe('dark');
  });

  it('displays moon icon for light theme', () => {
    localStorage.setItem('theme', 'light');
    render(<ThemeToggle />);
    const button = screen.getByRole('button');
    expect(button.textContent).toBe('🌙');
  });

  it('displays sun icon for dark theme', () => {
    localStorage.setItem('theme', 'dark');
    render(<ThemeToggle />);
    const button = screen.getByRole('button');
    expect(button.textContent).toBe('☀️');
  });
});
