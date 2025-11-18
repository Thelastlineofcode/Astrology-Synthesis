import React from "react";
import { ChartData } from "@/types/chart";
import "./ChartCanvas.css";

export interface ChartCanvasProps {
  chartData: ChartData;
  width?: number;
  height?: number;
}

const PLANET_SYMBOLS: { [key: string]: string } = {
  Sun: "☉",
  Moon: "☽",
  Mercury: "☿",
  Venus: "♀",
  Mars: "♂",
  Jupiter: "♃",
  Saturn: "♄",
  Uranus: "♅",
  Neptune: "♆",
  Pluto: "♇",
  "North Node": "☊",
  "South Node": "☋",
  Chiron: "⚷",
};

const SIGN_SYMBOLS: { [key: string]: string } = {
  Aries: "♈",
  Taurus: "♉",
  Gemini: "♊",
  Cancer: "♋",
  Leo: "♌",
  Virgo: "♍",
  Libra: "♎",
  Scorpio: "♏",
  Sagittarius: "♐",
  Capricorn: "♑",
  Aquarius: "♒",
  Pisces: "♓",
};

const SIGNS_ORDER = [
  "Aries",
  "Taurus",
  "Gemini",
  "Cancer",
  "Leo",
  "Virgo",
  "Libra",
  "Scorpio",
  "Sagittarius",
  "Capricorn",
  "Aquarius",
  "Pisces",
];

