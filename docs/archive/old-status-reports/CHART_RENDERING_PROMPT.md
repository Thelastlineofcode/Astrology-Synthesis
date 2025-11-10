# Professional Astrological Chart Rendering Prompt

## Context

I need to render a professional-quality natal chart (birth chart) in a web application using SVG. The chart must display accurate astronomical data and follow traditional astrological chart conventions.

## Requirements

### 1. Chart Structure (Concentric Rings)

From outer to inner:

- **Outer Ring (Signs)**: 12 zodiac signs (30° each), starting with Aries at 0°
- **Degree Ring**: Degree markers (0-360°) with major lines every 10° and minor lines every 5°
- **Planet Ring**: Planetary positions with symbols and exact degree labels
- **House Ring**: 12 house divisions based on house cusps (variable sizes)
- **Center**: Aspect lines connecting planets (optional, toggleable)

### 2. Coordinate System

- Chart rotates so **Ascendant (0°) appears at 9 o'clock** (left/west position)
- Degrees increase **counter-clockwise**: 0° → 90° → 180° → 270° → 360°
- All planetary longitudes are **ecliptic degrees** (0-360°)
- House cusps are **ecliptic longitudes** that define house boundaries

### 3. Essential Visual Elements

#### Zodiac Signs

- Display all 12 signs in outer ring with Unicode symbols: ♈♉♊♋♌♍♎♏♐♑♒♓
- Each sign occupies exactly 30° of arc
- Signs should be visually distinct (alternating background shading)
- Sign boundaries marked with radial lines

#### Degree Markers

- Major degree lines every 10° (thicker, more visible)
- Minor degree lines every 5° (thinner, subtle)
- Degree labels at 0°, 30°, 60°, 90°, 120°, 150°, 180°, 210°, 240°, 270°, 300°, 330°
- Degree ring should be distinct belt between signs and planets

#### Planets

- Display with Unicode astronomical symbols: ☉☽☿♀♂♃♄♅♆♇
- Show exact degree below each planet symbol (e.g., "245.3°")
- Retrograde planets marked with ℞ symbol
- Planets placed at exact ecliptic longitude on the wheel
- Anti-collision: Adjust planet positions if too close together

#### Houses

- 12 radial lines from center to outer edge
- Each line positioned at house cusp longitude
- House numbers (1-12) displayed near center
- House cusp degrees shown on degree ring
- Lines should be distinct from sign boundaries

#### Ascendant

- Special marker at 9 o'clock position (left)
- Thicker line or arrow pointing outward
- "ASC" label clearly visible
- This is the starting point (0°) for the rotated chart

#### Aspects (Optional)

- Lines connecting planets in the center
- Color-coded by aspect type:
  - Conjunction (0°): Red/Orange
  - Sextile (60°): Blue
  - Square (90°): Red
  - Trine (120°): Green
  - Opposition (180°): Purple
- Line thickness varies by orb exactness
- Toggleable on/off

### 4. Mathematical Considerations

#### Angle Conversion

```
SVG coordinate system: 0° at 3 o'clock (right), clockwise
Astrological system: 0° at 9 o'clock (left), counter-clockwise

Conversion formula:
svg_angle = (180 - (ecliptic_longitude - ascendant_longitude)) * (π/180)

x = centerX + radius * cos(svg_angle)
y = centerY - radius * sin(svg_angle)  // Note: minus because SVG Y increases downward
```

#### House Calculation

- Houses are NOT equal 30° divisions
- Each house starts at its cusp longitude
- House size varies based on latitude and house system (Placidus, Koch, etc.)
- Handle wrap-around at 360°/0° boundary

#### Planet Collision Detection

When planets are within ~15° of each other:

- Offset them radially (different distances from center)
- Use connecting lines to show true position on wheel
- Prioritize inner planets (Sun, Moon, Mercury, Venus, Mars)

### 5. Accessibility & Usability

#### Interactive Features

- Hover over planet: Show tooltip with full data (planet, sign, degree, house, aspects)
- Hover over house: Highlight that house segment
- Click planet: Lock tooltip/panel open with detailed interpretation
- Zoom in/out controls for detailed inspection
- Pan/drag to reposition view

