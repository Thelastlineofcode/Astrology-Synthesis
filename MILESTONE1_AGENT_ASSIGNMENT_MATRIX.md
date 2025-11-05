# MILESTONE 1: AGENT ASSIGNMENT MATRIX

## Who Does What - Dasha Timer MVP (Nov 5-15)

---

## 📊 QUICK REFERENCE TABLE

| Todo      | Feature                        | Frontend Agent                             | Backend Agent                            | Your Role                 | Hours     | Deadline   |
| --------- | ------------------------------ | ------------------------------------------ | ---------------------------------------- | ------------------------- | --------- | ---------- |
| #3        | GitHub Repos + Deploy Skeleton | @frontend setup Next.js on Vercel          | @backend setup FastAPI on Railway        | Review, test, deploy      | 2-3       | Nov 5      |
| #4        | Auth System                    | @frontend: signup/login UI (Copilot)       | @backend: JWT endpoints (Copilot)        | Review, test, iterate     | 8-10      | Nov 5-6    |
| #5        | Birth Chart Form               | @frontend: form component (Copilot)        | @backend: storage API (Copilot)          | Test accuracy, iterate UX | 6-8       | Nov 7-8    |
| #6        | Dasha Display & Timer          | @frontend: display + timer (Copilot)       | @backend: dasha calc API (Copilot)       | Verify accuracy, debug    | 8-10      | Nov 9-10   |
| #7        | Notifications                  | @frontend: settings UI (Copilot)           | @backend: SendGrid + scheduler (Copilot) | Test email delivery       | 4-6       | Nov 11-12  |
| #8        | Testing & Deploy               | @frontend: component + E2E tests (Copilot) | @backend: unit tests (Copilot)           | QA + smoke test + go-live | 10-12     | Nov 13-15  |
| #9        | Go/No-Go Gate                  | Review all metrics                         | Review all metrics                       | Make go/no-go decision    | 1         | Nov 15     |
| **TOTAL** | **Dasha Timer MVP**            | **Copilot generates all**                  | **Copilot generates all**                | **40-50 hrs**             | **40-50** | **Nov 15** |

---

## 🎯 AGENT ASSIGNMENTS BY ROLE

### YOUR ROLE: Founder/Executor/Decision Maker

You do NOT code. You:

- ✅ Ask Copilot to generate code
- ✅ Review generated code (5-10 min per feature)
- ✅ Test implementations (does it work?)
- ✅ Iterate with user feedback
- ✅ Deploy to production
- ✅ Monitor + fix bugs
- ✅ Make decisions (go/no-go)

**Your 40-50 hours breaks down**:

- Repo setup + deployment: 2-3 hrs
- Testing + iteration: 20-25 hrs
- Code review: 5-10 hrs
- Deployment + monitoring: 5-10 hrs
- Decision making + planning: 5 hrs

---

### @FRONTEND: Copilot (Code Generation + Testing)

Copilot generates:

**Signup/Login**

```
✅ Next.js page components (signup.tsx, login.tsx)
✅ Form validation (email, password)
✅ Error/success messages
✅ Loading states
✅ Auth context hook (useAuth)
✅ Protected routes wrapper
✅ Component tests (Jest)
✅ E2E tests (Playwright)
```

**Birth Chart Form**

```
✅ Form component (date/time/location inputs)
✅ Geocoding integration
✅ Form validation
✅ Submit handler
✅ Error display
✅ Tests
```

**Dasha Display**

```
✅ Dasha display component (shows current dasha)
✅ Real-time timer component (updates every second)
✅ Progress bar visualization
✅ Next dasha preview
✅ Tests
```

**Notification Settings**

```
✅ Toggle + dropdown for preferences
✅ Submit handler
✅ Tests
```

**What YOU do**:

- Copy generated code to project
- Review for security + best practices
- Test locally (run `npm run dev`)
- Run component tests
- Fix any issues
- Deploy to Vercel

---

### @BACKEND: Copilot (Code Generation + Testing)

Copilot generates:

**Auth System**

```
✅ User SQLAlchemy model
✅ POST /api/v1/auth/signup endpoint
✅ POST /api/v1/auth/login endpoint
✅ JWT token generation + validation
✅ Password hashing (bcrypt)
✅ Error handling (duplicate email, invalid credentials)
✅ Unit tests (pytest)
```

**Birth Chart Storage**

```
✅ BirthChart SQLAlchemy model
✅ POST /api/v1/birth-charts endpoint (create)
✅ GET /api/v1/birth-charts endpoint (list)
✅ GET /api/v1/birth-charts/{id} endpoint (get)
✅ Auth validation (JWT required)
✅ Geocoding integration
✅ Unit tests
```

**Dasha Calculation**

```
✅ GET /api/v1/dasha/{chart_id} endpoint
✅ Wraps existing dasha calculation logic
✅ Returns: {current_dasha, period_start, period_end, meaning}
✅ Caching (24 hour TTL)
✅ Error handling
✅ Unit tests
```

**Notifications**

```
✅ SendGrid client initialization
✅ send_email() function
✅ Email templates (dasha_change_notification)
✅ POST /api/v1/notifications/subscribe endpoint
✅ POST /api/v1/notifications/unsubscribe endpoint
✅ Background task (APScheduler) to check daily + send emails
✅ Unit tests
```

**What YOU do**:

