# BMAD Astrology App - Redesign Project Overview

## 🎯 Project Vision

Transform the current astrology chart calculator into a comprehensive, healing-focused astrology platform that seamlessly integrates:
- **Natal Chart Generation** (Swiss Ephemeris powered)
- **BMAD Behavioral Analysis** (10-dimension personality framework)
- **Symbolon Archetypal Cards** (79-card system)
- **Personal Journaling** with mood tracking and insights
- **Workflow Automation** for practice rituals and reminders

## 🎨 Design Philosophy

**"Modern Mysticism Meets Clinical Psychology"**

### Core Principles
1. **Inclusive & Healing**: Welcoming to all backgrounds, non-dogmatic, empowering
2. **Professional & Trustworthy**: Clean, spacious layouts; clinical assessment feel
3. **Accessible**: WCAG AA compliant, keyboard navigation, screen reader support
4. **Multicultural**: Support for multiple astrological traditions (Western, Vedic, African, etc.)
5. **Modular & Card-Based**: Information architecture built on reusable card components

### Brand Voice Attributes
- **Wise, not preachy**: Offer insights without dogma
- **Warm, not frivolous**: Approachable yet respectful
- **Empowering, not prescriptive**: Guide, don't dictate
- **Inclusive, not exclusive**: Welcome all backgrounds and beliefs
- **Clear, not mystical jargon**: Accessible language

## 📚 Reference Artifacts

All design decisions reference these core documents:

1. **[Component Structure](../../../attachments/bmad_component_structure.txt)** - Complete UI component hierarchy
2. **[Color Schemes](../../../attachments/bmad_color_schemes.txt)** - "Healing Cosmos" palette and usage guidelines
3. **[UX Copy Guide](../../../attachments/bmad_ux_copy_guide.txt)** - All microcopy, error messages, CTAs
4. **[Design Inspiration](../../../attachments/bmad_design_inspiration.txt)** - Visual references and best practices

## 🎨 Primary Color Palette: "Healing Cosmos"

```css
--color-primary: #3E4B6E;        /* Deep Indigo - Trust, wisdom, depth */
--color-secondary: #A5B8A4;      /* Soft Sage - Healing, balance, renewal */
--color-accent: #B296CA;         /* Muted Lavender - Spirituality, transformation */
--color-cta: #C17B5C;            /* Warm Terracotta - Grounding, action */
--color-neutral-light: #F5F3EE;  /* Cream Neutral - Clarity, openness */
--color-neutral-dark: #2D3142;   /* Charcoal - Sophistication, depth */

/* Semantic */
--color-success: #81987F;        /* Forest Sage */
--color-warning: #E8B86D;        /* Golden Amber */
--color-error: #C17B5C;          /* Terracotta (softened) */
--color-info: #7FA99B;           /* Soft Teal */
```

## 🏗️ Technical Architecture

### Frontend Stack
- **Framework**: React 18.2.0
- **Styling**: CSS-in-JS or CSS Modules with CSS Variables
- **Icons**: Lucide Icons (outlined style)
- **Typography**: Inter or Plus Jakarta Sans
- **State Management**: React Context + Hooks
- **Routing**: React Router v6
- **Charts**: Recharts or D3.js for BMAD radar charts

### Backend (Existing)
- **API**: Flask (Python) on port 5000
- **Chart Engine**: Swiss Ephemeris
- **Data**: JSON-based content system

### Responsive Breakpoints
```css
/* Mobile-first approach */
--breakpoint-mobile: 320px - 767px;
--breakpoint-tablet: 768px - 1023px;
--breakpoint-desktop: 1024px - 1439px;
--breakpoint-large: 1440px+;
```

## 📐 Layout System

### Grid
- **Desktop**: 12-column grid, 24px gutters
- **Tablet**: 8-column grid, 20px gutters
- **Mobile**: 4-column grid, 16px gutters

### Spacing (8pt Grid)
- 4px, 8px, 16px, 24px, 32px, 48px, 64px

### Card Dimensions
- Small: 280px min-width
- Medium: 320px min-width
- Large: 400px min-width
- Border Radius: 12px
- Shadow: `0 2px 8px rgba(0,0,0,0.08)`

## ♿ Accessibility Standards

