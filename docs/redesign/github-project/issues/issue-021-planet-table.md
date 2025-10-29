---
title: "Display Planet List Table"
labels: ["component:chart", "P1-High", "data-display"]
assignees: []
milestone: "Milestone 2: Core Features"
---

## 🎯 Objective

Create a responsive table component displaying planet positions with columns: planet name, sign, degree, house, and retrograde status.

## 📋 Description

The planet list table is a key component of chart output, showing all planetary positions at a glance. Users should be able to quickly scan positions and identify retrograde planets.

## 🔗 References

- **Design Artifact**: `COMPONENT_STRUCTURE.md` (Chart Results - Planet List)
- **Design Artifact**: `UX_COPY_GUIDE.md` (Planet labels)
- **Existing Code**: `/frontend/src/components/PlanetList/PlanetList.jsx`

## ✅ Acceptance Criteria

- [ ] Table displays all planets (Sun, Moon, Mercury...Pluto, Nodes)
- [ ] Columns: Planet Name, Sign, Degree, House, Retrograde
- [ ] Planet glyphs/icons displayed (not just text names)
- [ ] Retrograde indicator (℞ symbol or badge)
- [ ] Degree formatted (e.g., "15°32'")
- [ ] Responsive: table on desktop, card list on mobile
- [ ] Sortable columns (optional)
- [ ] Hover highlights row
- [ ] Loading skeleton while calculating
- [ ] Print-friendly layout

## 💻 Implementation Notes

### Planet Table Component

```jsx
// /frontend/src/components/chart/PlanetTable.jsx
import React from 'react';
import Card from '../shared/Card';
import Badge from '../shared/Badge';
import './PlanetTable.css';

const planetGlyphs = {
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
  'North Node': '☊',
  'South Node': '☋'
};

const PlanetTable = ({ planets, loading }) => {
  if (loading) {
    return (
      <Card>
        <h3>Planet Positions</h3>
        <div className="planet-table-skeleton">
          {Array.from({ length: 10 }).map((_, i) => (
            <div key={i} className="skeleton-row" />
          ))}
        </div>
      </Card>
    );
  }
  
  const formatDegree = (degree) => {
    const deg = Math.floor(degree);
    const min = Math.floor((degree - deg) * 60);
    return `${deg}°${min.toString().padStart(2, '0')}'`;
  };
  
  return (
    <Card className="planet-table-card">
      <h3>Planet Positions</h3>
      
      {/* Desktop: Table */}
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
          {planets.map((planet) => (
            <tr key={planet.name} className="planet-table__row">
              <td className="planet-table__planet">
                <span className="planet-glyph" aria-hidden="true">
                  {planetGlyphs[planet.name] || ''}
                </span>
                <span className="planet-name">{planet.name}</span>
              </td>
              <td className="planet-table__sign">{planet.sign}</td>
              <td className="planet-table__degree">
                {formatDegree(planet.degree)}
              </td>
              <td className="planet-table__house">
                {planet.house}
              </td>
              <td className="planet-table__status">
                {planet.retrograde && (
                  <Badge variant="warning" size="small">
                    ℞ Retrograde
                  </Badge>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      
      {/* Mobile: Card List */}
      <div className="planet-list">
        {planets.map((planet) => (
          <div key={planet.name} className="planet-card">
            <div className="planet-card__header">
              <span className="planet-glyph" aria-hidden="true">
                {planetGlyphs[planet.name] || ''}
              </span>
              <strong>{planet.name}</strong>
              {planet.retrograde && (
                <Badge variant="warning" size="small">℞</Badge>
              )}
            </div>
            <div className="planet-card__details">
              <span><strong>Sign:</strong> {planet.sign}</span>
              <span><strong>Degree:</strong> {formatDegree(planet.degree)}</span>
              <span><strong>House:</strong> {planet.house}</span>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};

export default PlanetTable;
```

### Planet Table Styles

```css
/* /frontend/src/components/chart/PlanetTable.css */
.planet-table-card {
  overflow-x: auto;
}

.planet-table-card h3 {
  margin-bottom: var(--space-5);
}

/* Table (Desktop) */
.planet-table {
  width: 100%;
  border-collapse: collapse;
}

.planet-table thead {
  background: var(--bg-hover);
}

.planet-table th {
  padding: var(--space-3) var(--space-4);
  text-align: left;
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-small);
  color: var(--text-secondary);
  border-bottom: 2px solid var(--border-color);
}

.planet-table__row {
  border-bottom: 1px solid var(--border-color);
  transition: background 150ms ease;
}

.planet-table__row:hover {
  background: var(--bg-hover);
}

.planet-table td {
  padding: var(--space-4);
}

.planet-table__planet {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.planet-glyph {
  font-size: 24px;
  width: 32px;
  text-align: center;
}

.planet-name {
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}

/* Mobile: Card List (hidden on desktop) */
.planet-list {
  display: none;
}

@media (max-width: 767px) {
  .planet-table {
    display: none;
  }
  
  .planet-list {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }
  
  .planet-card {
    background: var(--bg-hover);
    padding: var(--space-4);
    border-radius: 8px;
  }
  
  .planet-card__header {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    margin-bottom: var(--space-3);
  }
  
  .planet-card__header .planet-glyph {
    font-size: 20px;
  }
  
  .planet-card__details {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-2);
    font-size: var(--font-size-small);
  }
  
  .planet-card__details strong {
    color: var(--text-secondary);
  }
}

/* Loading Skeleton */
.planet-table-skeleton {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.skeleton-row {
  height: 40px;
  background: linear-gradient(90deg, var(--bg-secondary), var(--bg-hover), var(--bg-secondary));
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

## 🧪 Testing Checklist

- [ ] Table displays all planets correctly
- [ ] Planet glyphs render (Sun, Moon, etc.)
- [ ] Retrograde badge appears for retrograde planets
- [ ] Degrees formatted correctly (15°32')
- [ ] Hover highlights table row
- [ ] Loading skeleton displays while calculating
- [ ] Responsive: table on desktop (≥768px), cards on mobile (<768px)
- [ ] No horizontal scroll on mobile
- [ ] Print layout readable (table format)
- [ ] Empty state if no planet data (error handling)

## 🔍 Accessibility Requirements

- [ ] Table has proper `<thead>` and `<tbody>`
- [ ] Table headers have `scope="col"`
- [ ] Retrograde badge text readable (not icon-only)
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Glyphs have `aria-hidden="true"` (decorative)
- [ ] Planet names in text (not glyph-only)
- [ ] Keyboard navigable (tab through rows)

## 📦 Files to Create/Modify

- `frontend/src/components/chart/PlanetTable.jsx` (create - replace PlanetList)
- `frontend/src/components/chart/PlanetTable.css` (create)
- `frontend/src/components/chart/PlanetTable.test.jsx` (create)
- `frontend/src/components/PlanetList/PlanetList.jsx` (deprecate)

## 🔗 Dependencies

- Issue #4 (Card Component)
- Issue #11 (Badge Component)
- Backend chart calculation API

## 📝 Additional Notes

- Existing `PlanetList.jsx` can be refactored or replaced
- Consider adding planet ruler information (future)
- Consider adding dignity/detriment indicators (future)
- Test with all 12 zodiac signs
- Ensure Unicode glyphs render on all browsers/devices

---

**Priority**: P1 (High)  
**Estimated Effort**: 5 hours  
**Assignee**: TBD  
**Epic**: Epic 4 - Enhanced Natal Chart Viewer
