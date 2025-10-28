import React from 'react';
import './HouseTable.css';

const ZODIAC_SYMBOLS = {
  Aries: '♈',
  Taurus: '♉',
  Gemini: '♊',
  Cancer: '♋',
  Leo: '♌',
  Virgo: '♍',
  Libra: '♎',
  Scorpio: '♏',
  Sagittarius: '♐',
  Capricorn: '♑',
  Aquarius: '♒',
  Pisces: '♓'
};

const HouseTable = ({ houses, angles }) => {
  if (!houses || Object.keys(houses).length === 0) return null;

  const formatDegree = (degree) => {
    const deg = Math.floor(degree);
    const min = Math.floor((degree - deg) * 60);
    return `${deg}°${min}'`;
  };

  // Convert houses object to array for display
  const houseArray = [];
  for (let i = 1; i <= 12; i++) {
    const houseKey = `house_${i}`;
    if (houses[houseKey]) {
      houseArray.push({
        house: i,
        zodiacSign: houses[houseKey].sign,
        degree: houses[houseKey].degree,
        cusp: houses[houseKey].longitude
      });
    }
  }

  return (
    <div className="house-table">
      <h2>Houses & Angles</h2>
      
      {houses.ascendant && (
        <div className="angles-section">
          <div className="angle-card ascendant">
            <div className="angle-label">🌅 Ascendant (Rising)</div>
            <div className="angle-value">
              <span className="zodiac-symbol">{ZODIAC_SYMBOLS[houses.ascendant.sign]}</span>
              <span className="sign-name">{houses.ascendant.sign}</span>
              <span className="degree">
                {formatDegree(houses.ascendant.degree)}
              </span>
            </div>
          </div>
          
          <div className="angle-card midheaven">
            <div className="angle-label">🌠 Midheaven (MC)</div>
            <div className="angle-value">
              <span className="zodiac-symbol">{ZODIAC_SYMBOLS[houses.midheaven.sign]}</span>
              <span className="sign-name">{houses.midheaven.sign}</span>
              <span className="degree">
                {formatDegree(houses.midheaven.degree)}
              </span>
            </div>
          </div>
        </div>
      )}

      <div className="houses-table-container">
        <table className="houses-table">
          <thead>
            <tr>
              <th>House</th>
              <th>Sign</th>
              <th>Cusp Position</th>
              <th>Degrees</th>
            </tr>
          </thead>
          <tbody>
            {houseArray.map((house) => (
              <tr key={house.house} className={`house-row house-${house.house}`}>
                <td className="house-number">
                  <span className="house-badge">{house.house}</span>
                </td>
                <td className="house-sign">
                  <span className="zodiac-symbol-small">{ZODIAC_SYMBOLS[house.zodiacSign]}</span>
                  <span>{house.zodiacSign}</span>
                </td>
                <td className="house-position">
                  {formatDegree(house.degree)}
                </td>
                <td className="house-cusp monospace">
                  {house.cusp.toFixed(4)}°
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="house-meanings">
        <h3>House Interpretations</h3>
        <div className="meanings-grid">
          <div className="meaning-item">
            <strong>1st:</strong> Self, Identity, Physical Body
          </div>
          <div className="meaning-item">
            <strong>2nd:</strong> Values, Money, Possessions
          </div>
          <div className="meaning-item">
            <strong>3rd:</strong> Communication, Siblings, Learning
          </div>
          <div className="meaning-item">
            <strong>4th:</strong> Home, Family, Roots
          </div>
          <div className="meaning-item">
            <strong>5th:</strong> Creativity, Romance, Children
          </div>
          <div className="meaning-item">
            <strong>6th:</strong> Health, Work, Service
          </div>
          <div className="meaning-item">
            <strong>7th:</strong> Partnerships, Marriage, Others
          </div>
          <div className="meaning-item">
            <strong>8th:</strong> Transformation, Shared Resources
          </div>
          <div className="meaning-item">
            <strong>9th:</strong> Philosophy, Travel, Higher Learning
          </div>
          <div className="meaning-item">
            <strong>10th:</strong> Career, Public Image, Status
          </div>
          <div className="meaning-item">
            <strong>11th:</strong> Friends, Groups, Aspirations
          </div>
          <div className="meaning-item">
            <strong>12th:</strong> Spirituality, Subconscious, Hidden
          </div>
        </div>
      </div>
    </div>
  );
};

export default HouseTable;
