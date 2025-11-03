# Mula: The Root - AI Agent Team Structure

**Date**: November 3, 2025  
**Project**: Mula: The Root - Spiritual Companion Mobile App  
**Team Size**: 5 AI Agents + 1 Orchestrator

---

## 🎯 Team Overview

This document defines the AI agent team structure for Phase 3 development (MVP Launch + AI Integration). Each agent has a specific domain of expertise and assigned GitHub issues.

---

## 👥 Team Members & Roles

### 1. **Backend Agent** (`@backend-agent`)

**Expertise**: FastAPI, Python, SQLAlchemy ORM, REST APIs, business logic

**Responsibilities**:

- Develop and maintain FastAPI server
- Implement REST API endpoints
- Design and manage database schema
- Implement JWT authentication system
- Write integration tests (pytest)
- Handle error handling and validation
- Optimize query performance

**Assigned Issues**:

- **#87**: Backend Server & Integration Tests (4h)
- **#89**: Deploy Backend to Railway/Render (4h)
- **#91**: PostgreSQL Setup & Schema Migration (6h)
- **#92**: JWT Authentication & User Sessions (8h)

**Key Technologies**:

- FastAPI 0.109+
- SQLAlchemy 2.0+
- Pydantic 2.0+
- pytest
- PostgreSQL 14+
- uvicorn

**Success Metrics**:

- All 36 integration tests passing
- 0 database connection errors
- API response time < 500ms
- JWT token generation/validation 100% successful

**Definition of Done**:

- Code peer-reviewed
- Tests passing (> 95% coverage)
- API documentation updated
- No high-severity bugs
- Performance benchmarks met

---

### 2. **Frontend Agent** (`@frontend-agent`)

**Expertise**: Next.js, React, TypeScript, UI/UX, responsive design

**Responsibilities**:

- Develop Next.js application and pages
- Build React components with strict TypeScript
- Implement Cosmic Midnight design system
- Ensure mobile responsiveness (375px - 1440px)
- Create user-facing features (fortune, chat, profile)
- Fix accessibility issues (WCAG 2.1 AA)
- Optimize bundle size and performance

**Assigned Issues**:

- **#88**: Deploy Frontend to Vercel (3h)
- **#94**: User Profile & Reading History Pages (8h)
- **#95**: Comprehensive E2E Test Suite (6h)

**Key Technologies**:

- Next.js 16+
- React 19+
- TypeScript (strict mode)
- Tailwind CSS / CSS Modules
- Playwright (E2E testing)
- Vercel (deployment)

**Success Metrics**:

- Lighthouse Performance > 80
- Lighthouse Accessibility > 90
- TypeScript strict mode: 0 errors
- Mobile responsiveness verified
- E2E test coverage > 90%

**Definition of Done**:

- All TypeScript errors resolved
- Mobile tested at 375px, 768px, 1440px
- Accessibility audit passed
- E2E tests pass
- Lighthouse > 80 all metrics

---

### 3. **DevOps Agent** (`@devops-agent`)

**Expertise**: Infrastructure, CI/CD, deployment, monitoring, security

**Responsibilities**:

- Set up and maintain deployment pipelines
- Manage environment configurations
- Configure database backups and disaster recovery
- Implement error tracking (Sentry)
- Set up performance monitoring
- Manage uptime and alerting
- Secure API keys and secrets
- Configure GitHub Actions workflows

**Assigned Issues**:

- **#89**: Deploy Backend to Railway/Render (4h)
- **#96**: Error Tracking & Performance Monitoring (4h)

**Key Technologies**:

- Railway / Render
- Vercel
- Sentry (error tracking)
- Uptime.com (monitoring)
- GitHub Actions
- PostgreSQL backups
- SSL/TLS certificates

**Success Metrics**:

- 99.5% uptime SLA
- Error tracking capturing > 95% of errors
- Deployment time < 5 minutes
- All alerts working
- Zero security vulnerabilities

**Definition of Done**:

- Deployment pipeline automated
- Monitoring dashboards active
- Alerts configured and tested
- Backup strategy verified
- Documentation complete

---

### 4. **QA Agent** (`@qa-agent`)

**Expertise**: Testing, quality assurance, accessibility, performance

**Responsibilities**:

- Design and implement E2E test suite
- Perform manual testing of critical flows
- Run accessibility tests (WCAG 2.1 AA)
- Execute performance tests and benchmarking
- Test cross-browser compatibility
- Verify mobile responsiveness
- Create test documentation
- Track and triage bugs

**Assigned Issues**:

- **#95**: Comprehensive E2E Test Suite (6h)

