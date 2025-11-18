# Mula: The Root 🌳

**A modern spiritual companion app powered by precision astrology and authentic oracle wisdom**

> ⚡ **Project Status (Nov 2025)**: Active development of mobile-first fortune reading app backed by AI-powered KP astrology engine

---

## 🎯 What is Mula?

**Mula** (Sanskrit: मूल = "root") is a mobile companion app that brings together three powerful spiritual traditions:

1. **Vedic Astrology (KP System)**: Precision natal charts with sub-lord accuracy
2. **Vodou Modern Oracle**: Authentic Afro-Caribbean wisdom cards
3. **AI-Powered Guidance**: Personalized interpretations from spiritual consultant chat

### Core Features

- 📱 **Daily Fortune Readings**: Get guidance from Vodou Oracle or Tarot cards
- 🔮 **Tarot Spreads**: Single card, 3-card, Celtic Cross (premium)
- 💬 **Spiritual Consultant**: Chat with AI advisors (Papa Legba, Erzulie, Baron Samedi, Ogoun)
- 🌌 **Natal Chart**: KP-precision birth chart with planetary positions, houses, dashas
- 📓 **Reading Journal**: Save and reflect on past readings
- 💎 **Premium Features**: Unlimited readings, advanced spreads, audio narration

### Why "Mula"?

- **Sanskrit Meaning**: "Root" or "foundation" - returning to spiritual roots
- **Vedic Astrology**: Mula is the 19th nakshatra, ruled by Ketu (transformation planet)
- **Symbolism**: Deep roots + cosmic connection = grounded spiritual wisdom

---

## 🏗️ Architecture Overview

```
┌────────────────────────────────────────────┐
│          MULA MOBILE APP (Frontend)        │
│   Next.js 16 • React 19 • TypeScript       │
│   Mobile-First • PWA • Dark Mystical UI    │
└────────────────────────────────────────────┘
                     ▼
┌────────────────────────────────────────────┐
│           AI PREDICTION ENGINE             │
│   FastAPI • Python 3.11 • GPT-4 RAG        │
│   Syncretic Astrology • Oracle System      │
└────────────────────────────────────────────┘
                     ▼
┌────────────────────────────────────────────┐
│            CALCULATION CORE                │
│   Swiss Ephemeris • KP Engine              │
│   Vedic Dasha • Vodou Correspondences      │
└────────────────────────────────────────────┘
```

### How It Works

**1. User Opens Mula App**
- Mobile-first interface with dark mystical theme
- Tap "Get Daily Fortune" or "Ask Consultant"

**2. Frontend Sends Request to Backend**
```json
{
  "type": "fortune_reading",
  "spread": "single_card",
  "question": "What should I focus on today?",
  "birth_data": { "date": "1990-08-15", "time": "14:30", "lat": 29.76, "lon": -95.36 }
}
```

**3. Backend Engine Processes**
- KP Engine calculates current planetary positions
- AI synthesizes oracle card meaning with natal chart context
- Vodou correspondences activate relevant Lwa energies

**4. Response Returns to Frontend**
```json
{
  "card": {
    "name": "Papa Legba - The Crossroads",
    "image_url": "/cards/papa-legba.webp",
    "meaning": "New opportunities require decisive action"
  },
  "interpretation": "With Moon transiting your 10th house...",
  "affirmation": "I stand at the crossroads with clarity",
  "timing": {
    "optimal_hours": ["6:00 AM", "12:00 PM", "6:00 PM"],
    "moon_phase": "Waxing Crescent"
  }
}
```

**5. User Views Beautiful Card Animation**
- Shuffle animation → Card flip → Reading display
- Save to journal, share, or ask follow-up questions

---

## 🔮 The Syncretic AI Prediction Engine

At the heart of Mula is our **multi-tradition prediction engine** that combines:

### KP (Krishnamurti Paddhati) System
- **Sub-lord precision**: 249 subdivisions per zodiac sign
- **Ruling Planet Algorithm**: Planet → Sign Lord → Nakshatra Lord → Sub-lord
- **Timing Accuracy**: Pinpoints events to specific date ranges
- **Current Status**: ✅ WORKING - Core engine complete

### Vedic Astrology
- **Vimshottari Dasha**: 120-year planetary period system
- **27 Nakshatras**: Lunar mansions with psychological profiles
- **Yogas & Combinations**: Classical auspicious/inauspicious patterns
- **Remedies**: Mantras, gemstones, fasting days

