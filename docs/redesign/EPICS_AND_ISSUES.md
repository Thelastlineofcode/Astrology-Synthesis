# BMAD Astrology App - Epics and Issues

## 📋 Project Kanban Board Structure

**Columns**: Backlog → To Do → In Progress → Review → Done

---

## EPIC 1: Design System & Foundation 🎨

**Description**: Establish the core design system including color palette, typography, spacing, and reusable UI components that will be used across the entire application.

**Priority**: P0 (Blocking - must complete first)  
**Estimated Effort**: 2 weeks  
**Dependencies**: None  
**Reference**: COLOR_SCHEMES.md, DESIGN_INSPIRATION.md

---

### Issue 1.1: Set Up CSS Variables & Theme System

**Labels**: `design-system`, `foundation`, `p0`

**Description**:
Implement the "Healing Cosmos" color palette and spacing system using CSS custom properties. Include light/dark mode support with theme toggle functionality.

**Acceptance Criteria**:
- [ ] All colors from COLOR_SCHEMES.md defined as CSS variables
- [ ] Spacing scale (4px, 8px, 16px, 24px, 32px, 48px, 64px) implemented
- [ ] Light and dark theme variants created
- [ ] Theme persists in localStorage
- [ ] Theme toggle component functional
- [ ] `prefers-color-scheme` media query respected

**Implementation Notes**:
```css
/* /frontend/src/styles/variables.css */
:root {
  /* Colors - Healing Cosmos Palette */
  --color-primary: #3E4B6E;
  --color-primary-light: #5A6B8F;
  --color-primary-dark: #2C3651;
  
  --color-secondary: #A5B8A4;
  --color-secondary-light: #C4D4C3;
  --color-secondary-dark: #8A9C89;
  
  /* Spacing Scale */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 16px;
  --space-4: 24px;
  /* ... etc */
}

[data-theme="dark"] {
  --text-primary: var(--color-neutral-50);
  /* Override for dark mode */
}
```

**Testing**:
- [ ] Contrast ratios meet WCAG AA (4.5:1 for text)
- [ ] Theme toggle works without page refresh
- [ ] All components inherit theme correctly

**Reference**: COLOR_SCHEMES.md (CSS Variables Structure section)

---

### Issue 1.2: Typography System Setup

**Labels**: `design-system`, `foundation`, `p0`

**Description**:
Implement typography scale using Inter or Plus Jakarta Sans with proper hierarchy, line heights, and responsive sizing.

**Acceptance Criteria**:
- [ ] Font files loaded (local or Google Fonts)
- [ ] Typography scale defined (H1-H3, body, small, tiny)
- [ ] Responsive font sizes for mobile/tablet/desktop
- [ ] Line heights set (1.5 body, 1.2 headings)
- [ ] Font weights defined (Regular, Medium, Semibold)
- [ ] Typography CSS classes created

**Implementation Notes**:
```css
/* /frontend/src/styles/typography.css */
:root {
  /* Desktop Scale */
  --font-size-h1: 32px;
  --font-size-h2: 24px;
  --font-size-h3: 20px;
  --font-size-body: 16px;
  --font-size-small: 14px;
  --font-size-tiny: 12px;
  
  --line-height-heading: 1.2;
  --line-height-body: 1.5;
  
  --font-family-base: 'Inter', system-ui, sans-serif;
  --font-family-accent: 'Crimson Text', serif;
}

@media (max-width: 767px) {
  :root {
    --font-size-h1: 28px;
    --font-size-h2: 22px;
    /* ... mobile scale */
  }
}
```

**Testing**:
- [ ] Text readable on all screen sizes
- [ ] Font weight variations display correctly
- [ ] No FOUT (Flash of Unstyled Text)

**Reference**: DESIGN_INSPIRATION.md (Typography Inspiration section)

---

### Issue 1.3: Create Button Component Library

**Labels**: `component`, `design-system`, `p0`

**Description**:
Build reusable button component with Primary, Secondary, Tertiary, and Icon variants. Include hover, active, disabled, and loading states.

**Acceptance Criteria**:
- [ ] Button component accepts variant prop
- [ ] All states implemented (hover, active, disabled, loading)
- [ ] Keyboard accessible (Enter/Space triggers click)
- [ ] Focus indicator visible (2px outline, 2px offset)
- [ ] Min touch target 44px × 44px on mobile
- [ ] Loading spinner integrated
- [ ] ARIA attributes present

**Component Signature**:
```jsx
// /frontend/src/components/shared/Button.jsx
<Button 
  variant="primary" // primary | secondary | tertiary | icon
  size="medium"     // small | medium | large
  disabled={false}
  loading={false}
  onClick={handleClick}
  ariaLabel="Calculate Chart"
>
  Calculate Chart
</Button>
```

**Styles**:
- Primary: Deep Indigo bg, Cream text
- Secondary: Transparent bg, Deep Indigo border/text
- Tertiary: Transparent bg, Deep Indigo text (underline on hover)
- Icon: Circular, 44px min, icon only

**Testing**:
- [ ] Keyboard navigation works
- [ ] Screen reader announces button purpose
- [ ] Hover states smooth (150ms transition)
- [ ] Disabled state clearly visible

**Reference**: DESIGN_INSPIRATION.md (Interactive Elements - Buttons)

---

### Issue 1.4: Create Card Component Variants

**Labels**: `component`, `design-system`, `p0`

**Description**:
Build the foundational Card component with multiple variants (Basic, Stat, Image, Action, Expansion, Highlight) that will be used throughout the app.

**Acceptance Criteria**:
- [ ] Card base component with 12px border radius
- [ ] Shadow system: default (2px 8px), hover (4px 16px)
- [ ] 6+ variants implemented
- [ ] Expansion cards animate smoothly
- [ ] Cards responsive (stack on mobile)
- [ ] Semantic HTML (article, section tags)

**Component Signature**:
```jsx
// /frontend/src/components/shared/Card.jsx
<Card 
  variant="basic"  // basic | stat | image | action | expansion | highlight
  padding="medium" // small | medium | large
  elevated={false} // adds hover shadow
  onClick={optional}
>
  {children}
</Card>

// Stat Card Example
<Card variant="stat">
  <Card.Icon><CalendarIcon /></Card.Icon>
  <Card.Metric>7 days</Card.Metric>
  <Card.Label>Journal Streak</Card.Label>
</Card>
```

