# Design Agent Prompt - Production-Ready Asset Specifications

## Agent Role & Context

You are a professional UI/UX design agent creating production-ready assets for "Mula: The Root" - a mystical astrology web application. All assets must be development-ready, properly formatted, and optimized for web deployment.

## Brand Identity

- **Name:** Mula: The Root
- **Theme:** Tree of Life, Celtic mysticism, cosmic astrology
- **Visual Style:** Mystical, elegant, spiritual, sophisticated
- **Primary Motif:** Tree of Life circular design with Celtic knotwork
- **Atmosphere:** Dark, warm, inviting with glowing accents

## Color Palette (Use Exact Hex Values)

```css
/* Primary Colors */
--dark-brown: #3d2e29; /* Backgrounds, cards */
--orange-accent: #e86f4d; /* CTA buttons, highlights */
--copper: #d4a574; /* Borders, secondary text */
--blue-accent: #4a5f8e; /* Navigation, info cards */
--gold: #ffd700; /* Stars, premium features */

/* Gradients */
--orange-gradient: linear-gradient(
  135deg,
  #e86f4d 0%,
  #e8a380 50%,
  #e8b598 100%
);
--dark-gradient: linear-gradient(180deg, #3d2e29 0%, #2a1f1c 100%);
--copper-gradient: linear-gradient(135deg, #d4a574 0%, #c89555 100%);

/* Semantic Colors */
--background-primary: #1a1412;
--background-secondary: #3d2e29;
--text-primary: #f5f5f5;
--text-secondary: #d4a574;
```

## Typography

```css
/* Fonts */
--font-primary: "Inter", sans-serif; /* Body, UI elements */
--font-mono: "JetBrains Mono", monospace; /* Data, coordinates */

/* Weights */
--weight-regular: 400;
--weight-medium: 500;
--weight-semibold: 600;
--weight-bold: 700;
```

---

## Asset Delivery Requirements

### 1. LOGO ASSETS

**Deliverables:** 4 variations × 7 formats = 28 files

#### Variations Required:

1. **Full Logo** - Complete Tree of Life with "Mula: The Root" text
2. **Icon Only** - Tree of Life symbol without text (square format)
3. **Horizontal Lockup** - Logo + text in horizontal layout
4. **Wordmark** - Text only with decorative elements

#### File Format Matrix:

```
For Each Variation, Provide:

1. SVG Vector (Primary Source)
   - Filename: {variation}-logo.svg
   - Requirements:
     * Clean, optimized paths (no unnecessary points)
     * Organized layers with proper naming
     * Artboard sized to exact design bounds
     * No embedded raster images
     * Export text as outlines/paths
   - Size: Vector (scalable)
   - Color Mode: RGB
   - Example: full-logo.svg, icon-only.svg

2. PNG @ 1024×1024 (Master)
   - Filename: {variation}-1024.png
   - Transparent background
   - 72 DPI
   - Color: RGB, 8-bit
   - Compression: Optimal (PNG-24)

3. PNG @ 512×512 (App Icons)
   - Filename: {variation}-512.png
   - Use for: PWA icons, large displays

4. PNG @ 256×256 (Standard Icons)
   - Filename: {variation}-256.png
   - Use for: App icons, social media

5. PNG @ 128×128 (Thumbnails)
   - Filename: {variation}-128.png

6. PNG @ 64×64 (Small Icons)
   - Filename: {variation}-64.png

7. Favicon Sizes:
   - favicon-32×32.png
   - favicon-16×16.png
   - favicon.ico (multi-resolution: 16, 32, 48)
```

#### Logo Technical Specs:

- **Canvas:** Start with 1024×1024px canvas for all designs
- **Safe Zone:** Keep critical elements 10% inset from edges
- **Line Weight:** Minimum 2px stroke weight at 1024px size
- **Background:** Always transparent (alpha channel)
- **Format:** Export all PNG as PNG-24 with transparency
- **Optimization:** Run through ImageOptim or TinyPNG before delivery

---

### 2. PLANET RENDERS

**Deliverables:** 10 celestial bodies in mystical style

#### Planet List:

1. Sun ☉
2. Moon ☽
3. Mercury ☿
4. Venus ♀
5. Mars ♂
6. Jupiter ♃
7. Saturn ♄
8. Uranus ♅
9. Neptune ♆
10. Pluto ♇

