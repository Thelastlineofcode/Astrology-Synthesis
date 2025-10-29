---
title: "Build Interactive Chart Canvas (SVG)"
labels: ["component:chart", "P1-High", "feature", "visualization"]
assignees: []
milestone: "Milestone 2: Core Features"
---

## 🎯 Objective

Create an interactive SVG natal chart wheel with zoom, pan, and hover tooltips for planets and aspects. This replaces or enhances the existing static chart display with modern interactivity.

## 📋 Description

The natal chart is the centerpiece of the application. Users should be able to interact with the chart wheel to explore planetary positions, aspects, and house divisions. The chart must be accurate, beautiful, and accessible.

## 🔗 References

- **Design Artifact**: `COMPONENT_STRUCTURE.md` (Chart Viewer section)
- **Design Artifact**: `DESIGN_INSPIRATION.md` (Data Visualization)
- **Guide**: `AI_COPILOT_GUIDE.md` - Accessibility Requirements
- **Epic**: #4 (Enhanced Natal Chart Viewer)

## ✅ Acceptance Criteria

- [ ] Chart wheel rendered as SVG (not canvas or image)
- [ ] All 12 houses displayed with division lines
- [ ] Planet glyphs positioned accurately based on longitude
- [ ] Zodiac signs shown around wheel perimeter
- [ ] Aspect lines drawn between planets (major aspects)
- [ ] Aspect lines toggleable (show/hide)
- [ ] Hover tooltips show planet details (name, position, retrograde status)
- [ ] Zoom controls (+/- buttons) functional
- [ ] Chart scales responsively on mobile/tablet/desktop
- [ ] No layout breaks when chart is resized
- [ ] Export chart as PNG/SVG option (bonus)
- [ ] Print-friendly view available

## 💻 Implementation Notes

### Chart Structure

```jsx
// /frontend/src/components/chart/ChartCanvas.jsx
import React, { useState, useRef } from 'react';
import './ChartCanvas.css';

const ChartCanvas = ({ chartData }) => {
  const [showAspects, setShowAspects] = useState(true);
  const [zoom, setZoom] = useState(1);
  const [hoveredPlanet, setHoveredPlanet] = useState(null);
  const svgRef = useRef(null);
  
  // Calculate positions
  const centerX = 300;
  const centerY = 300;
  const radius = 250;
  
  const calculatePosition = (longitude) => {
    // Convert longitude to radians (starting at 0° Aries at 9 o'clock)
    const angle = (longitude - 90) * (Math.PI / 180);
    return {
      x: centerX + radius * Math.cos(angle),
      y: centerY + radius * Math.sin(angle)
    };
  };
  
  const handleZoomIn = () => setZoom(Math.min(zoom + 0.2, 2));
  const handleZoomOut = () => setZoom(Math.max(zoom - 0.2, 0.5));
  
  return (
    <div className="chart-canvas">
      <div className="chart-controls">
        <button onClick={handleZoomOut} aria-label="Zoom out">−</button>
        <span>{Math.round(zoom * 100)}%</span>
        <button onClick={handleZoomIn} aria-label="Zoom in">+</button>
        
        <label>
          <input
            type="checkbox"
            checked={showAspects}
            onChange={(e) => setShowAspects(e.target.checked)}
          />
          Show Aspects
        </label>
      </div>
      
      <svg
        ref={svgRef}
        viewBox="0 0 600 600"
        className="chart-svg"
        style={{ transform: `scale(${zoom})` }}
        role="img"
        aria-label="Natal chart wheel"
      >
        {/* Chart background circle */}
        <circle
          cx={centerX}
          cy={centerY}
          r={radius}
          fill="var(--bg-secondary)"
          stroke="var(--border-color)"
          strokeWidth="2"
        />
        
        {/* House divisions */}
        {chartData.houses && Object.entries(chartData.houses).map(([key, house], index) => {
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
              strokeWidth="1"
              opacity="0.4"
            />
          );
        })}
        
        {/* Planets */}
        {chartData.planets && chartData.planets.map((planet) => {
          const pos = calculatePosition(planet.longitude);
          return (
            <g
              key={planet.name}
              onMouseEnter={() => setHoveredPlanet(planet)}
              onMouseLeave={() => setHoveredPlanet(null)}
            >
              <circle
                cx={pos.x}
                cy={pos.y}
                r="8"
                fill="var(--color-accent)"
                stroke="var(--color-primary)"
                strokeWidth="2"
              />
              <text
                x={pos.x}
                y={pos.y}
                textAnchor="middle"
                dominantBaseline="middle"
                fontSize="10"
                fill="var(--text-primary)"
              >
                {planet.symbol || planet.name[0]}
              </text>
            </g>
          );
        })}
        
        {/* Aspect lines */}
        {showAspects && chartData.aspects && chartData.aspects.map((aspect, i) => {
          const planet1 = chartData.planets.find(p => p.name === aspect.planet1);
          const planet2 = chartData.planets.find(p => p.name === aspect.planet2);
          if (!planet1 || !planet2) return null;
          
          const pos1 = calculatePosition(planet1.longitude);
          const pos2 = calculatePosition(planet2.longitude);
          
          // Color by aspect type
          const aspectColors = {
            conjunction: 'var(--color-success)',
            opposition: 'var(--color-error)',
            trine: 'var(--color-success)',
            square: 'var(--color-error)',
            sextile: 'var(--color-info)'
          };
          
          return (
            <line
              key={`aspect-${i}`}
              x1={pos1.x}
              y1={pos1.y}
              x2={pos2.x}
              y2={pos2.y}
              stroke={aspectColors[aspect.type] || 'var(--color-info)'}
              strokeWidth="1"
              opacity="0.5"
              strokeDasharray={aspect.type === 'sextile' ? '3,3' : '0'}
            />
          );
        })}
      </svg>
      
      {/* Hover tooltip */}
      {hoveredPlanet && (
        <div className="chart-tooltip" role="tooltip">
          <strong>{hoveredPlanet.name}</strong>
          <div>{hoveredPlanet.sign} {hoveredPlanet.degree.toFixed(2)}°</div>
          <div>House {hoveredPlanet.house}</div>
          {hoveredPlanet.retrograde && <div>Retrograde ℞</div>}
        </div>
      )}
    </div>
  );
};

export default ChartCanvas;
```

