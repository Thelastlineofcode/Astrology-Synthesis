import React from 'react';
import './PlanetList.css';

const PLANET_SYMBOLS = {
  Sun: '☉',
  Moon: '☽',
  Mercury: '☿',
  Venus: '♀',
  Mars: '♂',
  Jupiter: '♃',
  Saturn: '♄',
  Uranus: '♅',
  Neptune: '♆',
  Pluto: '♇',
  NorthNode: '☊',
  Chiron: '⚷'
};

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

const PlanetList = ({ planets }) => {
  if (!planets) return null;

  const formatDegree = (degree) => {
    const deg = Math.floor(degree);
    const min = Math.floor((degree - deg) * 60);
    const sec = Math.floor(((degree - deg) * 60 - min) * 60);
    return `${deg}°${min}'${sec}"`;
  };

  const getPlanetColor = (planetName) => {
    const colors = {
      Sun: '#FFD700',
      Moon: '#C0C0C0',
      Mercury: '#FFA500',
      Venus: '#FF69B4',
      Mars: '#FF4500',
      Jupiter: '#4169E1',
      Saturn: '#8B4513',
      Uranus: '#00CED1',
      Neptune: '#9370DB',
      Pluto: '#8B0000',
      NorthNode: '#32CD32',
      Chiron: '#B8860B'
    };
    return colors[planetName] || '#666';
  };

  return (
    <div className="planet-list">
      <h2>Planetary Positions</h2>
      <div className="planets-container">
        {Object.entries(planets).map(([name, data]) => {
          if (!data) return null;
          
          return (
            <div 
              key={name} 
              className="planet-card"
              style={{'--planet-color': getPlanetColor(name)}}
            >
              <div className="planet-header">
                <div className="planet-name">
                  <span className="planet-symbol">{PLANET_SYMBOLS[name]}</span>
                  <span className="planet-text">{name}</span>
                </div>
                {data.retrograde && (
                  <span className="retrograde-badge" title="Retrograde">℞</span>
                )}
              </div>
              
              <div className="planet-info">
                <div className="info-row">
                  <span className="label">Sign:</span>
                  <span className="value">
                    <span className="zodiac-symbol">{ZODIAC_SYMBOLS[data.sign]}</span>
                    {data.sign}
                  </span>
                </div>
                
                <div className="info-row">
                  <span className="label">Position:</span>
                  <span className="value monospace">
                    {formatDegree(data.degree)}
                  </span>
                </div>
                
                {data.house && (
                  <div className="info-row">
                    <span className="label">House:</span>
                    <span className="value">{data.house}</span>
                  </div>
                )}
                
                <div className="info-row">
                  <span className="label">Longitude:</span>
                  <span className="value monospace">{data.longitude.toFixed(4)}°</span>
                </div>
                
                <div className="info-row">
                  <span className="label">Speed:</span>
                  <span className="value monospace">
                    {data.speed.toFixed(4)}°/day
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default PlanetList;
