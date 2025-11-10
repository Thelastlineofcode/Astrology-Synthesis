# HYBRID MVP BUILD - ROLES & TODOS ASSIGNMENT

## Team Coordination & Individual Accountability

**Date**: November 4, 2025  
**Status**: READY FOR TEAM ASSIGNMENT  
**Target Launch**: November 8 (Sprint Kickoff)

---

## TEAM STRUCTURE

### Core Team (Required Full-Time)

| Role                | Person | Availability                           | Start Date | Key Responsibilities                         |
| ------------------- | ------ | -------------------------------------- | ---------- | -------------------------------------------- |
| **Founder/Product** | [Name] | Full 8 weeks                           | Nov 4      | Strategy, decisions, fundraising prep        |
| **Backend Lead**    | [Name] | Full 8 weeks                           | Nov 8      | API design, database, integrations           |
| **Frontend Lead**   | [Name] | Full 8 weeks                           | Nov 8      | UI/UX, web apps, PWA setup                   |
| **DevOps Lead**     | [Name] | Full-time (Weeks 1-4), Part-time (5-8) | Nov 5      | CI/CD, deployment, infrastructure            |
| **QA Lead**         | [Name] | Full 8 weeks                           | Nov 8      | Testing, quality, launch readiness           |
| **Growth Lead**     | [Name] | Part-time (Weeks 1-2), Full (2-8)      | Nov 15     | Marketing, viral mechanics, user acquisition |

### Support Team (Optional)

| Role                 | Hours/Week | Key Responsibilities               |
| -------------------- | ---------- | ---------------------------------- |
| Support Engineer     | 20 hrs     | Customer support, bug triage       |
| Designer (Part-time) | 20 hrs     | UI improvements, brand consistency |
| Data Analyst         | 10 hrs     | Metrics tracking, analytics setup  |

---

## FOUNDER/PRODUCT LEAD - [NAME]

### Pre-Launch Tasks (Nov 4-7)

- [ ] **PRIORITY 1**: Approve hybrid strategy vs alternatives
  - [ ] Read `HYBRID_MVP_STRATEGY.md` (30 min)
  - [ ] Review financial projections
  - [ ] Make final go/no-go decision
  - [ ] Document in Slack thread
- [ ] **PRIORITY 2**: Confirm team availability
  - [ ] Get confirmation from each lead
  - [ ] Verify nobody has conflicts
  - [ ] Schedule kickoff meeting
- [ ] **PRIORITY 3**: Allocate budget
  - [ ] Review $40-50K breakdown
  - [ ] Get finance approval
  - [ ] Set up accounting tracking
- [ ] **PRIORITY 4**: Prepare for launch
  - [ ] Set up communication channels
  - [ ] Create Slack workspace (if needed)
  - [ ] Invite all team members

### Week 1-8: Ongoing Leadership

- [ ] Daily standup (9:30 AM, 15 min)
- [ ] Weekly sprint review (Friday 4 PM, 1 hour)
- [ ] Bi-weekly retro (2 hours)
- [ ] Unblock team as needed
- [ ] Make go/no-go decisions per week

### Week 1 Specific Tasks

- [ ] Day 1 (Nov 8): Team kickoff meeting (1 hour)
  - [ ] Review strategy with entire team
  - [ ] Answer questions
  - [ ] Clarify priorities
- [ ] Day 1-5: Available for quick decisions
  - [ ] Review/approve tech decisions
  - [ ] Sign off on architecture
  - [ ] Clarify product questions
- [ ] Week 1 end: Review metrics and go/no-go

### Financial & Reporting

- [ ] Prepare investor update (weekly)
- [ ] Track burn rate vs budget
- [ ] Prepare Series A deck materials by Week 8

---

## BACKEND LEAD - [NAME]

### Pre-Launch Tasks (Nov 5-7)

**GitHub & Repos** (6 hours)