#### File Specifications:

```
Filename: {planet-name}-render.png
Example: sun-render.png, mercury-render.png

Format: PNG-24 with Alpha
Size: 1024×1024px
DPI: 72
Color Mode: RGB
Background: Transparent
Compression: Optimized PNG

Visual Style:
- Photorealistic rendered planet
- Mystical glowing aura/halo effect
- Soft radial gradient glow (matching planet colors)
- Slight atmospheric haze
- Consistent lighting from upper-left
- Shadow/depth to create 3D sphere illusion
- Transparent background with glow extending ~50px beyond planet edge

Technical Requirements:
- Planet should occupy 70-80% of canvas
- Centered positioning
- Glow should fade smoothly to transparency
- No hard edges or clipping
- Consistent style across all planets
```

#### Planet-Specific Color Guidance:

```
Sun: Warm yellow-orange glow (#FFD700 → #E86F4D)
Moon: Cool silver-blue (#C0C0C0 → #4A5F8E)
Mercury: Gray-brown (#8B7355)
Venus: Pale yellow-white (#F5DEB3)
Mars: Red-orange (#CD5C5C)
Jupiter: Orange-tan bands (#DAA520)
Saturn: Pale gold with rings (#F0E68C)
Uranus: Pale cyan-blue (#AFEEEE)
Neptune: Deep blue (#4169E1)
Pluto: Icy gray-blue (#B0C4DE)
```

---

### 3. TAROT CARD COMPONENTS

**Deliverables:** Card template + 22 Major Arcana designs

#### Card Template:

```
Filename: tarot-card-template.psd / .fig / .ai
PNG Export: tarot-card-blank.png

Dimensions: 400×700px (portrait)
Format: PNG-24 with transparency
DPI: 144 (retina-ready)
Color Mode: RGB

Template Elements (Layered):
1. Background: Dark gradient (#3D2E29 → #2A1F1C)
2. Border: Ornate Celtic copper frame (2px, #D4A574)
3. Corner Decorations: Celtic knots in all 4 corners
4. Title Area: Top 80px reserved for card name
5. Illustration Area: Center 440×440px square
6. Footer Area: Bottom 80px for number/subtitle
7. Glow Effects: Soft inner shadow, copper highlight

Layer Structure Required:
- Background (locked)
- Border/Frame (locked)
- [ILLUSTRATION SLOT] (editable)
- Title Text (editable)
- Footer Text (editable)
- Glow/Effects (adjustment layers)
```

#### Individual Card Exports:

```
Filename Pattern: tarot-{number}-{name}.png
Examples:
  - tarot-00-fool.png
  - tarot-01-magician.png
  - tarot-21-world.png

Format: PNG-24
Size: 400×700px
DPI: 144
Background: Included (not transparent for cards)

Each card must include:
- Unique central illustration
- Card name at top
- Roman numeral at bottom
- Consistent border/frame from template
- Subtle glow effects
```

#### Card Back Design:

```
Filename: tarot-card-back.png
Size: 400×700px
Style: Symmetrical Tree of Life pattern
Colors: Copper and gold on dark brown
Must be: Perfectly symmetrical, ornate, mysterious
```

---

### 4. BUTTON COMPONENTS

**Deliverables:** Visual mockups for 4 button states × 3 variants

#### Button Variants:

1. **Primary (Orange Gradient)**
2. **Secondary (Copper Outline)**
3. **Tertiary (Blue Ghost)**

#### States Required for Each Variant:

- Normal (default)
- Hover
- Active (pressed)
- Disabled

#### File Specifications:

```
Filename: button-{variant}-{state}.png
Examples:
  - button-primary-normal.png
  - button-primary-hover.png
  - button-secondary-disabled.png

Format: PNG-24 with transparency
Size: 400×80px (scale for design showcase)
DPI: 144
Background: Transparent
Include: Drop shadow/glow effects

Deliver Also:
- Figma/Sketch file with all states
- CSS specifications document
- Spacing/padding measurements
```

#### Primary Button Specs:

