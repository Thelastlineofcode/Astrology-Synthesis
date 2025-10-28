---
title: "Show House System Table"
labels: ["component:chart", "P1-High", "data-display"]
assignees: []
milestone: "Milestone 2: Core Features"
---

## 🎯 Objective

Create a table component displaying house cusps and angles (Ascendant, Midheaven, Descendant, IC) with zodiac signs and degrees.

## 📋 Description

The house table complements the natal chart wheel, showing exact house cusp positions. Users should see all 12 house cusps plus the four major angles clearly labeled.

## 🔗 References

- **Design Artifact**: `COMPONENT_STRUCTURE.md` (Chart Results - House Table)
- **Existing Code**: `/frontend/src/components/HouseTable/HouseTable.jsx`

## ✅ Acceptance Criteria

- [ ] Table displays all 12 house cusps
- [ ] Columns: House Number, Cusp Sign, Degree
- [ ] Four angles highlighted: ASC (1st), IC (4th), DESC (7th), MC (10th)
- [ ] Angle badges/labels visible
- [ ] Degree formatted (e.g., "15°32'")
- [ ] Responsive: table on desktop, card list on mobile
- [ ] Hover highlights row
- [ ] Loading skeleton while calculating
- [ ] Print-friendly layout

## 💻 Implementation Notes

### House Table Component

