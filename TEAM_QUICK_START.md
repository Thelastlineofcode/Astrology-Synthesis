# Mula: The Root - Quick Start Guide for Team Leads

## 🎯 Your Role & Responsibilities

### If you are @frontend-lead:

**Primary Focus**: Next.js app, React components, UI/UX  
**Key Issues**: #88, #94, #95  
**Your GitHub Issues**:

- #88: Deploy Frontend to Vercel
  - Fix TypeScript strict mode errors
  - Build and deploy to Vercel
  - Test on mobile/tablet/desktop
- #94: User Profile & Reading History Pages
  - Create `/profile` page
  - Create `/readings/history` page
  - Create reading detail view
  - Connect to backend APIs

- #95: E2E Test Suite
  - Collaborate with @qa-lead
  - Provide test scenarios for pages
  - Ensure accessibility in components

**Quick Actions**:

```bash
# Check TypeScript errors
tsc --noEmit

# Build and test
npm run build
npm run dev

# Test responsiveness at breakpoints
# 375px (mobile), 768px (tablet), 1440px (desktop)
```

**Contact @backend-lead for**: API contracts, endpoint responses  
**Contact @devops-lead for**: Vercel deployment credentials

---

### If you are @backend-lead:

**Primary Focus**: FastAPI, database, APIs, authentication  
**Key Issues**: #87, #89, #91, #92  
**Your GitHub Issues**:

- #87: Start Backend Server & Integration Tests
  - Fix any import errors
  - Run backend locally
  - Execute pytest suite
  - Document any failures

- #89: Deploy to Railway/Render (with @devops-lead)
  - Create deployment config
  - Set up environment variables
  - Test production endpoints

- #91: PostgreSQL Setup & Schema Migration
  - Design database schema
  - Create SQLAlchemy models
  - Set up Alembic migrations
  - Seed initial data (advisors, cards)

- #92: JWT Authentication
  - Create `/auth/register` endpoint
  - Create `/auth/login` endpoint
  - Create `/auth/refresh` endpoint
  - Secure all existing endpoints

**Quick Actions**:

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Start backend server
python backend/main.py
# or
uvicorn backend.main:app --reload

# Run tests
pytest tests/test_mula_api.py -v

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Swagger UI
```

**Contact @frontend-lead for**: Component requirements, error handling expectations  
**Contact @devops-lead for**: Database credentials, deployment setup  
**Contact @ai-lead for**: Advisor prompt formats, response structure

---

### If you are @ai-lead:

**Primary Focus**: LLM integration, RAG, knowledge base  
**Key Issues**: #90, #93  
**Your GitHub Issues**:

- #90: OpenAI GPT-4 Integration
  - Create `backend/services/llm_service.py`
  - Define system prompts for 4 advisors
  - Integrate with consultant endpoint
  - Set up error handling & fallbacks

- #93: RAG Knowledge Base
  - Curate knowledge base documents
  - Set up Pinecone vector database
  - Create document ingestion script
  - Integrate with LLM responses

**Quick Actions**:

```bash
# Install OpenAI SDK
pip install openai

# Test GPT-4 API (after key is set)
python -c "from openai import OpenAI; print('API key configured')"

# Ingest knowledge base (when ready)
python backend/scripts/ingest_knowledge_base.py
```

**Environment Variables Needed**:

```
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
PINECONE_INDEX_NAME=mula-knowledge-base
```

**Contact @backend-lead for**: API integration points  
**Contact @devops-lead for**: API key management

---

### If you are @devops-lead:

**Primary Focus**: Deployment, infrastructure, monitoring  
**Key Issues**: #88, #89, #96  
**Your GitHub Issues**:

- #88: Deploy Frontend to Vercel
  - Connect GitHub repo to Vercel
  - Configure build settings
  - Set environment variables
  - Test deployed site

- #89: Deploy Backend to Railway/Render
  - Set up PostgreSQL database
  - Create backend service
  - Configure environment variables
  - Enable auto-deployments

- #96: Monitoring & Error Tracking
  - Set up Sentry for error tracking
  - Configure uptime monitoring
  - Set up performance monitoring
  - Create dashboards & alerts

**Quick Actions**:

```bash
# Vercel deployment (after connecting GitHub)
# → Automatic on push to main

# Railway/Render deployment
# → Link GitHub repo and auto-deploy

