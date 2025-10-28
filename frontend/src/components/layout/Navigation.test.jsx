import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Navigation from './Navigation';

// Helper to render component with Router
const renderWithRouter = (component) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('Navigation component', () => {
  it('renders the logo and brand text', () => {
    renderWithRouter(<Navigation />);
    expect(screen.getByText('✨')).toBeInTheDocument();
    expect(screen.getByText('BMAD Astrology')).toBeInTheDocument();
  });

  it('renders all navigation links on desktop', () => {
    renderWithRouter(<Navigation />);
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('New Chart')).toBeInTheDocument();
    expect(screen.getByText('BMAD Analysis')).toBeInTheDocument();
    expect(screen.getByText('Symbolon Cards')).toBeInTheDocument();
    expect(screen.getByText('Journal')).toBeInTheDocument();
  });

  it('renders theme toggle button', () => {
    renderWithRouter(<Navigation />);
    const themeButton = screen.getByRole('button', { name: /switch to/i });
    expect(themeButton).toBeInTheDocument();
  });

  it('renders hamburger menu button', () => {
    renderWithRouter(<Navigation />);
    const hamburgerButton = screen.getByRole('button', { name: /open menu/i });
    expect(hamburgerButton).toBeInTheDocument();
  });

  it('opens mobile menu when hamburger is clicked', () => {
    renderWithRouter(<Navigation />);
    const hamburgerButton = screen.getByRole('button', { name: /open menu/i });
    
    fireEvent.click(hamburgerButton);
    
    const mobileMenu = screen.getByRole('dialog', { name: /mobile menu/i });
    expect(mobileMenu).toBeInTheDocument();
  });

  it('closes mobile menu when overlay is clicked', () => {
    renderWithRouter(<Navigation />);
    const hamburgerButton = screen.getByRole('button', { name: /open menu/i });
    
    fireEvent.click(hamburgerButton);
    
    const overlay = document.querySelector('.nav__overlay');
    fireEvent.click(overlay);
    
    expect(screen.queryByRole('dialog', { name: /mobile menu/i })).not.toBeInTheDocument();
  });

  it('closes mobile menu when Escape key is pressed', () => {
    renderWithRouter(<Navigation />);
    const hamburgerButton = screen.getByRole('button', { name: /open menu/i });
    
    fireEvent.click(hamburgerButton);
    expect(screen.getByRole('dialog', { name: /mobile menu/i })).toBeInTheDocument();
    
    fireEvent.keyDown(window, { key: 'Escape' });
    
    expect(screen.queryByRole('dialog', { name: /mobile menu/i })).not.toBeInTheDocument();
  });

  it('has proper ARIA attributes', () => {
    renderWithRouter(<Navigation />);
    
    const nav = screen.getByRole('navigation', { name: /main navigation/i });
    expect(nav).toBeInTheDocument();
    
    const hamburgerButton = screen.getByRole('button', { name: /open menu/i });
    expect(hamburgerButton).toHaveAttribute('aria-expanded', 'false');
    
    fireEvent.click(hamburgerButton);
    expect(hamburgerButton).toHaveAttribute('aria-expanded', 'true');
  });

  it('logo links to home page', () => {
    renderWithRouter(<Navigation />);
    const logo = screen.getByText('BMAD Astrology').closest('a');
    expect(logo).toHaveAttribute('href', '/');
  });

  it('all navigation links are keyboard navigable', () => {
    renderWithRouter(<Navigation />);
    const dashboardLink = screen.getAllByText('Dashboard')[0].closest('a');
    
    dashboardLink.focus();
    expect(document.activeElement).toBe(dashboardLink);
  });
});