**Key Technologies**:

- Playwright
- Jest
- pytest
- Lighthouse
- Axe DevTools
- OWASP ZAP

**Success Metrics**:

- E2E test coverage > 90%
- All critical flows tested
- Accessibility score > 90
- Performance benchmarks met
- Zero high-severity bugs in production

**Definition of Done**:

- Test suite written and passing
- Test documentation complete
- Performance baselines established
- Accessibility audit passed
- Release sign-off given

---

### 5. **AI/LLM Agent** (`@ai-agent`)

**Expertise**: LLM integration, prompt engineering, RAG systems, knowledge bases

**Responsibilities**:

- Integrate Perplexity API for advisor responses
- Engineer system prompts for each Lwa advisor
- Design RAG (Retrieval-Augmented Generation) system
- Build and maintain knowledge base
- Optimize token usage and costs
- Monitor LLM quality and accuracy
- Implement safety guidelines and content filtering
- Handle streaming responses

**Assigned Issues**:

- **#90**: Integrate Perplexity API for Advisor Responses (6h)
- **#93**: Build Knowledge Base & Context Retrieval (8h)

**Key Technologies**:

- Perplexity API
- Vector databases (Chroma)
- Embeddings
- Prompt engineering
- Token optimization
- Streaming

**Success Metrics**:

- Advisor responses maintain personality
- Response time < 3 seconds
- Cost per response < $0.05 (free tier)
- RAG retrieval accuracy > 80%
- User satisfaction > 4.0/5.0

**Definition of Done**:

- Perplexity integration complete
- Advisor prompts tested and approved
- Response quality validated
- Cost tracking implemented
- Knowledge base indexed

---

### 6. **Orchestrator Agent** (`@orchestrator`)

**Role**: Project coordination, dependency management, risk assessment

**Responsibilities**:

- Track overall project progress
- Manage cross-team dependencies
- Identify and escalate blockers
- Ensure communication between agents
- Monitor critical path
- Generate status reports
- Validate completion criteria

**Key Metrics**:

- All issues on track to Phase 3a deadline
- Zero blocked issues
- Cross-team dependencies met
- Team velocity tracked
- Risk assessment current

---

## 📊 Team Assignments Summary

| Agent          | Phase   | Issues             | Hours        | Status    |
| -------------- | ------- | ------------------ | ------------ | --------- |
| Backend Agent  | 3a      | #87, #89, #91, #92 | 22           | Ready     |
| Frontend Agent | 3a      | #88, #94, #95      | 17           | Ready     |
| DevOps Agent   | 3a      | #89, #96           | 8            | Ready     |
| QA Agent       | 3a      | #95                | 6            | Ready     |
| AI Agent       | 3b/3c   | #90, #93           | 14           | Ready     |
| **Total**      | **All** | **10 issues**      | **61 hours** | **Ready** |

---

## 🔄 Cross-Team Dependencies

```
Backend Agent        Frontend Agent        DevOps Agent
     #87 ────┐              #88 ────┐              #89
     #91 ────┼──────────────────────┼──────────────┼──► Database
     #92 ────┤              #94 ────┤              #96
             │              #95 ────┤
             └──────────────────────┘
                    ↓
                AI Agent
                  #90, #93
```

**Critical Path**:

1. Backend #87 (Server) + #91 (Database) → Foundation
2. Frontend #88 (Deploy) → Live URL
3. Backend #92 (Auth) → Security layer
4. QA #95 (E2E tests) → Quality gates
5. AI #90 (Perplexity) → Intelligence layer

---

## 📅 Weekly Schedule

### Week 1 (Nov 3-9, 2025)

**Focus**: Foundation & Infrastructure

| Agent    | Monday      | Tuesday          | Wednesday   | Thursday      | Friday       |
| -------- | ----------- | ---------------- | ----------- | ------------- | ------------ |
| Backend  | #87 setup   | #87 tests        | #91 schema  | #91 migration | #91 complete |
| Frontend | #88 prep    | #88 deploy       | #88 verify  | #94 start     | #94 progress |
| DevOps   | #89 setup   | #89 Railway      | #89 CORS    | #96 start     | #96 Sentry   |
| QA       | Plan tests  | Setup Playwright | Write tests | #95 progress  | #95 progress |
| AI       | Review APIs | Prompt design    | #90 setup   | #90 progress  | #90 progress |

### Week 2 (Nov 10-16, 2025)

**Focus**: Integration & Testing