**Variants**:
1. **Basic**: Simple container, cream bg
2. **Stat**: Icon + metric + label, centered
3. **Image**: Image header + content
4. **Action**: Includes CTA button at bottom
5. **Expansion**: Collapsible with chevron
6. **Highlight**: Gradient border, featured content

**Testing**:
- [ ] Cards stack properly on mobile
- [ ] Expansion animation < 250ms
- [ ] Hover states work on desktop only
- [ ] Touch feedback on mobile

**Reference**: COMPONENT_STRUCTURE.md (Card Variants section)

---

### Issue 1.5: Form Elements (Input, Select, Checkbox, Toggle)

**Labels**: `component`, `design-system`, `p0`

**Description**:
Create accessible form components with validation states, labels, and error messaging.

**Acceptance Criteria**:
- [ ] Input, Textarea, Select, Checkbox, Radio, Toggle components
- [ ] Validation states (default, focus, error, success)
- [ ] Floating labels or clear placeholders
- [ ] Error messages below fields
- [ ] Required field indicators (*)
- [ ] ARIA attributes (aria-invalid, aria-describedby)
- [ ] Keyboard navigation (Tab, Arrow keys for Select)

**Component Signature**:
```jsx
// /frontend/src/components/shared/Input.jsx
<Input
  type="text"
  name="year"
  label="Birth Year"
  value={value}
  onChange={handleChange}
  error={errors.year}
  required={true}
  placeholder="1990"
/>

// Toggle Switch
<Toggle
  checked={darkMode}
  onChange={toggleTheme}
  label="Dark Mode"
/>
```

**Styles**:
- Border: 1px Soft Sage (30% opacity)
- Focus: Deep Indigo border + box shadow
- Error: Terracotta border
- Border radius: 6px
- Padding: 12px 16px

**Testing**:
- [ ] Form validation works
- [ ] Screen reader announces errors
- [ ] Keyboard navigation smooth
- [ ] Touch targets adequate (44px)

**Reference**: DESIGN_INSPIRATION.md (Form Elements section)

---

### Issue 1.6: Loading & Feedback Components

**Labels**: `component`, `design-system`, `p1`

**Description**:
Create loading spinners, skeleton screens, progress bars, toasts, and alert banners for user feedback.

**Acceptance Criteria**:
- [ ] Spinner component (circular, branded colors)
- [ ] Skeleton loader for cards and lists
- [ ] Progress bar (linear, determinate/indeterminate)
- [ ] Toast notification system
- [ ] Alert banners (info, success, warning, error)
- [ ] Accessible announcements (aria-live)

**Component Signatures**:
```jsx
// Spinner
<Spinner size="medium" label="Loading chart..." />

// Skeleton
<Skeleton variant="card" count={3} />

// Toast
showToast({ message: "Chart saved!", type: "success" });

// Alert Banner
<Alert type="info" dismissible>
  Your chart is ready to explore!
</Alert>
```

**Testing**:
- [ ] Screen reader announces loading states
- [ ] Toasts auto-dismiss after 5 seconds
- [ ] Skeleton matches content layout
- [ ] Animations respect reduced motion

**Reference**: UX_COPY_GUIDE.md (Loading States section)

---

## EPIC 2: Layout & Navigation 🏗️

**Description**: Build the core application shell with responsive navigation, sidebar, header, and routing structure.

**Priority**: P0 (Blocking)  
**Estimated Effort**: 1 week  
**Dependencies**: Epic 1 (Design System)  
**Reference**: COMPONENT_STRUCTURE.md (Core Layout Components)

---

### Issue 2.1: App Shell & Routing Setup

**Labels**: `layout`, `navigation`, `p0`

**Description**:
Create the main app structure with React Router, persistent header, collapsible sidebar, and main content area.

**Acceptance Criteria**:
- [ ] React Router v6 configured
- [ ] Routes defined for all main sections
- [ ] Header component (logo, search, profile, notifications)
- [ ] Sidebar navigation (collapsible on mobile)
- [ ] Main content area with proper padding
- [ ] Footer (minimal)
- [ ] Mobile: Bottom navigation bar
- [ ] Tablet/Desktop: Side navigation

**Routes**:
```jsx
// /frontend/src/App.jsx
<Routes>
  <Route path="/" element={<Dashboard />} />
  <Route path="/chart" element={<NatalChart />} />
  <Route path="/bmad" element={<BMADAnalysis />} />
  <Route path="/symbolon" element={<SymbolonCards />} />
  <Route path="/journal" element={<Journal />} />
  <Route path="/workflows" element={<Workflows />} />
  <Route path="/settings" element={<Settings />} />
</Routes>
```

**Testing**:
- [ ] Navigation works on all devices
- [ ] Active route highlighted
- [ ] Sidebar collapses on mobile
- [ ] Skip to content link present

**Reference**: COMPONENT_STRUCTURE.md (App Shell section)

---

### Issue 2.2: Header Navigation Component

**Labels**: `layout`, `navigation`, `p0`

**Description**:
Build persistent header with logo, search bar, user profile dropdown, and notification bell.

**Acceptance Criteria**:
- [ ] Header sticky at top
- [ ] Logo/brand links to dashboard
- [ ] Search bar functional (searches journal, cards)
- [ ] Profile dropdown (avatar, name, settings, logout)
- [ ] Notification bell with badge count
- [ ] Mobile: Hamburger menu
- [ ] Keyboard accessible

**Component Structure**:
```jsx
<Header>
  <Logo />
  <SearchBar placeholder="Search journal, cards..." />
  <NotificationBell count={3} />
  <ProfileDropdown user={currentUser} />
</Header>
```

**Testing**:
- [ ] Header responsive on all screens
- [ ] Dropdown closes on outside click
- [ ] Keyboard navigation works (Tab, Enter, Esc)

**Reference**: COMPONENT_STRUCTURE.md (Header Navigation)

---

### Issue 2.3: Sidebar Navigation Component

**Labels**: `layout`, `navigation`, `p0`

**Description**:
Create collapsible sidebar with icons and labels for main sections. Includes active state indication.