export default function ChartCanvas({
  chartData,
  width = 500,
  height = 500,
}: ChartCanvasProps) {
  const centerX = width / 2;
  const centerY = height / 2;
  const outerRadius = Math.min(width, height) * 0.45;
  const signRadius = outerRadius * 0.9; // Outer ring for zodiac signs
  const degreeOuterRadius = outerRadius * 0.75; // Outer edge of degree ring
  const degreeInnerRadius = outerRadius * 0.65; // Inner edge of degree ring
  const middleRadius = outerRadius * 0.6; // Planet ring
  const innerRadius = outerRadius * 0.45; // Inner circle

  // Round to 6 decimal places to prevent hydration mismatches
  const round = (num: number): number => {
    return Math.round(num * 1000000) / 1000000;
  };

  // Calculate position on circle
  const getPosition = (
    degree: number,
    radius: number
  ): { x: number; y: number } => {
    // Convert to radians and adjust so 0° is at 9 o'clock (left) and increases counterclockwise
    const angle = (180 - degree) * (Math.PI / 180);
    return {
      x: round(centerX + radius * Math.cos(angle)),
      y: round(centerY - radius * Math.sin(angle)),
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

      // Calculate path for segment (signs in outer ring)
      const startOuter = {
        x: round(centerX + outerRadius * Math.cos(startRad)),
        y: round(centerY - outerRadius * Math.sin(startRad)),
      };
      const endOuter = {
        x: round(centerX + outerRadius * Math.cos(endRad)),
        y: round(centerY - outerRadius * Math.sin(endRad)),
      };
      const startSign = {
        x: round(centerX + signRadius * Math.cos(startRad)),
        y: round(centerY - signRadius * Math.sin(startRad)),
      };
      const endSign = {
        x: round(centerX + signRadius * Math.cos(endRad)),
        y: round(centerY - signRadius * Math.sin(endRad)),
      };

      // Position for sign symbol
      const symbolRadius = (outerRadius + signRadius) / 2;
      const symbolPos = {
        x: round(centerX + symbolRadius * Math.cos(midRad)),
        y: round(centerY - symbolRadius * Math.sin(midRad)),
      };

      const pathData = `
        M ${startOuter.x} ${startOuter.y}
        A ${outerRadius} ${outerRadius} 0 0 0 ${endOuter.x} ${endOuter.y}
        L ${endSign.x} ${endSign.y}
        A ${signRadius} ${signRadius} 0 0 1 ${startSign.x} ${startSign.y}
        Z
      `;

      segments.push(
        <g key={sign}>
          <path
            d={pathData}
            className={`zodiac-segment zodiac-${sign.toLowerCase()}`}
            stroke="var(--color-primary)"
            strokeWidth="1"
            fill={
              index % 2 === 0
                ? "rgba(100, 100, 200, 0.05)"
                : "rgba(150, 150, 255, 0.05)"
            }
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

  // Draw degree ring with degree markers
  const drawDegreeRing = () => {
    const degreeMarkers: React.ReactElement[] = [];

    // Draw major degree lines every 5 degrees
    for (let deg = 0; deg < 360; deg += 5) {
      const adjustedDeg = deg - ascendantDegree;
      const normalizedDeg = adjustedDeg < 0 ? adjustedDeg + 360 : adjustedDeg;

      const outerPos = getPosition(normalizedDeg, degreeOuterRadius);
      const innerPos = getPosition(normalizedDeg, degreeInnerRadius);

      // Major line every 10 degrees
      const isMajor = deg % 10 === 0;

      degreeMarkers.push(
        <line
          key={`deg-${deg}`}
          x1={outerPos.x}
          y1={outerPos.y}
          x2={innerPos.x}
          y2={innerPos.y}
          stroke="var(--color-primary)"
          strokeWidth={isMajor ? "1.5" : "0.5"}
          opacity={isMajor ? "0.6" : "0.3"}
        />
      );

      // Add degree text every 30 degrees (at sign boundaries)
      if (deg % 30 === 0) {
        const textRadius = (degreeOuterRadius + degreeInnerRadius) / 2;
        const textPos = getPosition(normalizedDeg, textRadius);

        degreeMarkers.push(
          <text
            key={`deg-text-${deg}`}
            x={textPos.x}
            y={textPos.y}
            textAnchor="middle"
            dominantBaseline="middle"
            fontSize="10"
            fill="var(--text-secondary)"
            fontWeight="bold"
          >
            {deg}°
          </text>
        );
      }
    }

    // Draw inner and outer circles for degree ring
    degreeMarkers.push(
      <circle
        key="degree-ring-outer"
        cx={centerX}
        cy={centerY}
        r={degreeOuterRadius}
        fill="none"
        stroke="var(--color-primary)"
        strokeWidth="1"
        opacity="0.4"
      />
    );

    degreeMarkers.push(
      <circle
        key="degree-ring-inner"
        cx={centerX}
        cy={centerY}
        r={degreeInnerRadius}
        fill="none"
        stroke="var(--color-primary)"
        strokeWidth="1"
        opacity="0.4"
      />
    );

    return degreeMarkers;
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
        const degreeTextPos = getPosition(
          adjustedDegree,
          degreeInnerRadius - 10
        );

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
            {/* Show house cusp degree */}
            <text
              x={degreeTextPos.x}
              y={degreeTextPos.y}
              textAnchor="middle"
              dominantBaseline="middle"
              fontSize="8"
              fill="var(--text-secondary)"
            >
              {house.longitude.toFixed(1)}°
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
              stroke={planet.retrograde ? "#ef4444" : "var(--color-accent)"}
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
            {/* Show exact degree below planet */}
            <text
              x={pos.x}
              y={pos.y + 24}
              textAnchor="middle"
              fontSize="9"
              fill="var(--text-secondary)"
              fontWeight="normal"
            >
              {planet.longitude.toFixed(1)}°
            </text>
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

          {/* Degree ring with markers */}
          {drawDegreeRing()}

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
          <span
            className="legend-color"
            style={{ background: "#10b981" }}
          ></span>
          <span>Direct Motion</span>
        </div>
        <div className="legend-item">
          <span
            className="legend-color"
            style={{ background: "#ef4444" }}
          ></span>
          <span>Retrograde ℞</span>
        </div>
      </div>
    </div>
  );
}
