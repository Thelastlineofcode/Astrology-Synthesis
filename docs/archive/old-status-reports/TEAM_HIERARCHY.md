# Mula: The Root - Team Hierarchy & Communication Map

**Date**: November 3, 2025  
**Project**: Mula: The Root (AI Agent Team)

---

## 🏗️ Organizational Structure

```
                        PROJECT GOAL
                  MVP Launch (Phase 3a)
                            |
                            v
                    ORCHESTRATOR AGENT
              (Coordination, Risk Management)
                            |
            ____________________|____________________
           |                   |                    |
           v                   v                    v
      BACKEND TEAM         FRONTEND TEAM        INFRASTRUCTURE TEAM
      (22 hours)           (17 hours)              (8 hours + QA)
           |                   |                    |
      Backend Agent       Frontend Agent        DevOps Agent
      #87, #91, #92       #88, #94, #95        #89, #96
           |                   |                    |
           v                   v                    v
      Services:            Components:          Platforms:
      - FastAPI           - React Pages        - Railway
      - SQLAlchemy        - TypeScript         - Vercel
      - PostgreSQL        - Responsive         - Sentry
      - JWT Auth          - CSS System         - GitHub Actions

                                |
                                v
                          QA AGENT
                   Testing & Quality (6 hours)
                            |
                    Focus: #95 E2E Tests

                                |
                                v
                          AI AGENT
                   LLM Integration (14 hours)
                            |
                    #90: Perplexity API
                    #93: RAG Knowledge Base
```

---

## 🔄 Dependency Graph

```
CRITICAL PATH (Sequential Dependencies):

Week 1:
┌──────────────────────────────────────────────────────┐
│                  Backend #87                         │
│            (Server + Integration Tests)              │
│         Dependency: Python 3.11, FastAPI             │
│         Completion: ~4 hours                         │
└────────────────────┬─────────────────────────────────┘
                     │
                     v
┌──────────────────────────────────────────────────────┐
│                  Backend #91                         │
│        (PostgreSQL Setup & Schema Migration)         │
│      Dependencies: Database, Alembic migrations      │
│        Completion: ~6 hours (needs #87 done first)   │
└────┬─────────────────────────────┬──────────────────┘
     │                             │
     v                             v
┌──────────────────┐    ┌──────────────────────────┐
│  Backend #92     │    │  DevOps #89              │
│ JWT Auth & Users │    │ Deploy Backend to Railway│
│ (Needs #91 DB)   │    │ (Needs #87 server ready) │
│ ~8 hours         │    │ ~4 hours                 │
└──────────────────┘    └──────────────────────────┘
                                 │
                                 v
                        ┌──────────────────┐
                        │ Frontend #88     │
                        │ Deploy to Vercel │
                        │ ~3 hours         │
                        └────────┬─────────┘
                                 │
                                 v
                        ┌──────────────────┐
                        │ Frontend #94     │
                        │ Profile & History│
                        │ ~8 hours         │
                        └────────┬─────────┘
                                 │
                                 v
                        ┌──────────────────┐
                        │ QA #95           │
                        │ E2E Test Suite   │
                        │ ~6 hours         │
                        └──────────────────┘

PARALLEL WORK (Can start simultaneously):
├── DevOps #96 (Monitoring) - 4 hours (independent)
└── AI #90 (Perplexity) - 6 hours (after #87 basic setup)

POST-MVP (Phase 3b/3c):
└── AI #93 (RAG Knowledge Base) - 8 hours (phase 3c)
```

---

## 👥 Agent Communication Map