### Styling

```css
/* /frontend/src/components/chart/ChartCanvas.css */
.chart-canvas {
  position: relative;
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}

.chart-controls {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
  padding: var(--space-3);
  background: var(--bg-secondary);
  border-radius: 8px;
}

.chart-controls button {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-primary);
  color: var(--color-neutral-light);
  border: none;
  font-size: 24px;
  cursor: pointer;
  transition: transform 150ms ease;
}

.chart-controls button:hover:not(:disabled) {
  transform: scale(1.1);
}

.chart-svg {
  width: 100%;
  height: auto;
  transition: transform 250ms ease;
}

.chart-svg g {
  cursor: pointer;
}

.chart-tooltip {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: var(--bg-secondary);
  padding: var(--space-3);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  pointer-events: none;
  z-index: 10;
}

/* Responsive */
@media (max-width: 767px) {
  .chart-canvas {
    max-width: 100%;
  }
  
  .chart-controls {
    flex-wrap: wrap;
  }
}
```

## 🧪 Testing Checklist

- [ ] Chart renders correctly with sample data (Metairie, LA Dec 19, 1984)
- [ ] All 12 houses visible
- [ ] All planets positioned accurately (verify with ephemeris)
- [ ] Aspect lines draw correctly
- [ ] Toggle aspects on/off works
- [ ] Zoom in/out functions smoothly (no layout breaks)
- [ ] Hover tooltips appear and disappear correctly
- [ ] Tooltips don't overflow viewport edges
- [ ] Chart responsive on mobile (375px), tablet (768px), desktop (1440px)
- [ ] No console errors when interacting with chart
- [ ] Chart accessible via keyboard (tab to planets, show tooltip on focus)
- [ ] Screen reader announces chart presence and planet count

## 🔍 Accessibility Requirements

- [ ] SVG has `role="img"` and descriptive `aria-label`
- [ ] Planet elements keyboard focusable (tabindex="0")
- [ ] Tooltips appear on focus (not just hover)
- [ ] Zoom controls have clear `aria-label`
- [ ] Aspect toggle checkbox properly labeled
- [ ] High contrast mode: lines and planets remain visible
- [ ] Tooltips use `role="tooltip"` and proper ARIA

## 📦 Files to Create/Modify

- `frontend/src/components/chart/ChartCanvas.jsx` (create)
- `frontend/src/components/chart/ChartCanvas.css` (create)
- `frontend/src/components/chart/ChartCanvas.test.jsx` (create)
- `frontend/src/components/chart/NatalChart.jsx` (modify to use ChartCanvas)

## 🔗 Dependencies

- Issue #14 (Chart Input Form) - Need chart data structure
- Issue #3 (Button Component) - For zoom controls

## 🚫 Blocked By

- None (can use mock data for development)

## 📝 Additional Notes

- Use existing Swiss Ephemeris data from backend API
- Planet symbols: Consider using Unicode symbols or SVG icons
- Consider using D3.js for complex calculations (optional)
- Export feature can be phase 2 (not blocking)
- Performance: Optimize for charts with many aspects (50+)

---

**Priority**: P1 (High)  
**Estimated Effort**: 12 hours  
**Assignee**: TBD  
**Epic**: Epic 4 - Enhanced Natal Chart Viewer