**Acceptance Criteria**:
- [ ] Navigation items with icons (Lucide Icons)
- [ ] Active route highlighted
- [ ] Collapse/expand animation
- [ ] Tooltip on collapsed state
- [ ] Keyboard navigation
- [ ] ARIA landmarks (nav, role="navigation")

**Navigation Items**:
- 🏠 Dashboard
- 🌟 Natal Chart
- 🧠 BMAD Analysis
- 🃏 Symbolon Cards
- 📔 Journal
- ⚙️ Workflow Automation
- ⚙️ Settings

**Testing**:
- [ ] Active state clearly visible
- [ ] Sidebar persists state in localStorage
- [ ] Tooltips appear on hover (collapsed mode)

**Reference**: COMPONENT_STRUCTURE.md (Sidebar Navigation)

---

### Issue 2.4: Mobile Bottom Navigation

**Labels**: `layout`, `navigation`, `mobile`, `p1`

**Description**:
Create bottom navigation bar for mobile devices with quick access to top 5 sections.

**Acceptance Criteria**:
- [ ] Fixed position at bottom on mobile only
- [ ] Icons with labels
- [ ] Active tab highlighted
- [ ] Safe area inset for iOS
- [ ] Touch targets 44px minimum

**Mobile Nav Items**:
- Dashboard, Chart, BMAD, Journal, More (overflow menu)

**Testing**:
- [ ] Only visible on mobile (<768px)
- [ ] Doesn't overlap content
- [ ] Active state visible

**Reference**: COMPONENT_STRUCTURE.md (Responsive Behavior - Mobile)

---

## EPIC 3: Dashboard 📊

**Description**: Create the main dashboard with personalized welcome, quick actions, insight cards, and activity timeline.

**Priority**: P0  
**Estimated Effort**: 1.5 weeks  
**Dependencies**: Epic 1 (Design System), Epic 2 (Layout)  
**Reference**: COMPONENT_STRUCTURE.md (Dashboard Components)

---

### Issue 3.1: Dashboard Hero & Welcome Section

**Labels**: `dashboard`, `p0`

**Description**:
Create personalized welcome message with time-based greeting and quick action buttons.

**Acceptance Criteria**:
- [ ] Greeting changes by time ("Good morning", "Welcome back")
- [ ] User's name displayed
- [ ] Quick action card with 4 CTAs
- [ ] Responsive layout (stacks on mobile)
- [ ] Empty state for new users

**Quick Actions**:
1. Generate Chart
2. View Last Analysis
3. Start Journal Entry
4. Explore Archetypes

**Copy Reference**: UX_COPY_GUIDE.md (Dashboard - Hero Welcome)

**Testing**:
- [ ] Greeting updates correctly
- [ ] Empty state shows for new users
- [ ] All CTAs functional

---

### Issue 3.2: Insights Grid - Card Components

**Labels**: `dashboard`, `component`, `p0`

**Description**:
Build dashboard insight cards: Today's Transit, BMAD Highlight, Primary Archetype, Journal Streak, Progress Tracker.

**Acceptance Criteria**:
- [ ] 5 insight cards implemented
- [ ] Cards use consistent Card component
- [ ] Data fetched from API/localStorage
- [ ] Loading states for async data
- [ ] Empty states with CTAs
- [ ] Grid layout (responsive)

**Card Types**:
1. **Today's Transit** - Current planetary movements
2. **BMAD Dimension Highlight** - Featured dimension score
3. **Primary Archetype Card** - Top Symbolon card
4. **Journal Streak** - Day count with fire emoji
5. **Progress Tracker** - Overall completion

**Testing**:
- [ ] Cards load without layout shift
- [ ] Empty states encourage action
- [ ] Grid responsive on all screens

**Reference**: COMPONENT_STRUCTURE.md (Insights Grid)

---

### Issue 3.3: Recent Activity Timeline

**Labels**: `dashboard`, `p1`

**Description**:
Display chronological timeline of recent user actions (charts generated, journal entries, card draws).

**Acceptance Criteria**:
- [ ] Timeline shows last 10 activities
- [ ] Activity types clearly differentiated (icons, colors)
- [ ] Timestamps relative ("2 hours ago")
- [ ] Click activity to view details
- [ ] Empty state: "Start exploring to see your activity"

**Activity Types**:
- Chart generated
- Journal entry created
- BMAD analysis completed
- Symbolon cards drawn
- Workflow activated

**Testing**:
- [ ] Timeline updates in real-time
- [ ] Links to activities work
- [ ] Timestamps accurate

**Reference**: COMPONENT_STRUCTURE.md (Quick Links Section)

---

## EPIC 4: Natal Chart Viewer (Enhanced) 🌟

**Description**: Enhance the existing natal chart calculator with improved UI, interactive chart visualization, and comprehensive interpretations.

**Priority**: P0  
**Estimated Effort**: 2 weeks  
**Dependencies**: Epic 1, Epic 2  
**Reference**: COMPONENT_STRUCTURE.md (Natal Chart Components)

---

### Issue 4.1: Chart Input Form - Simplified UI

**Labels**: `chart`, `form`, `p0`

**Description**:
Redesign birth data input form with better UX, validation, and sample data loading.

**Acceptance Criteria**:
- [ ] Clean, spacious form layout
- [ ] Date/time inputs with proper validation
- [ ] Coordinate inputs OR location search
- [ ] "Load Sample" button with Metairie, LA data
- [ ] Chart options (Zodiac type, House system, Ayanamsa)
- [ ] Real-time validation feedback
- [ ] Mobile-friendly inputs

**Current Implementation**: `SimpleBirthDataForm.jsx` - enhance this

**Improvements Needed**:
- Better visual hierarchy
- Clearer labels and help text
- Coordinate validation
- Time zone handling clarity

**Copy Reference**: UX_COPY_GUIDE.md (Birth Data Collection)

**Testing**:
- [ ] Form validates before submission
- [ ] Sample data loads correctly
- [ ] Errors display clearly

---

### Issue 4.2: Interactive Chart Canvas (SVG)

**Labels**: `chart`, `visualization`, `p1`

**Description**:
Create interactive SVG natal chart wheel with zoom, pan, and hover tooltips for planets and aspects.

**Acceptance Criteria**:
- [ ] Chart wheel rendered in SVG
- [ ] Planet glyphs positioned accurately
- [ ] House divisions visible
- [ ] Aspect lines (toggleable)
- [ ] Hover tooltips show planet details
- [ ] Zoom controls (+/- buttons)
- [ ] Responsive sizing