```
                        ORCHESTRATOR
                    (Issue Tracking Hub)
                      /  |  |  \  \
            _________/   |  |   \  \___________
           /             |  |    \            \
          v              v  v     v            v
     Backend Agent   Frontend   DevOps   QA Agent    AI Agent
         (Main)       Agent     Agent   (Secondary)   (Integration)
          |            |        |           |         |
          |            |        |           |         |
    Owns: #87,91,92   Owns:    Owns:   Owns: #95   Owns: #90,93
           #89(part)  #88,94,95  #89,96

    COMMUNICATION FLOW:
    ─────────────────

    Backend → Frontend:
    "API endpoints ready for integration"
    GitHub PR link
    Expected response format

    Backend → DevOps:
    "Server ready for deployment"
    Environment variables needed
    Database requirements

    Frontend → QA:
    "Pages ready for testing"
    Feature specifications
    Test scenarios

    Backend → AI:
    "Chat endpoints ready"
    Message format specification
    Response integration point

    DevOps → All:
    "Deployment status"
    Environment variables
    Secrets & API keys
    Monitoring dashboard

    Orchestrator → All:
    "Weekly status"
    Blocker resolution
    Risk assessment
    Dependency updates
```

---

## 📊 Timeline Gantt Chart

```
Week 1: NOV 3-9 (Foundation & Infrastructure)

MON 3  TUE 4  WED 5  THU 6  FRI 7  SAT 8  SUN 9
──────────────────────────────────────────────────

Backend #87    [████████████] (4h)           → Done
Backend #91    ░░░░ [████████████████] (6h)  → Done
DevOps #89     [████████████] (4h)           → Done
Frontend #88   ░░░░░░░ [██████████] (3h)     → Done
Frontend #94   ░░░░░░░░░░░░░░░ [████████...] In Progress
QA Plan/Setup  ░░░░░░░░░ [████████████]      In Progress
AI #90 Setup   ░░░░░░░░░░░░ [██████...]      In Progress

Legend:
█ = Active work
░ = Waiting/Planning
... = Continues next week

Week 2: NOV 10-16 (Integration & Testing)

MON 10 TUE 11 WED 12 THU 13 FRI 14 SAT 15 SUN 16
───────────────────────────────────────────────────

Backend #92    [████████████████████] (8h)   → Done
DevOps #96     [████████████] (4h)           → Done
Frontend #94   [████████████████████] (8h)   → Done
QA #95         [████████████████████] (6h)   → Done
AI #90         [████████████] (6h)           → Done
Integration    [████████████████]             → Testing
Deployment     [████████████]                 → Production

Status:
✅ Phase 3a (MVP) - Complete
🔄 Phase 3b (AI) - Starting
```

---

## 🎯 Decision Matrix

**Who decides what?**

| Decision              | Owner        | Approves     | Input From                  |
| --------------------- | ------------ | ------------ | --------------------------- |
| Database schema       | Backend      | Orchestrator | DevOps                      |
| API design            | Backend      | Frontend     | QA                          |
| UI/UX design          | Frontend     | QA           | Backend (API compatibility) |
| Deployment strategy   | DevOps       | Orchestrator | Backend, Frontend           |
| Test strategy         | QA           | Orchestrator | Backend, Frontend           |
| Prompt design         | AI           | Orchestrator | QA (quality testing)        |
| Critical path changes | Orchestrator | -            | All agents                  |
| Risk escalation       | Orchestrator | -            | Any agent                   |

---

## 📈 Escalation Path

```
ISSUE SEVERITY ESCALATION:

BLOCKER (Blocks 2+ issues)
        ↓
    ESCALATE TO: Orchestrator
    Response Time: 1 hour
    Action: Re-prioritize, find workaround

HIGH PRIORITY (Impacts 1 issue)
        ↓
    ESCALATE TO: Relevant agent leads
    Response Time: 2-4 hours
    Action: Direct assistance or pair programming

MEDIUM PRIORITY (Technical question)
        ↓
    ESCALATE TO: Domain expert
    Response Time: 1 day
    Action: Code review, guidance

LOW PRIORITY (Enhancement, discussion)
        ↓
    GitHub Issue Discussion
    Response Time: 1-2 days
    Action: Async feedback
```

---

## 🔐 Access & Permissions