```css
Background: linear-gradient(135deg, #E86F4D 0%, #E8A380 50%, #E8B598 100%);
Border: none
Border-radius: 24px (pill shape)
Padding: 12px 32px
Font: Inter, 600 weight, 16px
Color: #FFFFFF
Shadow: 0 4px 12px rgba(232, 111, 77, 0.3)

Hover State:
  - Gradient shifts lighter
  - Shadow increases: 0 6px 16px rgba(232, 111, 77, 0.4)
  - Slight lift: transform translateY(-2px)

Active State:
  - Gradient shifts darker
  - Shadow reduces: 0 2px 8px rgba(232, 111, 77, 0.2)
  - Press down: transform translateY(0)
```

---

### 5. NAVIGATION ICONS

**Deliverables:** 6 icons × 3 states = 18 files

#### Icon List:

1. **Home** - Tree roots symbol
2. **Chart** - Circular natal chart
3. **Discover** - Magnifying glass with stars
4. **Profile** - User silhouette
5. **Settings** - Gear/cog with mystical elements
6. **Help** - Question mark in circular frame

#### File Specifications:

```
Filename: icon-{name}-{state}.svg
Examples:
  - icon-home-default.svg
  - icon-home-active.svg
  - icon-home-hover.svg

Format: SVG (vector)
Artboard: 24×24px
Stroke Width: 2px
Stroke Cap: Round
Stroke Join: Round
Fill: None (outline style)
Color Variables: Use CSS custom properties
  - Default: var(--icon-default, #D4A574)
  - Hover: var(--icon-hover, #E8A380)
  - Active: var(--icon-active, #E86F4D)

Export Settings:
- Minified SVG
- No unnecessary metadata
- Presentation attributes (not inline styles)
- ViewBox attribute included
- Accessible <title> tag

Also Provide:
- PNG exports @ 24×24, 48×48, 72×72 (for non-SVG contexts)
- Icon sprite sheet (all icons in one SVG)
```

---

### 6. AVATAR ILLUSTRATIONS

**Deliverables:** 5 fortune teller avatars OR 12 zodiac avatars

#### Fortune Teller Avatars:

```
Filename: avatar-fortune-teller-{number}.png
Count: 5 diverse characters

Format: PNG-24 with transparency
Size: 400×400px (circular crop)
DPI: 144
Style: Illustrated, mystical, diverse
Background: Transparent (but include subtle glow)

Character Requirements:
- Diverse ethnicities and genders
- Mystical accessories (crystal ball, tarot cards, jewelry)
- Golden/copper glow around character
- Consistent illustration style
- Warm, inviting expressions
- Visible from shoulders up
```

#### Alternative: Zodiac Sign Avatars:

```
Filename: avatar-zodiac-{sign}.png
Count: 12 signs

Format: PNG-24 with transparency
Size: 400×400px
Style: Symbolic/illustrated constellation art
Background: Transparent with star glow

Each avatar features:
- Zodiac symbol/constellation
- Sign's elemental color
- Mystical background elements
- Consistent geometric style
```

---

### 7. UI COMPONENTS & PATTERNS

#### Card Components:

```
Deliverable: card-component-mockups.png
Size: 1920×1080px showcase

Include Designs For:
1. Data Card (stats display)
   - Size: 320×180px
   - Background: Dark brown with copper border
   - Typography: Title (16px), Value (32px bold), Subtitle (12px)

2. Planet Card (planet info)
   - Size: 280×320px
   - Includes: Planet render, name, degree, sign
   - Background: Gradient with glow

3. Aspect Card (relationship display)
   - Size: 360×120px horizontal
   - Shows: Two planet icons + aspect symbol + degree

4. User Card (profile preview)
   - Size: 320×100px
   - Includes: Avatar, name, level, badges
```

---

## File Organization & Delivery Structure

