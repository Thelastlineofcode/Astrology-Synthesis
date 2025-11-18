# Project Pivot Guide: Mula: The Root → Mula: The Root

**Migration Date:** November 3, 2025  
**Status:** Active Transition  
**Completion Target**: December 15, 2025

---

## 📋 What's Changing

### OLD: Mula: The Root
- ❌ Desktop-first astrology calculator
- ❌ Complex multi-feature dashboard (BMAD, Symbolon, Journaling, Workflows)
- ❌ "Healing Cosmos" pastel color scheme
- ❌ Feature bloat, unfocused product vision
- ❌ Target: Professional astrologers

### NEW: Mula: The Root
- ✅ Mobile-first spiritual companion app
- ✅ Focused features: Fortune readings, Tarot, Consultant chat, Natal chart
- ✅ "Cosmic Midnight" dark mystical theme
- ✅ Clear value proposition and monetization
- ✅ Target: Everyday spiritual seekers (25-45 age)

---

## 🗂️ Documentation Migration Map

### Files to Archive (Move to `/docs/archive/roots-revealed/`)

**Design System (Old)**
- `COLOR_PALETTE_AND_DESIGN_SYSTEM.md` → Replaced by design tokens in `MULA_APP_ARCHITECTURE.md`
- `docs/redesign/` → Entire folder archived
- `DESIGN_COMPLETE_SUMMARY.md`
- `DESIGN_SYSTEM_IMPLEMENTATION_SUMMARY.md`

**Features (Deprecated)**
- `BMAD_USAGE_GUIDE.md` → BMAD removed from MVP
- `SYMBOLON_INTEGRATION_GUIDE.md` → Replaced by Vodou Oracle system
- `CHART_TESTING_GUIDE.md` → Simplified for Mula

**Old Branding**
- Any references to "Mula: The Root" as product name
- "Healing Cosmos" color palette documentation

### Files to Update (In-Place)

**Core Documentation**
- `README.md` → Update project description, add Mula branding
- `CONTRIBUTING.md` → Update contribution guidelines for Mula
- `API_DOCUMENTATION.md` → Keep (backend still valid)
- `AUTHENTICATION_SYSTEM_COMPLETE.md` → Keep (auth unchanged)

**Technical Docs (Keep)**
- `KP_SYSTEM_ARCHITECTURE.md` → ✅ Core engine unchanged
- `SYNCRETIC_AI_PREDICTION_SYSTEM.md` → ✅ Backend prediction logic valid
- `API_ARCHITECTURE.md` → Update endpoints for Mula features

### New Files Created

**Mula-Specific**
- ✅ `docs/MULA_APP_ARCHITECTURE.md` (this file)
- ✅ `docs/PROJECT_PIVOT_MIGRATION_GUIDE.md` (this guide)
- 📄 `docs/MULA_DESIGN_SYSTEM.md` (to create)
- 📄 `docs/VODOU_ORACLE_GUIDE.md` (to create)
- 📄 `docs/MULA_API_SPEC.md` (to create)

---

## 🎨 Frontend Component Migration

### Components to Remove/Archive

**Dashboard Components** (Old "Mula: The Root" design)
```
frontend/src/components/dashboard/
├── QuickChartCard.tsx          → Archive (too complex)
├── BMADSummaryCard.tsx         → Archive (BMAD deprecated)
├── SymbolonCard.tsx            → Archive (replaced by Fortune)
└── RecentChartsCard.tsx        → Keep (useful for Mula)
```

**Pages to Remove**
```
frontend/src/app/
├── chart-demo/                 → Archive (old chart UI)
├── symbolon-demo/              → Archive (replaced by Tarot system)
└── loading-demo/               → Archive (demo page)
```

**Pages to Keep & Modernize**
```
frontend/src/app/
├── fortune/                    → ✅ Primary feature, modernize design
├── admin/                      → ✅ Keep for internal use
├── profile/                    → ✅ Update for Mula branding
└── dashboard/                  → ✅ Redesign as "Starbase" home
```

### New Components to Create

**Mula-Specific Components**
```
frontend/src/components/mula/
├── CardDraw/
│   ├── CardStack.tsx          # Shuffling animation
│   ├── CardFlip.tsx           # 3D flip reveal
│   └── SpreadLayout.tsx       # Tarot spread positioning
├── Consultant/
│   ├── ChatInterface.tsx      # AI chat UI
│   ├── AdvisorAvatar.tsx      # Lwa persona display
│   └── MessageBubble.tsx      # Chat message styling
├── NatalChart/
│   ├── ChartWheel.tsx         # Zodiac wheel visualization
│   ├── PlanetInfo.tsx         # Planet detail cards
│   └── HouseOverlay.tsx       # House meanings
└── Reading/
    ├── ReadingCard.tsx        # Daily/weekly/monthly reading
    ├── InterpretationPanel.tsx
    └── SaveShareActions.tsx
```