**Chart Controls**:
- Zoom in/out
- Toggle aspects on/off
- Filter aspect types (major/minor)
- Export as PNG
- Print-friendly view

**Testing**:
- [ ] Chart accurate for test data
- [ ] Tooltips don't overflow viewport
- [ ] Zoom smooth, doesn't break layout

**Reference**: COMPONENT_STRUCTURE.md (Chart Viewer)

---

### Issue 4.3: Interpretation Accordion Panels

**Labels**: `chart`, `content`, `p0`

**Description**:
Display chart interpretations in collapsible accordion format with sections for Sun, Moon, Rising, Planets, Houses, Aspects.

**Acceptance Criteria**:
- [ ] Accordion component with smooth animation
- [ ] Sections: Sun, Moon, Rising, Planets, Houses, Aspects
- [ ] Each section expandable/collapsible
- [ ] Deep link support (#sun-sign)
- [ ] Print includes all expanded content
- [ ] Keyboard navigation (Arrow keys)

**Content Structure**:
```jsx
<Accordion>
  <AccordionItem title="Your Core Identity: Leo Sun">
    <p>The Sun represents your essential self...</p>
    {/* Interpretation content */}
  </AccordionItem>
  {/* Repeat for other sections */}
</Accordion>
```

**Copy Reference**: UX_COPY_GUIDE.md (Chart Interpretation Sections)

**Testing**:
- [ ] Only one section open at a time (optional)
- [ ] Smooth expand/collapse animation
- [ ] Deep links work

**Reference**: COMPONENT_STRUCTURE.md (Interpretation Panel)

---

### Issue 4.4: Chart Results Display - Planets List

**Labels**: `chart`, `display`, `p0`

**Description**:
Enhance PlanetList component with better formatting, zodiac symbols, and degree precision.

**Current Component**: `PlanetList.jsx` - refactor/enhance

**Acceptance Criteria**:
- [ ] Table or card layout
- [ ] Planet glyphs (symbols)
- [ ] Zodiac sign symbols
- [ ] Degree formatting (°'")
- [ ] Retrograde indicator (℞)
- [ ] House placement
- [ ] Responsive layout

**Testing**:
- [ ] Data matches chart calculation
- [ ] Symbols display correctly
- [ ] Retrograde clearly visible

---

### Issue 4.5: House Table Enhancement

**Labels**: `chart`, `display`, `p0`

**Description**:
Improve HouseTable component with robust validation and better visual design.

**Current Component**: `HouseTable.jsx` - already has validation from agent PR

**Acceptance Criteria**:
- [ ] Handles houses object structure
- [ ] Displays ascendant and midheaven prominently
- [ ] Shows all 12 house cusps
- [ ] Degree formatting consistent
- [ ] Responsive table design

**Testing**:
- [ ] No more houses.map errors
- [ ] Ascendant/MC displayed correctly
- [ ] Mobile table scrolls horizontally

**Reference**: Agent PR #9 (already merged)

---

## EPIC 5: BMAD Analysis System 🧠

**Description**: Implement the 10-dimension behavioral analysis framework with visualization, recommendations, and detailed dimension views.

**Priority**: P1  
**Estimated Effort**: 2 weeks  
**Dependencies**: Epic 1, Epic 2, backend BMAD API  
**Reference**: COMPONENT_STRUCTURE.md (BMAD Analysis Components)

---

### Issue 5.1: BMAD Landing Page & Overview

**Labels**: `bmad`, `p1`

**Description**:
Create landing page introducing BMAD with assessment CTA and overview of 10 dimensions.

**Acceptance Criteria**:
- [ ] Hero section explaining BMAD
- [ ] "Start Assessment" or "View My Analysis" CTA
- [ ] 10 dimension preview cards
- [ ] Each card shows icon, name, brief description
- [ ] Links to detailed dimension view
- [ ] Responsive grid layout

**Copy Reference**: UX_COPY_GUIDE.md (BMAD Analysis - Landing Page)

**Testing**:
- [ ] CTA prominent and accessible
- [ ] Cards clickable
- [ ] Copy clear and non-technical

---

### Issue 5.2: Dimensional Analysis Grid - 10 Cards

**Labels**: `bmad`, `component`, `p1`

**Description**:
Build dimension cards showing score, percentile, and preview interpretation for each of 10 dimensions.

**10 Dimensions**:
1. Emotional Regulation
2. Social Dynamics
3. Cognitive Patterns
4. Behavioral Tendencies
5. Decision-Making Style
6. Stress Response
7. Communication Style
8. Relationship Patterns
9. Goal Orientation
10. Identity Formation

**Acceptance Criteria**:
- [ ] Each dimension has unique icon
- [ ] Score displayed (X/10 format)
- [ ] Percentile shown
- [ ] Color-coded by dimension (see COLOR_SCHEMES.md)
- [ ] Preview text (1-2 sentences)
- [ ] "Explore" CTA
- [ ] Grid responsive (3 cols desktop, 1 col mobile)

**Dimension Colors**: Reference COLOR_SCHEMES.md (Dimension-Specific Colors)

**Testing**:
- [ ] Scores display accurately
- [ ] Colors match design specs
- [ ] Grid responsive

**Reference**: COMPONENT_STRUCTURE.md (Dimensional Analysis Grid)

---

### Issue 5.3: BMAD Radar Chart Visualization

**Labels**: `bmad`, `visualization`, `p1`

**Description**:
Create radar/spider chart visualizing all 10 dimension scores simultaneously.

**Acceptance Criteria**:
- [ ] 10-point radar chart
- [ ] Scores plotted accurately
- [ ] Dimension labels on axes
- [ ] Filled area colored (Muted Lavender with opacity)
- [ ] Hover shows exact score
- [ ] Responsive (scales on mobile)
- [ ] Export as image option

**Library**: Recharts or D3.js

**Testing**:
- [ ] Chart renders without errors
- [ ] Scales correctly on all screens
- [ ] Hover tooltips work

**Reference**: COMPONENT_STRUCTURE.md (Visualization Dashboard)

---

### Issue 5.4: Dimension Detail View

**Labels**: `bmad`, `content`, `p1`

**Description**:
Create detailed view for individual dimension with full interpretation, strengths, growth areas, and recommendations.

**Acceptance Criteria**:
- [ ] Dimension name and icon header
- [ ] Your score section (numeric + percentile)
- [ ] Full interpretation (3-5 paragraphs)
- [ ] Strengths list
- [ ] Growth opportunities list
- [ ] Related chart placements
- [ ] Action recommendations
- [ ] Navigation to other dimensions

**Content Structure**:
- Score display
- Interpretation text
- Strengths (bullet list)
- Growth areas (bullet list)
- Recommendations (3-5 actionable items)
- Related resources

**Copy Reference**: UX_COPY_GUIDE.md (BMAD Detail View)

**Testing**:
- [ ] Content loads correctly
- [ ] Navigation works
- [ ] Copy helpful and clear

---

### Issue 5.5: BMAD Recommendations Panel

**Labels**: `bmad`, `content`, `p1`

**Description**:
Display personalized recommendations based on BMAD scores with links to journal prompts, resources, and practices.

**Acceptance Criteria**:
- [ ] Top 3-5 recommendations shown
- [ ] Recommendations personalized to scores
- [ ] Links to journal prompts
- [ ] Links to relevant Symbolon cards
- [ ] Links to external resources
- [ ] Bookmarking capability

**Copy Reference**: UX_COPY_GUIDE.md (BMAD Recommendations)

**Testing**:
- [ ] Recommendations relevant to user
- [ ] Links functional
- [ ] Bookmarks persist

**Reference**: COMPONENT_STRUCTURE.md (Recommendations Panel)

---

## EPIC 6: Symbolon Card System 🃏

**Description**: Build the Symbolon archetypal card system with gallery, detail views, spreads, and archetype matching.

**Priority**: P1  
**Estimated Effort**: 1.5 weeks  
**Dependencies**: Epic 1, Epic 2, Symbolon content JSON  
**Reference**: COMPONENT_STRUCTURE.md (Symbolon Card Components)

---

### Issue 6.1: Card Gallery with Grid/List Toggle

**Labels**: `symbolon`, `gallery`, `p1`

**Description**:
Create browsable gallery of 79 Symbolon cards with filtering, search, and view toggle.

**Acceptance Criteria**:
- [ ] Grid view (3-4 cols desktop, 2 mobile)
- [ ] List view (single column with details)
- [ ] Toggle between views
- [ ] Filter by element, archetype type
- [ ] Search by card name
- [ ] Sort by relevance score
- [ ] Card thumbnails with name and relevance badge
- [ ] Lazy loading for performance

**Card Data**: Load from `/backend/content/symbolon_universal_v1.json`

**Testing**:
- [ ] All 79 cards display
- [ ] Filter/search work correctly
- [ ] View toggle smooth
- [ ] Images load progressively

**Reference**: COMPONENT_STRUCTURE.md (Card Gallery)

---

### Issue 6.2: Card Detail Modal

**Labels**: `symbolon`, `modal`, `p1`

**Description**:
Create modal popup showing full card details: image, meaning, astrological correspondence, personal relevance.

**Acceptance Criteria**:
- [ ] Large card image
- [ ] Tabbed interface (Meaning, Your Connection, Reflections)
- [ ] Meaning tab: archetypal interpretation
- [ ] Your Connection: chart placements linked to this card
- [ ] Reflections: text area for user notes
- [ ] Relevance score displayed
- [ ] Share/bookmark buttons
- [ ] Keyboard accessible (Esc closes)

**Modal Structure**:
```jsx
<CardDetailModal card={selectedCard} onClose={handleClose}>
  <Tabs>
    <Tab label="Meaning">
      <CardMeaning card={card} />
    </Tab>
    <Tab label="Your Connection">
      <YourConnection card={card} userChart={chart} />
    </Tab>
    <Tab label="Reflections">
      <ReflectionsEditor cardId={card.id} />
    </Tab>
  </Tabs>
</CardDetailModal>
```

**Copy Reference**: UX_COPY_GUIDE.md (Card Detail Modal)

**Testing**:
- [ ] Modal accessible
- [ ] Tabs navigate smoothly
- [ ] Notes save correctly

**Reference**: COMPONENT_STRUCTURE.md (Card Detail Modal)

---

### Issue 6.3: Card Spread Layouts

**Labels**: `symbolon`, `spreads`, `p1`

**Description**:
Implement card spread functionality: single card, 3-card, Celtic Cross, with question input.

**Acceptance Criteria**:
- [ ] Question input field
- [ ] Spread type selector (1-card, 3-card, Celtic Cross)
- [ ] "Draw Cards" button
- [ ] Cards animate into position
- [ ] Position labels (Past, Present, Future for 3-card)
- [ ] Save spread to history
- [ ] Print spread option

**Spread Types**:
1. **Single Card**: One card for quick insight
2. **3-Card Spread**: Past, Present, Future
3. **Celtic Cross**: 10-card traditional spread
4. **Custom**: User-defined positions (future)

**Testing**:
- [ ] Cards draw randomly from deck
- [ ] Animations smooth
- [ ] Spread saves correctly

**Reference**: COMPONENT_STRUCTURE.md (Card Spread Layouts)

---

### Issue 6.4: Archetype Matching Algorithm

**Labels**: `symbolon`, `algorithm`, `p1`

**Description**:
Implement algorithm to calculate relevance scores for each card based on natal chart placements.

**Acceptance Criteria**:
- [ ] Algorithm considers Sun, Moon, Rising signs
- [ ] Weighs house placements
- [ ] Includes aspect patterns
- [ ] Outputs relevance score (0-100%)
- [ ] Updates when chart changes
- [ ] Top 5 archetypes highlighted

**Algorithm Factors**:
- Sun sign: 30% weight
- Moon sign: 25% weight
- Rising sign: 20% weight
- Dominant element: 15% weight
- Major aspects: 10% weight

**Testing**:
- [ ] Scores calculate correctly
- [ ] Top matches make sense
- [ ] Performance acceptable (<100ms)

**Reference**: COMPONENT_STRUCTURE.md (Archetype Matching)

---

## EPIC 7: Journal System 📔

**Description**: Create personal journaling feature with rich text editor, mood tracking, tags, and analytics.

**Priority**: P1  
**Estimated Effort**: 1.5 weeks  
**Dependencies**: Epic 1, Epic 2  
**Reference**: COMPONENT_STRUCTURE.md (Journal Components)

---

### Issue 7.1: Journal Entry Editor with Rich Text

**Labels**: `journal`, `editor`, `p1`

**Description**:
Build journal entry editor with rich text formatting, mood selector, and tag input.

**Acceptance Criteria**:
- [ ] Rich text editor (bold, italic, lists)
- [ ] Mood selector (6 icons: 😊 😐 😔 😠 😰 😴)
- [ ] Tag input with autocomplete
- [ ] Date/time stamp (auto)
- [ ] Auto-save every 30 seconds
- [ ] Auto-save indicator
- [ ] Character count (optional)
- [ ] "Save" and "Cancel" buttons

**Editor Library**: Draft.js, Slate, or Tiptap

**Copy Reference**: UX_COPY_GUIDE.md (Journal - New Entry)

**Testing**:
- [ ] Auto-save works
- [ ] No data loss on refresh
- [ ] Formatting persists

**Reference**: COMPONENT_STRUCTURE.md (Journal Entry Editor)

---

### Issue 7.2: Journal Entry List View

**Labels**: `journal`, `list`, `p1`

**Description**:
Display list of journal entries with filtering, search, and preview.

**Acceptance Criteria**:
- [ ] Chronological list (newest first)
- [ ] Entry cards show: date, mood icon, excerpt, tags
- [ ] Filter by date range
- [ ] Filter by mood
- [ ] Filter by tags
- [ ] Search by text content
- [ ] Edit/Delete actions
- [ ] Pagination or infinite scroll
- [ ] Empty state with CTA

**Entry Card**:
- Date header (October 28, 2025)
- Mood icon
- Text excerpt (first 100 chars)
- Tags (max 3 visible)
- Edit/Delete icons

**Copy Reference**: UX_COPY_GUIDE.md (Journal Entry List)

**Testing**:
- [ ] Filters work correctly
- [ ] Search fast and accurate
- [ ] Delete confirmation modal

**Reference**: COMPONENT_STRUCTURE.md (Entry List View)

---

### Issue 7.3: Journal Analytics Dashboard

**Labels**: `journal`, `analytics`, `p1`

**Description**:
Build analytics view showing writing streak, mood trends, tag cloud, and consistency heatmap.

**Acceptance Criteria**:
- [ ] Streak counter (days)
- [ ] Streak visualization (calendar heatmap)
- [ ] Mood trends chart (line chart over time)
- [ ] Most used tags (word cloud or list)
- [ ] Writing consistency metrics
- [ ] Total entries count
- [ ] Average entries per week
- [ ] Most active day/time

**Visualizations**:
- Calendar heatmap (GitHub-style)
- Line chart for mood trends
- Tag cloud or bar chart
- Stat cards for key metrics

**Copy Reference**: UX_COPY_GUIDE.md (Journal Analytics)

**Testing**:
- [ ] Charts render correctly
- [ ] Data accurate
- [ ] Responsive on mobile

**Reference**: COMPONENT_STRUCTURE.md (Journal Analytics)

---

### Issue 7.4: Journal Prompts System

**Labels**: `journal`, `prompts`, `p2`

**Description**:
Create system of journal prompts to inspire writing, including astrologically-timed prompts.

**Acceptance Criteria**:
- [ ] "Need inspiration?" button in editor
- [ ] List of 20+ prompts
- [ ] Prompts categorized (reflection, gratitude, growth, etc.)
- [ ] Prompts tied to transits (optional)
- [ ] Random prompt generator
- [ ] Prompt inserts into editor on click

**Sample Prompts**:
- "What am I grateful for today?"
- "What pattern did I notice in myself?"
- "How did my chart show up today?"
- "What emotion needs attention?"

**Copy Reference**: UX_COPY_GUIDE.md (Journal Prompts)

**Testing**:
- [ ] Prompts insert correctly
- [ ] Randomization works
- [ ] Variety of topics

---

## EPIC 8: Workflow Automation ⚡

**Description**: Build no-code workflow automation for transit reminders, journal prompts, and practice rituals.

**Priority**: P2  
**Estimated Effort**: 1 week  
**Dependencies**: Epic 1, Epic 2  
**Reference**: COMPONENT_STRUCTURE.md (Workflow Automation Components)

---

### Issue 8.1: Workflow List & Management

**Labels**: `workflow`, `automation`, `p2`

**Description**:
Display list of user's workflows with status toggles and management actions.

**Acceptance Criteria**:
- [ ] List of workflows (cards)
- [ ] Each card shows: name, status toggle, description, last run
- [ ] Active/Inactive toggle
- [ ] Edit/Delete/Duplicate actions
- [ ] "Create New Workflow" CTA
- [ ] Empty state for new users

**Workflow Card**:
- Name: "Full Moon Reflection Reminder"
- Toggle: Active/Inactive
- Description: Brief summary
- Last Run: Date/time
- Actions: Edit | Duplicate | Delete

**Copy Reference**: UX_COPY_GUIDE.md (Workflows Page)

**Testing**:
- [ ] Toggle changes status
- [ ] Delete asks confirmation
- [ ] Duplicate creates new workflow

**Reference**: COMPONENT_STRUCTURE.md (Saved Workflows List)

---

### Issue 8.2: Workflow Builder - Visual Editor

**Labels**: `workflow`, `builder`, `p2`

**Description**:
Create visual workflow builder with trigger and action selection.

**Acceptance Criteria**:
- [ ] Step-by-step wizard (3 steps)
- [ ] Step 1: Choose trigger
- [ ] Step 2: Choose action
- [ ] Step 3: Customize details
- [ ] Visual flow diagram (optional)
- [ ] Save/Activate buttons
- [ ] Validation before activation

**Trigger Options**:
- Transit occurs (planet, aspect, house)
- Specific date/time
- Recurring (daily, weekly, monthly)
- User opens app

**Action Options**:
- Send notification
- Create journal prompt
- Update dashboard card
- Generate report

**Copy Reference**: UX_COPY_GUIDE.md (Create Workflow)

**Testing**:
- [ ] Wizard navigation smooth
- [ ] All trigger/action combos work
- [ ] Workflow saves correctly

**Reference**: COMPONENT_STRUCTURE.md (Workflow Builder)

---

### Issue 8.3: Workflow Templates Library

**Labels**: `workflow`, `templates`, `p2`

**Description**:
Provide pre-built workflow templates users can activate with one click.

**Acceptance Criteria**:
- [ ] 5-10 template workflows
- [ ] Template cards with description
- [ ] "Use Template" button
- [ ] Template customization before activation
- [ ] Examples: Full Moon Reminder, Morning Check-in, Weekly Reflection

**Templates**:
1. Full Moon Reflection (monthly)
2. Morning Meditation Prompt (daily)
3. Weekly Chart Review (weekly)
4. Transit Alert (when major transit occurs)
5. Journal Streak Reminder (daily if not written)

**Copy Reference**: UX_COPY_GUIDE.md (Automation Templates)

**Testing**:
- [ ] Templates load correctly
- [ ] Customization works
- [ ] Activated templates appear in list

**Reference**: COMPONENT_STRUCTURE.md (Automation Templates)

---

## EPIC 9: Settings & Profile ⚙️

**Description**: User settings, preferences, profile management, and data export.

**Priority**: P2  
**Estimated Effort**: 3 days  
**Dependencies**: Epic 1, Epic 2  
**Reference**: COMPONENT_STRUCTURE.md (Settings Components)

---

### Issue 9.1: Profile Settings Page

**Labels**: `settings`, `profile`, `p2`

**Description**:
User profile management with avatar upload, birth data editing, and display preferences.

**Acceptance Criteria**:
- [ ] Avatar upload (image file)
- [ ] Display name field
- [ ] Birth data editor (date, time, location)
- [ ] Save changes button
- [ ] Change confirmation toast

**Copy Reference**: UX_COPY_GUIDE.md (Settings - Profile)

**Testing**:
- [ ] Avatar uploads successfully
- [ ] Birth data updates chart
- [ ] Validation works

---

### Issue 9.2: App Preferences & Theme

**Labels**: `settings`, `preferences`, `p2`

**Description**:
Application preferences including theme toggle, chart calculation settings, and notification preferences.

**Acceptance Criteria**:
- [ ] Theme toggle (Light/Dark/Auto)
- [ ] Chart calculation method (Sidereal/Tropical)
- [ ] Default house system
- [ ] Cultural framework selector
- [ ] Notification preferences checkboxes
- [ ] Language selection (future)

**Copy Reference**: UX_COPY_GUIDE.md (Settings - Preferences)

**Testing**:
- [ ] Theme changes apply immediately
- [ ] Chart settings persist
- [ ] Notifications honor preferences

---

### Issue 9.3: Data Management & Privacy

**Labels**: `settings`, `privacy`, `p2`

**Description**:
Data export, import, cache clearing, and account deletion.

**Acceptance Criteria**:
- [ ] "Export All Data" button (downloads JSON)
- [ ] "Import Data" button
- [ ] "Clear Cache" button
- [ ] "Delete Account" button (confirmation modal)
- [ ] Privacy policy link
- [ ] Data encryption statement

**Copy Reference**: UX_COPY_GUIDE.md (Settings - Privacy & Data)

**Testing**:
- [ ] Export includes all user data
- [ ] Import validates JSON
- [ ] Delete requires confirmation

**Reference**: COMPONENT_STRUCTURE.md (Data Management)

---

## EPIC 10: Accessibility & Polish ♿

**Description**: Comprehensive accessibility audit, keyboard navigation, screen reader support, and final UX polish.

**Priority**: P0 (Must complete before launch)  
**Estimated Effort**: 1 week  
**Dependencies**: All other epics  
**Reference**: DESIGN_INSPIRATION.md (Accessibility Requirements)

---

### Issue 10.1: WCAG AA Compliance Audit

**Labels**: `accessibility`, `audit`, `p0`

**Description**:
Run automated and manual accessibility tests to ensure WCAG AA compliance.

**Acceptance Criteria**:
- [ ] Lighthouse accessibility score 95+
- [ ] axe DevTools shows zero violations
- [ ] All color contrasts meet 4.5:1 ratio
- [ ] All images have alt text
- [ ] All interactive elements keyboard accessible
- [ ] No reliance on color alone for meaning
- [ ] Form validation errors announced

**Tools**:
- Lighthouse (automated)
- axe DevTools (automated)
- WAVE browser extension
- Manual keyboard testing
- Manual screen reader testing (NVDA/JAWS/VoiceOver)

**Testing Checklist**:
- [ ] All buttons keyboard accessible
- [ ] All forms accessible
- [ ] All modals trap focus
- [ ] All images have alt text
- [ ] Heading hierarchy correct
- [ ] Color contrast passes

---

### Issue 10.2: Keyboard Navigation Implementation

**Labels**: `accessibility`, `keyboard`, `p0`

**Description**:
Ensure 100% keyboard navigation throughout the app with visible focus indicators.

**Acceptance Criteria**:
- [ ] Tab order logical
- [ ] All interactive elements reachable
- [ ] Focus indicators visible (2px outline, 2px offset)
- [ ] Skip to content link at top
- [ ] Escape closes modals
- [ ] Arrow keys navigate lists/menus
- [ ] Enter/Space activate buttons

**Key Shortcuts** (optional):
- `?` - Show keyboard shortcuts help
- `Ctrl+K` or `Cmd+K` - Open search
- `Esc` - Close modal/drawer

**Testing**:
- [ ] Navigate entire app with keyboard only
- [ ] Focus visible at all times
- [ ] No keyboard traps

---

### Issue 10.3: Screen Reader Optimization

**Labels**: `accessibility`, `screen-reader`, `p0`

**Description**:
Optimize all components for screen reader users with proper ARIA labels and announcements.

**Acceptance Criteria**:
- [ ] All buttons have aria-label
- [ ] All images have alt text
- [ ] All form inputs have labels
- [ ] Loading states announced (aria-live)
- [ ] Error messages announced
- [ ] Dynamic content changes announced
- [ ] Landmarks used (nav, main, aside, footer)
- [ ] Heading hierarchy (h1 → h2 → h3)

**ARIA Attributes**:
- `aria-label` - Accessible name
- `aria-describedby` - Additional description
- `aria-live` - Announce dynamic changes
- `aria-expanded` - Accordion/dropdown state
- `role` - Semantic role when needed

**Testing**:
- [ ] Test with NVDA (Windows)
- [ ] Test with JAWS (Windows)
- [ ] Test with VoiceOver (Mac/iOS)
- [ ] All content accessible

---

### Issue 10.4: Responsive Testing & Polish

**Labels**: `responsive`, `polish`, `p0`

**Description**:
Test and refine responsive behavior on all devices and screen sizes.

**Devices to Test**:
- iPhone SE (375px)
- iPhone 12 Pro (390px)
- iPad (768px)
- iPad Pro (1024px)
- Desktop (1440px)
- Large desktop (1920px)

**Acceptance Criteria**:
- [ ] No horizontal scroll on any screen
- [ ] Touch targets 44px on mobile
- [ ] Text readable without zoom
- [ ] Images scale appropriately
- [ ] No layout breaks at any breakpoint
- [ ] Bottom nav only on mobile
- [ ] Sidebar collapses on tablet

**Testing**:
- [ ] Test on real devices (iOS, Android)
- [ ] Test in Chrome DevTools device mode
- [ ] Test with different text sizes
- [ ] Test landscape and portrait

---

### Issue 10.5: Performance Optimization

**Labels**: `performance`, `optimization`, `p1`

**Description**:
Optimize bundle size, lazy loading, and runtime performance.

**Acceptance Criteria**:
- [ ] Lighthouse performance score 90+
- [ ] Bundle size < 500KB gzipped
- [ ] Lazy load routes
- [ ] Lazy load heavy components (chart, cards)
- [ ] Image optimization (WebP, lazy load)
- [ ] Code splitting implemented
- [ ] No blocking resources

**Optimizations**:
- React.lazy() for routes
- Dynamic imports for heavy libraries
- Image lazy loading
- SVG optimization
- Tree shaking
- Minification

**Testing**:
- [ ] Lighthouse audit passes
- [ ] Bundle analyzer shows no bloat
- [ ] Page load < 2 seconds on 3G

---

## EPIC 11: Documentation & Developer Experience 📚

**Description**: Complete documentation for components, API, and contributor guidelines.

**Priority**: P2  
**Estimated Effort**: 3 days  
**Dependencies**: All epics complete  

---

### Issue 11.1: Component Documentation

**Labels**: `documentation`, `components`, `p2`

**Description**:
Document all reusable components with props, examples, and accessibility notes.

**Acceptance Criteria**:
- [ ] Component README in each folder
- [ ] Props documented with TypeScript types or PropTypes
- [ ] Usage examples for each variant
- [ ] Accessibility notes included
- [ ] Do's and Don'ts section

**Template**:
```markdown
# Button Component

## Props
- `variant`: 'primary' | 'secondary' | 'tertiary' | 'icon'
- `size`: 'small' | 'medium' | 'large'
- `disabled`: boolean
- `loading`: boolean

## Usage
\`\`\`jsx
<Button variant="primary" onClick={handleClick}>
  Click Me
</Button>
\`\`\`

## Accessibility
- Keyboard accessible (Enter/Space)
- ARIA label required for icon buttons
- Focus indicator visible
```

---

### Issue 11.2: API Documentation

**Labels**: `documentation`, `api`, `p2`

**Description**:
Document all backend API endpoints with request/response examples.

**Acceptance Criteria**:
- [ ] Endpoint list with HTTP methods
- [ ] Request body schemas
- [ ] Response schemas
- [ ] Error codes and messages
- [ ] Authentication requirements
- [ ] Rate limiting info

---

### Issue 11.3: Contributor Guidelines

**Labels**: `documentation`, `contributing`, `p2`

**Description**:
Write comprehensive contributor guide for developers and AI agents.

**Acceptance Criteria**:
- [ ] CONTRIBUTING.md file
- [ ] Code style guide
- [ ] Git workflow (branches, PRs)
- [ ] Testing requirements
- [ ] Accessibility checklist
- [ ] Design system usage
- [ ] How to reference design artifacts

---

## 🏷️ Label Definitions

**Priority**:
- `p0` - Critical, blocking
- `p1` - High priority
- `p2` - Medium priority
- `p3` - Low priority, nice-to-have

**Component Type**:
- `component` - UI component
- `layout` - Layout/structure
- `visualization` - Charts/graphs
- `form` - Form elements

**Feature Area**:
- `dashboard` - Dashboard
- `chart` - Natal chart
- `bmad` - BMAD analysis
- `symbolon` - Symbolon cards
- `journal` - Journaling
- `workflow` - Automation
- `settings` - Settings/profile
- `accessibility` - A11y features

**Technical**:
- `design-system` - Design tokens/foundation
- `responsive` - Responsive design
- `performance` - Optimization
- `documentation` - Docs

---

## 📊 Progress Tracking

### Kanban Columns

**Backlog**
- All issues not yet prioritized
- New ideas and suggestions

**To Do**
- Prioritized and ready to start
- Dependencies resolved
- Design specs available (if needed)

**In Progress**
- Actively being worked on
- Assign to developer/agent
- Limit WIP to 3-5 issues

**Review**
- Code complete, awaiting review
- Testing in progress
- Design QA
- Accessibility check

**Done**
- All acceptance criteria met
- Code merged to main
- Tests passing
- Documentation updated

---

## 🎯 Sprint Planning

### Sprint 1 (Week 1-2): Foundation
- Epic 1: Design System (all issues)
- Epic 2: Layout & Navigation (all issues)

### Sprint 2 (Week 3-4): Core Features
- Epic 3: Dashboard
- Epic 4: Natal Chart Viewer (enhanced)

### Sprint 3 (Week 5-6): Extended Features
- Epic 5: BMAD Analysis
- Epic 6: Symbolon Cards

### Sprint 4 (Week 7): User Features
- Epic 7: Journal System
- Epic 8: Workflow Automation

### Sprint 5 (Week 8): Polish & Launch
- Epic 9: Settings & Profile
- Epic 10: Accessibility & Polish
- Epic 11: Documentation

---

**End of Epics and Issues Document**

Total Epics: 11  
Total Issues: 60+  
Estimated Timeline: 8 weeks  
Team Size: 2-3 developers or AI agents