#### Responsive Design

- Minimum chart size: 400x400px
- Maximum chart size: 800x800px
- All text should scale with chart size
- Touch-friendly hit targets (minimum 44x44px)

#### Keyboard Navigation

- Tab through all planets
- Enter/Space to open planet details
- Arrow keys to navigate between planets
- Escape to close panels

### 6. Data Input Format

```typescript
interface ChartData {
  ascendant: { longitude: number }; // 0-360°
  midheaven?: { longitude: number }; // Optional

  planets: {
    [planetName: string]: {
      longitude: number; // 0-360° ecliptic
      latitude?: number; // Declination (optional)
      sign: string; // "Aries", "Taurus", etc.
      degree: number; // 0-30° within sign
      house: number; // 1-12
      retrograde: boolean;
    };
  };

  houses: {
    house_1: { longitude: number }; // Cusp longitudes
    house_2: { longitude: number };
    // ... through house_12
  };

  aspects?: Array<{
    planet1: string;
    planet2: string;
    type: string; // "conjunction", "sextile", etc.
    angle: number; // Actual angle between planets
    orb: number; // Difference from exact aspect
  }>;
}
```

### 7. Visual Hierarchy

**Most Important (High Contrast, Largest)**

1. Planet symbols
2. Ascendant marker
3. House cusp lines

**Secondary (Medium Contrast, Medium Size)** 4. Zodiac sign symbols 5. Degree markers (major) 6. Planet degree labels

**Tertiary (Low Contrast, Smallest)** 7. Degree markers (minor) 8. House cusp degree labels 9. Aspect lines (when enabled)

### 8. Color Scheme Recommendations

#### Light Mode

- Background: White or light gray (#F8F9FA)
- Primary lines: Dark blue (#1E3A8A)
- Zodiac signs: Subtle purple/blue alternating (#E0E7FF / #DDD6FE)
- Planets: Distinct colors per planet (traditional associations)
- Text: Dark gray (#1F2937)

#### Dark Mode

- Background: Dark navy (#0F172A)
- Primary lines: Light blue (#60A5FA)
- Zodiac signs: Subtle dark blue alternating (#1E3A8A / #1E40AF)
- Planets: Brighter versions of traditional colors
- Text: Light gray (#E5E7EB)

### 9. Performance Optimization

- Use SVG `<defs>` for reusable symbols
- Implement virtual rendering for aspect lines (only draw visible ones)
- Debounce zoom/pan operations
- Cache calculated positions
- Use CSS transforms for zoom (hardware accelerated)
- Lazy load aspect calculations

### 10. Testing Requirements

#### Visual Accuracy Tests

- Chart matches Swiss Ephemeris calculations
- Planets at correct ecliptic positions
- Houses sized correctly for given latitude
- Ascendant appears at 9 o'clock position
- Degree markers align with sign boundaries

#### Edge Cases

- Planets in retrograde motion
- Multiple planets in same degree (stellium)
- Houses crossing 360°/0° boundary
- Very northern/southern latitudes (intercepted signs)
- Charts at equator (equal houses)

#### Browser Compatibility

- Chrome, Firefox, Safari, Edge (latest 2 versions)
- iOS Safari, Android Chrome
- SVG rendering consistency across browsers

## Expected Output

A complete, professional natal chart wheel that:

1. ✅ Displays all 12 zodiac signs correctly positioned
2. ✅ Shows degree ring with clear markers (0-360°)
3. ✅ Places planets at exact ecliptic longitudes
4. ✅ Shows exact degrees for all planets and house cusps
5. ✅ Rotates chart so Ascendant is at 9 o'clock
6. ✅ Handles house divisions accurately
7. ✅ Provides interactive tooltips and controls
8. ✅ Responsive and accessible
9. ✅ Performs smoothly even with all features enabled

## Reference Examples

**Professional Astrology Software Charts:**

- Astro.com chart wheels
- Solar Fire chart layouts
- Kepler astrology program charts
- Traditional hand-drawn astrological charts

**Key Visual Standard:**
The chart should look like a traditional astrologer's chart wheel with modern, clean UI design - immediately recognizable to professional astrologers while being intuitive for beginners.