### Design Token Migration

**Old Tokens (Healing Cosmos)**
```css
/* DEPRECATED */
--color-primary: #3E4B6E;      /* Deep Indigo */
--color-secondary: #A5B8A4;    /* Soft Sage */
--color-accent: #B296CA;       /* Muted Lavender */
--color-cta: #C17B5C;          /* Warm Terracotta */
--color-neutral-50: #F5F3EE;   /* Cream */
```

**New Tokens (Cosmic Midnight)**
```css
/* ACTIVE */
--bg-cosmic-dark: #1A0F1E;        /* Deep space purple-black */
--accent-golden: #E8B598;         /* Golden highlights */
--accent-orange: #E86F4D;         /* CTAs, active states */
--accent-purple: #8B6FA8;         /* Mystical elements */
--text-primary: #FFFFFF;
```

**Migration Script**
```bash
# Search and replace old tokens in all CSS files
find frontend/src -name "*.css" -exec sed -i 's/--color-primary/--accent-purple/g' {} +
find frontend/src -name "*.css" -exec sed -i 's/--color-cta/--accent-orange/g' {} +
find frontend/src -name "*.css" -exec sed -i 's/--color-neutral-50/--bg-cosmic-dark/g' {} +
```

---

## 🗄️ Backend Migration

### API Endpoints to Deprecate

**Remove from `backend/src/routes/`**
```python
# Deprecated endpoints
/api/v1/bmad/analyze          # BMAD feature removed
/api/v1/symbolon/draw         # Replaced by /oracle/draw
/api/v1/workflow/             # Workflow management removed
/api/v1/journal/              # Journal moved to client-side
```

### API Endpoints to Add

**New Mula-specific endpoints**
```python
# Fortune Readings
POST /api/v1/fortune/daily
POST /api/v1/fortune/weekly
POST /api/v1/fortune/monthly
POST /api/v1/fortune/custom   # Question-based reading

# Vodou Oracle
POST /api/v1/oracle/draw      # Draw oracle cards
GET  /api/v1/oracle/decks     # List available decks
GET  /api/v1/oracle/card/{id} # Get card details

# Tarot Spreads
POST /api/v1/tarot/spread/{type}  # Single, 3-card, Celtic Cross
GET  /api/v1/tarot/decks          # Rider-Waite, Lenormand, etc.

# Consultant Chat
POST /api/v1/consultant/chat  # Send message to AI advisor
GET  /api/v1/consultant/advisors  # List available personas
POST /api/v1/consultant/context   # Update user context

# Natal Chart (Keep existing + enhance)
POST /api/v1/chart/calculate  # Calculate natal chart (existing)
GET  /api/v1/chart/transits   # Get current transits (new)
GET  /api/v1/chart/dashas     # Get Vimshottari periods (new)

# Premium Features
POST /api/v1/subscription/checkout  # Stripe checkout
GET  /api/v1/subscription/status    # Check premium status
```

### Database Schema Updates

**New Tables to Create**
```sql
-- User readings history
CREATE TABLE readings (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  type VARCHAR(20),  -- 'daily', 'weekly', 'monthly', 'custom'
  cards JSONB,       -- Array of drawn cards
  interpretation TEXT,
  created_at TIMESTAMP
);

-- Oracle card metadata
CREATE TABLE oracle_cards (
  id INTEGER PRIMARY KEY,
  name VARCHAR(100),
  number VARCHAR(10),  -- Roman numeral
  lwa VARCHAR(100),    -- Associated deity
  element VARCHAR(20),
  planet VARCHAR(20),
  keywords TEXT[],
  meaning_upright TEXT,
  meaning_reversed TEXT,
  image_url TEXT
);

-- Consultant chat history
CREATE TABLE consultant_messages (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  advisor VARCHAR(50),  -- 'papa_legba', 'erzulie_freda', etc.
  role VARCHAR(10),     -- 'user' or 'assistant'
  content TEXT,
  created_at TIMESTAMP
);

-- Premium subscriptions
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  stripe_subscription_id VARCHAR(100),
  status VARCHAR(20),  -- 'active', 'canceled', 'past_due'
  current_period_end TIMESTAMP,
  created_at TIMESTAMP
);
```