### Vodou Modern Oracle
- **21 Lwa Cards**: Authentic representations of Vodou spirits
- **Elemental Correspondences**: Fire, Water, Earth, Air, Ether
- **Cultural Authenticity**: Reviewed by Vodou practitioners
- **Divination Method**: Single card, 3-card spread, Lwa consultation

### AI Synthesis Layer
- **LangChain Orchestration**: Chains multiple tradition analyses
- **GPT-4 RAG**: Retrieval from 72+ astrology books
- **ChromaDB Vector Store**: Semantic search of knowledge base
- **Confidence Scoring**: Validates predictions across traditions

---

## 📱 Mula App Features

### 🎴 Fortune Readings
- **Daily Card**: Free daily fortune from Vodou Oracle or Tarot
- **Ask a Question**: Specific guidance for life decisions
- **Spreads**: Single, 3-card (past/present/future), Celtic Cross (premium)
- **Shuffle Animation**: Beautiful card shuffle with haptic feedback

### 💬 Spiritual Consultant Chat
- **4 AI Advisors**: Papa Legba, Erzulie Freda, Baron Samedi, Ogoun
- **Context-Aware**: Knows your natal chart and recent readings
- **Voice of Lwa**: Each advisor has unique personality and wisdom style
- **Follow-Up Questions**: "Tell me more about this card"

### 🌌 Natal Chart
- **Birth Chart Wheel**: Interactive planetary positions
- **Planetary Positions**: Exact degrees with retrograde indicators
- **Dasha Periods**: Current & upcoming life cycles
- **KP Houses**: 12 house cusps with sub-lords
- **Yogas**: Beneficial and challenging planetary combinations

### 📓 Reading Journal
- **Save Readings**: All fortune cards auto-saved
- **Reflection Notes**: Add your own insights
- **Search History**: Find past readings by date or keyword
- **Export**: Download as PDF or share on social media

### 💎 Premium Features ($9.99/month)
- **Unlimited Readings**: No daily limits
- **Advanced Spreads**: Celtic Cross, Relationship, Career
- **Audio Narration**: Listen to interpretations
- **Priority Consultant**: Faster AI response times
- **Personalized Reports**: Monthly astrological forecast

---

## 🚀 Quick Start

### Prerequisites

- **Node.js**: v18.0.0 or higher
- **Python**: v3.11 or higher
- **PostgreSQL**: v14.0 or higher
- **Redis**: v7.0 or higher (for caching)
- **Git**: v2.30 or higher

Verify installations:
```bash
node --version  # v18+
python --version  # v3.11+
psql --version  # v14+
redis-cli --version  # v7+
```

### 1. Clone Repository

```bash
git clone https://github.com/Thelastlineofcode/Astrology-Synthesis.git
cd Astrology-Synthesis
```

### 2. Set Up PostgreSQL Database

```bash
# Start PostgreSQL
# macOS: brew services start postgresql@14
# Linux: sudo systemctl start postgresql

# Create database
psql postgres
```

In PostgreSQL console:
```sql
CREATE DATABASE mula_db;
CREATE USER mula_user WITH ENCRYPTED PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE mula_db TO mula_user;
\q
```

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 4. Configure Environment Variables

Create `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
DATABASE_URL=postgresql://mula_user:your_secure_password@localhost:5432/mula_db
NEXTAUTH_SECRET=your_nextauth_secret_here
NEXTAUTH_URL=http://localhost:3000
STRIPE_PUBLISHABLE_KEY=pk_test_your_key
STRIPE_SECRET_KEY=sk_test_your_key
```

Create `backend/.env`:
```env
DATABASE_URL=postgresql://mula_user:your_secure_password@localhost:5432/mula_db
OPENAI_API_KEY=your_openai_key_here
REDIS_URL=redis://localhost:6379
JWT_SECRET=your_jwt_secret_here
STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

### 5. Initialize Database

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head  # Run migrations
python scripts/seed_cards.py  # Load Vodou Oracle cards
```

### 6. Download Ephemeris Files

```bash
cd backend
./scripts/download_ephemeris.sh
```

This downloads Swiss Ephemeris data (1800-2100) for astronomical calculations.

