# Design Assets Required - Mula: The Root

**Project:** Mula: The Root - Astrological Birth Chart Application  
**Designer Reference:** See provided mockup images for style guidance  
**Brand Name:** Mula: The Root (not "Stellaris")

---

## 1. LOGO & BRANDING (HIGHEST PRIORITY)

### Company Logo

**Style:** Circular celestial design inspired by Tree of Life concept

**Required Deliverables:**

- `logo-full.svg` - Complete logo with "ROOTS REVEALED" text
- `logo-icon.svg` - Icon only (no text) for app icons
- `logo-full.png` - PNG version (2000x2000px minimum)
- `icon-512.png` - App icon large (512x512px)
- `icon-256.png` - App icon medium (256x256px)
- `icon-128.png` - App icon small (128x128px)
- `icon-64.png` - Standard icon (64x64px)
- `favicon-32.png` - Browser tab icon (32x32px)
- `favicon-16.png` - Small browser icon (16x16px)
- `favicon.ico` - Multi-size ICO file

**Design Elements to Include:**

- Tree of Life motif (roots below, branches above) - symbolizes "Mula: The Root"
- Celestial/cosmic theme (stars, planets, orbits)
- Ornate circular border (Celtic/mystical style)
- Zodiac symbolism (optional: 12 signs around border)
- Color palette: Dark browns, copper/gold accents, cosmic blues
- Should work on both dark and light backgrounds
- Modern mystical aesthetic (not overly fantasy/medieval)

**Typography:**

