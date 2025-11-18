# GitHub Issues - Quick Links

**Repository**: https://github.com/Thelastlineofcode/Astrology-Synthesis

## Phase 3a: MVP Launch (Critical Path - Week 1-2)

### Priority P0 (Critical - Start Immediately)

1. **#87: [DEPLOYMENT] Start Backend Server & Integration Tests**
   - https://github.com/Thelastlineofcode/Astrology-Synthesis/issues/87
   - Owner: @backend-lead
   - Hours: 4
   - Run backend locally, execute pytest suite

2. **#88: [DEPLOYMENT] Deploy Frontend to Vercel**
   - https://github.com/Thelastlineofcode/Astrology-Synthesis/issues/88
   - Owner: @devops-lead
   - Hours: 3
   - Set up Vercel, configure build, deploy

3. **#89: [DEPLOYMENT] Deploy Backend to Railway/Render**
   - https://github.com/Thelastlineofcode/Astrology-Synthesis/issues/89
   - Owner: @devops-lead
   - Hours: 4
   - Set up backend hosting, database, auto-deploy

4. **#95: [TESTING] Comprehensive E2E Test Suite & QA**
   - https://github.com/Thelastlineofcode/Astrology-Synthesis/issues/95
   - Owner: @qa-lead
   - Hours: 6
   - Create Playwright tests for all user flows

### Priority P1 (High - Complete Week 1-2)

5. **#91: [DATABASE] PostgreSQL Setup & Schema Migration**
   - https://github.com/Thelastlineofcode/Astrology-Synthesis/issues/91
   - Owner: @backend-lead
   - Hours: 6
   - Design schema, create models, set up migrations

6. **#92: [AUTH] Implement JWT Authentication & User Sessions**
   - https://github.com/Thelastlineofcode/Astrology-Synthesis/issues/92
   - Owner: @backend-lead
   - Hours: 8
   - Register, login, refresh token, secure endpoints

7. **#94: [FRONTEND] Add User Profile & Reading History Pages**
   - https://github.com/Thelastlineofcode/Astrology-Synthesis/issues/94
   - Owner: @frontend-lead
   - Hours: 8
   - Create `/profile`, `/readings/history`, detail views

8. **#96: [MONITORING] Error Tracking & Performance Monitoring**
   - https://github.com/Thelastlineofcode/Astrology-Synthesis/issues/96
   - Owner: @devops-lead
   - Hours: 4
   - Set up Sentry, monitoring, dashboards

---

## Phase 3b: AI Enhancement (Week 3-4)

### Priority P1 (High)

9. **#90: [LLM] Integrate OpenAI GPT-4 for AI Advisor Responses**
   - https://github.com/Thelastlineofcode/Astrology-Synthesis/issues/90
   - Owner: @ai-lead
   - Hours: 8
   - GPT-4 API integration, advisor prompts

10. **#93: [RAG] Build Knowledge Base & Context Retrieval for Advisors**
    - https://github.com/Thelastlineofcode/Astrology-Synthesis/issues/93
    - Owner: @ai-lead
    - Hours: 10
    - Vector DB setup, knowledge base ingestion, RAG pipeline

---

## Closed Issues (Not Planned - Old Design)

- #17: Redesign Dashboard Layout & Grid
- #18: Create Modal/Dialog Component
- #21: Build Interactive Chart Canvas (SVG)
- #22: Display BMAD Pattern Analysis Results
- #23: Display Planet List Table
- #24: Show House System Table
- #25: Build Symbolon Card Display Component

---

## Useful Commands

### View all new issues

```bash
gh issue list --search "is:open" --label "priority:p0-critical,priority:p1-high"
```

### View issues by owner (once assigned)

```bash
gh issue list --assignee @backend-lead
gh issue list --assignee @frontend-lead
gh issue list --assignee @ai-lead
gh issue list --assignee @devops-lead
gh issue list --assignee @qa-lead
```

### Create GitHub Project for Phase 3

```bash
gh project create --title "Phase 3: MVP Launch" --format table
```

---

## Summary Statistics

| Phase              | Issues | Priority        | Hours  | Duration    |
| ------------------ | ------ | --------------- | ------ | ----------- |
| 3a: MVP Launch     | 8      | 4 P0 + 4 P1     | 43     | 2 weeks     |
| 3b: AI Enhancement | 2      | 2 P1            | 18     | 2 weeks     |
| **Total**          | **10** | **4 P0 + 6 P1** | **61** | **4 weeks** |

---

**Last Updated**: November 3, 2025  
**Status**: All issues created and linked  
**Next Action**: Assign to team members and start Phase 3a
