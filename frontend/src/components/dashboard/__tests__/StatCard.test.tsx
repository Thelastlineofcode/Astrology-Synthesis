import React from 'react';
import { render, screen } from '@testing-library/react';
import StatCard from '../StatCard';

describe('StatCard', () => {
  it('renders title and value', () => {
    render(
      <StatCard 
        title="Test Metric" 
        value={100} 
      />
    );
    
    expect(screen.getByText('Test Metric')).toBeInTheDocument();
    expect(screen.getByText('100')).toBeInTheDocument();
  });

  it('renders unit when provided', () => {
    render(
      <StatCard 
        title="Average Time" 
        value={24.5} 
        unit="hours"
      />
    );
    
    expect(screen.getByText('hours')).toBeInTheDocument();
  });

  it('renders trend indicator when provided', () => {
    render(
      <StatCard 
        title="Total Readings" 
        value={127} 
        change={12.5}
        trend="up"
      />
    );
    
    expect(screen.getByText('↑')).toBeInTheDocument();
    expect(screen.getByText('12.5%')).toBeInTheDocument();
  });

  it('handles string values', () => {
    render(
      <StatCard 
        title="Status" 
        value="Active" 
      />
    );
    
    expect(screen.getByText('Active')).toBeInTheDocument();
  });

  it('handles down trend', () => {
    render(
      <StatCard 
        title="Pending" 
        value={38} 
        change={-3.2}
        trend="down"
      />
    );
    
    expect(screen.getByText('↓')).toBeInTheDocument();
    expect(screen.getByText('3.2%')).toBeInTheDocument();
  });

  it('handles neutral trend', () => {
    render(
      <StatCard 
        title="Stable Metric" 
        value={50} 
        change={0}
        trend="neutral"
      />
    );
    
    expect(screen.getByText('→')).toBeInTheDocument();
  });
});