- [ ] GitHub organization setup
- [ ] Create repos:
  - [ ] `mula-dasha-timer-backend`
  - [ ] `mula-compatibility-backend` (or shared if combined)
  - [ ] `mula-backend-unified` (for Week 3+)
- [ ] Add CI/CD templates (GitHub Actions)
- [ ] Setup branch protection rules
- [ ] Create development guidelines doc

**Database Planning** (4 hours)

- [ ] Review `HYBRID_BUILD_WEEK1_DASHA_TIMER.md` database schema
- [ ] Review `HYBRID_BUILD_WEEK2_COMPATIBILITY.md` database schema
- [ ] Plan PostgreSQL instances (separate Week 1-2, unified Week 3+)
- [ ] Create database migration plan
- [ ] Document schema versions

**Architecture Design** (6 hours)

- [ ] Review API specifications from Week 1 spec
- [ ] Design FastAPI project structure
- [ ] Plan authentication flow (JWT, OAuth)
- [ ] List all external integrations needed
- [ ] Create architecture diagram

**Local Development Setup** (4 hours)

- [ ] Create Docker Compose for local dev
- [ ] Create requirements.txt with all dependencies
- [ ] Create .env.example for team
- [ ] Write setup guide for developers
- [ ] Test setup with one developer

### Week 1: Dasha Timer Backend (80 hours)

**Day 1-2: Setup & Foundation** (16 hours)

- [ ] FastAPI project scaffold
- [ ] Database schema creation (users, birth_charts, dasha_data, etc.)
- [ ] Database migrations setup (Alembic)
- [ ] Create User model + repository pattern
- [ ] Setup logging and error handling
- [ ] Create base API response format

**Day 2-3: Authentication** (16 hours)

- [ ] JWT token generation/validation
- [ ] Google OAuth integration
- [ ] Apple Sign-In integration
- [ ] User registration endpoint (POST /auth/signup)
- [ ] User login endpoint (POST /auth/login)
- [ ] OAuth callback handlers
- [ ] Auth middleware
- [ ] Unit tests for auth

**Day 3-4: Birth Chart & Dasha** (16 hours)

- [ ] Database schema for birth_charts table
- [ ] POST /chart/create endpoint:
  - [ ] Validate input data
  - [ ] Call existing Mula dasha engine
  - [ ] Store chart in database
- [ ] GET /dasha/current endpoint (with caching)
- [ ] GET /dasha/meanings endpoint
- [ ] Database queries optimized
- [ ] Unit tests

**Day 4-5: Notifications Infrastructure** (16 hours)

- [ ] Firebase Cloud Messaging setup
- [ ] FCM tokens table + POST /notification/register
- [ ] SendGrid email setup
- [ ] Email template system
- [ ] APScheduler setup for daily jobs
- [ ] Daily dasha change notification job
- [ ] Email sending service
- [ ] Unit tests

**Day 5-6: API Refinement** (10 hours)

- [ ] Implement caching (Redis) for dasha calculations
- [ ] Rate limiting middleware
- [ ] CORS configuration
- [ ] Input validation everywhere
- [ ] Error handling standardization

**Day 7-8: Testing** (8 hours)

- [ ] Unit test coverage (80%+)
- [ ] Integration tests (signup → dasha flow)
- [ ] Load testing (simulate 500+ users)
- [ ] Security audit (JWT, CORS, injection attacks)

**Day 9-10: Deployment Prep** (2 hours)

- [ ] Railway setup
- [ ] Environment variables created
- [ ] Database migrations tested in staging
- [ ] Health check endpoint ready
- [ ] Monitoring configured (Sentry)

### Week 2: Compatibility Backend (64 hours)

**Day 1: Algorithm Design** (8 hours)

- [ ] Design compatibility scoring algorithm
- [ ] Venus compatibility logic (romance)
- [ ] Mars compatibility logic (passion)
- [ ] Moon compatibility logic (emotion)
- [ ] Sun compatibility logic (personality)
- [ ] Documentation

**Day 1-2: API Endpoints** (16 hours)