### 7. Start Development Servers

**Terminal 1 - Backend API:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend App:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Redis (caching):**
```bash
redis-server
```

### 8. Open the App

Navigate to **http://localhost:3000** 🎉

---

## 📚 Documentation

### Core Documentation
- **[Mula App Architecture](docs/MULA_APP_ARCHITECTURE.md)** - Complete product design & features
- **[Migration Guide](docs/PROJECT_PIVOT_MIGRATION_GUIDE.md)** - Transition from Roots Revealed
- **[Quick Start Guide](QUICK_START_GUIDE.md)** - Detailed setup instructions

### Design & UX
- **[Design System](docs/Design_Art_Component_Blueprints.md)** - Cosmic Midnight theme
- **[Vodou Oracle Guide](docs/vodou-tarot-template.md)** - Card system & cultural authenticity
- **[Tarot Deck Assets](docs/Design/Tarot-Deck/)** - Card artwork specifications
- **[Color Palette](COLOR_PALETTE_AND_DESIGN_SYSTEM.md)** - Cosmic Midnight design tokens

### Backend & API
- **[KP System Architecture](docs/KP_SYSTEM_ARCHITECTURE.md)** - Sub-lord calculation engine
- **[Syncretic AI System](SYNCRETIC_AI_PREDICTION_SYSTEM.md)** - Multi-tradition prediction logic
- **[API Documentation](API_DOCUMENTATION.md)** - Endpoint reference
- **[Database Schema](DATABASE_SCHEMA_DETAILED.md)** - PostgreSQL table structure

### Development
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to Mula
- **[Development Workflow](DEVELOPMENT.md)** - Git workflow, PR guidelines
- **[Testing Guide](CHART_TESTING_GUIDE.md)** - Unit, integration, E2E tests
- **[Accessibility Guide](ACCESSIBILITY_TESTING_GUIDE.md)** - WCAG 2.1 AA compliance

### Deployment
- **[Production Guide](DEPLOYMENT_GUIDE_PRODUCTION.md)** - Vercel + Railway deployment
- **[Authentication System](AUTHENTICATION_SYSTEM_COMPLETE.md)** - NextAuth.js setup
- **[Docker Setup](AGENT_1_DOCKER_CICD_GUIDE.md)** - Containerization guide
- **[Cost Analysis](COST_ANALYSIS_REPORT.md)** - Infrastructure costs

---

## 🛠️ Technology Stack

### Frontend (Mula Mobile App)
- **Framework**: Next.js 16 (App Router)
- **UI Library**: React 19 with TypeScript
- **Styling**: Tailwind CSS + CSS Modules
- **Animation**: Framer Motion
- **State**: Zustand (global), React Query (server)
- **Auth**: NextAuth.js with JWT
- **PWA**: next-pwa for offline support
- **Testing**: Vitest + React Testing Library + Playwright

### Backend (Prediction API)
- **Framework**: FastAPI (Python 3.11+)
- **Astronomy**: Swiss Ephemeris (JPL precision)
- **KP Engine**: Custom sub-lord calculator ✅
- **Database**: PostgreSQL 14+ with SQLAlchemy ORM
- **Caching**: Redis 7+ for session and rate limiting
- **AI**: OpenAI GPT-4 with LangChain orchestration
- **Vector DB**: ChromaDB for RAG knowledge base
- **Testing**: pytest + pytest-asyncio

### Infrastructure
- **Frontend Hosting**: Vercel (Edge Network)
- **Backend Hosting**: Railway or Render
- **CDN**: Cloudflare (assets, DDoS protection)
- **Database**: Supabase PostgreSQL (production)
- **Monitoring**: Sentry (error tracking), Plausible (analytics)
- **Payments**: Stripe (subscriptions)
- **Email**: SendGrid (transactional emails)

### DevOps
- **Version Control**: Git + GitHub
- **CI/CD**: GitHub Actions
- **Containerization**: Docker + docker-compose
- **Secrets**: GitHub Secrets + Vercel Env Vars
- **Linting**: ESLint (frontend), Ruff (backend)
- **Formatting**: Prettier (frontend), Black (backend)

---

## 🌍 Project Structure