```
REPOSITORY ACCESS:
├── All Agents: Write access to master
├── Backend Agent: Direct access to /backend folder
├── Frontend Agent: Direct access to /frontend folder
├── DevOps Agent: Full repo access (handles CI/CD)
├── QA Agent: Read access + test folder write
└── AI Agent: Access to /backend/services

INFRASTRUCTURE ACCESS:
├── Backend Agent: Railway database access (read-only)
├── DevOps Agent: Full Railway, Vercel, Sentry access
├── Frontend Agent: Vercel project access
├── QA Agent: Monitoring dashboards (read-only)
└── AI Agent: Perplexity API key (env variable)

GITHUB SETTINGS:
├── Branch protection: Requires 1 review for master
├── Required status checks: Tests must pass
├── Auto-merge: Enabled for dependabot
├── Code owners: @backend-agent, @frontend-agent, etc.
└── Issue templates: Filled for each agent
```

---

## 💬 Meeting Schedule

```
WEEKLY SYNC
Time: Monday 10am UTC
Duration: 30 minutes
Attendees: All agents + Orchestrator
Format: Standing meeting

AGENDA:
1. Previous week blockers (5 min)
   - Did we resolve last week's issues?
   - Any follow-ups needed?

2. This week priorities (10 min)
   - What's starting?
   - What's the critical path?
   - Any risks?

3. Cross-team dependencies (10 min)
   - What do you need from others?
   - What can you unblock?
   - Timeline impacts?

4. Action items (5 min)
   - Decisions made
   - Who owns what
   - Next sync

AD-HOC MEETINGS:
├── Blocker resolution: ASAP (1 hour response)
├── Code review pairing: As needed
├── Technical deep-dive: Wednesday if needed
└── Post-incident review: If issues occur
```

---

## 🚨 Crisis Management

**If Critical Issue Found**:

```
1. DETECT
   Agent discovers issue
   ↓
2. REPORT
   Post in GitHub issue immediately
   Tag Orchestrator and relevant agents
   ↓
3. ASSESS
   Orchestrator evaluates severity
   Can it wait until tomorrow? Or blocker?
   ↓
4. RESPOND
   If blocker:
   - All hands on deck
   - Pair programming if needed
   - Skip next lower-priority task

   If high-priority:
   - Focused team response
   - May delay other work

   If medium/low:
   - Schedule response
   - No disruption to roadmap
   ↓
5. RESOLVE
   Agent fixes with support
   ↓
6. DOCUMENT
   Post-mortem added to GitHub
   Lessons learned recorded
```

---

## 📋 Checklist: Team Ready to Launch

- [ ] All 5 agents understand their role
- [ ] GitHub issues reviewed by each agent
- [ ] Development environments set up
- [ ] API keys/credentials configured
- [ ] Repository access verified
- [ ] Communication channels active
- [ ] First standup scheduled
- [ ] Week 1 priorities confirmed
- [ ] Blocker resolution process understood
- [ ] Definition of Done criteria clear
- [ ] Deployment process understood
- [ ] Testing strategy aligned
- [ ] Monitoring dashboards ready
- [ ] Escalation path documented
- [ ] Ready to launch! 🚀

---

## 🎉 Phase 3a Success Criteria

**LAUNCH IS SUCCESSFUL WHEN**:

```
✅ Backend Agent:
   - 36/36 tests passing
   - API endpoints responding
   - Database schema complete
   - Authentication working

✅ Frontend Agent:
   - Deployed to Vercel (live URL)
   - TypeScript: 0 errors
   - Lighthouse > 80
   - Responsive design verified

✅ DevOps Agent:
   - Backend deployed to Railway
   - Monitoring active (Sentry)
   - 99.5% uptime metric met
   - Auto-deploy working

✅ QA Agent:
   - E2E test suite passing
   - Accessibility audit: PASS
   - Performance benchmarks met
   - Release sign-off given

✅ AI Agent:
   - Perplexity API integrated
   - 4 advisor personalities live
   - Response quality validated
   - Cost tracking active

✅ PROJECT:
   - All 10 issues closed
   - 61 hours of work complete
   - MVP ready for users
   - Phase 3b ready to start
```

---

**Document Version**: 1.0  
**Last Updated**: November 3, 2025  
**Team Status**: ✅ Ready to Launch
