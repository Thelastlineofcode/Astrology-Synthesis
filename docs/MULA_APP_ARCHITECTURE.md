# Mula: The Root - Companion App Architecture

**Project Pivot Date:** November 3, 2025  
**Version:** 1.0  
**Status:** Architecture Design Phase

---

## 🎯 Executive Summary

**Mula** (Sanskrit for "root") is a mobile-first companion app for spiritual readings, combining Vedic astrology, Vodou oracle wisdom, and tarot divination. The app pivots from the desktop-focused "Mula: The Root" astrology calculator to a modern, mystical experience designed for daily spiritual guidance.

### Vision Statement

> "Your pocket guide to cosmic wisdom. Connect with ancestral knowledge through personalized readings, mystical consultations, and synchronistic guidance—all in the palm of your hand."

### Core Value Proposition

- **Mobile-First Design**: Optimized for iPhone/Android with progressive web app (PWA) capabilities
- **Daily Guidance**: Fortune readings, tarot pulls, and astrological insights delivered daily
- **Vodou Modern Oracle**: Authentic Afro-Caribbean spiritual wisdom in contemporary format
- **AI-Powered Consultations**: Chat with virtual spiritual advisors trained on traditional knowledge
- **Freemium Model**: Free daily readings with premium features (unlimited readings, advanced interpretations, live consultations)

---

## 📱 App Overview

### Platform Strategy

- **Primary**: Mobile web app (responsive, installable PWA)
- **Secondary**: Native iOS/Android apps (future Phase 2)
- **Technology**: Next.js 16, React 19, TypeScript, Tailwind CSS
- **Backend**: FastAPI (Python) with KP prediction engine + RAG AI

### Target Audience

1. **Primary**: Millennials/Gen Z (25-45) interested in mysticism, astrology, and alternative spirituality
2. **Secondary**: Professional astrologers and spiritual practitioners seeking consultation tools
3. **Tertiary**: Vodou/Hoodoo practitioners looking for authentic digital oracle systems

---

## 🏗️ Application Architecture

### Three-Layer Structure

```
┌─────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                 │
│            (Mobile-First React Components)          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │  Fortune   │  │   Tarot    │  │ Consultant │   │
│  │  Readings  │  │   Spread   │  │    Chat    │   │
│  └────────────┘  └────────────┘  └────────────┘   │
└─────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC                    │
│         (Reading Engine + AI Orchestration)         │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │   Natal    │  │   Oracle   │  │    RAG     │   │
│  │   Chart    │  │   System   │  │  Interpret │   │
│  └────────────┘  └────────────┘  └────────────┘   │
└─────────────────────────────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│                     DATA LAYER                      │
│      (KP Engine + Knowledge Base + User Data)       │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │  Swiss     │  │   Vodou    │  │  User DB   │   │
│  │ Ephemeris  │  │  Oracles   │  │ (SQLite)   │   │
│  └────────────┘  └────────────┘  └────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 🎨 Visual Design System: "Cosmic Midnight"

### Design Philosophy

**Mystic realism meets urban spirituality.** Dark, immersive interface with glowing elements, celestial motifs, and deep space aesthetics.

### Color Palette

```css
/* Primary Background */
--bg-cosmic-dark: #1A0F1E;        /* Deep space purple-black */
--bg-card-surface: #2D1F2B;       /* Card surfaces */
--bg-input: rgba(255, 255, 255, 0.05); /* Input fields */

/* Accent Colors */
--accent-golden: #E8B598;         /* Golden highlights, premium features */
--accent-orange: #E86F4D;         /* CTAs, active states */
--accent-purple: #8B6FA8;         /* Mystical elements */
--accent-cyan: #5FA9B8;           /* Water/moon elements */

/* Planet Colors (from KP system) */
--planet-sun: #FFD700;
--planet-moon: #C0C0D0;
--planet-mars: #E8684D;
--planet-mercury: #6FA8C0;
--planet-jupiter: #D4A574;
--planet-venus: #FFC1CC;
--planet-saturn: #4A5F8E;