- [ ] POST /compatibility/calculate:
  - [ ] Accepts two birth charts
  - [ ] Calls algorithm
  - [ ] Returns score + breakdowns
  - [ ] Stores result in database
- [ ] GET /compatibility/results (user's history)
- [ ] GET /compatibility/results/{id} (single result)
- [ ] POST /compatibility/share (generate share code)

**Day 2-3: Monetization Integration** (16 hours)

- [ ] Stripe integration for premium reports
- [ ] POST /compatibility/report/purchase:
  - [ ] Create Stripe checkout session
  - [ ] Handle webhook for payment
  - [ ] Generate detailed report
  - [ ] Email report to user
- [ ] GET /compatibility/report/{id} (retrieve paid report)

**Day 3-4: Analytics & Sharing** (16 hours)

- [ ] Referral tracking database table
- [ ] POST /share/track endpoint (track shares)
- [ ] GET /share/stats endpoint (sharing metrics)
- [ ] Email invite system
- [ ] Social share tracking

**Day 4-5: Testing & QA** (8 hours)

- [ ] Unit tests (80%+)
- [ ] Integration tests
- [ ] Stripe payment testing (sandbox)
- [ ] Performance optimization

### Week 3-4: Migration & Unified Backend (80 hours)

- See MIGRATION_STRATEGY section below

### Week 5-8: New Features Backend

- See schedule in timeline

### Ongoing Throughout

- [ ] Daily standup (9:30 AM, 15 min)
- [ ] Code reviews for all PRs
- [ ] Weekly technical sync (with frontend lead)
- [ ] Performance optimization

---

## FRONTEND LEAD - [NAME]

### Pre-Launch Tasks (Nov 5-7)

**GitHub & Repos** (4 hours)

- [ ] Create `mula-dasha-timer` repo
- [ ] Create `mula-compatibility` repo
- [ ] Create `mula-web-unified` (for Week 3+)
- [ ] Setup GitHub Actions CI for frontend
- [ ] Create component library setup

**Design & Mockups** (8 hours)

- [ ] Review design system (Tailwind, Shadcn/ui)
- [ ] Create mockups for Dasha Timer:
  - [ ] Landing page
  - [ ] Login page
  - [ ] Birth chart form
  - [ ] Dashboard with timer
  - [ ] Settings page
- [ ] Review with product lead
- [ ] Document color scheme, typography

**Local Development** (4 hours)

- [ ] Create Next.js starter template
- [ ] Setup Tailwind + Shadcn/ui
- [ ] Create component folder structure
- [ ] Setup ESLint + Prettier
- [ ] Create .env.example
- [ ] Write development guide

### Week 1: Dasha Timer Frontend (80 hours)

**Day 1-2: Setup & Layout** (16 hours)

- [ ] Next.js project initialized
- [ ] Tailwind CSS configured
- [ ] Shadcn/ui setup
- [ ] Global layout component
- [ ] Navigation/header component
- [ ] Footer component
- [ ] Dark mode support

**Day 2-3: Auth Pages** (16 hours)

- [ ] Landing page design
- [ ] Login page component
- [ ] Signup page component
- [ ] OAuth login buttons (Google, Apple)
- [ ] Form validation
- [ ] Error messaging
- [ ] Success/redirect handling

**Day 3-4: Birth Chart Form** (16 hours)

- [ ] BirthChartForm component
- [ ] DateInput sub-component
- [ ] TimeInput sub-component (time zone aware)
- [ ] LocationPicker component (with map)
- [ ] Form validation
- [ ] Styling complete
- [ ] Mobile responsiveness

**Day 4-5: Dashboard & Timer** (16 hours)

- [ ] DashaTimer component (countdown visual)
- [ ] DashaInfo component (meanings + traits)
- [ ] Dashboard layout
- [ ] API integration (React Query)
- [ ] Real-time updates (WebSocket if needed)
- [ ] Dark mode verification

**Day 5-6: Settings & Notifications** (10 hours)

- [ ] NotificationSettings component
- [ ] FCM permission request UI
- [ ] Email preferences form
- [ ] Settings page layout
- [ ] Data persistence

**Day 7-8: Polish & Testing** (8 hours)

- [ ] Mobile responsiveness audit
- [ ] Lighthouse testing (>85 score)
- [ ] Component story tests
- [ ] User journey testing
- [ ] Accessibility audit (WCAG AA)

**Day 9-10: Deployment Prep** (2 hours)

- [ ] Vercel setup
- [ ] Environment variables
- [ ] Auto-deploy configuration
- [ ] Preview deployments enabled

### Week 2: Compatibility Frontend (64 hours)

**Day 1-2: Design & Components** (16 hours)

- [ ] DualChartInput component
- [ ] CompatibilityScore visualization (0-100)
- [ ] DetailedBreakdown component
  - [ ] Venus breakdown
  - [ ] Mars breakdown
  - [ ] Moon breakdown
  - [ ] Sun breakdown
- [ ] ShareCard component (for social)

**Day 2-3: Main Calculator** (16 hours)

- [ ] /calculator page layout
- [ ] Two-chart input flow
- [ ] Results page display
- [ ] API integration
- [ ] Loading states
- [ ] Error handling

**Day 3-4: Social Sharing** (16 hours)

- [ ] ShareCard component
- [ ] Twitter share button + integration
- [ ] WhatsApp share button + integration
- [ ] Email invite form
- [ ] Shared link page (/share/{code})
- [ ] Share preview metadata (OG tags)

**Day 4-5: Premium & Upgrade** (8 hours)

- [ ] ReportUpgrade component (CTA)
- [ ] Premium report purchase flow
- [ ] Checkout integration with backend
- [ ] Success page
- [ ] Report download/email

**Day 5: Testing & Polish** (8 hours)

- [ ] Mobile testing
- [ ] Social share testing
- [ ] Lighthouse audit
- [ ] Accessibility check

### Week 3-4: Web Unification (64 hours)

- See unified frontend section below

### Ongoing Throughout

- [ ] Daily standup (9:30 AM, 15 min)
- [ ] Code reviews for all PRs
- [ ] Component library maintenance
- [ ] Accessibility compliance

---

## DEVOPS LEAD - [NAME]

### Pre-Launch Tasks (Nov 5-7)

**Infrastructure Provisioning** (12 hours)

- [ ] GitHub organization setup + team permissions
- [ ] Vercel account + projects:
  - [ ] `mula-dasha-timer` (production domain)
  - [ ] `mula-compatibility` (production domain)
  - [ ] `mula-web-unified` (for Week 3+)
- [ ] Railway account + projects:
  - [ ] `mula-dasha-timer-backend`
  - [ ] `mula-compatibility-backend`
  - [ ] PostgreSQL instance (Week 1)
- [ ] Database setup:
  - [ ] PostgreSQL databases created
  - [ ] Backups configured
  - [ ] Connection strings generated
- [ ] Email & Third-party:
  - [ ] SendGrid account setup
  - [ ] Firebase project created
  - [ ] Sentry project created
  - [ ] Plausible analytics account

**CI/CD Setup** (8 hours)

- [ ] GitHub Actions workflows:
  - [ ] Frontend: Build + Deploy (on main push)
  - [ ] Backend: Test + Deploy (on main push)
- [ ] Staging environment setup
- [ ] Production environment setup
- [ ] Preview deployments for PRs

**Monitoring & Observability** (6 hours)

- [ ] Sentry project integration (backend)
- [ ] Plausible analytics setup (frontend)
- [ ] CloudWatch/Monitoring dashboards
- [ ] Alert rules configured

**Documentation** (4 hours)

- [ ] DevOps runbook created
- [ ] Deployment procedures documented
- [ ] Rollback procedures documented
- [ ] Incident response plan

### Week 1: Deployment & Operations (40 hours)

**Day 1-2: Infrastructure Monitoring** (8 hours)

- [ ] Setup health checks
- [ ] Database monitoring
- [ ] API response time monitoring
- [ ] Error rate alerts
- [ ] Daily log reviews

**Day 5-10: Staging & Production Deploy** (16 hours)

- [ ] Staging environment testing
- [ ] Database migrations in staging
- [ ] Load testing (500+ concurrent)
- [ ] Production deployment
- [ ] Post-deployment verification
- [ ] Monitoring active

**Day 10: Ongoing Operations** (16 hours)

- [ ] Monitor for production issues
- [ ] Review error logs daily
- [ ] Database backups verified
- [ ] Performance optimization notes

### Week 2-8: Ongoing DevOps (20 hours/week)

- [ ] Maintain infrastructure
- [ ] Update monitoring
- [ ] Backup verification
- [ ] Performance optimization
- [ ] New feature deployments

### Critical Responsibilities

- [ ] 99.9% uptime target
- [ ] <300ms p95 API latency
- [ ] Zero data loss (backups + redundancy)
- [ ] Security patches applied immediately
- [ ] On-call for production issues

---

## QA LEAD - [NAME]

### Pre-Launch Tasks (Nov 4-7)

**Test Plan & Strategy** (6 hours)

- [ ] Review test requirements from specs
- [ ] Create test plan document
- [ ] Setup test environment
- [ ] Create test case templates

**Tools Setup** (4 hours)

- [ ] GitHub issue templates for bugs
- [ ] Test tracking (Jira/Linear setup)
- [ ] Screenshot/video recording tools
- [ ] Device lab setup (for mobile testing)

### Week 1: Dasha Timer Testing (40 hours)

**Day 1-2: Setup** (8 hours)

- [ ] Test environment accessible
- [ ] Staging databases setup
- [ ] Test user data prepared
- [ ] Test frameworks ready

**Day 3-5: Functional Testing** (16 hours)

- [ ] Auth flow testing:
  - [ ] Email signup
  - [ ] Email login
  - [ ] Google OAuth
  - [ ] Apple Sign-In
  - [ ] Logout
- [ ] Birth chart form testing:
  - [ ] Valid data
  - [ ] Invalid data handling
  - [ ] Mobile input
  - [ ] Timezone handling
- [ ] Dasha calculation:
  - [ ] Accuracy verification
  - [ ] Edge cases (midnight, leap year, etc.)
  - [ ] Caching working

**Day 6-7: E2E Testing** (8 hours)

- [ ] Full user journey (signup → dashboard → settings)
- [ ] Cross-browser testing (Chrome, Safari, Firefox)
- [ ] Mobile responsiveness testing
- [ ] PWA functionality testing

**Day 8-9: Load & Performance Testing** (8 hours)

- [ ] Load test (500 concurrent users)
- [ ] Response time checks (<500ms p95)
- [ ] Database query performance
- [ ] Caching effectiveness

### Week 1 End: Go/No-Go Decision

- [ ] <2 critical bugs remaining
- [ ] All P1 features tested
- [ ] Performance acceptable
- [ ] Go/no-go recommendation to founder

### Week 2: Compatibility Testing (32 hours)

- Similar testing cycle for Compatibility app
- Focus on viral/sharing mechanics
- Referral tracking verification
- Payment flow testing (Stripe sandbox)

### Week 3-8: Continuous Testing

- [ ] UAT with beta users
- [ ] Regression testing post-deployments
- [ ] Performance monitoring
- [ ] User feedback tracking

### Critical Metrics Tracked

- [ ] Bug count by severity
- [ ] Test coverage %
- [ ] Time to fix (TTF)
- [ ] Uptime %
- [ ] Performance metrics

---

## GROWTH LEAD - [NAME]

### Pre-Launch Tasks (Nov 4-7)

**Marketing Strategy** (8 hours)

- [ ] Define Week 1 acquisition strategy
- [ ] Review Compatibility viral mechanics from spec
- [ ] Create launch messaging
- [ ] Identify initial user segments
- [ ] Plan Week 2 campaign

**Asset Creation** (12 hours)

- [ ] Landing page copy
- [ ] Social media templates
- [ ] Email templates (welcome, nurture)
- [ ] Presentation deck for beta users
- [ ] Referral program documentation

### Week 1: Awareness & Beta Signup (40 hours)

**Product Launch Prep** (16 hours)

- [ ] Create launch email (to existing Mula audience)
- [ ] Social media announcement posts
- [ ] Beta user onboarding sequence
- [ ] FAQ preparation

**Day 1-10: Beta Recruitment** (24 hours)

- [ ] Announce to existing users
- [ ] Recruit 100+ beta testers
- [ ] Setup beta tester communication channel
- [ ] Gather early feedback
- [ ] Create feedback forms

### Week 2: Viral Mechanics & Growth (40 hours)

**Day 1-3: Pre-Launch Campaign** (16 hours)

- [ ] Create Compatibility launch announcement
- [ ] Design shareable cards
- [ ] Setup email invite system
- [ ] Prepare social content calendar

**Day 4-10: Launch & Growth** (24 hours)

- [ ] Track signup velocity
- [ ] Monitor share rate
- [ ] Track referral conversions
- [ ] Analyze viral coefficient (target: 1.5-2.0)
- [ ] Optimize messaging based on early data
- [ ] Recruit influencers for social proof

**Key Metrics to Track**

- [ ] Signups/day
- [ ] Share rate (% who share)
- [ ] Referral conversions
- [ ] Email open rate
- [ ] Click-through rate
- [ ] Cost per acquisition (CPA)

### Week 3-8: Ongoing Growth

- [ ] Paid ads (if needed)
- [ ] Partnership outreach
- [ ] PR/Media coverage
- [ ] Community building
- [ ] Retention optimization

### Critical Success Metrics

- [ ] Week 1: 500+ signups (Dasha Timer)
- [ ] Week 2: 2000+ signups (Compatibility)
- [ ] Week 2: $300-500 MRR
- [ ] Week 8: 10,000+ total users
- [ ] Week 8: $5K-9K MRR

---

## SHARED RESPONSIBILITIES

### Daily Standup (9:30 AM, 15 min)

**Attendees**: All team members  
**Format**: Each person answers 3 questions

1. What did I complete yesterday?
2. What am I working on today?
3. What blockers do I have?

**Facilitator**: Product Lead

### Weekly Sprint Review (Friday 4 PM, 1 hour)

**Attendees**: All team members + founder  
**Agenda**:

1. Demo completed features (15 min)
2. Metrics review (10 min)
3. Blockers discussion (15 min)
4. Next week preview (10 min)
5. Go/no-go decision (10 min)

### Bi-Weekly Retro (Every 2 weeks, 2 hours)

**Attendees**: All team members  
**Format**: What went well / What didn't / What to improve

### GitHub Collaboration

**Everyone**:

- [ ] Pushes code daily
- [ ] Uses feature branches (`feature/xxx`)
- [ ] Creates descriptive PRs
- [ ] Reviews others' PRs within 24 hours
- [ ] Merges to main after 1+ approvals
- [ ] Keeps PRs small (<300 lines)

### Communication Channels

**#hybrid-mvp**: Main team channel (all discussions)  
**#backend**: Backend team sync  
**#frontend**: Frontend team sync  
**#devops**: Infrastructure issues  
**#support**: Customer issues

---

## WEEK-BY-WEEK TODO SUMMARY

### Week 1 (Nov 8-15): Dasha Timer MVP

**Everyone**:

- [ ] Daily standup
- [ ] Deploy to staging daily
- [ ] Monitor errors/logs
- [ ] Friday sprint review

**Backend** (80 hrs):

- [ ] Auth system
- [ ] Dasha calculation APIs
- [ ] Notifications infrastructure
- [ ] Testing + deployment

**Frontend** (80 hrs):

- [ ] Auth pages
- [ ] Birth chart form
- [ ] Dashboard + timer
- [ ] Settings page

**DevOps** (40 hrs):

- [ ] Infrastructure monitoring
- [ ] Staging → Production deployment
- [ ] Performance optimization

**QA** (40 hrs):

- [ ] Functional testing
- [ ] E2E testing
- [ ] Performance testing
- [ ] Go/no-go decision

**Growth** (40 hrs):

- [ ] Beta recruitment
- [ ] Feedback collection
- [ ] Metrics tracking

**Founder** (20 hrs):

- [ ] Daily standups
- [ ] Unblock team
- [ ] Make quick decisions
- [ ] Sprint review

### Week 2 (Nov 15-22): Compatibility MVP

**Same structure as Week 1**

**Backend** (64 hrs):

- [ ] Compatibility algorithm
- [ ] Calculation APIs
- [ ] Stripe integration
- [ ] Analytics/referral tracking

**Frontend** (64 hrs):

- [ ] Dual chart input
- [ ] Score visualization
- [ ] Social sharing components
- [ ] Premium flow

**Growth** (40 hrs):

- [ ] Launch campaign
- [ ] Viral growth monitoring
- [ ] Referral optimization

### Weeks 3-4: Migration & Unification

**Backend** (80 hrs):

- [ ] Data migration scripts
- [ ] Federated authentication
- [ ] Unified database schema
- [ ] API consolidation

**Frontend** (64 hrs):

- [ ] Unified web app
- [ ] Dashboard consolidation
- [ ] New navigation
- [ ] Integration testing

**DevOps** (60 hrs):

- [ ] Database migration
- [ ] Cutover planning
- [ ] Monitoring during migration
- [ ] Rollback readiness

**QA** (40 hrs):

- [ ] Migration testing
- [ ] Data integrity verification
- [ ] Federated auth testing
- [ ] User communication testing

### Weeks 5-8: New Features

**Backend** (200+ hrs):

- [ ] Moon Rituals feature
- [ ] Remedy of the Day feature
- [ ] AI Oracle Chat feature
- [ ] Each feature: APIs + database + integrations

**Frontend** (200+ hrs):

- [ ] Moon Rituals UI
- [ ] Remedy feature UI
- [ ] Oracle Chat UI
- [ ] Integration into main dashboard

**Growth** (80+ hrs):

- [ ] Feature launch campaigns
- [ ] Retention mechanics
- [ ] Premium upsell optimization
- [ ] Series A prep materials

---

## CRITICAL PATH & BLOCKERS

### Must-Have Dependencies

```
Week 1 → Week 2:
├── Auth system (must work perfectly)
├── Dasha calculation accuracy (must be verified)
└── Database operational (must scale to 2000+)

Week 2 → Week 3:
├── Payment flow tested (Stripe working)
├── Viral metrics tracked (sharing/referral system working)
└── User data cleaned (ready for migration)

Week 3 → Week 4:
├── Old data migrated (0% loss)
├── Federated auth working (old users can login)
└── Unified platform stable (< 2 critical bugs)

Weeks 4 → 5+:
├── Core platform reliable (99.9% uptime)
├── New feature infrastructure ready
└── Growth momentum maintained (retention > 35%)
```

### Known Risks & Mitigations

| Risk                       | Impact              | Mitigation                               |
| -------------------------- | ------------------- | ---------------------------------------- |
| Auth system bugs           | Blocks all users    | 2-day buffer, extensive testing          |
| Dasha calculation errors   | Loss of credibility | Verify accuracy vs Swiss Ephemeris       |
| Database migration failure | Data loss, restart  | Staging test, backups, rollback ready    |
| Performance degradation    | Users leave         | Load testing, caching, CDN               |
| Payment system failure     | Lost revenue        | Stripe sandbox testing, backup processor |
| Team member unavailable    | Timeline slips      | Cross-training, documentation            |

---

## SUCCESS CRITERIA (Per Week)

### Week 1 Success

- [ ] 500+ signups (Dasha Timer)
- [ ] <2 critical bugs in production
- [ ] <3 second page load
- [ ] 100+ engaged users (daily usage)
- [ ] $0 MRR (free beta)
- [ ] Team velocity on track

### Week 2 Success

- [ ] 2000+ signups (Compatibility)
- [ ] $300-500 MRR
- [ ] Viral coefficient ≥ 1.5
- [ ] <2 critical bugs
- [ ] Combined 2500+ active users
- [ ] Social sharing working

### Weeks 3-4 Success

- [ ] 4000+ users migrated
- [ ] 0% data loss
- [ ] <1% failed logins
- [ ] Unified dashboard working
- [ ] Revenue maintained ($300-500 MRR)
- [ ] <2 critical bugs

### Weeks 5-7 Success

- [ ] 3 new features launched
- [ ] Revenue growing to $1.5K-2.5K MRR
- [ ] 5000+ active users
- [ ] 35%+ D7 retention
- [ ] <1 critical bug

### Week 8 Success

- [ ] 10,000+ users
- [ ] $5K-9K MRR
- [ ] 5 features working perfectly
- [ ] 40%+ D7 retention
- [ ] Series A ready
- [ ] 0 critical bugs

---

## QUICK REFERENCE

### By Role

- **Founder**: Strategy, decisions, go/no-go calls
- **Backend Lead**: APIs, database, integrations
- **Frontend Lead**: UI/UX, web apps, user experience
- **DevOps Lead**: Infrastructure, deployment, uptime
- **QA Lead**: Testing, quality, launch readiness
- **Growth Lead**: Users, revenue, metrics

### By Timeline

- **Nov 4-7**: Founder approval → Team confirmation → Infrastructure setup
- **Nov 8-15**: Week 1 - Build Dasha Timer MVP
- **Nov 15-22**: Week 2 - Build Compatibility MVP
- **Nov 22-29**: Week 3 - Migrate & unify data
- **Nov 29-Dec 6**: Week 4 - Unified platform + federation
- **Dec 6-13**: Week 5 - Moon Rituals
- **Dec 13-20**: Week 6 - Remedy of Day
- **Dec 20-27**: Week 7 - AI Oracle Chat
- **Dec 27-Jan 2**: Week 8 - Optimize & launch

### Contact Escalation Path

**Quick Questions** → Slack #hybrid-mvp  
**Technical Decisions** → Backend/Frontend Lead  
**Product Decisions** → Founder/Product Lead  
**Infrastructure Issues** → DevOps Lead  
**Quality Issues** → QA Lead  
**Growth Questions** → Growth Lead  
**Urgent Blockers** → Founder (direct message)

---

## DOCUMENT REFERENCES

| Document                              | Role             | Purpose                 |
| ------------------------------------- | ---------------- | ----------------------- |
| `HYBRID_MVP_STRATEGY.md`              | Everyone         | Strategic foundation    |
| `HYBRID_BUILD_WEEK1_DASHA_TIMER.md`   | Backend/Frontend | Week 1 detailed spec    |
| `HYBRID_BUILD_WEEK2_COMPATIBILITY.md` | Backend/Frontend | Week 2 detailed spec    |
| `HYBRID_BUILD_MIGRATION_STRATEGY.md`  | Backend/DevOps   | Migration planning      |
| `HYBRID_BUILD_EXECUTION_TIMELINE.md`  | Founder/PM       | Timeline + financials   |
| `HYBRID_BUILD_CHECKLIST.md`           | QA/Everyone      | Daily execution tracker |
| `HYBRID_BUILD_QUICK_START.md`         | Founder          | One-page reference      |

---

## VERSION HISTORY

| Version | Date        | Changes                            |
| ------- | ----------- | ---------------------------------- |
| 1.0     | Nov 4, 2025 | Initial roles and todos assignment |

**Status**: Ready for team assignment and execution  
**Next Step**: Founder approves, sends out to team, everyone starts Nov 8
