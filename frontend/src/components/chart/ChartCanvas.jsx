"use client";

import React, { useState, useRef } from 'react';
import './ChartCanvas.css';

/**
 * Interactive SVG Natal Chart Canvas
 * 
 * Renders an interactive natal chart wheel with:
 * - 12 houses with division lines
 * - Planet glyphs positioned by longitude
 * - Zodiac signs around perimeter
 * - Aspect lines between planets (toggleable)
 * - Hover tooltips with planet details
 * - Zoom controls (+/- buttons)
 * 
 * @param {Object} chartData - Chart data containing planets, houses, aspects
 * @param {Array} chartData.planets - Array of planet objects with name, longitude, sign, degree, house, retrograde
 * @param {Object} chartData.houses - Object with house cusps (house_1 through house_12)
 * @param {Array} chartData.aspects - Array of aspect objects with planet1, planet2, type, orb
 * 
 * @accessibility
 * - SVG has role="img" and aria-label
 * - Planet elements are keyboard focusable
 * - Tooltips appear on focus (not just hover)
 * - Zoom controls have clear aria-labels
 * - High contrast mode compatible
 */
const ChartCanvas = ({ chartData }) => {
  const [showAspects, setShowAspects] = useState(true);
  const [zoom, setZoom] = useState(1);
  const [hoveredPlanet, setHoveredPlanet] = useState(null);
  const svgRef = useRef(null);
  
  // Chart dimensions
  const centerX = 300;
  const centerY = 300;
  const radius = 250;
  
  /**
   * Calculate position on chart wheel from longitude
   * Astrological charts start at 0° Aries at 9 o'clock position
   */
  const calculatePosition = (longitude, customRadius = radius) => {
    // Convert longitude to radians (starting at 0° Aries at 9 o'clock)
    const angle = (longitude - 90) * (Math.PI / 180);
    return {
      x: centerX + customRadius * Math.cos(angle),
      y: centerY + customRadius * Math.sin(angle)
    };
  };
  
  /**
   * Get planet symbol (Unicode or fallback to first letter)
   */
  const getPlanetSymbol = (planet) => {
    const symbols = {
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
      'Ascendant': 'AC',
      'Midheaven': 'MC'
    };
    return symbols[planet.name] || planet.name[0];
  };
  
  /**
   * Get zodiac sign symbol
   */
  const getZodiacSymbol = (sign) => {
    const symbols = {
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
    return symbols[sign] || sign;
  };
  
  const handleZoomIn = () => setZoom(Math.min(zoom + 0.2, 2));
  const handleZoomOut = () => setZoom(Math.max(zoom - 0.2, 0.5));
  
  // Handle keyboard events for planet elements
  const handlePlanetKeyDown = (e, planet) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      setHoveredPlanet(planet);
    } else if (e.key === 'Escape') {
      setHoveredPlanet(null);
    }
  };
  
  // If no chart data provided, show placeholder
  if (!chartData || !chartData.planets) {
    return (
      <div className="chart-canvas">
        <div className="chart-placeholder">
          <p>No chart data available. Please generate a chart first.</p>
        </div>
      </div>
    );
  }
  
  // Aspect color mapping
  const aspectColors = {
    conjunction: 'var(--color-success)',
    opposition: 'var(--color-error)',
    trine: 'var(--color-success)',
    square: 'var(--color-error)',
    sextile: 'var(--color-info)'
  };
  
  return (
    <div className="chart-canvas">
      {/* Controls */}
      <div className="chart-controls">
        <button 
          onClick={handleZoomOut} 
          aria-label="Zoom out"
          className="zoom-button"
          disabled={zoom <= 0.5}
        >
          −
        </button>
        <span className="zoom-level">{Math.round(zoom * 100)}%</span>
        <button 
          onClick={handleZoomIn} 
          aria-label="Zoom in"
          className="zoom-button"
          disabled={zoom >= 2}
        >
          +
        </button>
        
        <label className="aspect-toggle">
          <input
            type="checkbox"
            checked={showAspects}
            onChange={(e) => setShowAspects(e.target.checked)}
            aria-label="Toggle aspect lines visibility"
          />
          Show Aspects
        </label>
      </div>
      
      {/* SVG Chart */}
      <div className="chart-container">
        <svg
          ref={svgRef}
          viewBox="0 0 600 600"
          className="chart-svg"
          style={{ transform: `scale(${zoom})` }}
          role="img"
          aria-label={`Natal chart wheel with ${chartData.planets.length} planets`}
        >
          {/* Background circle */}
          <circle
            cx={centerX}
            cy={centerY}
            r={radius}
            fill="var(--bg-secondary)"
            stroke="var(--border-color)"
            strokeWidth="2"
          />
          
          {/* Inner circles for visual reference */}
          <circle
            cx={centerX}
            cy={centerY}
            r={radius * 0.8}
            fill="none"
            stroke="var(--border-color)"
            strokeWidth="1"
            opacity="0.3"
          />
          <circle
            cx={centerX}
            cy={centerY}
            r={radius * 0.6}
            fill="none"
            stroke="var(--border-color)"
            strokeWidth="1"
            opacity="0.3"
          />
          
          {/* Zodiac signs around perimeter */}
          {['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'].map((sign, index) => {
            const longitude = index * 30; // Each sign is 30 degrees
            const pos = calculatePosition(longitude, radius * 0.95);
            return (
              <text
                key={sign}
                x={pos.x}
                y={pos.y}
                textAnchor="middle"
                dominantBaseline="middle"
                fontSize="16"
                fill="var(--text-secondary)"
                className="zodiac-sign"
              >
                {getZodiacSymbol(sign)}
              </text>
            );
          })}
          
          {/* House divisions */}
          {chartData.houses && Object.entries(chartData.houses).map(([key, house]) => {
            if (!key.startsWith('house_')) return null;
            const pos = calculatePosition(house.longitude);
            return (
              <line
                key={key}
                x1={centerX}
                y1={centerY}
                x2={pos.x}
                y2={pos.y}
                stroke="var(--color-primary)"
                strokeWidth="1.5"
                opacity="0.5"
              />
            );
          })}
          
          {/* Aspect lines */}
          {showAspects && chartData.aspects && chartData.aspects.map((aspect, i) => {
            const planet1 = chartData.planets.find(p => p.name === aspect.planet1);
            const planet2 = chartData.planets.find(p => p.name === aspect.planet2);
            if (!planet1 || !planet2) return null;
            
            const pos1 = calculatePosition(planet1.longitude, radius * 0.6);
            const pos2 = calculatePosition(planet2.longitude, radius * 0.6);
            
            return (
              <line
                key={`aspect-${i}`}
                x1={pos1.x}
                y1={pos1.y}
                x2={pos2.x}
                y2={pos2.y}
                stroke={aspectColors[aspect.type] || 'var(--color-info)'}
                strokeWidth="1.5"
                opacity="0.4"
                strokeDasharray={aspect.type === 'sextile' ? '4,4' : '0'}
              />
            );
          })}
          
          {/* Planets */}
          {chartData.planets.map((planet) => {
            const pos = calculatePosition(planet.longitude, radius * 0.8);
            return (
              <g
                key={planet.name}
                className="planet-group"
                onMouseEnter={() => setHoveredPlanet(planet)}
                onMouseLeave={() => setHoveredPlanet(null)}
                onFocus={() => setHoveredPlanet(planet)}
                onBlur={() => setHoveredPlanet(null)}
                onKeyDown={(e) => handlePlanetKeyDown(e, planet)}
                tabIndex={0}
                role="button"
                aria-label={`${planet.name} at ${planet.degree.toFixed(2)} degrees ${planet.sign}${planet.retrograde ? ', retrograde' : ''}`}
              >
                <circle
                  cx={pos.x}
                  cy={pos.y}
                  r="14"
                  fill="var(--bg-secondary)"
                  stroke="var(--color-primary)"
                  strokeWidth="2"
                  className="planet-bg"
                />
                <text
                  x={pos.x}
                  y={pos.y}
                  textAnchor="middle"
                  dominantBaseline="middle"
                  fontSize="12"
                  fill="var(--color-primary)"
                  className="planet-symbol"
                  pointerEvents="none"
                >
                  {getPlanetSymbol(planet)}
                </text>
                {planet.retrograde && (
                  <text
                    x={pos.x + 12}
                    y={pos.y - 12}
                    textAnchor="middle"
                    fontSize="10"
                    fill="var(--color-error)"
                    className="retrograde-indicator"
                    pointerEvents="none"
                  >
                    ℞
                  </text>
                )}
              </g>
            );
          })}
        </svg>
        
        {/* Hover tooltip */}
        {hoveredPlanet && (
          <div className="chart-tooltip" role="tooltip" aria-live="polite">
            <strong>{hoveredPlanet.name}</strong>
            <div>{hoveredPlanet.sign} {hoveredPlanet.degree.toFixed(2)}°</div>
            <div>House {hoveredPlanet.house}</div>
            {hoveredPlanet.retrograde && <div className="retrograde">Retrograde ℞</div>}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChartCanvas;