# Test health endpoints after deployment
curl https://api.mula-app.com/health
curl https://mula-app.vercel.app/
```

**Environment Variables for Production**:

```
DATABASE_URL=postgresql://user:pass@host/dbname
ENVIRONMENT=production
DEBUG=False
CORS_ORIGINS=https://mula-app.vercel.app
SECRET_KEY=generate-new-secure-key
LOG_LEVEL=INFO
SENTRY_DSN=...
```

**Contact @backend-lead for**: Environment variable requirements  
**Contact @frontend-lead for**: Frontend domain for CORS

---

### If you are @qa-lead:

**Primary Focus**: Testing, quality assurance, release readiness  
**Key Issues**: #95, #96  
**Your GitHub Issues**:

- #95: E2E Test Suite
  - Set up Playwright or Cypress
  - Create test scenarios for:
    - User registration/login
    - Fortune card draw
    - Consultant chat
    - Reading history
    - Navigation
  - Run tests in CI/CD pipeline
  - Generate coverage report

- #96: Monitoring (collaborate with @devops-lead)
  - Verify Sentry is capturing errors
  - Test error notifications
  - Verify uptime monitoring
  - Create monitoring dashboard

**Quick Actions**:

```bash
# Install Playwright
npm install --save-dev @playwright/test

# Run E2E tests
npx playwright test

# Generate test report
npx playwright show-report
```

**Test Scenarios Needed**:

- Auth flow (register → login → logout)
- Fortune draw (select type → draw card → view reading)
- Chat (select advisor → send message → get response)
- Navigation (all pages accessible)
- Mobile responsiveness (375px, 768px, 1440px)
- Error handling (400, 401, 500 responses)

**Contact @backend-lead for**: API contracts, error responses  
**Contact @frontend-lead for**: UI/component selectors  
**Contact @devops-lead for**: Staging environment access

---

## 📊 Critical Path Timeline

```
WEEK 1 (Nov 4-10)
├─ Monday: Kick-off standup
├─ Backend: Start local testing (#87)
├─ Frontend: Fix TypeScript errors (#88)
├─ DevOps: Set up PostgreSQL & environments (#89, #91)
├─ AI: Design system prompts (#90)
└─ QA: Plan test suite (#95)

WEEK 2 (Nov 11-17)
├─ Backend: Complete Auth (#92), Schema (#91)
├─ Frontend: Deploy to Vercel (#88)
├─ DevOps: Deploy backend & monitoring (#89, #96)
├─ QA: Implement E2E tests (#95)
└─ Status: MVP ready for launch

WEEK 3+ (Nov 18+)
├─ AI: Integrate GPT-4 (#90)
├─ AI: Build RAG knowledge base (#93)
├─ Frontend: User profile pages (#94)
└─ Ongoing: Bug fixes & optimization
```

---

## 🚨 How to Get Help

**Slack Channel**: #mula-dev (post questions here)  
**Weekly Standup**: Monday 10am UTC  
**GitHub Issues**: Add comments with blockers  
**1-on-1**: Schedule with project lead if stuck

---

## ✅ Definition of Done (for each issue)

- [ ] Code merged to `main` branch
- [ ] All tests passing (100%)
- [ ] TypeScript/linting checks pass
- [ ] Documentation updated
- [ ] Related issues updated
- [ ] Dependencies tracked
- [ ] Performance requirements met
- [ ] Accessibility verified (for UI)
- [ ] Security reviewed (for API)

---

## 🎯 Week 1 Action Items (Do This First)

**By EOD Tomorrow**:

If @backend-lead:

```
1. Run: python backend/main.py
2. Test: curl http://localhost:8000/health
3. Report: Any errors in GitHub #87
```

If @frontend-lead:

```
1. Run: tsc --noEmit
2. Run: npm run build
3. Report: Errors in GitHub #88
```

If @devops-lead:

```
1. Create Vercel project (mula-app)
2. Create Railway/Render account
3. Document credentials (securely)
4. Report: Setup complete in #88, #89
```

If @ai-lead:

```
1. Outline advisor system prompts
2. Design knowledge base structure
3. Report: Strategy in GitHub #90, #93
```

If @qa-lead:

```
1. Review existing test files
2. Plan E2E test scenarios
3. Report: Test plan in GitHub #95
```

---

## 📚 Useful Documentation

- **ARCHITECTURE_ROLES.md** - Full architecture & dependencies
- **PHASE_3_ISSUES_UPDATE.md** - Issues summary & metrics
- **IMPLEMENTATION_CHECKLIST.md** - What's already done
- **README.md** - Project overview
- **API_DOCUMENTATION.md** - API reference (when available)

---

**Last Updated**: November 3, 2025  
**Questions?** Create issue or post in #mula-dev