```
Astrology-Synthesis/
├── frontend/                 # Next.js Mula mobile app
│   ├── src/
│   │   ├── app/              # Next.js 16 App Router pages
│   │   │   ├── fortune/      # Daily fortune reading page
│   │   │   ├── consultant/   # AI spiritual advisor chat
│   │   │   ├── chart/        # Natal chart viewer
│   │   │   ├── journal/      # Reading history
│   │   │   └── dashboard/    # User home (recent readings)
│   │   ├── components/       # React components
│   │   │   ├── mula/         # Mula-specific (CardDraw, Consultant)
│   │   │   ├── chart/        # Chart wheel, house table
│   │   │   └── shared/       # Button, Card, Modal, etc.
│   │   ├── lib/              # Utilities, API clients
│   │   ├── hooks/            # Custom React hooks
│   │   └── styles/           # Global CSS, Tailwind config
│   ├── public/               # Static assets
│   │   ├── cards/            # Vodou Oracle & Tarot images
│   │   ├── avatars/          # Consultant Lwa avatars
│   │   └── fonts/            # Cinzel, Montserrat fonts
│   └── package.json
├── backend/                  # FastAPI prediction engine
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   │   ├── fortune.py    # /api/fortune (card readings)
│   │   │   ├── consultant.py # /api/consultant (AI chat)
│   │   │   └── chart.py      # /api/chart (natal calculations)
│   │   ├── core/             # Configuration, security, DB
│   │   ├── engines/          # Calculation engines
│   │   │   ├── kp_engine.py  # KP sub-lord calculator ✅
│   │   │   ├── vedic.py      # Dasha, nakshatra, yogas
│   │   │   └── vodou.py      # Oracle correspondences
│   │   ├── ai/               # AI orchestration
│   │   │   ├── langchain.py  # LangChain chains
│   │   │   ├── embeddings.py # Vector search
│   │   │   └── prompts.py    # GPT-4 prompt templates
│   │   ├── models/           # SQLAlchemy ORM models
│   │   └── schemas/          # Pydantic request/response
│   ├── data/
│   │   ├── ephe/             # Swiss Ephemeris files
│   │   ├── cards/            # Vodou Oracle metadata JSON
│   │   └── knowledge_base/   # 72+ astrology books (PDF/TXT)
│   ├── alembic/              # Database migrations
│   ├── tests/                # pytest test suite
│   └── requirements.txt
├── docs/                     # Project documentation
│   ├── MULA_APP_ARCHITECTURE.md
│   ├── PROJECT_PIVOT_MIGRATION_GUIDE.md
│   ├── Design_Art_Component_Blueprints.md
│   └── archive/              # Old "Roots Revealed" docs
├── scripts/                  # Utility scripts
│   ├── download_ephemeris.sh
│   └── seed_cards.py
└── README.md                 # This file
```

---

## 🎨 Design System: Cosmic Midnight

Mula uses a **dark, mystical theme** inspired by midnight skies and cosmic energy.

### Color Palette

```css
/* Background & Surfaces */
--bg-cosmic-dark: #1A0F1E;      /* Deep space black */
--bg-surface-dark: #2D1B33;     /* Card backgrounds */
--bg-surface-elevated: #3D2844; /* Modals, dropdowns */

/* Accents & Actions */
--accent-purple: #9D4EDD;       /* Primary actions, links */
--accent-orange: #FF6B35;       /* CTAs, highlights */
--accent-gold: #FFD700;         /* Premium features */

/* Text */
--text-primary: #F5F3F7;        /* Main text (high contrast) */
--text-secondary: #C8B8D0;      /* Secondary text */
--text-tertiary: #8B7A94;       /* Disabled, subtle text */

/* Semantic */
--success-green: #4CAF50;
--warning-yellow: #FFC107;
--error-red: #E63946;
```

### Typography

- **Headings**: Cinzel (serif) - mystical elegance
- **Body**: Montserrat (sans-serif) - modern readability
- **Monospace**: JetBrains Mono - code snippets

### Components

- **Cards**: Rounded corners (16px), subtle glow shadows
- **Buttons**: Gradient backgrounds with hover lift animations
- **Inputs**: Dark with accent borders on focus
- **Modals**: Frosted glass effect (backdrop-blur)

See full design system: [Design_Art_Component_Blueprints.md](docs/Design_Art_Component_Blueprints.md)

---

## 🗺️ Development Roadmap

