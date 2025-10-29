import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChartCanvas from './ChartCanvas';
import { mockChartData } from './mockChartData';

describe('ChartCanvas Component', () => {
  describe('Rendering', () => {
    test('renders chart with provided data', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      // Check that the SVG is rendered
      const svg = screen.getByRole('img', { name: /Natal chart wheel with \d+ planets/ });
      expect(svg).toBeInTheDocument();
    });

    test('renders placeholder when no chart data provided', () => {
      render(<ChartCanvas chartData={null} />);
      
      expect(screen.getByText(/No chart data available/i)).toBeInTheDocument();
    });

    test('renders zoom controls', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      expect(screen.getByLabelText('Zoom in')).toBeInTheDocument();
      expect(screen.getByLabelText('Zoom out')).toBeInTheDocument();
      expect(screen.getByText('100%')).toBeInTheDocument();
    });

    test('renders aspect toggle checkbox', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      const checkbox = screen.getByLabelText(/Toggle aspect lines/i);
      expect(checkbox).toBeInTheDocument();
      expect(checkbox).toBeChecked();
    });

    test('renders all planets', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      // Check that planet buttons are rendered
      Object.keys(mockChartData.planets).forEach(planetName => {
        const planetElement = screen.getByRole('button', { name: new RegExp(planetName, 'i') });
        expect(planetElement).toBeInTheDocument();
      });
    });
  });

  describe('Zoom Functionality', () => {
    test('zoom in increases zoom level', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      const zoomInButton = screen.getByLabelText('Zoom in');
      
      fireEvent.click(zoomInButton);
      
      expect(screen.getByText('120%')).toBeInTheDocument();
    });

    test('zoom out decreases zoom level', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      const zoomOutButton = screen.getByLabelText('Zoom out');
      
      fireEvent.click(zoomOutButton);
      
      expect(screen.getByText('80%')).toBeInTheDocument();
    });

    test('zoom in reaches maximum zoom level', async () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      const zoomInButton = screen.getByLabelText('Zoom in');
      
      // Click multiple times to reach max zoom (200%)
      // Each click adds 0.2, so 5 clicks from 1.0 = 2.0
      fireEvent.click(zoomInButton);
      fireEvent.click(zoomInButton);
      fireEvent.click(zoomInButton);
      fireEvent.click(zoomInButton);
      fireEvent.click(zoomInButton);
      
      expect(screen.getByText('200%')).toBeInTheDocument();
      
      // Try to zoom in further - should stay at 200%
      fireEvent.click(zoomInButton);
      expect(screen.getByText('200%')).toBeInTheDocument();
    });

    test('zoom out button disabled at minimum zoom', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      const zoomOutButton = screen.getByLabelText('Zoom out');
      
      // Click multiple times to reach min zoom (50%)
      fireEvent.click(zoomOutButton);
      fireEvent.click(zoomOutButton);
      fireEvent.click(zoomOutButton);
      
      expect(zoomOutButton).toBeDisabled();
      expect(screen.getByText('50%')).toBeInTheDocument();
    });
  });

  describe('Aspect Toggle', () => {
    test('toggle aspects checkbox works', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      const checkbox = screen.getByLabelText(/Toggle aspect lines/i);
      
      expect(checkbox).toBeChecked();
      
      fireEvent.click(checkbox);
      
      expect(checkbox).not.toBeChecked();
      
      fireEvent.click(checkbox);
      
      expect(checkbox).toBeChecked();
    });
  });

  describe('Tooltips', () => {
    test('hovering over planet shows tooltip', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      const sunButton = screen.getByRole('button', { name: /Sun at/i });
      
      fireEvent.mouseEnter(sunButton);
      
      // Check tooltip appears
      expect(screen.getByRole('tooltip')).toBeInTheDocument();
      expect(screen.getByText('Sun')).toBeInTheDocument();
    });

    test('leaving planet hides tooltip', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      const sunButton = screen.getByRole('button', { name: /Sun at/i });
      
      fireEvent.mouseEnter(sunButton);
      expect(screen.getByRole('tooltip')).toBeInTheDocument();
      
      fireEvent.mouseLeave(sunButton);
      expect(screen.queryByRole('tooltip')).not.toBeInTheDocument();
    });

    test('tooltip shows retrograde indicator when applicable', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      const mercuryButton = screen.getByRole('button', { name: /Mercury.*retrograde/i });
      
      fireEvent.mouseEnter(mercuryButton);
      
      expect(screen.getByText(/Retrograde/i)).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    test('planets are keyboard focusable', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      const sunButton = screen.getByRole('button', { name: /Sun at/i });
      
      sunButton.focus();
      expect(sunButton).toHaveFocus();
    });

    test('focusing planet shows tooltip', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      const sunButton = screen.getByRole('button', { name: /Sun at/i });
      
      fireEvent.focus(sunButton);
      
      expect(screen.getByRole('tooltip')).toBeInTheDocument();
    });

    test('Enter key on planet shows tooltip', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      const sunButton = screen.getByRole('button', { name: /Sun at/i });
      
      fireEvent.keyDown(sunButton, { key: 'Enter' });
      
      expect(screen.getByRole('tooltip')).toBeInTheDocument();
    });

    test('Space key on planet shows tooltip', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      const sunButton = screen.getByRole('button', { name: /Sun at/i });
      
      fireEvent.keyDown(sunButton, { key: ' ' });
      
      expect(screen.getByRole('tooltip')).toBeInTheDocument();
    });

    test('Escape key hides tooltip', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      const sunButton = screen.getByRole('button', { name: /Sun at/i });
      
      fireEvent.keyDown(sunButton, { key: 'Enter' });
      expect(screen.getByRole('tooltip')).toBeInTheDocument();
      
      fireEvent.keyDown(sunButton, { key: 'Escape' });
      expect(screen.queryByRole('tooltip')).not.toBeInTheDocument();
    });

    test('SVG has proper aria-label', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      const svg = screen.getByRole('img');
      expect(svg).toHaveAttribute('aria-label', expect.stringContaining('Natal chart wheel'));
    });

    test('zoom buttons have aria-labels', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      expect(screen.getByLabelText('Zoom in')).toBeInTheDocument();
      expect(screen.getByLabelText('Zoom out')).toBeInTheDocument();
    });

    test('planet buttons have descriptive aria-labels', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      const sunButton = screen.getByRole('button', { name: /Sun at.*Sagittarius/i });
      expect(sunButton).toBeInTheDocument();
    });
  });

  describe('Chart Structure', () => {
    test('renders with proper viewBox', () => {
      render(<ChartCanvas chartData={mockChartData} />);
      
      const svg = screen.getByRole('img');
      expect(svg).toHaveAttribute('viewBox', '0 0 600 600');
    });
  });
});
