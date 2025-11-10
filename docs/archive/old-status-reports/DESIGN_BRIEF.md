# Design Brief: Professional Astrology Companion App

## Project Overview

**App Name:** Mula (The Root)  
**Purpose:** A professional companion tool for astrologers to generate natal charts, track client readings, log predictions, and develop their methodology.  
**Target User:** Solo professional astrologer conducting private client consultations  
**Platform:** Web app (mobile-first, responsive design)

---

## Design Direction

### Core Identity

- **NOT a consumer app** - This is a professional tool for practitioners
- **NOT mystical/cosmic/ethereal** - Avoid typical astrology app aesthetics
- Should feel like: Modern SaaS tools (Linear, Notion, Arc browser)
- Inspiration: Clinical precision meets elegant design
- Tone: Professional, trustworthy, efficient, intelligent

### Brand Keywords & Visual Motifs

**"Mula" = The Root** - Foundation, origin, source intelligence
**"Synthesis"** - Combining traditional wisdom with modern data visualization

Visual motifs to explore:

- **Root systems/networks**: Subtle background patterns suggesting interconnection (like mycelium or neural networks)
- **Convergence**: Multiple data streams coming together into unified insights
- **Layered knowledge**: Transparent overlays showing depth of analysis
- **Growth/evolution**: Progressive disclosure, expanding complexity
- **Organic geometry**: Natural mathematical patterns (spirals, fractals) rendered in clean vectors

These should be **subtle and modern** - think generative art or data visualization aesthetics, not mystical mandalas.

### Visual Style

**Primary Aesthetic:** Neo-brutalist minimalism with subtle depth

- Clean geometric shapes
- Strong contrast and hierarchy
- Purposeful use of negative space
- Sophisticated color palette (not mystical purples/golds)
- Modern sans-serif typography
- Subtle gradients or glass morphism for depth

**Alternative Aesthetic:** Scandinavian minimalism with data visualization focus

- Light/neutral base with strategic color accents
- Chart-focused design language
- Information hierarchy through typography and spacing
- Clean data tables and cards
- Professional dashboard aesthetic

---

## Key Screens to Design

### 1. Landing Page (Desktop & Mobile)

**Purpose:** Quick entry point for returning users, minimal marketing
**Key Elements:**

- Minimal hero: "Chart Reading Simplified" tagline
- Two primary CTAs: "New Reading" + "Dashboard"
- 3-4 feature highlights (Swiss Ephemeris calculations, prediction tracking, session notes, client management)
- Clean footer with settings link
- **Mood:** Confident, professional, get-to-work feel

### 2. Dashboard (Desktop & Mobile)

**Purpose:** Command center for active work
**Key Elements:**

- Stats overview: Total readings, this week, active clients (3 stat cards)
- Quick actions grid: New Chart, View Readings, Settings (3-4 cards)
- Recent charts list (5 most recent with date, location, view link)
- Empty state for new users
- **Mood:** Productive workspace, clear information hierarchy

**Data Density Considerations:**

Moderate information density - balance overview with detail:

- **Stats cards:** Large numbers with micro-charts (sparklines showing trend)
- **Recent charts:** Compact list with key info visible, expandable for notes preview
- **Pagination:** Show 10-20 recent items, "View All" link to full archive
- **Filters:** Quick filters at top (This week | This month | All time)

### 3. Chart Reading Tool (Desktop & Mobile)

**Purpose:** Primary work interface for creating natal charts
**Key Elements:**

- Left panel: Birth data form (date, time, location, coordinates, timezone)
- Center: Chart wheel visualization (SVG with zodiac signs, houses, planets)
- Right panel (collapsible on mobile):
  - Prediction tracking list (transit, dasha, progression, aspect, custom types)
  - Client observation notes textarea
  - Method development notes textarea
  - Save session button
- **Mood:** Focused workspace, all tools at hand, distraction-free

**Data Density Considerations:**

This screen will have HIGH information density - need smart layout strategies:

- **Three-panel layout (desktop):**
  - Left sidebar: 280px (form inputs, collapsible)
  - Center canvas: Flexible (chart wheel + planet table below)
  - Right sidebar: 320px (predictions, notes, scrollable)

- **Tab system for dense data:**
  - Primary tabs: "Chart View" | "Predictions" | "Notes" | "Aspects"
  - Keeps chart wheel always visible on main tab
  - Secondary data in organized tabs to prevent overwhelm

- **Collapsible sections with counts:**
  - "Predictions (12)" - collapse/expand to manage vertical space
  - "Transits (5)" | "Dashas (3)" | "Custom (4)"
  - Smart defaults: Start with most recent/relevant expanded

