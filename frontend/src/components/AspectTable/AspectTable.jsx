import React from 'react';
import './AspectTable.css';

const ASPECT_SYMBOLS = {
  conjunction: '☌', opposition: '☍', trine: '△',
  square: '□', sextile: '⚹', quincunx: '⚻',
  semisextile: '⚺', semisquare: '∠', sesquisquare: '⚼',
  quintile: 'Q', biquintile: 'bQ'
};

const AspectTable = ({ aspects }) => {
  if (!aspects || aspects.length === 0) return null;

  const getAspectColor = (aspect) => {
    const colors = {
      conjunction: '#FFD700', trine: '#4169E1', sextile: '#32CD32',
      square: '#FF4500', opposition: '#DC143C', quincunx: '#9370DB'
    };
    return colors[aspect] || '#718096';
  };

  return (
    <div className="aspect-table">
      <h2>Planetary Aspects</h2>
      <div className="aspects-container">
        {aspects.map((aspect, index) => (
          <div key={index} className="aspect-card" style={{'--aspect-color': getAspectColor(aspect.aspect)}}>
            <div className="aspect-planets">
              <span className="planet">{aspect.planet1}</span>
              <span className="aspect-symbol">{ASPECT_SYMBOLS[aspect.aspect]}</span>
              <span className="planet">{aspect.planet2}</span>
            </div>
            <div className="aspect-details">
              <span className="aspect-name">{aspect.aspect}</span>
              <span className="aspect-orb">Orb: {aspect.orb}°</span>
              <span className={`aspect-type ${aspect.isApplying ? 'applying' : 'separating'}`}>
                {aspect.isApplying ? '→ Applying' : '← Separating'}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AspectTable;