- Font: Elegant serif (like Cinzel, Trajan Pro, or similar)
- Letter spacing: Wide/tracked for mystical elegance
- Text color: Copper/gold gradient (#E8B598 → #D4A574 → #C19A6B)

**Reference:** The Tree of Life design from the provided mockup is the correct aesthetic direction.

---

## 2. PLANET CARD ART

### Overview

Create glowing, mystical renders of all 10 celestial bodies for planet cards.

**Required Planets (10 total):**

1. **Sun** - Bright golden sphere with intense radiant glow
2. **Moon** - Silver-white with soft ethereal lunar glow
3. **Mercury** - Small gray-silver with subtle blue shimmer
4. **Venus** - Bright white-gold with soft pink/peach glow
5. **Earth** - Blue-green with cyan atmospheric glow _(provided)_
6. **Mars** - Orange-red with golden/amber aura _(provided)_
7. **Jupiter** - Large gas giant with horizontal bands, warm glow _(provided)_
8. **Saturn** - Golden planet with prominent rings, purple-pink glow _(provided)_
9. **Uranus** - Cyan-blue ice giant with electric blue aura
10. **Neptune** - Deep blue with purple-blue mystical glow
11. **Pluto** - Dark reddish-brown dwarf with faint copper glow

**Specifications:**

- **Size:** 800x800px (PNG with transparency)
- **Style:** Photorealistic with mystical glow effects
- **Lighting:** Consistent top-right light source across all planets
- **Glow:** Radial gradient halo extending 60-100px beyond planet edge
- **Colors:** Match the warm copper/gold palette for glows
- **Details:** Include surface features (craters, clouds, bands) appropriate to each planet
- **Background:** Transparent with optional subtle star sparkles
- **Format:** PNG with alpha channel

**Naming Convention:**

- `sun.png`, `moon.png`, `mercury.png`, etc. (lowercase)

**Reference:** The 4 provided planet images (Earth, Mars, Jupiter, Saturn) show the exact style needed.

---

## 3. TAROT CARD TEMPLATE & ART

### Card Template

**Base Template Required:**

- `card-template-portrait.svg` - 400x700px mobile card
- `card-template-landscape.svg` - 700x400px desktop card
- `card-back.svg` - Universal back design for unrevealed cards

**Template Structure:**

```
┌──────────────────────┐
│ ╔════════════════╗   │ ← Ornate copper border (40px frame)
│ ║   [Top Icon]   ║   │ ← Celestial symbol slot
│ ║                ║   │
│ ║   [Artwork]    ║   │ ← Main card art area
│ ║                ║   │
│ ║   [Title]      ║   │ ← Card name text
│ ║                ║   │
│ ║  [Bottom Icon] ║   │ ← Symbol slot
│ ╚════════════════╝   │
└──────────────────────┘
```

**Border Design:**

- Ornate Celtic knotwork pattern in copper/bronze
- Corner decorations (mystical symbols: ❋, ✦, etc.)
- Subtle gradient: #E8B598 → #D4A574 → #C19A6B
- Inner shadow for depth

**Background:**

- Gradient: Dark brown #3D2E29 → Warm brown #6B5645
- Cosmic dust particle overlay (subtle)
- Starfield texture (optional, very subtle)

### Major Arcana Cards (22 cards - FUTURE PHASE)

Create mystical astrological-themed interpretations:

- 0 The Fool through 21 The World
- Each needs unique central artwork
- Consistent ornate border style
- Top icon relates to card meaning
- Bottom symbol/number

**Priority Card:**

- **Fortune's Path** - Already designed (reference provided)
- Use this as style template for all other cards

**Specifications:**

- Dimensions: 400x700px (portrait) or 700x400px (landscape)
- Format: PNG with high quality, or SVG if vectorized
- Corner radius: 20px
- Typography: Cinzel or Trajan Pro, 28-32px titles, letter-spacing 6px
- File naming: `00-fool.png`, `01-magician.png`, etc.

---

## 4. UI BUTTONS & COMPONENTS

### Primary CTA Buttons

**Style Reference:** "Get Premium" and "Invite Friends" buttons from mockup

**Design Specifications:**

- **Shape:** Rounded pill (border-radius: 50px or full round)
- **Background:** Orange gradient
  - Start: #E86F4D (primary orange accent)
  - Mid: #E8A380 (peach)
  - End: #E8B598 (light copper)
- **Glow Effect:** Soft outer glow/shadow in orange (rgba(232, 111, 77, 0.5))
- **Text:** White, medium weight, letter-spacing 1-2px
- **Size:** Large (56px height), Medium (48px height)
- **Hover:** Brightened gradient + increased glow
- **Shadow:** 0 4px 12px rgba(232, 111, 77, 0.3)

**Required States:**

- Default
- Hover
- Active/Pressed
- Disabled (50% opacity)

**Deliverables:**

- Design specs/style guide (colors, spacing, effects)
- Optional: Figma/Sketch component for developer handoff

### Secondary Buttons

- **Style:** Transparent with orange border (2px solid #E86F4D)
- **Text:** Orange #E86F4D
- **Hover:** Light orange background (rgba(232, 111, 77, 0.1))

---

## 5. NAVIGATION ICONS

### Bottom Navigation (Mobile)

**Style Reference:** Circular blue icons from mockup

**5 Navigation Items Required:**

1. **Discover** - Search/magnifying glass icon
2. **Astorbase** - Star/constellation icon
3. **Shortbase** - Chart/graph icon
4. **Consultant** - Chat bubble/speech icon (with notification badge)
5. **Profile** - User/person icon

**Icon Specifications:**

- **Container:** Circular (48px diameter)
- **Background:** Blue gradient (rgba(74, 95, 142, 0.3) → rgba(74, 95, 142, 0.2))
- **Border:** 2px solid rgba(74, 95, 142, 0.4)
- **Icon Size:** 22-24px
- **Active State:** Enhanced blue glow + scale 1.1x
- **Style:** Line icons or minimal filled, consistent weight

**Badge (for notifications):**

- Small red-orange circle (18px diameter)
- White text (10px bold)
- Position: Top-right corner of icon
- Background: Linear gradient #E86F4D → #E8A380

**Deliverables:**

- 5 icon SVGs (one per navigation item)
- Active and inactive states
- Consistent stroke width and style

---

## 6. FORTUNE TELLER AVATARS

### User Profile & Consultant Avatars

**Purpose:** Fortune teller/mystic advisor character illustrations

**Required Variations:**

- 3-5 different mystical character designs
- Diverse representation (different genders, ethnicities)
- Circular crop format (profile picture style)
- Golden glow effect around avatar

**Specifications:**

- **Size:** 400x400px (circular crop)
- **Style:** Illustrated/artistic (not photos)
- **Theme:** Mystical, wise, approachable fortune tellers
- **Accessories:** May include: turbans, crystals, tarot cards, mystical jewelry
- **Background:** Transparent or subtle cosmic gradient
- **Border:** Optional golden ring (#D4A574)
- **Format:** PNG with alpha channel

**Fallback:**

- Generic zodiac sign avatars (12 signs) if custom characters not feasible

---

## 7. STATISTICS & DATA VISUALIZATION

### BMAD Summary Card Components

**Reference:** Statistics panel from mockup showing bar chart

**Required Elements:**

- Large number display (balance/metric)
- Horizontal bar chart visualization
- Multiple data bars with labels
- Active bar highlighted in orange (#E86F4D)
- Inactive bars in muted brown/gray
- Clean, minimal design

**Specifications:**

- Bar height: 8-10px
- Bar radius: 4px (rounded ends)
- Spacing: 12px between bars
- Font: JetBrains Mono or similar monospace for numbers
- Large number: 48-60px bold
- Labels: 14px regular

**Deliverables:**

- Style guide for data visualization
- Color coding system
- Icon set for metric types (gauge, bar, dot chart)

---

## 8. ADDITIONAL UI ELEMENTS

### User List Items

**Style:** Dark card with avatar and info

**Layout:**

```
┌────────────────────────────┐
│  [Avatar] Name             │
│           @username        │
│           [Status/Info]    │
└────────────────────────────┘
```

**Specifications:**

- Avatar: 48px circle (left aligned)
- Background: Dark brown #3D2E29
- Text: White primary, gray-400 secondary
- Padding: 16px
- Border radius: 12px
- Hover: Slight lift + shadow

### Invite Friends Module

- Card design matching mockup
- "Earn a 5% discount" subtitle styling
- Button integrated

---

## 9. DESIGN SYSTEM COLORS (FOR REFERENCE)

**Primary Colors:**

- `#3D2E29` - Dark chocolate brown (primary background)
- `#1A1F2E` - Deep navy (alternate dark background)
- `#E86F4D` - Orange accent (primary CTA, active states)
- `#8B6F47` - Warm brown (cards, tree elements)
- `#4A5F8E` - Blue accent (navigation, cool cards)

**Accent Colors:**

- `#D4A574` - Copper (borders, text accents, logo)
- `#C19A6B` - Bronze (secondary copper tone)
- `#E8B598` - Light copper (gradient ends)
- `#FFD700` - Gold (stars, highlights)
- `#FFF8DC` - Cream white (primary text on dark)

**Gradients:**

- Orange CTA: `#E86F4D → #E8A380 → #E8B598`
- Copper border: `#E8B598 → #D4A574 → #C19A6B`
- Dark background: `#3D2E29 → #4A3B35 → #6B5645`
- Blue nav: `rgba(74, 95, 142, 0.3) → rgba(74, 95, 142, 0.2)`

---

## PRIORITY ORDER

### Phase 1 - CRITICAL (Start Here)

1. **Company Logo** - Full suite (SVG + all PNG sizes)
2. **Primary Button Design** - Specs for orange gradient style
3. **Planet Art** - Complete all 10 planet renders

### Phase 2 - HIGH PRIORITY

4. **Navigation Icons** - 5 circular icons with active states
5. **Tarot Card Template** - Reusable border/frame design
6. **Fortune's Path Card** - Already provided, ensure proper format

### Phase 3 - MEDIUM PRIORITY

7. **Fortune Teller Avatars** - 3-5 character designs
8. **Statistics Components** - Bar chart styling
9. **User List Card** - Design specs

### Phase 4 - FUTURE

10. **Major Arcana Set** - 22 tarot cards
11. **Minor Arcana** - 56 additional cards (long-term)

---

## FILE ORGANIZATION

**Deliver assets in this structure:**

```
/design-assets/
├── logo/
│   ├── logo-full.svg
│   ├── logo-icon.svg
│   ├── logo-full.png
│   ├── icon-512.png
│   ├── icon-256.png
│   ├── icon-128.png
│   ├── icon-64.png
│   ├── favicon-32.png
│   ├── favicon-16.png
│   └── favicon.ico
├── planets/
│   ├── sun.png
│   ├── moon.png
│   ├── mercury.png
│   └── [etc... all 10 planets]
├── tarot/
│   ├── card-template-portrait.svg
│   ├── card-template-landscape.svg
│   ├── card-back.svg
│   └── fortune-path.png
├── avatars/
│   ├── fortune-teller-01.png
│   ├── fortune-teller-02.png
│   └── [3-5 variations]
├── icons/
│   ├── nav-discover.svg
│   ├── nav-astorbase.svg
│   ├── nav-shortbase.svg
│   ├── nav-consultant.svg
│   └── nav-profile.svg
└── style-guide.pdf (design specifications document)
```

---

## NOTES FOR DESIGNER

- **Brand Name:** Use "Mula: The Root" NOT "Stellaris" (Stellaris was prototype only)
- **Aesthetic:** Modern mystical - avoid being too medieval/fantasy
- **Consistency:** All assets should feel cohesive (same color palette, style, lighting)
- **File Formats:** SVG preferred for logos/icons, PNG for illustrations/photos
- **Resolution:** All raster images should be @2x for retina displays
- **Transparency:** Use alpha channels where appropriate
- **Accessibility:** Ensure sufficient contrast ratios for text/icons
- **Dark Theme:** All designs are for dark brown background (#3D2E29)

**Questions?** Reference the provided mockup images for exact style direction.

- **Style:** Modern, mystical, cosmically inspired
- **Imagery:** Celestial elements (planets, moon, astrological motifs), glowing highlights, subtle orbit/constellation lines
- **Colors:** Deep space tones (blacks, dark browns, navy/copper gradients), accents in silver, gold, blue
- **Shape:** Circular, enclosing the mystic core; must also work as app icon
- **Typography:** Smooth, sans-serif with subtle astrological or occult-inspired tweaks; highly readable for all sizes
- **Usage:** Header, splash, app icon

## 2. Planet Card Art

- **Visual:** Orb-like planet render for easy stacking; each planet with unique features (e.g., Saturn’s rings)
- **Effects:** Subtle textures/shadows, glowing aura
- **Palette:** Matches the deep, rich color suite

## 3. Fortune Teller & Tarot Experience Cards

- **Shape:** Rounded rectangles with gradient backgrounds
- **Main Area:** Central avatar/illustration
- **Text:** Sub-header and description in strong contrast
- **Borders:** Ornate but subtle—astrology wheels, runes

## 4. Avatar/Profile Images

- **Crop:** Circular
- **Effect:** Drop shadow or golden glow ring
- **Fallback:** Illustrated avatar if no photo available

## 5. Statistics Panel

- **Graph:** Gauge, bar, or dot graphs with glowing red/orange highlights
- **Card Layout:** Each metric on its own card
- **Font:** Clean, sans-serif, digital-feel

## 6. Action Buttons & Nav

- **Shape:** Rounded rectangles or pill shapes
- **Effects:** Gradients, soft drop shadow or glow, hover highlight

## 7. Invite Friends/Promo Modules

- **Colors:** Blue accent blending smoothly to background gradient
- **Shape:** Focused, rounded box with strong contrast text

## 8. User List Items

- **Avatar:** Left-aligned
- **Info:** Name and join date right
- **Box:** Rounded, dark background distinct from panels

## Additional Art Direction

- All interface elements unified by glow, shadow, gradients
- Faint textures: cosmic dust, starfields
- UI prioritizes contrast
- Design order: Logo & icon, planetary/fortune-teller avatars, background panels

---

**Attached:** Mockup reference (`image.jpg`). Begin work with the logo as priority; all elements must harmonize with style/palette shown in mockup.