**Tables to Deprecate**
```sql
-- Remove BMAD tables
DROP TABLE bmad_analyses;
DROP TABLE bmad_predictions;

-- Remove Symbolon tables  
DROP TABLE symbolon_readings;

-- Remove workflow tables
DROP TABLE workflows;
DROP TABLE workflow_steps;
```

---

## 📱 Frontend File Structure (Target State)

```
frontend/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   └── signup/
│   │   ├── fortune/              # ✅ Daily readings (keep & update)
│   │   ├── tarot/                # 🆕 Tarot spread system
│   │   ├── consultant/           # 🆕 AI chat interface
│   │   ├── chart/                # ✅ Natal chart (modernize)
│   │   ├── profile/              # ✅ User profile (update)
│   │   ├── premium/              # 🆕 Subscription management
│   │   ├── journal/              # 🆕 Saved readings & notes
│   │   └── page.tsx              # 🔄 Home → "Starbase" dashboard
│   ├── components/
│   │   ├── mula/                 # 🆕 Mula-specific components
│   │   │   ├── CardDraw/
│   │   │   ├── Consultant/
│   │   │   ├── NatalChart/
│   │   │   └── Reading/
│   │   ├── shared/               # ✅ Keep (Button, Card, etc.)
│   │   └── layout/               # ✅ Keep (Nav, Footer)
│   ├── styles/
│   │   ├── variables.css         # 🔄 Update tokens
│   │   ├── themes.css            # 🔄 Cosmic Midnight theme
│   │   └── globals.css           # 🔄 Base styles
│   └── lib/
│       ├── api/                  # ✅ API client functions
│       ├── store/                # ✅ Zustand stores
│       └── utils/                # ✅ Helpers
├── public/
│   ├── oracle/                   # 🆕 Vodou Oracle card images
│   ├── tarot/                    # 🆕 Tarot card images
│   ├── avatars/                  # 🆕 Consultant avatars
│   └── logo/                     # 🔄 Update Mula branding
└── tests/                        # ✅ Update test suites
```

---

## ✅ Migration Checklist

### Phase 1: Documentation (Week 1)
- [x] Create `MULA_APP_ARCHITECTURE.md`
- [x] Create `PROJECT_PIVOT_MIGRATION_GUIDE.md` (this file)
- [ ] Archive old design docs to `/docs/archive/roots-revealed/`
- [ ] Update `README.md` with Mula branding
- [ ] Create `MULA_DESIGN_SYSTEM.md`
- [ ] Create `VODOU_ORACLE_GUIDE.md`

### Phase 2: Frontend Cleanup (Week 1-2)
- [ ] Archive deprecated components (`/components/dashboard/`, `/app/symbolon-demo/`)
- [ ] Update CSS variables (`variables.css`, `themes.css`)
- [ ] Replace "Mula: The Root" text with "Mula" throughout codebase
- [ ] Update logo files in `/public/`
- [ ] Create placeholder Vodou Oracle card images
- [ ] Test existing `/fortune` page with new design

### Phase 3: New Component Development (Week 2-3)
- [ ] Create `/components/mula/CardDraw/` components
- [ ] Create `/components/mula/Consultant/` chat interface
- [ ] Create `/components/mula/NatalChart/` modernized chart
- [ ] Create `/app/tarot/` spread system
- [ ] Create `/app/consultant/` chat page
- [ ] Create `/app/premium/` subscription page

### Phase 4: Backend Updates (Week 3-4)
- [ ] Remove deprecated API endpoints (BMAD, Symbolon, Workflow)
- [ ] Create new endpoints (`/fortune`, `/oracle`, `/tarot`, `/consultant`)
- [ ] Update database schema (add readings, oracle_cards, consultant_messages tables)
- [ ] Implement Stripe subscription logic
- [ ] Set up RAG pipeline for consultant chat

### Phase 5: Testing & Polish (Week 5-6)
- [ ] Update all test suites
- [ ] Mobile responsiveness testing
- [ ] Cross-browser testing
- [ ] Performance optimization
- [ ] Accessibility audit
- [ ] Beta user testing

### Phase 6: Deployment (Week 6)
- [ ] Deploy to staging
- [ ] Final QA testing
- [ ] Deploy to production
- [ ] Launch announcement
- [ ] Monitor analytics

---

## 🔍 Search & Replace Commands