```
📁 design-assets/
├── 📁 logos/
│   ├── 📁 svg/
│   │   ├── full-logo.svg
│   │   ├── icon-only.svg
│   │   ├── horizontal-lockup.svg
│   │   └── wordmark.svg
│   ├── 📁 png/
│   │   ├── full-logo-1024.png
│   │   ├── full-logo-512.png
│   │   ├── [... all sizes for all variations]
│   │   └── favicon.ico
│   └── 📄 logo-specifications.pdf
│
├── 📁 planets/
│   ├── sun-render.png
│   ├── moon-render.png
│   ├── [... all 10 planets]
│   └── 📄 planet-specs.pdf
│
├── 📁 tarot/
│   ├── 📁 templates/
│   │   ├── tarot-card-template.psd
│   │   ├── tarot-card-template.fig
│   │   └── tarot-card-blank.png
│   ├── 📁 major-arcana/
│   │   ├── tarot-00-fool.png
│   │   ├── [... all 22 cards]
│   │   └── tarot-card-back.png
│   └── 📄 tarot-guidelines.pdf
│
├── 📁 buttons/
│   ├── 📁 mockups/
│   │   ├── button-primary-normal.png
│   │   ├── [... all states/variants]
│   ├── button-design-specs.fig
│   └── 📄 button-css-specs.css
│
├── 📁 icons/
│   ├── 📁 svg/
│   │   ├── icon-home-default.svg
│   │   ├── [... all icons/states]
│   │   └── icon-sprite.svg
│   ├── 📁 png/
│   │   └── [PNG exports for each icon]
│   └── 📄 icon-usage-guide.md
│
├── 📁 avatars/
│   ├── avatar-fortune-teller-1.png
│   ├── [... 5 total OR 12 zodiac]
│   └── 📄 avatar-specs.pdf
│
├── 📁 components/
│   ├── card-components.png
│   ├── statistics-components.png
│   ├── navigation-components.png
│   └── 📄 component-specs.pdf
│
└── 📄 MASTER-DESIGN-SYSTEM.pdf
    (Complete style guide with all specifications)
```

---

## Quality Checklist (Before Delivery)

### All Assets Must:

- [ ] Match exact color palette (use hex codes provided)
- [ ] Be properly named according to conventions
- [ ] Include transparent backgrounds where specified
- [ ] Be optimized for web (compressed but not degraded)
- [ ] Use consistent visual style across all assets
- [ ] Include all required file formats
- [ ] Be organized in proper folder structure
- [ ] Include measurements/specifications document
- [ ] Be tested at target display sizes
- [ ] Include source files (PSD/Figma/AI) for future edits

### Image Optimization:

- [ ] PNG files run through TinyPNG or ImageOptim
- [ ] SVG files minified (remove metadata, optimize paths)
- [ ] No embedded fonts in SVGs (convert text to paths)
- [ ] Proper color profiles (sRGB for web)
- [ ] Consistent DPI (72 for standard, 144 for retina mockups)

### Documentation:

- [ ] Style guide PDF with color codes
- [ ] Measurement specifications for each component
- [ ] Usage guidelines (where/how to use each asset)
- [ ] Accessibility notes (contrast ratios, alt text suggestions)
- [ ] Source file locations noted

---

## Priority Phases

### Phase 1 - Critical (Deliver First)

1. Logo suite (all formats)
2. Favicon set
3. Primary button designs
4. Core navigation icons (6 icons)

### Phase 2 - High Priority

1. Planet renders (all 10)
2. Card components mockups
3. Secondary/tertiary button designs

### Phase 3 - Medium Priority

1. Tarot card template
2. Avatar illustrations (5 fortune tellers)
3. Additional UI components

### Phase 4 - Low Priority (Long-term)

1. Full Major Arcana tarot deck (22 cards)
2. Zodiac avatar alternatives
3. Animated versions of assets
4. Dark/light theme variations

---

## Communication & Iteration

**When delivering assets, please provide:**

1. Preview image showing all assets at a glance
2. Organized ZIP file with proper folder structure
3. README.md with:
   - What's included
   - What's pending
   - Any design decisions made
   - Known limitations or alternatives considered
4. Design rationale for key visual choices

**Questions to Address:**

- Are there alternative variations you created?
- Are there any technical limitations I should know about?
- Do any assets need special handling or preprocessing?
- Are the source files included for future edits?

---

## Example Prompt Usage

**Copy this prompt when requesting assets:**

> I need production-ready design assets for "Mula: The Root" - a mystical astrology app. Please follow the specifications in DESIGN_AGENT_PROMPT.md exactly.
>
> **Current Phase:** Phase 1 - Critical Assets
> **Specific Request:** Logo suite (all 4 variations in all formats per specs)
>
> **Key Requirements:**
>
> - Use exact color codes from brand palette
> - Tree of Life with Celtic knotwork style
> - Deliver SVG + PNG sizes: 1024, 512, 256, 128, 64, 32, 16
> - Include favicon.ico
> - Organize in logos/svg/ and logos/png/ folders
> - Include measurements PDF
>
> **Deliverable Format:** ZIP file with folder structure as specified, plus preview image.

---

_This document ensures all design assets are development-ready and require no post-processing before implementation._
