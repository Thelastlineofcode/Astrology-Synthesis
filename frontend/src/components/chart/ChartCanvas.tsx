import React from 'react';
import { ChartData } from '@/types/chart';
import './ChartCanvas.css';

export interface ChartCanvasProps {
  chartData: ChartData;
  width?: number;
  height?: number;
}

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

const SIGNS_ORDER = [
  'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
  'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
];

export default function ChartCanvas({ chartData, width = 500, height = 500 }: ChartCanvasProps) {
  const centerX = width / 2;
  const centerY = height / 2;
  const outerRadius = Math.min(width, height) * 0.45;
  const middleRadius = outerRadius * 0.75;
  const innerRadius = outerRadius * 0.5;

  // Calculate position on circle
  const getPosition = (degree: number, radius: number): { x: number; y: number } => {
    // Convert to radians and adjust so 0° is at 9 o'clock (left) and increases counterclockwise
    const angle = (180 - degree) * (Math.PI / 180);
    return {
      x: centerX + radius * Math.cos(angle),
      y: centerY - radius * Math.sin(angle)
    };
  };

  // Get ascendant degree for chart rotation
  const ascendantDegree = chartData.ascendant?.longitude || 0;

  // Adjust planet longitude relative to ascendant
  const adjustDegree = (longitude: number): number => {
    const adjusted = longitude - ascendantDegree;
    return adjusted < 0 ? adjusted + 360 : adjusted;
  };

  // Draw zodiac wheel
  const drawZodiacWheel = () => {
    const segments: React.ReactElement[] = [];
    const signSize = 360 / 12;

    SIGNS_ORDER.forEach((sign, index) => {
      const startAngle = index * signSize - ascendantDegree;
      const endAngle = startAngle + signSize;
      
      // Convert angles to radians (0° is at 9 o'clock, counterclockwise)
      const startRad = (180 - startAngle) * (Math.PI / 180);
      const endRad = (180 - endAngle) * (Math.PI / 180);
      const midRad = (180 - (startAngle + signSize / 2)) * (Math.PI / 180);

      // Calculate path for segment
      const startOuter = {
        x: centerX + outerRadius * Math.cos(startRad),
        y: centerY - outerRadius * Math.sin(startRad)
      };
      const endOuter = {
        x: centerX + outerRadius * Math.cos(endRad),
        y: centerY - outerRadius * Math.sin(endRad)
      };
      const startMiddle = {
        x: centerX + middleRadius * Math.cos(startRad),
        y: centerY - middleRadius * Math.sin(startRad)
      };
      const endMiddle = {
        x: centerX + middleRadius * Math.cos(endRad),
        y: centerY - middleRadius * Math.sin(endRad)
      };

      // Position for sign symbol
      const symbolRadius = (outerRadius + middleRadius) / 2;
      const symbolPos = {
        x: centerX + symbolRadius * Math.cos(midRad),
        y: centerY - symbolRadius * Math.sin(midRad)
      };

      const pathData = `
        M ${startOuter.x} ${startOuter.y}
        A ${outerRadius} ${outerRadius} 0 0 0 ${endOuter.x} ${endOuter.y}
        L ${endMiddle.x} ${endMiddle.y}
        A ${middleRadius} ${middleRadius} 0 0 1 ${startMiddle.x} ${startMiddle.y}
        Z
      `;

      segments.push(
        <g key={sign}>
          <path
            d={pathData}
            className={`zodiac-segment zodiac-${sign.toLowerCase()}`}
            stroke="var(--color-primary)"
            strokeWidth="1"
            fill={index % 2 === 0 ? 'rgba(100, 100, 200, 0.05)' : 'rgba(150, 150, 255, 0.05)'}
          />
          <text
            x={symbolPos.x}
            y={symbolPos.y}
            textAnchor="middle"
            dominantBaseline="middle"
            className="zodiac-symbol"
            fontSize="20"
            fill="var(--color-accent)"
          >
            {SIGN_SYMBOLS[sign]}
          </text>
        </g>
      );
    });

    return segments;
  };

  // Draw house divisions
  const drawHouses = () => {
    const houses: React.ReactElement[] = [];
    
    for (let i = 1; i <= 12; i++) {
      const houseKey = `house_${i}`;
      const house = chartData.houses[houseKey];
      
      if (house && house.longitude !== undefined) {
        const adjustedDegree = adjustDegree(house.longitude);
        const pos = getPosition(adjustedDegree, outerRadius);
        const innerPos = getPosition(adjustedDegree, innerRadius);

        houses.push(
          <g key={`house-${i}`}>
            <line
              x1={innerPos.x}
              y1={innerPos.y}
              x2={pos.x}
              y2={pos.y}
              stroke="var(--color-primary)"
              strokeWidth="2"
              className="house-line"
            />
            <text
              x={innerPos.x}
              y={innerPos.y}
              textAnchor="middle"
              dominantBaseline="middle"
              className="house-number"
              fontSize="14"
              fontWeight="bold"
              fill="var(--text-primary)"
            >
              {i}
            </text>
          </g>
        );
      }
    }

    return houses;
  };

  // Draw planets
  const drawPlanets = () => {
    const planets: React.ReactElement[] = [];
    const planetRadius = middleRadius * 0.85;

    Object.entries(chartData.planets).forEach(([name, planet]) => {
      if (planet && planet.longitude !== undefined) {
        const adjustedDegree = adjustDegree(planet.longitude);
        const pos = getPosition(adjustedDegree, planetRadius);

        planets.push(
          <g key={name} className="planet-marker">
            <circle
              cx={pos.x}
              cy={pos.y}
              r="16"
              fill="var(--bg-secondary)"
              stroke={planet.retrograde ? '#ef4444' : 'var(--color-accent)'}
              strokeWidth="2"
              className="planet-circle"
            />
            <text
              x={pos.x}
              y={pos.y}
              textAnchor="middle"
              dominantBaseline="middle"
              fontSize="16"
              fill="var(--text-primary)"
              className="planet-symbol-text"
            >
              {PLANET_SYMBOLS[name] || name[0]}
            </text>
            {planet.retrograde && (
              <text
                x={pos.x + 14}
                y={pos.y - 10}
                fontSize="10"
                fill="#ef4444"
                fontWeight="bold"
              >
                ℞
              </text>
            )}
          </g>
        );
      }
    });

    return planets;
  };

  // Draw ascendant marker
  const drawAscendant = () => {
    if (!chartData.ascendant) return null;

    const pos = getPosition(0, outerRadius * 1.05);
    
    return (
      <g className="ascendant-marker">
        <line
          x1={centerX}
          y1={centerY}
          x2={pos.x}
          y2={pos.y}
          stroke="var(--color-primary)"
          strokeWidth="3"
          className="ascendant-line"
        />
        <text
          x={pos.x + 10}
          y={pos.y}
          fontSize="14"
          fontWeight="bold"
          fill="var(--color-primary)"
        >
          ASC
        </text>
      </g>
    );
  };

  return (
    <div className="chart-canvas-container">
      <h2 className="chart-canvas-title">
        <span className="chart-canvas-icon">🌟</span>
        Birth Chart Wheel
      </h2>
      
      <div className="chart-svg-wrapper">
        <svg
          width={width}
          height={height}
          viewBox={`0 0 ${width} ${height}`}
          className="chart-svg"
        >
          {/* Background circle */}
          <circle
            cx={centerX}
            cy={centerY}
            r={outerRadius}
            fill="var(--bg-primary)"
            stroke="var(--color-primary)"
            strokeWidth="2"
          />

          {/* Zodiac wheel */}
          {drawZodiacWheel()}

          {/* Inner circle */}
          <circle
            cx={centerX}
            cy={centerY}
            r={innerRadius}
            fill="transparent"
            stroke="var(--color-primary)"
            strokeWidth="2"
          />

          {/* House divisions */}
          {drawHouses()}

          {/* Ascendant line */}
          {drawAscendant()}

          {/* Planets */}
          {drawPlanets()}
        </svg>
      </div>

      <div className="chart-canvas-legend">
        <div className="legend-item">
          <span className="legend-color" style={{ background: '#10b981' }}></span>
          <span>Direct Motion</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ background: '#ef4444' }}></span>
          <span>Retrograde ℞</span>
        </div>
      </div>
    </div>
  );
}