### Global Text Replacements

```bash
# Navigate to project root
cd /workspaces/Astrology-Synthesis

# Replace "Mula: The Root" with "Mula" in all markdown files
find . -name "*.md" -not -path "./node_modules/*" -not -path "./.git/*" \
  -exec sed -i 's/Mula: The Root/Mula: The Root/g' {} +

# Replace "Healing Cosmos" with "Cosmic Midnight"
find . -name "*.md" -not -path "./node_modules/*" \
  -exec sed -i 's/Healing Cosmos/Cosmic Midnight/g' {} +

# Update CSS variable names in all CSS files
find frontend/src -name "*.css" \
  -exec sed -i 's/--color-primary-light/#8B6FA8/g' {} +

# Update meta tags in layout.tsx
sed -i 's/Mula: The Root/Mula: The Root/g' frontend/src/app/layout.tsx
sed -i 's/Discover the roots of your astrological birth chart/Your pocket guide to cosmic wisdom/g' frontend/src/app/layout.tsx
```

### Specific File Updates

**Update `package.json`**
```json
{
  "name": "mula-app",
  "description": "Mula: The Root - Mobile companion for spiritual readings",
  "version": "2.0.0"
}
```

**Update `frontend/src/app/layout.tsx` metadata**
```typescript
export const metadata: Metadata = {
  title: "Mula: The Root",
  description: "Your pocket guide to cosmic wisdom. Daily readings, tarot, and astrology.",
  // ...
};
```

---

## 🚨 Breaking Changes

### For Existing Users (If Any)

**Data Migration Required:**
- User accounts: ✅ No changes (same auth system)
- Birth charts: ✅ Preserved (KP engine unchanged)
- BMAD analyses: ❌ Deprecated (will be deleted)
- Symbolon readings: ❌ Replaced by Vodou Oracle
- Workflow data: ❌ Removed (feature deprecated)

**User Communication:**
```
Subject: Exciting Update: Mula: The Root is Now Mula!

Hi [Name],

We're thrilled to announce that Mula: The Root has evolved into 
Mula: The Root—a mobile-first companion app for daily spiritual 
guidance.

What's New:
✨ Daily fortune readings
🔮 Vodou Modern Oracle cards
💬 AI-powered spiritual consultant
📱 Beautiful mobile experience

What's Changed:
• BMAD analysis → Simplified natal chart insights
• Symbolon cards → Vodou Modern Oracle system
• Desktop focus → Mobile-first design

Your birth chart data is safe and waiting for you in Mula.

Download the app: [App Store] [Google Play] [Web App]

Blessings,
The Mula Team
```

---

## 📊 Success Metrics

### Migration Completion Criteria

**Code Quality**
- [ ] Zero references to "Mula: The Root" in active codebase
- [ ] All old color tokens replaced with new system
- [ ] Test suite passing (>90% coverage)
- [ ] No console errors in production build

**Feature Parity**
- [ ] Fortune reading page functional
- [ ] Natal chart calculator working
- [ ] User authentication working
- [ ] Profile management working

**New Features Live**
- [ ] Tarot spread system operational
- [ ] Consultant chat responding
- [ ] Premium subscription checkout working
- [ ] Mobile PWA installable

**Performance**
- [ ] Lighthouse score >90 (mobile)
- [ ] First Contentful Paint <2s
- [ ] Time to Interactive <3s
- [ ] Bundle size <500KB (initial load)

---

## 🆘 Rollback Plan

If critical issues arise during migration:

1. **Immediate Revert**: Keep `master` branch stable, work in `mula-pivot` branch
2. **Database Backup**: Daily snapshots before schema changes
3. **Feature Flags**: Use environment variables to toggle new features
4. **Staged Rollout**: Deploy to staging → 10% users → 50% users → 100%

**Rollback Command:**
```bash
git checkout master
git reset --hard origin/master
npm run deploy:rollback
```

---

## 📞 Questions & Support

**For Developers:**
- Check `MULA_APP_ARCHITECTURE.md` for design decisions
- See `CONTRIBUTING.md` for code standards
- Join Slack channel: `#mula-pivot`

**For Stakeholders:**
- Review `docs/PROJECT_PIVOT_SUMMARY.md` for business rationale
- See roadmap in `MULA_APP_ARCHITECTURE.md` (Phase 1-4)

---

**Document Owner**: Development Team  
**Last Updated**: November 3, 2025  
**Next Review**: November 10, 2025 (after Phase 1 completion)

