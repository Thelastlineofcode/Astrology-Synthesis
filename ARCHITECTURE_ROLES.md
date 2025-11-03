# Mula: The Root - Architecture & Role Assignments

**Updated**: November 3, 2025  
**Status**: Phase 3 - MVP Launch Preparation

---

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    MULA: THE ROOT MOBILE APP                    │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │          FRONTEND (Next.js 16 + React 19)              │  │
│  │  - Fortune Card Draw (`/fortune`)                      │  │
│  │  - Spiritual Consultant Chat (`/consultant`)           │  │
│  │  - User Profile & Reading History (`/profile`, etc)    │  │
│  │  - Responsive Mobile-First UI (Dark Theme)             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │      BACKEND API (FastAPI + Python 3.11)              │  │
│  │  - REST Endpoints (/api/v1/*)                          │  │
│  │  - Authentication (JWT + Refresh Tokens)               │  │
│  │  - Business Logic (Fortune, Chat)                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │          EXTERNAL SERVICES & DATA                       │  │
│  │  - Perplexity API (LLM for advisor responses)          │  │
│  │  - Vector DB optional (RAG knowledge base)             │  │
│  │  - PostgreSQL (User data, readings, messages)          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 👥 Team Structure & Role Assignments

### 1. **@frontend-lead** - Frontend Architecture Owner

**Responsibilities:**

- Next.js application structure and configuration
- React component development and optimization
- TypeScript type safety and strict mode compliance
- CSS/Design system implementation (Cosmic Midnight theme)
- Frontend state management and API integration
- Mobile responsiveness (375px - 1440px)
- Accessibility (ARIA labels, keyboard navigation)
- Performance optimization (Lighthouse \u003e80)
- Bundle size monitoring

**Key Files/Folders:**

```
frontend/
├── src/app/                    # Next.js pages/routes
├── src/components/             # Reusable React components
├── src/styles/                 # Design system (CSS/Variables)
├── src/types/                  # TypeScript interfaces
├── next.config.js
├── tsconfig.json
└── package.json
```

**Phase 3 Issues:**

- #88: Deploy Frontend to Vercel
- #94: Add User Profile & Reading History Pages
- #95: Comprehensive E2E Testing

**KPIs:**

- All TypeScript strict mode errors resolved ✓
- Build passes with 0 errors, 0 warnings
- Lighthouse Performance \u003e80
- Accessibility \u003e90
- Mobile responsiveness verified at 3+ breakpoints

---

### 2. **@backend-lead** - Backend Architecture Owner

**Responsibilities:**

- FastAPI application structure and configuration
- Python code quality and testing
- Database design and ORM (SQLAlchemy)
- Authentication system (JWT, refresh tokens)
- API endpoint design and implementation
- Error handling and validation (Pydantic)
- Business logic (fortune logic, advisor logic)
- CORS and security headers
- API documentation (OpenAPI/Swagger)

**Key Files/Folders:**

```
backend/
├── main.py                     # FastAPI app entry point
├── api/v1/                     # API endpoints (fortune, consultant, auth)
├── models/                     # SQLAlchemy ORM models
├── schemas/                    # Pydantic request/response models
├── services/                   # Business logic (LLM, vector store)
├── config/                     # Configuration (security, database)
├── requirements.txt            # Python dependencies
└── tests/                      # Test suite
```

**Phase 3 Issues:**

- #87: Start Backend Server & Integration Tests
- #89: Deploy Backend to Railway/Render
- #91: PostgreSQL Setup & Schema Migration
- #92: JWT Authentication & User Sessions

**KPIs:**

- All 6 API endpoints working
- Test pass rate \u003e95% (34/36 tests)
- Database connections pooled and optimized
- JWT token generation/validation working
- Error responses follow consistent format

---

### 3. **@ai-lead** - LLM & RAG Architecture Owner

**Responsibilities:**

- OpenAI GPT-4 API integration and prompt engineering
- Advisor personality prompt development (4 Lwa)
- Retrieval-Augmented Generation (RAG) system
- Vector database (Pinecone) management
- Knowledge base curation and ingestion
- LLM response quality and grounding
- Token usage monitoring and cost optimization
- Streaming response implementation (phase 2)
- Safety guardrails and content filtering

**Key Files/Folders:**

```
backend/
├── services/llm_service.py     # OpenAI integration
├── services/vector_store.py    # Pinecone integration
├── knowledge_base/             # RAG documents
│   ├── vodou_traditions/
│   ├── astrology/
│   └── spirituality/
├── config/prompts.py           # System prompts for advisors
└── scripts/
    └── ingest_knowledge_base.py
```

**Phase 3 Issues:**

- #90: Integrate OpenAI GPT-4 for AI Advisor Responses
- #93: Build Knowledge Base & Context Retrieval for Advisors

**KPIs:**

- GPT-4 responses maintain advisor personality
- RAG retrieval relevance \u003e80%
- Response latency \u003c3s
- Cost per response \u003c$0.10
- Knowledge base documents: \u003e100 chunks indexed

---

### 4. **@devops-lead** - Infrastructure & Deployment Owner

**Responsibilities:**

- Deployment pipeline setup (Vercel, Railway/Render)
- Environment configuration management (.env, secrets)
- Database deployment and management (PostgreSQL)
- CI/CD pipeline (GitHub Actions)
- Monitoring and error tracking (Sentry, Datadog)
- Uptime monitoring and alerting
- Performance monitoring (Lighthouse, Vercel Analytics)
- Database backups and disaster recovery
- Security scanning and compliance
- Infrastructure as Code (if applicable)

**Key Services:**

- Vercel (Frontend hosting)
- Railway or Render (Backend hosting)
- PostgreSQL (Database)
- Sentry (Error tracking)
- Pinecone (Vector database)
- Uptime.com (Monitoring)

**Phase 3 Issues:**

- #88: Deploy Frontend to Vercel
- #89: Deploy Backend to Railway/Render
- #96: Set Up Error Tracking & Performance Monitoring

**KPIs:**

- Frontend deployed to Vercel with auto-deploy
- Backend deployed to Railway/Render with CI/CD
- 99.5% uptime SLA
- Error tracking capturing \u003e95% of errors
- Database backups running daily

---

### 5. **@qa-lead** - Quality Assurance & Testing Owner

**Responsibilities:**

- End-to-end test suite (Playwright/Cypress)
- Manual testing and QA workflows
- Test coverage tracking
- Performance testing and benchmarking
- Accessibility testing (WCAG 2.1 AA)
- Security testing and penetration testing
- Bug triaging and reporting
- Release readiness verification
- User acceptance testing (UAT)

**Key Tools:**

- Playwright or Cypress (E2E testing)
- Jest (Unit testing)
- pytest (Backend testing)
- Lighthouse (Performance & Accessibility)
- OWASP ZAP (Security scanning)

**Phase 3 Issues:**

- #95: Comprehensive E2E Test Suite & QA

**KPIs:**

- E2E test coverage \u003e90%
- All critical user flows tested
- Performance benchmarks met (LCP \u003c4s)
- Accessibility audit score \u003e90
- Zero high-severity security issues

---

## 📋 Phase 3 Roadmap & Milestones

### Phase 3a: MVP Launch (Weeks 1-2)

**Goal**: Production-ready deployment

**Issues**:

1. ✅ #87: Start Backend Server & Integration Tests
2. ✅ #88: Deploy Frontend to Vercel
3. ✅ #89: Deploy Backend to Railway/Render
4. ✅ #91: PostgreSQL Setup & Schema Migration
5. ✅ #92: JWT Authentication & User Sessions
6. ✅ #94: User Profile & Reading History Pages
7. ✅ #95: Comprehensive E2E Testing
8. ✅ #96: Error Tracking & Performance Monitoring

**Owners**: @devops-lead, @backend-lead, @frontend-lead, @qa-lead

**Success Criteria**:

- ✓ Frontend deployed to vercel.com
- ✓ Backend deployed to Railway/Render
- ✓ PostgreSQL database in production
- ✓ JWT authentication working
- ✓ All 6 API endpoints functional
- ✓ E2E tests passing 100%
- ✓ Error tracking active
- ✓ Uptime monitoring active

---

### Phase 3b: AI Enhancement (Weeks 3-4)

**Goal**: Real AI responses with grounded knowledge

**Issues**:

1. ✅ #90: Integrate OpenAI GPT-4 for AI Advisor Responses
2. ✅ #93: Build Knowledge Base & Context Retrieval for Advisors

**Owners**: @ai-lead, @backend-lead

**Success Criteria**:

- ✓ GPT-4 responses personalized per advisor
- ✓ RAG knowledge base indexed
- ✓ Context retrieval working
- ✓ Source attribution in responses
- ✓ Cost tracking in place

---

### Phase 3c: Premium Features (Weeks 5-6)

**Goal**: Multi-card spreads, audio, journal

**Potential Issues**:

- [ ] [FEATURE] Implement Multi-Card Spreads
- [ ] [FEATURE] Add Audio Narration for Readings
- [ ] [FEATURE] Enhanced Reading Journal
- [ ] [FEATURE] Social Sharing Features

**Owners**: TBD

---

## 🔄 Cross-functional Dependencies

```
Frontend Lead
    ├─ Needs Backend API contracts from Backend Lead
    ├─ Depends on Auth implementation (Backend Lead)
    └─ Needs API response formats (Backend Lead)

Backend Lead
    ├─ Needs Frontend API consumer feedback
    ├─ Needs LLM advisor personalities from AI Lead
    ├─ Depends on Database schema (Database Manager)
    └─ Provides API contracts to Frontend Lead

AI Lead
    ├─ Needs Backend API integration (Backend Lead)
    ├─ Needs PostgreSQL schema (Database Manager)
    ├─ Needs Pinecone setup (DevOps Lead)
    └─ Provides prompt templates to Backend Lead

DevOps Lead
    ├─ Needs deployment configs from Frontend/Backend Leads
    ├─ Needs monitoring requirements from QA Lead
    ├─ Provides deployment credentials to all leads
    └─ Manages infrastructure for all services

QA Lead
    ├─ Needs API contracts from Backend Lead
    ├─ Needs deployed environments from DevOps Lead
    ├─ Needs accessibility requirements from Frontend Lead
    └─ Provides test results to all leads
```

---

## 📊 Weekly Standup Template

```
Monday 10am UTC
├─ Frontend Lead: TypeScript status, component completion
├─ Backend Lead: API implementation, database progress
├─ AI Lead: LLM integration, knowledge base status
├─ DevOps Lead: Deployment status, infrastructure
└─ QA Lead: Test coverage, blockers, release readiness

Async Updates (Wednesday):
├─ Issue completion rates
├─ Risk/blocker identification
└─ Next week dependencies
```

---

## 🚀 Critical Path to Launch

```
Week 1 (Nov 4-10)
├─ Backend Server startup [Backend Lead]
├─ Frontend build fix [Frontend Lead]
├─ Database schema finalized [Backend Lead]
├─ PostgreSQL deployed [DevOps Lead]
└─ Integration tests passing [QA Lead]

Week 2 (Nov 11-17)
├─ Frontend → Vercel [DevOps Lead]
├─ Backend → Railway/Render [DevOps Lead]
├─ JWT Auth implemented [Backend Lead]
├─ Monitoring configured [DevOps Lead]
└─ E2E tests automated [QA Lead]

Week 3 (Nov 18-24)
├─ GPT-4 integrated [AI Lead]
├─ User profile pages [Frontend Lead]
├─ Reading history API [Backend Lead]
└─ Production readiness audit [QA Lead]

Week 4+ (Nov 25+)
├─ RAG knowledge base [AI Lead]
├─ Premium features [Frontend Lead]
└─ Ongoing monitoring [DevOps Lead]
```

---

## 🎯 Success Metrics

### Product

- ✓ MVP fully functional
- ✓ 99.5% uptime
- ✓ \u003c3s response times

### Team

- ✓ Zero P0 blockers
- ✓ All issues in Phase 3a completed
- ✓ Clear ownership across all areas

### Quality

- ✓ Test coverage \u003e90%
- ✓ Performance score \u003e80
- ✓ Accessibility score \u003e90
- ✓ Zero high-severity security issues

---

## 📞 Communication Channels

- **Slack**: #mula-dev (daily updates)
- **GitHub**: Issues and PRs (code review)
- **Standup**: Weekly Monday 10am UTC
- **Escalations**: Direct message to project lead

---

## 🔐 Security Checklist

- [ ] No secrets in code
- [ ] Environment variables configured
- [ ] Database backups automated
- [ ] CORS properly restricted
- [ ] HTTPS enforced
- [ ] Rate limiting configured
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (ORM)
- [ ] XSS prevention (React sanitization)
- [ ] CSRF tokens (if needed)
- [ ] Security headers (CSP, X-Frame-Options, etc)

---

**Document Owner**: Project Lead  
**Last Updated**: November 3, 2025  
**Next Review**: November 10, 2025 (after Phase 3a)
