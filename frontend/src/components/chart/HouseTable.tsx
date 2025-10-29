import React from 'react';
import { HouseCusp } from '@/types/chart';
import './HouseTable.css';

export interface HouseTableProps {
  houses: { [houseKey: string]: HouseCusp };
  ascendant?: HouseCusp;
  midheaven?: HouseCusp;
}

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

const HOUSE_MEANINGS: { [key: number]: string } = {
  1: 'Self, Identity, Appearance',
  2: 'Values, Money, Possessions',
  3: 'Communication, Siblings, Local Travel',
  4: 'Home, Family, Roots',
  5: 'Creativity, Romance, Children',
  6: 'Health, Work, Service',
  7: 'Partnerships, Marriage',
  8: 'Transformation, Shared Resources',
  9: 'Philosophy, Higher Learning, Travel',
  10: 'Career, Public Life, Reputation',
  11: 'Friends, Groups, Hopes',
  12: 'Subconscious, Spirituality, Hidden Matters'
};

export default function HouseTable({ houses, ascendant, midheaven }: HouseTableProps) {
  const formatDegree = (degree: number): string => {
    const deg = Math.floor(degree);
    const min = Math.floor((degree - deg) * 60);
    const sec = Math.floor(((degree - deg) * 60 - min) * 60);
    return `${deg}°${min}'${sec}"`;
  };

  // Extract house cusps from houses object
  const houseCusps: Array<{ number: number; cusp: HouseCusp }> = [];
  
  for (let i = 1; i <= 12; i++) {
    const houseKey = `house_${i}`;
    if (houses[houseKey]) {
      houseCusps.push({ number: i, cusp: houses[houseKey] });
    }
  }

  return (
    <div className="house-table-container">
      <h2 className="house-table-title">
        <span className="house-table-icon">🏠</span>
        House System
      </h2>

      {/* Special Points */}
      {(ascendant || midheaven) && (
        <div className="special-points">
          {ascendant && (
            <div className="special-point">
              <span className="special-point-label">⬆️ Ascendant (ASC)</span>
              <span className="special-point-sign">
                <span className="sign-symbol">{SIGN_SYMBOLS[ascendant.sign] || ''}</span>
                {ascendant.sign}
              </span>
              <span className="special-point-degree">{formatDegree(ascendant.degree)}</span>
            </div>
          )}
          {midheaven && (
            <div className="special-point">
              <span className="special-point-label">🔝 Midheaven (MC)</span>
              <span className="special-point-sign">
                <span className="sign-symbol">{SIGN_SYMBOLS[midheaven.sign] || ''}</span>
                {midheaven.sign}
              </span>
              <span className="special-point-degree">{formatDegree(midheaven.degree)}</span>
            </div>
          )}
        </div>
      )}
      
      <div className="house-table-wrapper">
        <table className="house-table">
          <thead>
            <tr>
              <th>House</th>
              <th>Sign</th>
              <th>Cusp Degree</th>
              <th>Areas of Life</th>
            </tr>
          </thead>
          <tbody>
            {houseCusps.map(({ number, cusp }) => (
              <tr key={number} className="house-row">
                <td className="house-number">
                  <span className="house-number-badge">{number}</span>
                </td>
                <td>
                  <span className="sign-symbol" title={cusp.sign}>
                    {SIGN_SYMBOLS[cusp.sign] || ''}
                  </span>
                  <span className="sign-name">{cusp.sign}</span>
                </td>
                <td className="house-degree">
                  {formatDegree(cusp.degree)}
                </td>
                <td className="house-meaning">
                  {HOUSE_MEANINGS[number]}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="house-table-footer">
        <p className="house-count">
          {houseCusps.length} house cusps calculated
        </p>
      </div>
    </div>
  );
}
