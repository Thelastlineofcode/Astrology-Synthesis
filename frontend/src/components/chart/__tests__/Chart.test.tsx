import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import PlanetTable from '../PlanetTable';
import HouseTable from '../HouseTable';
import ChartCanvas from '../ChartCanvas';
import { ChartData } from '@/types/chart';

// Mock chart data
const mockChartData: ChartData = {
  planets: {
    'Sun': { sign: 'Leo', degree: 15.5, house: 5, retrograde: false, longitude: 135.5 },
    'Moon': { sign: 'Cancer', degree: 22.3, house: 4, retrograde: false, longitude: 112.3 },
    'Mercury': { sign: 'Virgo', degree: 8.1, house: 6, retrograde: false, longitude: 158.1 },
    'Venus': { sign: 'Leo', degree: 28.7, house: 5, retrograde: false, longitude: 148.7 },
    'Mars': { sign: 'Gemini', degree: 12.4, house: 3, retrograde: false, longitude: 72.4 },
    'Jupiter': { sign: 'Sagittarius', degree: 5.2, house: 9, retrograde: true, longitude: 245.2 },
    'Saturn': { sign: 'Capricorn', degree: 18.9, house: 10, retrograde: false, longitude: 288.9 },
    'Uranus': { sign: 'Aquarius', degree: 2.1, house: 11, retrograde: false, longitude: 302.1 },
    'Neptune': { sign: 'Pisces', degree: 14.5, house: 12, retrograde: false, longitude: 344.5 },
    'Pluto': { sign: 'Capricorn', degree: 22.8, house: 10, retrograde: false, longitude: 292.8 },
    'North Node': { sign: 'Gemini', degree: 8.5, house: 3, retrograde: true, longitude: 68.5 },
    'South Node': { sign: 'Sagittarius', degree: 8.5, house: 9, retrograde: true, longitude: 248.5 },
    'Chiron': null
  },
  houses: {
    'house_1': { sign: 'Aries', degree: 12.0, longitude: 12.0 },
    'house_2': { sign: 'Taurus', degree: 8.5, longitude: 38.5 },
    'house_3': { sign: 'Gemini', degree: 5.2, longitude: 65.2 },
    'house_4': { sign: 'Cancer', degree: 12.0, longitude: 102.0 },
    'house_5': { sign: 'Leo', degree: 18.7, longitude: 138.7 },
    'house_6': { sign: 'Virgo', degree: 21.3, longitude: 171.3 },
    'house_7': { sign: 'Libra', degree: 12.0, longitude: 192.0 },
    'house_8': { sign: 'Scorpio', degree: 8.5, longitude: 218.5 },
    'house_9': { sign: 'Sagittarius', degree: 5.2, longitude: 245.2 },
    'house_10': { sign: 'Capricorn', degree: 12.0, longitude: 282.0 },
    'house_11': { sign: 'Aquarius', degree: 18.7, longitude: 318.7 },
    'house_12': { sign: 'Pisces', degree: 21.3, longitude: 351.3 }
  },
  ascendant: { sign: 'Aries', degree: 12.0, longitude: 12.0 },
  midheaven: { sign: 'Capricorn', degree: 12.0, longitude: 282.0 }
};