/* Text Hierarchy */
--text-primary: #FFFFFF;
--text-secondary: rgba(255, 255, 255, 0.7);
--text-muted: rgba(255, 255, 255, 0.5);
--text-gold: #E8B598;
```

### Typography

```css
/* Font Stack */
--font-primary: 'Inter', -apple-system, sans-serif;
--font-display: 'Cinzel', 'Trajan Pro', serif;  /* Headers, card titles */
--font-mono: 'JetBrains Mono', monospace;       /* Numbers, data */

/* Scale (Mobile-First) */
--text-xs: 12px;
--text-sm: 14px;
--text-base: 16px;
--text-lg: 18px;
--text-xl: 24px;
--text-2xl: 32px;
--text-3xl: 40px;
```

### Visual Effects

- **Glow Effects**: Radial gradients for planets, cards, and active elements
- **Glassmorphism**: Semi-transparent cards with backdrop blur
- **Particle Systems**: Floating cosmic dust, subtle star fields
- **Micro-Animations**: Smooth transitions, card flips, pulse effects
- **Haptic Feedback**: Vibration on card draws, reading completions (native only)

---

## 📱 Core Features & User Flows

### 1. **Home Screen: "Starbase"**

Landing page with daily cosmic overview.

**Components:**
- **Current Moon Phase**: Live moon phase with nakshatra name
- **Today's Fortune**: Quick daily reading (1-2 sentences)
- **Quick Actions**:
  - 🔮 Draw a Card (Vodou Oracle or Tarot)
  - 📊 View My Chart
  - 💬 Ask a Question (Consultant)
  - ⭐ Saved Readings
- **Progress Tracker**: Streak counter, premium benefits

**User Flow:**
```
App Launch → Auth Check → Home (Starbase)
         ↓
    [First Time User]
         ↓
    Onboarding (Name, Birth Data, Interests)
         ↓
    Generate Natal Chart
         ↓
    Welcome Reading
```

---

### 2. **Fortune Readings: "Daily Wisdom"**

Three reading modes: Daily, Weekly, Monthly.

**Reading Structure:**
- **Card Image**: Vodou Oracle or Tarot card visual
- **Title**: Card name + number (e.g., "IV. The Sovereign")
- **Lwa/Deity**: Associated spiritual entity
- **Keywords**: 3-5 core themes
- **Interpretation**: 2-3 paragraphs of guidance
- **Action Steps**: Practical advice
- **Meditation**: Short contemplative practice

**Features:**
- Save readings to journal
- Share readings (image + text)
- Audio narration (premium)
- Multiple deck options:
  - Vodou Modern Oracle (22 cards)
  - Rider-Waite Tarot (78 cards)
  - Lenormand (36 cards)

**API Integration:**
```typescript
GET /api/v1/fortune/daily
GET /api/v1/fortune/weekly
GET /api/v1/fortune/monthly
POST /api/v1/fortune/custom  // Question-based reading
```

---

### 3. **Tarot Spread: "The Draw"**

Interactive card-pulling experience.

**Spread Types:**
1. **Single Card**: Quick guidance
2. **Three-Card**: Past-Present-Future
3. **Celtic Cross**: Comprehensive 10-card spread (premium)
4. **Relationship**: Two-person synergy reading (premium)

**UX Flow:**
```
Select Spread → Shuffle Animation → Draw Cards (tap to reveal)
    ↓
Flip Animation → Card Interpretation → Save/Share
    ↓
View Full Reading → Add to Journal
```

**Technical Implementation:**
- **Card Shuffle**: Fisher-Yates algorithm with smooth animation
- **Card Flip**: 3D CSS transform with backface-visibility
- **Position Meanings**: Each spread position has unique significance
- **AI Enhancement**: GPT-4 synthesizes card combinations for personalized meaning

---

### 4. **Consultant Chat: "Ask the Oracle"**

AI-powered spiritual advisor chat.

**Advisor Personas:**
1. **Papa Legba**: Crossroads guidance, life decisions
2. **Erzulie Freda**: Love, relationships, self-care
3. **Erzulie Dantor**: Protection, boundaries, fierce love
4. **Baron Samedi**: Shadow work, death/rebirth, humor
5. **Ogoun**: Career, conflict resolution, strength

**Chat Features:**
- Natural language Q&A
- Context-aware (knows user's natal chart)
- Suggests relevant readings
- Can pull cards mid-conversation
- Voice input/output (premium)

**RAG Pipeline:**
```
User Question → Embedding → Vector Search (Knowledge Base)
    ↓