- **Data tables with filtering:**
  - Planet positions table below chart: sortable columns
  - Aspect grid: filter by type (major/minor), orb tolerance
  - Quick filters: "Show only active transits"

- **Scroll behavior:**
  - Chart wheel: Fixed/sticky at top
  - Sidebars: Independent scroll regions
  - Mobile: Vertical scroll with sticky chart at top

- **Responsive strategy:**
  - Desktop (1200px+): Three-panel layout
  - Tablet (768-1199px): Chart + one sidebar, second sidebar as drawer
  - Mobile (<768px): Vertical stack with chart first, data below in accordion sections

**Information Hierarchy:**

1. Chart wheel (primary visual)
2. Planet positions (essential reference)
3. Active predictions (secondary focus)
4. Notes/annotations (tertiary, collapsible)
5. Aspect details (on-demand, modal/drawer)

### 4. Mobile Navigation

**Key Elements:**

- Bottom tab bar or hamburger menu
- Quick access to: Dashboard, New Reading, Readings List, Profile
- Minimal chrome, content-focused

---

## Design System Components Needed

### Typography

- **Display font:** For headings and hero text (modern, geometric, high-contrast)
- **Body font:** For reading/data entry (excellent readability, professional)
- **Mono font:** For coordinates, timestamps, technical data
- Font scale: Mobile-first (16px base, scaling up to 18px desktop)

### Color Palette

**Option 1: Tech Professional**