- Copy generated code to project
- Review for security + correctness
- Run migrations (database schema)
- Test locally with `python3 -m uvicorn app.main:app --reload`
- Test endpoints with curl/Postman
- Run unit tests: `pytest tests/`
- Fix any issues
- Deploy to Railway

---

### @PERPLEXITY: Research & Debugging (On-Demand)

You ask Perplexity when:

- ❓ How do I handle timezone in birth charts?
- 🐛 Why is my password not hashing correctly?
- 📚 What's the standard for Vedic astrology dasha calculation?
- 🔍 Why is performance slow?
- 🏗️ How should I structure my FastAPI project?

Perplexity provides research + recommendations, then you ask Copilot to implement.

---

## 🔄 WORKFLOW: How They Work Together

### Example: Birth Chart Form

**Step 1: You**

```
"I need a birth chart form component.
It needs date (day/month/year), time (hour/minute), location.
Validation: future dates blocked, valid location required."
```

**Step 2: Copilot**

```
✅ Generates: BirthChart form component (React + TypeScript + Tailwind)
✅ Includes: Validation, error handling, loading state
✅ Output: You can copy directly to your project
```

**Step 3: You**

```
- Review generated code (2-3 min)
- Copy to app/components/BirthChartForm.tsx
- Run locally: npm run dev
- Test form: Can I input date? Validation works?
- If bug: "Copilot, fix the date validation..."
- Copilot regenerates just that part
```

**Step 4: Copilot** (when needed)

```
✅ Generates: Bug fix or improvement
✅ You: Copy, test, deploy
```

**Step 5: You**

```
- Deploy to Vercel: git push
- Test on production: mula-dasha.vercel.app
- Move to next todo
```

---

## ⚡ QUICK START: Nov 5 (TODAY)

### In the next 3 hours:

**9:00 AM: Start Todo #3 - GitHub Repos**

**Frontend**:

```bash
# Create repo
git clone https://github.com/yourusername/mula-dasha-timer-web.git
cd mula-dasha-timer-web

# Open in VS Code and open Copilot chat
# Ask Copilot:
"Create a Next.js 16 project with React 19,
TypeScript, Tailwind CSS, Shadcn/ui, ready for Vercel."

# Copilot generates files → You review → Copy to project
# Test locally: npm run dev
# Deploy: npx vercel deploy
```

**Backend**:

```bash
# Create repo
git clone https://github.com/yourusername/mula-dasha-timer-api.git
cd mula-dasha-timer-api

# Open in VS Code and open Copilot chat
# Ask Copilot:
"Create a FastAPI project with JWT auth, SQLAlchemy,
PostgreSQL, ready for Railway deployment."

# Copilot generates files → You review → Copy to project
# Test locally: python3 -m uvicorn app.main:app --reload
# Deploy: railway up
```

**By 12 PM**: Both apps deployed to Vercel + Railway ✅

---

## 📋 COPILOT PROMPT TEMPLATES

### Template 1: Generate Component

```
@Copilot: "Create a React component called [ComponentName] that:
- [Feature 1]
- [Feature 2]
- [Feature 3]
Include: Tailwind styling, dark mode, accessibility labels
Path: app/components/[ComponentName].tsx"
```

### Template 2: Generate API Endpoint

```
@Copilot: "Create a FastAPI endpoint:
- Method: [GET/POST/PUT/DELETE]
- URL: /api/v1/[path]
- Accepts: [input data]
- Returns: [output data]
- Requires: [JWT auth / public]
- Handles: [error cases]
File: app/routers/[name].py"
```

### Template 3: Generate Tests

```
@Copilot: "Create pytest tests for [feature]:
- Test case 1: [description]
- Test case 2: [description]
- Test case 3: [description]
Use fixtures for setup/teardown
File: tests/test_[name].py"
```

---

## 🎯 SUCCESS CHECKLIST

### By Nov 15 EOD, check off:

- [ ] Todo #3: GitHub repos + Vercel + Railway deployed
- [ ] Todo #4: Auth working (signup/login)
- [ ] Todo #5: Birth chart form working
- [ ] Todo #6: Dasha display accurate
- [ ] Todo #7: Notifications sending emails
- [ ] Todo #8: All tests passing, deployed to production
- [ ] Todo #9: Go/no-go decision made + documented
- [ ] 50-100 beta users signed up
- [ ] <3s page load time
- [ ] 0-1 critical bugs
- [ ] You spent 40-50 hours (not burned out)

**If all checked**: MILESTONE 1 SUCCESS ✅ → Proceed to MILESTONE 2 (Compatibility)

---

## 💬 Questions?

**"How do I get Copilot to generate good code?"**
→ Be specific: "Create X component that does Y, with Z styling. Include error handling."

**"What if Copilot generates wrong code?"**
→ Ask it to fix: "That's not right. [Describe issue]. Fix it."

**"When should I use Perplexity vs Copilot?"**
→ Copilot: Code generation. Perplexity: Research + debugging.

**"I'm stuck on a bug. What do I do?"**
→ Ask Perplexity: "Why does [thing] fail? What are common causes?"

**"How fast can I ship this?"**
→ 5-7 hrs/day = 40-50 hrs total = 9 days (Nov 5-15)

---

## 🚀 READY?

**Next action**:

1. Review this document
2. Open Copilot in VS Code
3. Start Todo #3: Create GitHub repos
4. Ask Copilot to scaffold Next.js starter
5. Deploy to Vercel

**Go time.**
