import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import HouseTable from './HouseTable';

describe('HouseTable component', () => {
  const validHousesData = {
    house_1: { sign: 'Leo', degree: 26.142947, longitude: 146.142947 },
    house_2: { sign: 'Virgo', degree: 24.5, longitude: 174.5 },
    house_3: { sign: 'Libra', degree: 20.3, longitude: 200.3 },
    house_4: { sign: 'Scorpio', degree: 15.8, longitude: 225.8 },
    house_5: { sign: 'Sagittarius', degree: 12.4, longitude: 252.4 },
    house_6: { sign: 'Capricorn', degree: 10.9, longitude: 280.9 },
    house_7: { sign: 'Aquarius', degree: 26.1, longitude: 326.1 },
    house_8: { sign: 'Pisces', degree: 24.5, longitude: 354.5 },
    house_9: { sign: 'Aries', degree: 20.3, longitude: 20.3 },
    house_10: { sign: 'Taurus', degree: 15.8, longitude: 45.8 },
    house_11: { sign: 'Gemini', degree: 12.4, longitude: 72.4 },
    house_12: { sign: 'Cancer', degree: 10.9, longitude: 100.9 },
    ascendant: { sign: 'Leo', degree: 26.142947, longitude: 146.142947 },
    midheaven: { sign: 'Taurus', degree: 15.8, longitude: 45.8 },
    vertex: { sign: 'Aquarius', degree: 10.5, longitude: 310.5 }
  };

  it('renders house table with valid data', () => {
    render(<HouseTable houses={validHousesData} />);
    expect(screen.getByText('Houses & Angles')).toBeInTheDocument();
    expect(screen.getByText('🌅 Ascendant (Rising)')).toBeInTheDocument();
  });

  it('renders all 12 houses', () => {
    const { container } = render(<HouseTable houses={validHousesData} />);
    const houseRows = container.querySelectorAll('.house-row');
    expect(houseRows.length).toBe(12);
  });

  it('handles null houses gracefully', () => {
    const { container } = render(<HouseTable houses={null} />);
    expect(container.firstChild).toBeNull();
  });

  it('handles undefined houses gracefully', () => {
    const { container } = render(<HouseTable houses={undefined} />);
    expect(container.firstChild).toBeNull();
  });

  it('handles array instead of object gracefully', () => {
    const { container } = render(<HouseTable houses={[]} />);
    expect(container.firstChild).toBeNull();
  });

  it('handles empty object gracefully', () => {
    const { container } = render(<HouseTable houses={{}} />);
    expect(container.firstChild).toBeNull();
  });

  it('handles missing ascendant gracefully', () => {
    const housesWithoutAscendant = { ...validHousesData };
    delete housesWithoutAscendant.ascendant;
    delete housesWithoutAscendant.midheaven;
    
    render(<HouseTable houses={housesWithoutAscendant} />);
    expect(screen.getByText('Houses & Angles')).toBeInTheDocument();
    expect(screen.queryByText('🌅 Ascendant (Rising)')).not.toBeInTheDocument();
  });

  it('handles invalid house data gracefully', () => {
    const housesWithInvalidData = {
      house_1: { sign: 'Leo', degree: 'invalid', longitude: null },
      house_2: null,
      house_3: { sign: 'Libra', degree: 20.3, longitude: 200.3 }
    };
    
    const { container } = render(<HouseTable houses={housesWithInvalidData} />);
    // Should render without crashing
    expect(container.querySelector('.house-table')).toBeInTheDocument();
  });

  it('handles missing zodiac symbols gracefully', () => {
    const housesWithUnknownSign = {
      house_1: { sign: 'UnknownSign', degree: 26.142947, longitude: 146.142947 },
      ascendant: { sign: 'UnknownSign', degree: 26.142947, longitude: 146.142947 }
    };
    
    const { container } = render(<HouseTable houses={housesWithUnknownSign} />);
    expect(container.querySelector('.house-table')).toBeInTheDocument();
  });

  it('formats degrees correctly', () => {
    const housesWithSpecificDegree = {
      house_1: { sign: 'Leo', degree: 26.75, longitude: 146.75 }
    };
    
    render(<HouseTable houses={housesWithSpecificDegree} />);
    expect(screen.getByText("26°45'")).toBeInTheDocument();
  });

  it('displays house interpretations', () => {
    render(<HouseTable houses={validHousesData} />);
    expect(screen.getByText('House Interpretations')).toBeInTheDocument();
    expect(screen.getByText(/Self, Identity, Physical Body/)).toBeInTheDocument();
  });
});
