# Mula: The Root - AI Agent Quick Reference

**Date**: November 3, 2025  
**For**: All AI Agents  
**Purpose**: Quick lookup for roles, responsibilities, and getting started

---

## 🎯 Your Role in 30 Seconds

### Backend Agent

**What**: FastAPI server, database, APIs  
**Where**: `/backend`  
**Time**: 22 hours  
**Issues**: #87, #89, #91, #92  
**Start**: Issue #87

### Frontend Agent

**What**: Next.js app, React components, UI  
**Where**: `/frontend`  
**Time**: 17 hours  
**Issues**: #88, #94, #95  
**Start**: Issue #88

### DevOps Agent

**What**: Deployments, monitoring, infrastructure  
**Where**: Railway, Render, Vercel, Sentry  
**Time**: 8 hours  
**Issues**: #89, #96  
**Start**: Issue #89

### QA Agent

**What**: E2E tests, accessibility, performance  
**Where**: `/frontend/e2e`, `/tests`  
**Time**: 6 hours  
**Issues**: #95  
**Start**: Issue #95

### AI Agent

**What**: Perplexity API, prompt engineering, RAG  
**Where**: `/backend/services`  
**Time**: 14 hours  
**Issues**: #90, #93  
**Start**: Issue #90

---

## ⚡ Quick Start (5 minutes)

### 1. Clone Repository

```bash
git clone https://github.com/Thelastlineofcode/Astrology-Synthesis.git
cd Astrology-Synthesis
```

### 2. Install Dependencies

**Backend Agent**:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend Agent**:

```bash
cd frontend
npm install
npm run build
```

**DevOps Agent**:

```bash
# Account setup for Railway/Render/Vercel
# (Already have accounts? Check your email for invites)
```

**QA Agent**:

```bash
cd frontend
npm install
npx playwright install
```

**AI Agent**:

```bash
cd backend
pip install -r requirements.txt
# Set environment variable: PERPLEXITY_API_KEY=your-key
```

### 3. Verify Setup

```bash
# Backend Agent
cd backend && python main.py  # Should start on http://localhost:8000

# Frontend Agent
cd frontend && npm run dev  # Should start on http://localhost:3000

# QA Agent
cd frontend && npx playwright test  # Should find test files

# AI Agent
cd backend && python  # Test: import httpx
```

### 4. Read Your Issue

- Open GitHub issue assigned to you
- Read full acceptance criteria
- Review implementation checklist
- Check dependencies & blockers

### 5. Create Feature Branch

```bash
git checkout -b feature/issue-{number}
# Example: git checkout -b feature/issue-87
```

---

## 📁 Project Structure

```
Astrology-Synthesis/
├── backend/                          # Backend Agent HQ
│   ├── main.py                      # FastAPI entry point
│   ├── api/v1/                      # REST endpoints
│   ├── models/                      # SQLAlchemy ORM
│   ├── schemas/                     # Pydantic models
│   ├── services/                    # Business logic
│   ├── config/                      # Settings & configs
│   ├── tests/                       # pytest tests
│   ├── requirements.txt             # Python dependencies
│   └── database/                    # SQL schemas
│
├── frontend/                         # Frontend Agent HQ
│   ├── src/app/                     # Next.js pages
│   ├── src/components/              # React components
│   ├── src/styles/                  # CSS & Design System
│   ├── e2e/                         # Playwright tests (QA)
│   ├── package.json                 # Dependencies
│   ├── tsconfig.json                # TypeScript config
│   └── next.config.js               # Next.js config
│
├── docs/                            # Documentation
│   ├── ARCHITECTURE_ROLES.md        # Your role details
│   ├── AI_AGENT_TEAM.md             # Team structure
│   └── TEAM_STRUCTURE.md            # Team organization
│
└── README.md                        # Project overview
```

---

## 🔑 Key Commands by Role

### Backend Agent

```bash
# Run server
cd backend && uvicorn main:app --reload

# Run tests
cd backend && pytest tests/ -v

# Check database
cd backend && python
>>> from backend.config.database import SessionLocal
>>> db = SessionLocal()
>>> db.execute("SELECT * FROM users").fetchall()
```

### Frontend Agent

```bash
# Run dev server
cd frontend && npm run dev

# Build for production
cd frontend && npm run build

# Check TypeScript errors
cd frontend && npm run tsc

# Run linter
cd frontend && npm run lint
```

### DevOps Agent

```bash
# Login to Railway
railway login

# Deploy
railway up

# Check logs
railway logs

# View environment variables
railway env
```

### QA Agent

```bash
# Run all E2E tests
cd frontend && npx playwright test

# Run in headed mode (see browser)
cd frontend && npx playwright test --headed

# Run specific test
cd frontend && npx playwright test critical-flows.spec.ts

# Generate HTML report
cd frontend && npx playwright show-report
```

### AI Agent

```bash
# Test Perplexity API
cd backend && python
>>> import httpx
>>> # Test Perplexity connection
```

---

## 📊 Issue Breakdown by Agent

### Backend Agent - 22 hours

