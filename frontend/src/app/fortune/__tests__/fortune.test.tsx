import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import FortunePage from '../page';

describe('FortunePage', () => {
  it('renders the fortune page with profile information', () => {
    render(<FortunePage />);
    
    // Check profile elements
    expect(screen.getByText('Emma Smith')).toBeInTheDocument();
    expect(screen.getByText('Gemini')).toBeInTheDocument();
    expect(screen.getByText('37,484')).toBeInTheDocument();
  });

  it('renders the Get Premium card', () => {
    render(<FortunePage />);
    
    expect(screen.getByText('Get Premium')).toBeInTheDocument();
    expect(screen.getByText(/Get Unlimited Tarot Reading/i)).toBeInTheDocument();
  });

  it('renders the Invite Friends card', () => {
    render(<FortunePage />);
    
    expect(screen.getByText('Invite Friends')).toBeInTheDocument();
    expect(screen.getByText(/Earn a 5% discount/i)).toBeInTheDocument();
  });

  it('renders progress indicator', () => {
    render(<FortunePage />);
    
    expect(screen.getByText('75%')).toBeInTheDocument();
    expect(screen.getByText('+15%')).toBeInTheDocument();
  });

  it('renders Reference Code section', () => {
    render(<FortunePage />);
    
    expect(screen.getByText('Reference Code')).toBeInTheDocument();
  });

  it('renders fortune readings section with tabs', () => {
    render(<FortunePage />);
    
    expect(screen.getByText('Your Fortune')).toBeInTheDocument();
    expect(screen.getByText('Daily')).toBeInTheDocument();
    expect(screen.getByText('Weekly')).toBeInTheDocument();
    expect(screen.getByText('Monthly')).toBeInTheDocument();
  });

  it('displays daily reading by default', () => {
    render(<FortunePage />);
    
    expect(screen.getByText(/Today's energies align perfectly/i)).toBeInTheDocument();
  });

  it('switches to weekly reading when Weekly button is clicked', () => {
    render(<FortunePage />);
    
    const weeklyButton = screen.getByText('Weekly');
    fireEvent.click(weeklyButton);
    
    expect(screen.getByText(/This week brings transformative energy/i)).toBeInTheDocument();
  });

  it('switches to monthly reading when Monthly button is clicked', () => {
    render(<FortunePage />);
    
    const monthlyButton = screen.getByText('Monthly');
    fireEvent.click(monthlyButton);
    
    expect(screen.getByText(/This month marks a powerful cycle/i)).toBeInTheDocument();
  });

  it('renders Save and Share buttons', () => {
    render(<FortunePage />);
    
    expect(screen.getByText('Save')).toBeInTheDocument();
    expect(screen.getByText('Share')).toBeInTheDocument();
  });

  it('renders bottom navigation with all items', () => {
    render(<FortunePage />);
    
    expect(screen.getByText('Discover')).toBeInTheDocument();
    expect(screen.getByText('Astrolocers')).toBeInTheDocument();
    expect(screen.getByText('Starbase')).toBeInTheDocument();
    expect(screen.getByText('Consultant')).toBeInTheDocument();
    expect(screen.getByText('Profile')).toBeInTheDocument();
  });

  it('displays notification badge', () => {
    render(<FortunePage />);
    
    // Find both notification badges (header and nav)
    const badges = screen.getAllByText('5');
    expect(badges.length).toBeGreaterThan(0);
  });

  it('applies active class to Daily button by default', () => {
    render(<FortunePage />);
    
    const dailyButton = screen.getByText('Daily');
    expect(dailyButton).toHaveClass('active');
  });

  it('changes active state when switching reading types', () => {
    render(<FortunePage />);
    
    const weeklyButton = screen.getByText('Weekly');
    const dailyButton = screen.getByText('Daily');
    
    fireEvent.click(weeklyButton);
    
    expect(weeklyButton).toHaveClass('active');
    expect(dailyButton).not.toHaveClass('active');
  });
});