describe('PlanetTable', () => {
  it('renders planet table with title', () => {
    render(<PlanetTable planets={mockChartData.planets} />);
    expect(screen.getByText('Planetary Positions')).toBeInTheDocument();
  });

  it('displays all planets in order', () => {
    render(<PlanetTable planets={mockChartData.planets} />);
    
    expect(screen.getByText('Sun')).toBeInTheDocument();
    expect(screen.getByText('Moon')).toBeInTheDocument();
    expect(screen.getByText('Mercury')).toBeInTheDocument();
    expect(screen.getByText('Venus')).toBeInTheDocument();
    expect(screen.getByText('Mars')).toBeInTheDocument();
    expect(screen.getByText('Jupiter')).toBeInTheDocument();
    expect(screen.getByText('Saturn')).toBeInTheDocument();
  });

  it('displays planet signs correctly', () => {
    render(<PlanetTable planets={mockChartData.planets} />);
    
    expect(screen.getAllByText('Leo').length).toBeGreaterThan(0);
    expect(screen.getByText('Cancer')).toBeInTheDocument();
    expect(screen.getByText('Virgo')).toBeInTheDocument();
  });

  it('displays retrograde status correctly', () => {
    render(<PlanetTable planets={mockChartData.planets} />);
    
    // Jupiter is retrograde
    const retrogradeBadges = screen.getAllByText('℞');
    expect(retrogradeBadges.length).toBeGreaterThan(0);
  });

  it('shows unavailable planet data', () => {
    render(<PlanetTable planets={mockChartData.planets} />);
    
    expect(screen.getByText('Chiron')).toBeInTheDocument();
    expect(screen.getByText('Data unavailable')).toBeInTheDocument();
  });

  it('displays planet count', () => {
    render(<PlanetTable planets={mockChartData.planets} />);
    expect(screen.getByText(/12 of 13 planets calculated/)).toBeInTheDocument();
  });
});

describe('HouseTable', () => {
  it('renders house table with title', () => {
    render(
      <HouseTable 
        houses={mockChartData.houses}
        ascendant={mockChartData.ascendant}
        midheaven={mockChartData.midheaven}
      />
    );
    expect(screen.getByText('House System')).toBeInTheDocument();
  });

  it('displays all 12 houses', () => {
    render(
      <HouseTable 
        houses={mockChartData.houses}
        ascendant={mockChartData.ascendant}
        midheaven={mockChartData.midheaven}
      />
    );
    
    // Check that houses 1-12 are present
    for (let i = 1; i <= 12; i++) {
      expect(screen.getByText(i.toString())).toBeInTheDocument();
    }
  });

  it('displays ascendant and midheaven', () => {
    render(
      <HouseTable 
        houses={mockChartData.houses}
        ascendant={mockChartData.ascendant}
        midheaven={mockChartData.midheaven}
      />
    );
    
    expect(screen.getByText(/Ascendant/)).toBeInTheDocument();
    expect(screen.getByText(/Midheaven/)).toBeInTheDocument();
  });

  it('displays house meanings', () => {
    render(
      <HouseTable 
        houses={mockChartData.houses}
        ascendant={mockChartData.ascendant}
        midheaven={mockChartData.midheaven}
      />
    );
    
    expect(screen.getByText(/Self, Identity, Appearance/)).toBeInTheDocument();
    expect(screen.getByText(/Values, Money, Possessions/)).toBeInTheDocument();
    expect(screen.getByText(/Career, Public Life, Reputation/)).toBeInTheDocument();
  });

  it('displays house count', () => {
    render(
      <HouseTable 
        houses={mockChartData.houses}
        ascendant={mockChartData.ascendant}
        midheaven={mockChartData.midheaven}
      />
    );
    expect(screen.getByText(/12 house cusps calculated/)).toBeInTheDocument();
  });
});

describe('ChartCanvas', () => {
  it('renders chart canvas with title', () => {
    render(<ChartCanvas chartData={mockChartData} />);
    expect(screen.getByText('Birth Chart Wheel')).toBeInTheDocument();
  });

  it('renders SVG element', () => {
    const { container } = render(<ChartCanvas chartData={mockChartData} />);
    const svg = container.querySelector('svg');
    expect(svg).toBeInTheDocument();
  });

  it('renders with custom dimensions', () => {
    const { container } = render(
      <ChartCanvas chartData={mockChartData} width={400} height={400} />
    );
    const svg = container.querySelector('svg');
    expect(svg).toHaveAttribute('width', '400');
    expect(svg).toHaveAttribute('height', '400');
  });

  it('displays legend', () => {
    render(<ChartCanvas chartData={mockChartData} />);
    expect(screen.getByText('Direct Motion')).toBeInTheDocument();
    expect(screen.getByText(/Retrograde/)).toBeInTheDocument();
  });
});