- Primary: Deep slate/charcoal (#1e293b, #0f172a)
- Accent: Electric blue or cyan (#3b82f6, #06b6d4)
- Semantic: Success green, warning amber, error red
- Text: High-contrast whites and grays
- Backgrounds: Layered darks with subtle gradients

**Option 2: Clinical Modern**

- Primary: Off-white/cream (#fafaf9, #f5f5f4)
- Accent: Deep indigo or forest green (#4f46e5, #059669)
- Semantic: Muted success/warning/error states
- Text: Near-black with excellent contrast
- Backgrounds: Soft neutrals with card elevation

### UI Components to Design

1. **Buttons:** Primary, secondary, ghost variants (with hover/active states)
2. **Input fields:** Text, number, date, time, select/dropdown (with validation states)
3. **Cards:** Stat cards, action cards, chart list items, feature cards
4. **Tables/Lists:** Recent charts, prediction log, planet positions
5. **Modals/Overlays:** Confirmation dialogs, info tooltips
6. **Empty states:** New user prompts, no data messages
7. **Loading states:** Skeletons, spinners for chart calculations
8. **Navigation:** Top nav, mobile bottom bar, breadcrumbs

---

## Icon Style

- **NOT:** Mystical symbols, ornate glyphs, cosmic imagery
- **YES:** Geometric line icons, outlined style, 24px grid system
- Examples: Chart icon (line graph/circle), Note icon (document), User icon (profile), Settings (gear)
- For planet symbols: Use Unicode glyphs (☉☽☿♀♂♃♄♅♆♇) but styled consistently

---

## Chart Wheel Specific Design

The birth chart wheel is the centerpiece visualization:

- **Style:** Clean SVG, not hand-drawn or ornate
- **Elements:** 12 houses (pie wedges), zodiac signs (outer ring), planets (positioned by degree), aspect lines (optional toggle)
- **Interactivity:** Hover states for tooltips, zoom controls, aspect line toggle
- **Responsive:** Scales from mobile (300px) to desktop (600px+)

### Modern Planet Color System (Synthesis Approach)

**Philosophy:** Modernize traditional planetary associations while maintaining archetypal recognition. Colors should work in both light and dark modes.

- **☉ Sun:** Warm amber `#f59e0b` (not pure gold - more refined, sustainable energy)
- **☽ Moon:** Cool silver-blue `#94a3b8` (not stark white - reflective, subtle)
- **☿ Mercury:** Electric cyan `#06b6d4` (communication, speed, neural pathways)
- **♀ Venus:** Rose copper `#ec4899` (refined pink, not pastel - creative synthesis)
- **♂ Mars:** Deep crimson `#dc2626` (assertive red, not aggressive - controlled power)
- **♃ Jupiter:** Royal indigo `#6366f1` (wisdom blue-purple, not cosmic - expansive intelligence)
- **♄ Saturn:** Graphite slate `#475569` (structured gray, not black - architectural foundation)
- **♅ Uranus:** Bright teal `#14b8a6` (innovation, not neon - breakthrough clarity)
- **♆ Neptune:** Misty violet `#8b5cf6` (intuitive purple, not mystical - liminal awareness)
- **♇ Pluto:** Deep burgundy `#9f1239` (transformation red-black - root power)

**Aspect Line Colors:**

- **Trine/Sextile (harmony):** Soft emerald `#10b981`
- **Square/Opposition (tension):** Amber warning `#f59e0b`
- **Conjunction (fusion):** Neutral slate `#64748b`

**House Colors:**

- Alternating subtle fills: `#1e293b` and `#0f172a` (dark mode) or `#f8fafc` and `#f1f5f9` (light mode)
- Should recede visually to prioritize planets/aspects

---

## Interaction Patterns

- **Form flow:** Progressive disclosure (only show what's needed)
- **Data entry:** Smart defaults, autocomplete for locations, timezone detection
- **Feedback:** Immediate validation, success confirmations, error messages in context
- **Saving:** Auto-save draft notes, manual save for finalized sessions
- **Navigation:** Breadcrumbs for deep navigation, clear back buttons

### Animation & Micro-interactions

**Philosophy:** Purposeful motion that enhances understanding, not decoration.

**Successful Modern Animation Patterns:**

1. **Page Transitions** (200-300ms ease-out)
   - Subtle slide-up fade-in for new views
   - Crossfade between dashboard sections
   - Example: Linear's smooth view changes

2. **Data Loading States** (Skeleton → Content)
   - Shimmer effect on skeleton screens (1.5s wave)
   - Stagger load for list items (50ms delay between items)
   - Example: Stripe dashboard loading patterns

3. **Chart Wheel Animations**
   - **Initial render:** Planets fade in sequentially by orbital distance (Sun→Moon→Mercury, etc.) over 800ms
   - **Aspect lines:** Draw in after planets settle (400ms stagger)
   - **Hover:** Gentle scale (1.05x) + glow effect on planet symbols
   - **Rotation:** Smooth drag-to-rotate with momentum physics

4. **Interactive Feedback** (60-150ms)
   - Button press: Subtle scale down (0.98x) + brightness shift
   - Toggle switches: Smooth slide with spring physics
   - Checkbox/radio: Check mark draw-in animation
   - Example: Arc browser's snappy interactions

5. **Data Visualization Transitions**
   - Number counters: Smooth count-up for stats (400ms)
   - Progress bars: Fill animation with easing
   - List reordering: Smooth position transitions (300ms)
   - Example: Vercel deployment animations

6. **Contextual Animations**
   - **Success:** Subtle green glow pulse + checkmark
   - **Error:** Red shake (3 rapid 5px horizontal shifts)
   - **Save:** Brief outline pulse on saved sections
   - **Delete:** Fade out + scale down (200ms)

7. **Background Subtlety**
   - Very slow gradient shift (60s cycle) on hero sections
   - Parallax scroll (0.5x speed) for layered elements
   - Ambient noise texture (animated grain)

**Animation Principles:**

- ⚡ **Performance first:** GPU-accelerated properties only (transform, opacity)
- 🎯 **Purposeful:** Every animation should communicate state or guide attention
- ⏱️ **Timing:** Fast actions (<200ms), moderate transitions (200-400ms), ambient slow (60s+)
- ♿ **Accessible:** Respect `prefers-reduced-motion` media query
- 🔇 **Subtle:** Animations should feel natural, not call attention to themselves

**Avoid:**

- ❌ Bouncy/elastic easing (too playful for professional tool)
- ❌ Long transitions (>500ms makes app feel slow)
- ❌ Decorative particles or confetti
- ❌ Spinning/rotating loaders (use progress bars or skeletons)

---

## Accessibility Requirements

- WCAG 2.1 AA compliant color contrast (4.5:1 text, 3:1 UI)
- Keyboard navigation for all interactions
- Screen reader friendly (proper ARIA labels)
- Focus indicators on interactive elements
- Responsive touch targets (minimum 44x44px)

---

## Technical Constraints

- Built with: Next.js 16 + React 19 + TypeScript
- Styling: CSS modules or Tailwind (need design tokens)
- Chart rendering: SVG with React components
- Icons: Can use icon library (Heroicons, Lucide, Phosphor) or custom SVG
- Fonts: Web fonts (Google Fonts or self-hosted)

---

## Deliverables Needed

### From AI Design Tool (MidJourney/DALL-E/etc.)

1. **Hero/landing page mockup** (desktop 1920x1080, mobile 390x844)
2. **Dashboard mockup** (desktop and mobile)
3. **Chart reading tool interface** (desktop wide layout)
4. **Color palette visualization** (swatches with hex codes)
5. **Typography pairing examples** (heading + body combos)
6. **UI component kit** (buttons, cards, inputs in various states)
7. **Icon set** (at least 12-15 core icons)

### Design Tokens to Extract

- Color values (primary, accent, semantic, grays)
- Font families and weights
- Spacing scale (4px, 8px, 16px, 24px, 32px, etc.)
- Border radius values
- Shadow/elevation system
- Breakpoint values

---

## Prompt Template for AI Image Generation

```
Design a modern, professional web application interface for a natal chart astrology tool used by professional astrologers.

Brand concept: "Mula" (The Root) - synthesis of traditional astrological wisdom with modern data intelligence. Visual themes: root systems, knowledge networks, layered synthesis, organic geometry rendered cleanly.

Style: [Neo-brutalist minimalism / Scandinavian design / Clinical modern]
Layout: [Landing page / Dashboard / Chart reading tool]
Viewport: [Desktop 1920x1080 / Mobile 390x844]

Key requirements:
- NOT mystical, cosmic, or ornate - should feel like a modern SaaS tool
- Clean geometric shapes, strong hierarchy, purposeful negative space
- Subtle visual motifs: interconnected networks, convergence patterns (think mycelium or neural pathways, not mandalas)
- Color palette: [Deep slate (#0f172a) with electric cyan (#06b6d4) accents / Cream (#fafaf9) with deep indigo (#4f46e5) accents]
- Planet colors from modern synthesis palette (sun=#f59e0b, moon=#94a3b8, mercury=#06b6d4, venus=#ec4899, mars=#dc2626, jupiter=#6366f1, saturn=#475569, uranus=#14b8a6, neptune=#8b5cf6, pluto=#9f1239)
- Typography: Modern sans-serif, excellent readability, 14-16px minimum body text
- Professional aesthetic similar to Linear, Notion, or Arc browser
- [For data-heavy screens: Include tabbed sections, collapsible panels, data tables with clear hierarchy]
- Focus on data visualization and information hierarchy
- Include [specific UI elements for this screen]

Mood: Professional, trustworthy, efficient, intelligent workspace for practitioners synthesizing complex information
```

---

## Reference Apps for Inspiration

- **Linear** - Project management (clean, fast, purposeful)
- **Arc Browser** - Web browser (beautiful gradients, card design)
- **Notion** - Note-taking (flexible layouts, typography hierarchy)
- **Stripe Dashboard** - Payment analytics (data visualization, tables)
- **Vercel Dashboard** - Deployment platform (dark mode, stats cards)
- **Figma** - Design tool (tool panels, canvas workspace)

**NOT like:** Co-Star, TimePassages, AstroSeek (too mystical/consumer-focused)

---

## Questions to Refine Design Direction

1. Do you prefer dark mode (slate/charcoal) or light mode (cream/neutral)?
2. Bold geometric shapes or soft Scandinavian minimalism?
3. Single accent color or dual accent system?
4. Illustrations/graphics or pure UI design?
5. Glass morphism effects or flat matte surfaces?

---

## Data Readability & High-Density Layouts

### Core Principles for Dense Data

**Typography Hierarchy:**

- Use font-weight and size to establish clear information layers
- Monospace for technical data (coordinates, degrees, timestamps)
- Sans-serif for labels and prose
- Minimum 14px for body text, 12px for metadata

**Visual Grouping:**

- Cards/panels with subtle borders or shadows to separate content blocks
- Consistent padding: 16px (mobile), 24px (desktop)
- Line-height: 1.5-1.6 for readability in dense paragraphs

**Color for Categorization:**

- Use planet colors (from synthesis palette) to quickly identify data types
- Semantic colors for status (active/pending/archived predictions)
- Low-contrast backgrounds for different data regions

**Progressive Disclosure:**

- Show summary data first, expand for details
- Accordion sections for large datasets
- "Show more" buttons instead of overwhelming initial load
- Tooltip/popovers for supplementary info

**Table Design for Dense Data:**

- Alternating row colors for easy scanning
- Fixed header row when scrolling long tables
- Sortable columns with clear indicators
- Compact mode toggle (reduce row height for power users)

**Mobile Strategy:**

- Horizontal scroll for wide tables (with scroll hint)
- Card view for list data instead of tables
- Stack data vertically with clear section headers
- Swipe gestures for quick actions (archive, favorite)

**Example Data-Dense Screens:**

- Airtable (grid view with filtering)
- Notion database views (multiple view types)
- Linear issues list (compact, scannable)
- GitHub pull request files (collapsible sections)

---

## Next Steps After Receiving Assets

1. Extract color hex codes → Create CSS custom properties
2. Identify font pairings → Add to globals.css
3. Screenshot UI components → Rebuild in React/Tailwind
4. Design spacing system → Create spacing scale variables
5. Implement responsive breakpoints from mockups
6. Create component library matching designs
