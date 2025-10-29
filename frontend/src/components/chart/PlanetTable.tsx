import React from 'react';
import { PlanetPosition } from '@/types/chart';
import './PlanetTable.css';

export interface PlanetTableProps {
  planets: { [planetName: string]: PlanetPosition | null };
}

const PLANET_ORDER = [
  'Sun', 'Moon', 'Mercury', 'Venus', 'Mars',
  'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto',
  'North Node', 'South Node', 'Chiron'
];

const PLANET_SYMBOLS: { [key: string]: string } = {
  'Sun': '☉',
  'Moon': '☽',
  'Mercury': '☿',
  'Venus': '♀',
  'Mars': '♂',
  'Jupiter': '♃',
  'Saturn': '♄',
  'Uranus': '♅',
  'Neptune': '♆',
  'Pluto': '♇',
  'North Node': '☊',
  'South Node': '☋',
  'Chiron': '⚷'
};

const SIGN_SYMBOLS: { [key: string]: string } = {
  'Aries': '♈',
  'Taurus': '♉',
  'Gemini': '♊',
  'Cancer': '♋',
  'Leo': '♌',
  'Virgo': '♍',
  'Libra': '♎',
  'Scorpio': '♏',
  'Sagittarius': '♐',
  'Capricorn': '♑',
  'Aquarius': '♒',
  'Pisces': '♓'
};

export default function PlanetTable({ planets }: PlanetTableProps) {
  const formatDegree = (degree: number): string => {
    const deg = Math.floor(degree);
    const min = Math.floor((degree - deg) * 60);
    const sec = Math.floor(((degree - deg) * 60 - min) * 60);
    return `${deg}°${min}'${sec}"`;
  };

  return (
    <div className="planet-table-container">
      <h2 className="planet-table-title">
        <span className="planet-table-icon">🪐</span>
        Planetary Positions
      </h2>
      
      <div className="planet-table-wrapper">
        <table className="planet-table">
          <thead>
            <tr>
              <th>Planet</th>
              <th>Sign</th>
              <th>Degree</th>
              <th>House</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {PLANET_ORDER.map((planetName) => {
              const planet = planets[planetName];
              
              if (!planet) {
                return (
                  <tr key={planetName} className="planet-row planet-unavailable">
                    <td>
                      <span className="planet-symbol" title={planetName}>
                        {PLANET_SYMBOLS[planetName] || ''}
                      </span>
                      <span className="planet-name">{planetName}</span>
                    </td>
                    <td colSpan={4} className="planet-unavailable-text">
                      Data unavailable
                    </td>
                  </tr>
                );
              }

              return (
                <tr key={planetName} className="planet-row">
                  <td>
                    <span className="planet-symbol" title={planetName}>
                      {PLANET_SYMBOLS[planetName] || ''}
                    </span>
                    <span className="planet-name">{planetName}</span>
                  </td>
                  <td>
                    <span className="sign-symbol" title={planet.sign}>
                      {SIGN_SYMBOLS[planet.sign] || ''}
                    </span>
                    <span className="sign-name">{planet.sign}</span>
                  </td>
                  <td className="planet-degree">
                    {formatDegree(planet.degree)}
                  </td>
                  <td className="planet-house">
                    {planet.house}
                  </td>
                  <td className="planet-status">
                    {planet.retrograde ? (
                      <span className="retrograde-badge" title="Retrograde">
                        ℞
                      </span>
                    ) : (
                      <span className="direct-badge" title="Direct">
                        D
                      </span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="planet-table-footer">
        <p className="planet-count">
          {Object.values(planets).filter(p => p !== null).length} of {PLANET_ORDER.length} planets calculated
        </p>
      </div>
    </div>
  );
}
