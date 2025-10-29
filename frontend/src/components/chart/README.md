# Chart Visualization Components

A collection of React/TypeScript components for displaying and visualizing astrological birth charts in the Roots Revealed application.

## Components

### ChartCanvas

Interactive SVG-based birth chart wheel displaying zodiac signs, house divisions, planetary positions, and the ascendant.

**Props:**
- `chartData` (ChartData): Complete chart data including planets, houses, ascendant, and midheaven
- `width` (number, optional): Width of the SVG canvas (default: 500)
- `height` (number, optional): Height of the SVG canvas (default: 500)

**Features:**
- 360° zodiac wheel with 12 signs
- House division lines (cusps)
- Planetary positions with symbols
- Retrograde indicators (℞)
- Ascendant marker (ASC)
- Interactive hover effects on planets
- Responsive design
- Color-coded retrograde/direct motion

**Example:**
```tsx
import { ChartCanvas } from '@/components/chart';

<ChartCanvas 
  chartData={myChartData}
  width={600}
  height={600}
/>
```

### PlanetTable

Displays planetary positions in a tabular format with signs, degrees, houses, and retrograde status.

**Props:**
- `planets` (object): Object containing planet positions keyed by planet name

**Features:**
- Displays all 13 planets (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, North Node, South Node, Chiron)
- Planet and zodiac symbols (☉, ♈, etc.)
- Degree/minute/second format (15°30'0")
- House assignments
- Retrograde/Direct indicators
- Handles missing planet data gracefully
- Planet count summary
- Responsive table layout

**Example:**
```tsx
import { PlanetTable } from '@/components/chart';

<PlanetTable planets={chartData.planets} />
```

### HouseTable

Shows the 12 house cusps with signs, degrees, and life area meanings.

**Props:**
- `houses` (object): Object containing house cusp data keyed by house number
- `ascendant` (HouseCusp, optional): Ascendant (1st house cusp) data
- `midheaven` (HouseCusp, optional): Midheaven (10th house cusp) data

**Features:**
- Displays all 12 houses in order
- House numbers with circular badges
- Zodiac sign symbols
- Degree/minute/second format
- Life area meanings for each house
- Special points section (Ascendant & Midheaven)
- House count summary
- Responsive table layout

**Example:**
```tsx
import { HouseTable } from '@/components/chart';

<HouseTable 
  houses={chartData.houses}
  ascendant={chartData.ascendant}
  midheaven={chartData.midheaven}
/>
```

## Data Types

### ChartData
```typescript
interface ChartData {
  planets: {
    [planetName: string]: PlanetPosition | null;
  };
  houses: {
    [houseKey: string]: HouseCusp;
  };
  ascendant?: HouseCusp;
  midheaven?: HouseCusp;
}
```

### PlanetPosition
```typescript
interface PlanetPosition {
  sign: string;           // Zodiac sign name
  degree: number;         // Degree position (0-360)
  house: number;          // House number (1-12)
  retrograde?: boolean;   // Retrograde status
  longitude?: number;     // Ecliptic longitude
  latitude?: number;      // Ecliptic latitude
  speed?: number;         // Daily motion
}
```

### HouseCusp
```typescript
interface HouseCusp {
  sign: string;       // Zodiac sign on cusp
  degree: number;     // Degree position
  longitude?: number; // Ecliptic longitude
}
```

## Styling

All components use CSS variables from the design system:
- `--color-primary`: Primary theme color
- `--color-accent`: Accent color for highlights
- `--bg-primary`: Background color
- `--bg-secondary`: Card/component background
- `--text-primary`: Primary text color
- `--text-secondary`: Secondary text color
- `--space-*`: Spacing scale (1-7)
- `--elevation-*`: Shadow levels

Components automatically adapt to light/dark themes via CSS variables.

## Accessibility

- Semantic HTML structure (tables, headings)
- ARIA attributes where appropriate
- Keyboard navigation support
- Descriptive alt text and titles
- Screen reader friendly
- Focus management

## Testing

Comprehensive test suite covers:
- Component rendering
- Data display accuracy
- Edge cases (missing data)
- Responsive behavior
- User interactions

Run tests:
```bash
npm test Chart.test.tsx
```

## Demo

Visit `/chart-demo` to see all components in action with sample chart data.

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- SVG support required for ChartCanvas
- CSS Grid support required for layouts

## Dependencies

### Required
- React 19
- Next.js 16
- TypeScript

### Shared Components
Uses the same design system as Symbolon components for consistency.

## File Structure

```
frontend/src/components/chart/
├── ChartCanvas.tsx         # SVG birth chart wheel
├── ChartCanvas.css         # Chart styles
├── PlanetTable.tsx         # Planet positions table
├── PlanetTable.css         # Table styles
├── HouseTable.tsx          # House system table
├── HouseTable.css          # Table styles
├── index.ts                # Component exports
└── __tests__/
    └── Chart.test.tsx      # Test suite (15 tests)
```

## Performance

- SVG rendering is efficient for static charts
- CSS animations for smooth transitions
- Lazy rendering where appropriate
- Optimized table layouts
- Minimal re-renders

## Future Enhancements

Potential improvements:
- Add aspect lines to ChartCanvas
- Interactive planet dragging
- Zoom/pan functionality
- Chart comparison mode
- Print-optimized layouts
- Export to PDF/PNG
- Animation of transits
- Mobile touch gestures

## Related Components

- Symbolon Card components (similar design patterns)
- Theme Toggle (integrated theme support)

## API Integration

These components are designed to work with chart data from:
- Backend `/api/chart` endpoint
- Python BMAD server chart calculations
- Swiss Ephemeris data

Example data flow:
```
User Input → Backend API → Chart Calculator → ChartData → Components → UI
```