| Issue | Title                  | Hours | Priority | Status |
| ----- | ---------------------- | ----- | -------- | ------ |
| #87   | Backend Server & Tests | 4     | P0       | Ready  |
| #89   | Deploy Backend         | 4     | P0       | Ready  |
| #91   | PostgreSQL Setup       | 6     | P1       | Ready  |
| #92   | JWT Authentication     | 8     | P1       | Ready  |

### Frontend Agent - 17 hours

| Issue | Title             | Hours | Priority | Status |
| ----- | ----------------- | ----- | -------- | ------ |
| #88   | Deploy Frontend   | 3     | P0       | Ready  |
| #94   | Profile & History | 8     | P1       | Ready  |
| #95   | E2E Test Suite    | 6     | P0       | Ready  |

### DevOps Agent - 8 hours

| Issue | Title          | Hours | Priority | Status |
| ----- | -------------- | ----- | -------- | ------ |
| #89   | Deploy Backend | 4     | P0       | Ready  |
| #96   | Monitoring     | 4     | P1       | Ready  |

### QA Agent - 6 hours

| Issue | Title          | Hours | Priority | Status |
| ----- | -------------- | ----- | -------- | ------ |
| #95   | E2E Test Suite | 6     | P0       | Ready  |

### AI Agent - 14 hours

| Issue | Title              | Hours | Priority | Status |
| ----- | ------------------ | ----- | -------- | ------ |
| #90   | Perplexity API     | 6     | P1       | Ready  |
| #93   | RAG Knowledge Base | 8     | P2       | Ready  |

---

## 🚀 Critical Path (Start Order)

```
Week 1:
┌─→ Backend #87 (Server tests)
│   ↓
│   Backend #91 (Database)
│   ↓
│   Backend #92 (Auth)
│
├─→ Frontend #88 (Deploy to Vercel)
│   ↓
│   Frontend #94 (Profile pages)
│   ↓
│   Frontend #95 (E2E tests)
│
└─→ DevOps #89 (Deploy to Railway)
    ↓
    DevOps #96 (Monitoring)

Week 2:
AI #90 (Perplexity API)
QA #95 (Test validation)
```

**Must Start First**: #87, #88, #89, #91  
**Can Start in Parallel**: #96, #90  
**Depends on Others**: #92 (needs #91), #94 (needs #88)

---

## 📞 Need Help?

### GitHub

- Post in issue comments
- Tag relevant agents
- Link related issues

### Questions by Type

| Question                       | Ask                             |
| ------------------------------ | ------------------------------- |
| "How should I structure this?" | Your domain expert              |
| "My code depends on issue #X"  | Orchestrator or dependent agent |
| "Is this a blocker?"           | Orchestrator                    |
| "How do I deploy this?"        | DevOps Agent                    |
| "Does this pass tests?"        | QA Agent                        |

### Response Times

- Blocker: 1 hour
- Urgent: 4 hours
- Normal: 1 day

---

## ✅ Checklist Before Starting

- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] Local environment working
- [ ] Created feature branch
- [ ] Read your GitHub issue(s)
- [ ] Understand acceptance criteria
- [ ] Know your blockers/dependencies
- [ ] Ready to code!

---

## 📈 Weekly Check-in

**Every Monday at 10am UTC**:

- What did I complete last week?
- What am I starting this week?
- Any blockers?
- Any risks?

---

## 🎯 Success = Definition of Done Met

**Your issue is DONE when**:

- ✅ All acceptance criteria met
- ✅ All tests passing
- ✅ Code reviewed & approved
- ✅ Documentation updated
- ✅ Merged to master
- ✅ Deployed (if applicable)
- ✅ No high-severity bugs
- ✅ Performance targets met

---

## 🔗 Important Links

**Repository**: https://github.com/Thelastlineofcode/Astrology-Synthesis  
**Issues**: https://github.com/Thelastlineofcode/Astrology-Synthesis/issues  
**Discussions**: Use GitHub issue comments

**Documentation**:

- ARCHITECTURE_ROLES.md - Full role details
- AI_AGENT_TEAM.md - Team structure & guidelines
- TEAM_STRUCTURE.md - Weekly schedule & syncs
- README.md - Project overview

---

## 💡 Pro Tips

1. **Start Early**: Pick your first issue, understand it completely
2. **Test Often**: Run tests before committing
3. **Communicate**: Ask questions early, don't get stuck
4. **Document**: Update docs as you learn new things
5. **Review**: Check others' code, learn from each other
6. **Deploy Early**: Get feedback from real environment
7. **Monitor**: Watch for errors in production
8. **Celebrate**: Celebrate wins with the team!

---

## 📝 Your First Actions

1. Read this quick reference (5 min)
2. Clone the repository (2 min)
3. Install dependencies (10 min)
4. Verify setup works (5 min)
5. Read your GitHub issue (15 min)
6. Create feature branch (1 min)
7. Start coding! 🚀

**Total: ~40 minutes to your first commit**

---

**Last Updated**: November 3, 2025  
**Status**: ✅ Ready to Go!  
**Questions?**: Check GitHub issue or ask in comments
