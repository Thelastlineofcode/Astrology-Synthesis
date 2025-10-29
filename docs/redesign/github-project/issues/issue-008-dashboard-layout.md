---
title: "Redesign Dashboard Layout & Grid"
labels: ["component:dashboard", "P1-High", "layout", "feature"]
assignees: []
milestone: "Milestone 2: Core Features"
---

## 🎯 Objective

Create a modern dashboard layout with card-based grid showcasing: Quick Chart Access, Recent Charts, BMAD Insights, and Saved Symbolon Readings.

## 📋 Description

The dashboard is the first screen users see after generating a chart. It should provide quick access to key features and recent activity. Design a responsive grid that adapts from 1 column (mobile) to 3 columns (desktop).

## 🔗 References

- **Design Artifact**: `COMPONENT_STRUCTURE.md` (Dashboard section)
- **Design Artifact**: `UX_COPY_GUIDE.md` (Dashboard copy)
- **Guide**: `AI_COPILOT_GUIDE.md` - Dashboard Requirements

## ✅ Acceptance Criteria

- [ ] Dashboard route established (`/dashboard`)
- [ ] Responsive grid: 1 col (mobile), 2 col (tablet), 3 col (desktop)
- [ ] Four main cards: Quick Chart Access, Recent Charts, BMAD Summary, Symbolon Readings
- [ ] Empty states when no data (e.g., "No recent charts yet")
- [ ] Loading states while fetching data
- [ ] "View All" links where applicable
- [ ] Smooth animations when cards appear
- [ ] No layout shift as data loads
- [ ] Consistent spacing using design system tokens
- [ ] Print-friendly layout (bonus)

## 💻 Implementation Notes

### Dashboard Component

```jsx
// /frontend/src/pages/Dashboard.jsx
import React, { useState, useEffect } from 'react';
import QuickChartCard from '../components/dashboard/QuickChartCard';
import RecentChartsCard from '../components/dashboard/RecentChartsCard';
import BMADSummaryCard from '../components/dashboard/BMADSummaryCard';
import SymbolonCard from '../components/dashboard/SymbolonCard';
import './Dashboard.css';

const Dashboard = () => {
  const [recentCharts, setRecentCharts] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Fetch recent charts from localStorage or API
    const storedCharts = JSON.parse(localStorage.getItem('recentCharts') || '[]');
    setRecentCharts(storedCharts.slice(0, 3));
    setLoading(false);
  }, []);
  
  return (
    <div className="dashboard">
      <header className="dashboard__header">
        <h1>Your Astrology Dashboard</h1>
        <p className="dashboard__subtitle">
          Welcome back. Ready to explore the cosmos?
        </p>
      </header>
      
      <div className="dashboard__grid">
        <QuickChartCard />
        
        <RecentChartsCard 
          charts={recentCharts}
          loading={loading}
        />
        
        <BMADSummaryCard />
        
        <SymbolonCard />
      </div>
    </div>
  );
};

export default Dashboard;
```

### Dashboard Styles

```css
/* /frontend/src/pages/Dashboard.css */
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-6) var(--space-4);
}

.dashboard__header {
  margin-bottom: var(--space-7);
}

.dashboard__header h1 {
  font-size: var(--font-size-h1);
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.dashboard__subtitle {
  font-size: var(--font-size-h4);
  color: var(--text-secondary);
  font-weight: var(--font-weight-regular);
}

.dashboard__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-5);
}

/* Tablet */
@media (min-width: 768px) {
  .dashboard__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .dashboard__grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  /* Quick Chart Card spans 2 columns */
  .dashboard__grid > :first-child {
    grid-column: span 2;
  }
}

/* Print styles */
@media print {
  .dashboard__grid {
    grid-template-columns: 1fr;
  }
}
```

### Sample Card Component (Recent Charts)

```jsx
// /frontend/src/components/dashboard/RecentChartsCard.jsx
import React from 'react';
import Card from '../shared/Card';
import Button from '../shared/Button';
import './RecentChartsCard.css';

const RecentChartsCard = ({ charts, loading }) => {
  if (loading) {
    return (
      <Card className="recent-charts-card">
        <h3>Recent Charts</h3>
        <div className="loading-skeleton" />
      </Card>
    );
  }
  
  if (charts.length === 0) {
    return (
      <Card className="recent-charts-card">
        <h3>Recent Charts</h3>
        <div className="empty-state">
          <p>No charts yet. Generate your first chart to get started!</p>
        </div>
      </Card>
    );
  }
  
  return (
    <Card className="recent-charts-card">
      <div className="card-header">
        <h3>Recent Charts</h3>
        <Button variant="ghost" size="small" href="/charts">
          View All
        </Button>
      </div>
      
      <ul className="chart-list">
        {charts.map((chart, i) => (
          <li key={i} className="chart-item">
            <div className="chart-item__info">
              <strong>{chart.name || 'Unnamed Chart'}</strong>
              <span className="chart-item__date">
                {new Date(chart.date).toLocaleDateString()}
              </span>
            </div>
            <Button variant="ghost" size="small" href={`/chart/${chart.id}`}>
              View
            </Button>
          </li>
        ))}
      </ul>
    </Card>
  );
};

export default RecentChartsCard;
```

## 🧪 Testing Checklist

- [ ] Dashboard loads without errors
- [ ] Grid responsive at mobile (375px), tablet (768px), desktop (1440px)
- [ ] Empty states display when no data
- [ ] Loading states show while fetching
- [ ] "View All" links navigate correctly
- [ ] Recent charts populated from localStorage
- [ ] Cards animate in smoothly (fade/slide)
- [ ] No layout shift as images/data load
- [ ] Header text matches UX_COPY_GUIDE.md
- [ ] Print layout readable (single column)

## 🔍 Accessibility Requirements

- [ ] Heading hierarchy correct (h1 → h2 → h3)
- [ ] "View All" links descriptive (not generic)
- [ ] Loading states announced to screen readers
- [ ] Empty states provide clear guidance
- [ ] Focus order logical (top to bottom, left to right)
- [ ] Cards keyboard navigable

## 📦 Files to Create/Modify

- `frontend/src/pages/Dashboard.jsx` (create)
- `frontend/src/pages/Dashboard.css` (create)
- `frontend/src/components/dashboard/QuickChartCard.jsx` (create)
- `frontend/src/components/dashboard/RecentChartsCard.jsx` (create)
- `frontend/src/components/dashboard/BMADSummaryCard.jsx` (create)
- `frontend/src/components/dashboard/SymbolonCard.jsx` (create)
- `frontend/src/App.jsx` (modify to add dashboard route)

## 🔗 Dependencies

- Issue #4 (Card Component) - Dashboard cards use Card component
- Issue #3 (Button Component) - "View All" buttons
- Issue #7 (Navigation Bar) - Dashboard accessible from nav

## 📝 Additional Notes

- Store recent charts in `localStorage` (max 10)
- Consider adding "Personalized Insights" card (future)
- Dashboard cards can lazy load for performance
- Use React Suspense for code splitting (optional)
- Chart thumbnails can be SVG snapshots (future enhancement)

---

**Priority**: P1 (High)  
**Estimated Effort**: 10 hours  
**Assignee**: TBD  
**Epic**: Epic 2 - Dashboard Redesign