| Agent    | Monday            | Tuesday      | Wednesday          | Thursday       | Friday        |
| -------- | ----------------- | ------------ | ------------------ | -------------- | ------------- |
| Backend  | #92 auth          | #92 tokens   | #92 sessions       | #92 testing    | #92 complete  |
| Frontend | #94 profile       | #94 history  | #95 critical flows | #95 test runs  | #95 complete  |
| DevOps   | #96 monitoring    | #96 alerting | #96 dashboards     | Verification   | Verification  |
| QA       | #95 accessibility | #95 mobile   | #95 perf tests     | #95 validation | Release ready |
| AI       | #90 testing       | Integration  | Fallbacks          | Streaming      | #90 complete  |

---

## 🎯 Success Criteria by Phase

### Phase 3a (MVP Launch)

**Target**: Week 1-2, 43 hours

- [ ] Backend server running with 36/36 tests passing
- [ ] Frontend deployed to Vercel (live URL)
- [ ] PostgreSQL database with all tables created
- [ ] JWT authentication working
- [ ] User profile & reading history pages functional
- [ ] E2E test suite passing
- [ ] Error tracking & monitoring active
- [ ] 99.5% uptime SLA met

### Phase 3b (AI Enhancement)

**Target**: Week 2-3, 6 hours

- [ ] Perplexity API integrated
- [ ] All 4 advisor personalities working
- [ ] Response time < 3 seconds
- [ ] Cost tracking implemented

### Phase 3c (Premium)

**Target**: Post-MVP, 8 hours

- [ ] Knowledge base indexed
- [ ] RAG system retrieving context
- [ ] Response grounding improved

---

## 🚀 Getting Started

### Step 1: Environment Setup (All Agents)

```bash
# Clone repo
git clone https://github.com/Thelastlineofcode/Astrology-Synthesis.git
cd Astrology-Synthesis

# Install dependencies
npm install
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
```

### Step 2: Assign Agents to Issues

Each agent should:

1. Review assigned issues
2. Read implementation details
3. Set up local development environment
4. Create feature branch: `git checkout -b feature/issue-{number}`

### Step 3: Weekly Standup

**Time**: Monday 10am UTC  
**Duration**: 30 minutes  
**Attendees**: All agents + Orchestrator

**Agenda**:

- Previous week blockers
- This week priorities
- Cross-team dependencies
- Risk assessment

---

## 📞 Communication Channels

| Channel            | Purpose              | Frequency     |
| ------------------ | -------------------- | ------------- |
| GitHub Issues      | Technical discussion | As needed     |
| PR Reviews         | Code quality         | Per PR        |
| Slack #development | Daily updates        | Daily standup |
| Slack #alerts      | Deployments & errors | Real-time     |
| Weekly Sync        | Status & blockers    | Every Monday  |

---

## 🔒 Security & Access

**API Keys & Secrets**:

- Perplexity API key: Environment variable `PERPLEXITY_API_KEY`
- Database credentials: Railway/Render managed secrets
- Sentry DSN: Environment variables (public & private)
- GitHub tokens: Limited scope, rotated quarterly

**Code Review**:

- Minimum 1 peer review before merge
- All tests must pass
- No secrets in code or logs
- TypeScript strict mode required (Frontend)

---

## 📈 Monitoring & Metrics

### Real-time Dashboards

- GitHub Project board (Phase 3 roadmap)
- Sentry dashboard (errors)
- Vercel analytics (frontend performance)
- Railway dashboard (backend health)
- Uptime.com (99.5% SLA)

### Weekly Reports

- Issue velocity (issues closed/week)
- Test coverage trend
- Performance metrics
- Incident log
- Cost tracking

---

## ⚠️ Risk Management

| Risk                   | Likelihood | Impact | Mitigation                     |
| ---------------------- | ---------- | ------ | ------------------------------ |
| API integration delays | Medium     | High   | Start #90 early, have fallback |
| Database performance   | Low        | High   | Optimize indexes early (#91)   |
| Deployment issues      | Medium     | High   | Test pipeline in staging first |
| E2E test flakiness     | Medium     | Medium | Increase timeout, retry logic  |
| Cost overruns          | Low        | Medium | Use free tier Perplexity       |

---

## ✅ Completion Checklist

- [ ] All agents understand their responsibilities
- [ ] Issues are reviewed and details clear
- [ ] Development environments set up
- [ ] GitHub access verified
- [ ] API keys configured
- [ ] Communication channels active
- [ ] Week 1 standup scheduled
- [ ] Ready to start development!

---

**Last Updated**: November 3, 2025  
**Next Review**: November 10, 2025  
**Status**: ✅ Ready for Phase 3a Launch