### WCAG AA Compliance
- ✅ Color contrast: 4.5:1 for text, 3:1 for UI components
- ✅ Keyboard navigation: All interactive elements accessible
- ✅ Screen reader: Semantic HTML, ARIA labels, alt text
- ✅ Focus indicators: 2px outline with 2px offset
- ✅ Reduced motion: Respect `prefers-reduced-motion`

### Touch Targets
- Minimum 44px × 44px on mobile
- Adequate spacing between interactive elements

## 🗂️ Project Structure

```
/frontend/src/
├── components/
│   ├── layout/          # App shell, nav, sidebar
│   ├── dashboard/       # Dashboard cards and widgets
│   ├── chart/           # Natal chart viewer and controls
│   ├── bmad/            # BMAD analysis components
│   ├── symbolon/        # Card gallery and spreads
│   ├── journal/         # Entry editor and list
│   ├── workflow/        # Automation builder
│   ├── settings/        # User preferences
│   └── shared/          # Reusable UI components
├── styles/
│   ├── variables.css    # CSS custom properties
│   ├── typography.css   # Font scales and styles
│   └── themes.css       # Light/dark mode
├── hooks/               # Custom React hooks
├── contexts/            # React Context providers
├── services/            # API calls
└── utils/               # Helper functions
```

## 📊 Success Metrics

### User Experience
- First chart generated in < 2 minutes
- Journal entry created in < 30 seconds
- Dashboard loads in < 1 second
- Mobile responsive on all major devices

### Accessibility
- Lighthouse accessibility score: 95+
- Zero critical WCAG violations
- Keyboard navigation: 100% coverage

### Technical
- Bundle size: < 500KB gzipped
- Lighthouse performance: 90+
- Zero console errors in production

## 🚀 Implementation Phases

### Phase 1: Foundation (Weeks 1-2)
- Design system & component library
- Layout & navigation
- Color palette & theming
- Typography system

### Phase 2: Core Features (Weeks 3-5)
- Dashboard with quick actions
- Natal chart viewer (enhanced)
- BMAD analysis framework
- Symbolon card gallery

### Phase 3: Extended Features (Weeks 6-7)
- Journal with mood tracking
- Workflow automation
- Settings & preferences
- Profile management

### Phase 4: Polish & Launch (Week 8)
- Accessibility audit
- Performance optimization
- User testing & iteration
- Documentation

## 🎯 Definition of Done

Each Epic/Issue is considered complete when:

1. ✅ **Code Complete**: All acceptance criteria met
2. ✅ **Design Matches**: Pixel-perfect to Figma specs (when applicable)
3. ✅ **Accessible**: Passes WCAG AA automated tests
4. ✅ **Responsive**: Works on mobile, tablet, desktop
5. ✅ **Tested**: Unit tests written, manual QA passed
6. ✅ **Documented**: Code comments, README updated
7. ✅ **Reviewed**: Code review approved by team
8. ✅ **Deployed**: Merged to main, deployed to staging

## 🤝 Contributor Guidelines

### For AI Copilot Agents
- Always reference design artifacts before implementation
- Follow component structure from `COMPONENT_STRUCTURE.md`
- Use colors from `COLOR_SCHEMES.md` palette
- Copy text from `UX_COPY_GUIDE.md` verbatim
- Implement accessibility requirements per `DESIGN_INSPIRATION.md`

### For Human Developers
- Review all four design documents before starting
- Use CSS variables for all colors and spacing
- Write semantic HTML with ARIA labels
- Test keyboard navigation on every component
- Ensure mobile-first responsive design

### Code Style
- **React**: Functional components with hooks
- **CSS**: BEM naming or CSS Modules
- **Accessibility**: Include ARIA labels, alt text, keyboard support
- **Comments**: Document props, complex logic, accessibility features

## 📞 Contact & Resources

- **Repository**: [Astrology-Synthesis](https://github.com/Thelastlineofcode/Astrology-Synthesis)
- **Design Files**: See `/docs/redesign/` for all artifacts
- **API Docs**: See `/backend/README.md`
- **Component Demo**: See `/frontend/src/components/README.md` (to be created)

---

**Last Updated**: October 28, 2025  
**Version**: 1.0  
**Status**: Planning Phase