```jsx
// /frontend/src/components/chart/HouseTable.jsx
import React from 'react';
import Card from '../shared/Card';
import Badge from '../shared/Badge';
import './HouseTable.css';

const angles = {
  1: { name: 'Ascendant', abbr: 'ASC' },
  4: { name: 'Imum Coeli', abbr: 'IC' },
  7: { name: 'Descendant', abbr: 'DESC' },
  10: { name: 'Midheaven', abbr: 'MC' }
};

const HouseTable = ({ houses, loading }) => {
  if (loading) {
    return (
      <Card>
        <h3>House Cusps</h3>
        <div className="house-table-skeleton">
          {Array.from({ length: 12 }).map((_, i) => (
            <div key={i} className="skeleton-row" />
          ))}
        </div>
      </Card>
    );
  }
  
  // Convert houses object to array
  const houseArray = houses && typeof houses === 'object'
    ? Object.entries(houses)
        .filter(([key]) => key.startsWith('house_'))
        .map(([key, value]) => ({
          number: parseInt(key.split('_')[1]),
          ...value
        }))
        .sort((a, b) => a.number - b.number)
    : [];
  
  const formatDegree = (degree) => {
    if (!degree && degree !== 0) return 'N/A';
    const deg = Math.floor(degree);
    const min = Math.floor((degree - deg) * 60);
    return `${deg}°${min.toString().padStart(2, '0')}'`;
  };
  
  if (!houseArray.length) {
    return (
      <Card>
        <h3>House Cusps</h3>
        <p>No house data available.</p>
      </Card>
    );
  }
  
  return (
    <Card className="house-table-card">
      <h3>House Cusps</h3>
      
      {/* Desktop: Table */}
      <table className="house-table">
        <thead>
          <tr>
            <th>House</th>
            <th>Cusp Sign</th>
            <th>Degree</th>
            <th>Angle</th>
          </tr>
        </thead>
        <tbody>
          {houseArray.map((house) => {
            const angle = angles[house.number];
            return (
              <tr
                key={house.number}
                className={`house-table__row ${angle ? 'house-table__row--angle' : ''}`}
              >
                <td className="house-table__number">
                  <strong>{house.number}</strong>
                </td>
                <td className="house-table__sign">
                  {house.sign || 'N/A'}
                </td>
                <td className="house-table__degree">
                  {formatDegree(house.degree)}
                </td>
                <td className="house-table__angle">
                  {angle && (
                    <Badge variant="accent" size="small" title={angle.name}>
                      {angle.abbr}
                    </Badge>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
      
      {/* Mobile: Card List */}
      <div className="house-list">
        {houseArray.map((house) => {
          const angle = angles[house.number];
          return (
            <div
              key={house.number}
              className={`house-card ${angle ? 'house-card--angle' : ''}`}
            >
              <div className="house-card__header">
                <strong>House {house.number}</strong>
                {angle && (
                  <Badge variant="accent" size="small" title={angle.name}>
                    {angle.abbr}
                  </Badge>
                )}
              </div>
              <div className="house-card__details">
                <span><strong>Sign:</strong> {house.sign}</span>
                <span><strong>Degree:</strong> {formatDegree(house.degree)}</span>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
};

export default HouseTable;
```

### House Table Styles

```css
/* /frontend/src/components/chart/HouseTable.css */
.house-table-card {
  overflow-x: auto;
}

.house-table-card h3 {
  margin-bottom: var(--space-5);
}

/* Table (Desktop) */
.house-table {
  width: 100%;
  border-collapse: collapse;
}

.house-table thead {
  background: var(--bg-hover);
}

.house-table th {
  padding: var(--space-3) var(--space-4);
  text-align: left;
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-small);
  color: var(--text-secondary);
  border-bottom: 2px solid var(--border-color);
}

.house-table__row {
  border-bottom: 1px solid var(--border-color);
  transition: background 150ms ease;
}

.house-table__row:hover {
  background: var(--bg-hover);
}

/* Highlight angle rows */
.house-table__row--angle {
  background: rgba(165, 184, 164, 0.1); /* Sage tint */
}

.house-table td {
  padding: var(--space-4);
}

.house-table__number {
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  width: 80px;
}

.house-table__sign {
  font-weight: var(--font-weight-medium);
}

.house-table__degree {
  font-family: var(--font-mono);
  font-size: var(--font-size-small);
}

/* Mobile: Card List (hidden on desktop) */
.house-list {
  display: none;
}

@media (max-width: 767px) {
  .house-table {
    display: none;
  }
  
  .house-list {
    display: grid;
    grid-template-columns: 1fr;
    gap: var(--space-3);
  }
  
  .house-card {
    background: var(--bg-hover);
    padding: var(--space-4);
    border-radius: 8px;
    border-left: 4px solid transparent;
  }
  
  .house-card--angle {
    border-left-color: var(--color-accent);
    background: rgba(165, 184, 164, 0.1);
  }
  
  .house-card__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-3);
  }
  
  .house-card__header strong {
    color: var(--color-primary);
  }
  
  .house-card__details {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-2);
    font-size: var(--font-size-small);
  }
  
  .house-card__details strong {
    color: var(--text-secondary);
  }
}

/* Loading Skeleton */
.house-table-skeleton {
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

- [ ] Table displays all 12 houses correctly
- [ ] Angles (ASC, IC, DESC, MC) highlighted with badges
- [ ] Degrees formatted correctly (15°32')
- [ ] Hover highlights table row
- [ ] Loading skeleton displays while calculating
- [ ] Responsive: table on desktop (≥768px), cards on mobile (<768px)
- [ ] No horizontal scroll on mobile
- [ ] Print layout readable (table format)
- [ ] Empty state if no house data (error handling)
- [ ] Handles missing/null house data gracefully

## 🔍 Accessibility Requirements

- [ ] Table has proper `<thead>` and `<tbody>`
- [ ] Table headers have `scope="col"`
- [ ] Angle badges have `title` attribute with full name
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Keyboard navigable (tab through rows)
- [ ] Screen reader announces angle rows differently

## 📦 Files to Create/Modify

- `frontend/src/components/chart/HouseTable.jsx` (modify existing)
- `frontend/src/components/chart/HouseTable.css` (create)
- `frontend/src/components/chart/HouseTable.test.jsx` (create)

## 🔗 Dependencies

- Issue #4 (Card Component)
- Issue #11 (Badge Component)
- Backend chart calculation API (houses object structure)

## 🚫 Blocked By

- None (existing HouseTable can be refactored)

## 📝 Additional Notes

- Existing `HouseTable.jsx` already has robust validation (from agent PR #9)
- Angle highlighting helps users quickly identify cardinal points
- Consider adding house system label (Placidus, Whole Sign, etc.)
- Test with different house systems (some have intercepted signs)
- Equal house system: all houses same size (30°)

---

**Priority**: P1 (High)  
**Estimated Effort**: 4 hours  
**Assignee**: TBD  
**Epic**: Epic 4 - Enhanced Natal Chart Viewer