### ✅ Phase 1: Foundation (Completed Nov 2024)
- [x] KP engine core calculation
- [x] Swiss Ephemeris integration
- [x] Basic FastAPI backend structure
- [x] PostgreSQL database schema
- [x] Initial Next.js frontend

### ✅ Phase 2: Backend Engine (Completed Dec 2024)
- [x] Vedic dasha calculations
- [x] Nakshatra psychological profiles
- [x] Multi-tradition synthesis logic
- [x] AI interpretation with GPT-4
- [x] Knowledge base RAG system

### 🚧 Phase 3: Mula Frontend (In Progress - Jan 2025)
- [x] Dashboard redesign with animations
- [x] Button component Link support
- [x] Accessibility improvements
- [ ] Fortune reading page with card shuffle
- [ ] Consultant AI chat interface
- [ ] Natal chart modernization
- [ ] Reading journal implementation

### 📋 Phase 4: Premium Features (Feb 2025)
- [ ] Stripe subscription integration
- [ ] Advanced tarot spreads (Celtic Cross)
- [ ] Audio narration for readings
- [ ] Export to PDF functionality
- [ ] Social sharing capabilities

### 🚀 Phase 5: Launch Prep (Mar 2025)
- [ ] PWA offline support
- [ ] Performance optimization (Lighthouse 90+)
- [ ] Security audit (penetration testing)
- [ ] Load testing (1000+ concurrent users)
- [ ] Beta testing with 100 users

### 🌟 Phase 6: Public Launch (Apr 2025)
- [ ] Production deployment (Vercel + Railway)
- [ ] Marketing landing page
- [ ] App Store & Play Store submission
- [ ] Influencer partnerships
- [ ] Launch event

---

## 🧪 Testing

### Run Frontend Tests
```bash
cd frontend
npm run test          # Unit tests (Vitest)
npm run test:e2e      # E2E tests (Playwright)
npm run test:a11y     # Accessibility tests
```

### Run Backend Tests
```bash
cd backend
source venv/bin/activate
pytest                # All tests
pytest tests/engines/ # Just calculation engines
pytest -k "test_kp"   # KP engine tests only
```

### Test Coverage Goals
- **Frontend**: 80%+ coverage
- **Backend**: 90%+ coverage (critical paths 100%)
- **E2E**: All user flows covered

---

## 🤝 Contributing

We welcome contributions to Mula! See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Code of Conduct
- Development workflow
- Pull request guidelines
- Coding standards

**Quick Contribution Steps:**

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes with tests
4. Run linting: `npm run lint` (frontend) or `ruff check .` (backend)
5. Commit: `git commit -m "feat: add fortune card shuffle animation"`
6. Push: `git push origin feature/your-feature`
7. Open Pull Request on GitHub

---

## 📄 License

This project is proprietary software. All rights reserved.

**Copyright © 2025 Mula: The Root**

Unauthorized copying, distribution, or modification is prohibited.

For licensing inquiries: contact@mula-app.com

---

## 📞 Support & Contact

- **Website**: https://mula-app.com (coming soon)
- **Email**: support@mula-app.com
- **Discord**: https://discord.gg/mula-community
- **Twitter/X**: @MulaTheRoot
- **GitHub Issues**: For bug reports and feature requests

---

## 🙏 Acknowledgments

- **Swiss Ephemeris**: Astrodienst AG for astronomical calculation library
- **KP System**: K.S. Krishnamurti for revolutionary sub-lord methodology
- **Vodou Community**: Cultural reviewers for authentic oracle representation
- **Open Source**: LangChain, Next.js, FastAPI, and all libraries we build upon

---

## 🔮 About the Name

**Mula** (मूल) carries deep meaning across traditions:

1. **Sanskrit**: "Root" or "Foundation" - representing return to spiritual roots
2. **Vedic Astrology**: 19th nakshatra (13°20' - 26°40' Sagittarius), ruled by Ketu
   - Symbolism: A bunch of roots tied together
   - Deity: Nirriti (goddess of destruction and chaos)
   - Energy: Transformation through destruction of old patterns
3. **Spiritual Significance**: Going to the root of problems, deep ancestral wisdom

Just as roots anchor a tree and provide nourishment, Mula grounds users in authentic spiritual traditions while helping them grow.

---

**Built with 💜 by the Mula Team**

*"Return to your roots. Reach for the stars."*