Retrieve Top 5 Texts → KP Chart Context → LLM Synthesis
    ↓
Personalized Response → Suggest Follow-Up Reading
```

---

### 5. **Natal Chart: "My Cosmos"**

Birth chart dashboard with KP precision.

**Sections:**
1. **Chart Wheel**: Zodiac wheel with planets, houses, aspects
2. **Planet Positions**: Degree-level accuracy, nakshatra, sub-lord
3. **Houses**: 12 house meanings with cuspal sub-lords
4. **Dashas**: Current planetary periods (Vimshottari)
5. **Predictions**: AI-generated life path insights

**Interactive Features:**
- Tap planet for detailed info
- House overlays (show/hide)
- Aspect lines visualization
- Export chart as image

---

### 6. **Profile & Settings: "Inner Sanctuary"**

User management and customization.

**Sections:**
- **Profile**: Avatar, name, birth data, zodiac
- **Preferences**: Deck choice, language, notifications
- **Premium**: Subscription status, benefits, upgrade CTA
- **Journal**: Saved readings, notes, reflections
- **History**: Past readings archive
- **Settings**: Account, privacy, data export

---

## 🎯 Monetization Strategy

### Freemium Model

**Free Tier:**
- 3 free readings per day
- Single-card draws
- Basic natal chart
- Limited consultant messages (5/day)
- Ad-supported (banner ads, interstitials)

**Premium Tier ($9.99/month or $79.99/year):**
- ✨ Unlimited readings
- 🎴 All tarot decks + spreads (Celtic Cross, etc.)
- 🔮 Advanced predictions (timing, transits)
- 💬 Unlimited consultant chat
- 🎙️ Audio narration
- 📸 HD card artwork
- 🚫 Ad-free experience
- 📊 Advanced chart features (progressed, solar return)

**Live Consultations ($29.99/session):**
- 30-minute video call with human astrologer/reader
- Personalized reading + recording
- Follow-up email summary

---

## 🔧 Technical Stack

### Frontend
- **Framework**: Next.js 16 (App Router)
- **UI Library**: React 19
- **Styling**: Tailwind CSS + CSS Modules
- **Animations**: Framer Motion
- **State Management**: Zustand + React Query
- **Forms**: React Hook Form + Zod
- **Charts**: D3.js (zodiac wheel), Recharts (data viz)

### Backend
- **API**: FastAPI (Python 3.11+)
- **Calculations**: Swiss Ephemeris + KP engine
- **AI**: OpenAI GPT-4 + Embeddings API
- **Database**: PostgreSQL (production), SQLite (dev)
- **Vector Store**: Chroma or Pinecone
- **Caching**: Redis
- **File Storage**: AWS S3 (card images, avatars)

### Infrastructure
- **Hosting**: Vercel (frontend), Railway (backend)
- **CDN**: Cloudflare
- **Analytics**: PostHog, Mixpanel
- **Monitoring**: Sentry
- **Payments**: Stripe

---

## 📊 Success Metrics (KPIs)

### User Engagement
- **DAU/MAU Ratio**: Target 40%+ (high daily usage)
- **Readings Per User**: Target 2.5 readings/day
- **Session Duration**: Target 8-12 minutes
- **Retention**: 30-day retention > 30%

### Revenue
- **Conversion Rate**: Free → Premium 5-8%
- **ARPU**: Average Revenue Per User $3-5/month
- **LTV**: Customer Lifetime Value $150+
- **Churn**: Monthly churn < 10%

### Product Quality
- **App Store Rating**: 4.5+ stars
- **NPS Score**: 40+ (good)
- **Crash Rate**: < 1%
- **API Response Time**: < 500ms p95

---

## 🚀 Development Roadmap

### Phase 1: MVP (Weeks 1-6)
- ✅ Modernize frontend design system
- ✅ Create Vodou Oracle card art (22 cards)
- ✅ Implement fortune reading flow
- ✅ Build natal chart display
- ✅ Set up authentication (email/password, Google)
- ✅ Deploy to staging

### Phase 2: Core Features (Weeks 7-12)
- 🔄 Tarot spread system (3 spreads)
- 🔄 Consultant chat with RAG
- 🔄 Premium subscription (Stripe)
- 🔄 Push notifications (daily reading reminder)
- 🔄 Journal & reading history
- 🔄 Beta testing with 100 users

### Phase 3: Enhancement (Weeks 13-18)
- 📅 Advanced chart features (transits, progressions)
- 📅 Multiple tarot decks
- 📅 Audio narration
- 📅 Social sharing (Instagram Stories format)
- 📅 Referral program
- 📅 Public launch

### Phase 4: Growth (Weeks 19-24)
- 📅 Live consultant marketplace
- 📅 Native iOS/Android apps
- 📅 Multi-language support (Spanish, Portuguese)
- 📅 Community features (forums, groups)
- 📅 Partner integrations

---

## 🎨 Branding: "Mula: The Root"

### Name Etymology
- **Sanskrit**: Mūla (मूल) = "root" or "foundation"
- **Vedic Astrology**: Mula is the 19th nakshatra, ruled by Ketu (shadow planet of transformation)
- **Symbolism**: Returning to spiritual roots, ancestral wisdom, deep transformation

### Logo Concept
- **Visual**: Tree of Life with cosmic roots extending into starfield
- **Colors**: Golden-copper gradient (#E8B598 → #D4A574)
- **Typography**: Elegant serif (Cinzel or Trajan Pro)
- **Icon**: Simplified root system in circular frame

### Tagline Options
1. "Return to Your Roots"
2. "Wisdom from the Source"
3. "Your Pocket Guide to the Cosmos"
4. "Where Tradition Meets Technology"

---

## 🔐 Privacy & Ethics

### Data Handling
- **Birth Data**: Encrypted at rest, never sold
- **Readings**: User owns all interpretations
- **AI Conversations**: Stored securely, deletable anytime
- **GDPR/CCPA Compliant**: Full data export and deletion

### Cultural Respect
- **Vodou Representation**: Authentic research, avoid stereotypes
- **Consultation**: Work with Vodou practitioners for accuracy
- **Attribution**: Credit sources (Haitian, West African traditions)
- **Avoid Appropriation**: Respectful presentation, not commodification

---

## 📞 Next Steps

### Immediate Actions
1. ✅ Create this architecture document
2. 🔄 Archive old "Mula: The Root" branding
3. 🔄 Update all frontend components with new design system
4. 🔄 Implement fortune reading page (already exists at `/fortune`)
5. 🔄 Create Vodou Oracle card dataset
6. 🔄 Build AI consultant backend

### Team Needs
- **Frontend Developer**: React/Next.js specialist
- **Backend Developer**: Python/FastAPI + AI/ML experience
- **Designer**: Mobile UI/UX, mystical aesthetics
- **Content Creator**: Vodou/tarot interpretation writer
- **Cultural Consultant**: Vodou practitioner for authenticity

---

**Document Owner**: Development Team  
**Last Updated**: November 3, 2025  
**Status**: Living Document - Update as project evolves

---

## 🌟 Conclusion

**Mula: The Root** represents a focused pivot from a complex desktop astrology calculator to a mobile-first spiritual companion app. By combining authentic Vodou oracle wisdom, KP astrology precision, and modern AI interpretation, we create a unique offering in the crowded wellness/spirituality app market.

**Key Differentiators:**
1. Authentic Vodou Modern oracle (not generic tarot)
2. KP-level astrological precision (not sun-sign horoscopes)
3. AI-powered personalization (not canned readings)
4. Beautiful, mystical UX (not clinical/boring)
5. Freemium with clear value ladder

**Next Milestone**: Complete MVP (fortune readings + natal chart + auth) and launch beta by December 15, 2025.

