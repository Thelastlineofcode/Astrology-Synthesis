# Perplexity Agent Team Setup Guide

**Project**: Mula: The Root  
**Date**: November 4, 2025  
**Purpose**: Configure 5-agent team in Perplexity for MVP development  
**Duration**: 12-month subscription access

---

## 🤖 Agent Team Overview

Your Mula development is powered by **5 specialized AI agents working as a coordinated team**. This guide explains who they are, how to access them, and how to work with them effectively in Perplexity.

### The 5-Agent Team

```
┌─────────────────────────────────────────────────────────────────┐
│                    MULA DEVELOPMENT TEAM                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  1️⃣  BACKEND AGENT (@backend-agent)                            │
│      Specialty: FastAPI, Python, Databases, APIs                │
│      Role: Build server logic, APIs, database schemas           │
│      Response: Technical, code-focused, asks clarifying Qs      │
│                                                                   │
│  2️⃣  FRONTEND AGENT (@frontend-agent)                          │
│      Specialty: Next.js, React, TypeScript, UX/UI               │
│      Role: Build pages, components, user interfaces             │
│      Response: Component-focused, visual-thinking, UX emphasis  │
│                                                                   │
│  3️⃣  DEVOPS AGENT (@devops-agent)                              │
│      Specialty: Deployment, Infrastructure, Monitoring          │
│      Role: Deploy to production, manage infrastructure           │
│      Response: Infrastructure-focused, reliability-driven        │
│                                                                   │
│  4️⃣  QA AGENT (@qa-agent)                                      │
│      Specialty: Testing, Accessibility, Performance             │
│      Role: Write tests, ensure quality, verify everything works │
│      Response: Test-focused, thinks in scenarios & edge cases   │
│                                                                   │
│  5️⃣  PERPLEXITY AI AGENT (@ai-agent)                           │
│      Specialty: Advisor personalities, Knowledge integration     │
│      Role: Build Papa Legba and advisor experiences             │
│      Access: 12-month Perplexity subscription                   │
│      Response: Creative, conversational, quality-focused        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📖 Agent Team Documentation

### Accessing the Full Agent Configuration

**Location**: `/Users/houseofobi/Documents/GitHub/Mula/AI_AGENT_TEAM.md`

**File Size**: ~20 KB (594 lines)  
**Format**: Markdown with YAML specs, tables, interaction examples  
**Access Method**: Open in VS Code or any text editor

### What's in AI_AGENT_TEAM.md

1. **Agent Roster** (Lines 1-350)
   - Detailed specs for each agent
   - Core competencies & when to engage
   - Example interactions
   - Response style guidelines

2. **Agent Communication Protocol** (Lines 350-400)
   - How agents collaborate
   - Dependency chains
   - Information sharing channels

3. **Specialization Matrix** (Lines 400-430)
   - Task-to-agent mapping
   - Expertise levels
   - Cross-functional capabilities

4. **Team Load Distribution** (Lines 430-460)
   - Phase 3a (MVP) workload
   - Hours per agent
   - Feature assignments

5. **Operational Guidelines** (Lines 460-530)
   - Daily workflow
   - Pull request process
   - Blocker escalation

6. **Success Metrics** (Lines 530-594)
   - Definition of Done per agent
   - Phase 3a checkpoints
   - Quality targets

---

## 🚀 How to Use Agents in Perplexity

### Step 1: Copy the Agent Configuration

1. Open `/Users/houseofobi/Documents/GitHub/Mula/AI_AGENT_TEAM.md`
2. Select all content: `Cmd+A`
3. Copy to clipboard: `Cmd+C`

### Step 2: Create a Perplexity Collection

1. Go to **Perplexity.ai**
2. Click **Collections** (left sidebar)
3. Click **+ New Collection**
4. Name it: `MULA Agent Team Configuration`
5. Description: "5-agent development team for Mula MVP"
6. Paste the full `AI_AGENT_TEAM.md` content
7. Click **Save**

### Step 3: Reference in Chats

When working on a task, include the collection:

```
@MULA Agent Team Configuration

@backend-agent: Please create the database schema for...
```

### Step 4: Route to Specific Agents

Use `@agent-name` to direct your request to the right specialist:

**For Backend Work**:

```
@backend-agent: Create the /api/v1/readings endpoint with...
```

**For Frontend Work**:

```
@frontend-agent: Build a responsive signup form component with...
```

**For Deployment**:

```
@devops-agent: Deploy the backend to Railway with environment vars...
```

**For Testing**:

```
@qa-agent: Write E2E tests for the authentication flow...
```

**For Advisor/AI Work**:

```
@ai-agent: Create a system prompt for Papa Legba that...
```

---

## 🎭 Important: Staying in Character

### What "Staying in Character" Means

Each agent has a specific **personality, expertise level, and response style**. To get the best results, they must remain consistent in their role:

- **Backend Agent** stays technical and code-focused
- **Frontend Agent** stays visual and UX-conscious
- **DevOps Agent** stays infrastructure-reliable
- **QA Agent** stays quality-thorough
- **Perplexity AI Agent** stays creative and personality-authentic

### How to Maintain Character

**DO**:

✅ Keep agents focused on their specialty domain  
✅ Ask them to explain decisions in their area of expertise  
✅ Have them reference their tools & best practices  
✅ Let them think through problems systematically  
✅ Have them communicate with other agents when needed

**DON'T**:

❌ Ask Frontend Agent to write backend API code (wrong specialty)  
❌ Ask DevOps Agent to design UI components (not their role)  
❌ Ask QA Agent to implement features (they verify, not build)  
❌ Ask Backend Agent to handle deployment (DevOps Agent's job)  
❌ Let agents break consistency by changing their expertise area

### Example: Breaking vs. Staying in Character

**❌ BREAKS CHARACTER**:

```
@backend-agent: I need you to build the React component for the login page

Backend Agent: Here's the React code...
[Agent is now doing frontend work - WRONG SPECIALTY]
```

**✅ STAYS IN CHARACTER**:

```
@backend-agent: I need the JWT authentication endpoint for login

Backend Agent: I'll design the auth API with...
[Agent focuses on backend logic and JWT tokens - RIGHT SPECIALTY]

Then ask @frontend-agent:
@frontend-agent: Use this auth endpoint to build a login form component

Frontend Agent: I'll create a responsive login form that calls the...
[Agent handles UI/UX for the form - CORRECT SPECIALTY]
```

### Character Consistency Template

When starting a new task, confirm the agent understands their role:

```
You are the [Backend/Frontend/DevOps/QA/AI] Agent for the Mula project.
Your specialty is [their domain].
You will:
- Focus only on [their area of expertise]
- Use [their tools/language]
- Think about [their concerns]
- Communicate with other agents when dependencies arise

Understand?
```

---

## 📋 Quick Reference: Who Does What

| Task                      | Agent           | Why                                        |
| ------------------------- | --------------- | ------------------------------------------ |
| Design database schema    | @backend-agent  | Specialty: databases & data modeling       |
| Create Next.js pages      | @frontend-agent | Specialty: React/Next.js components        |
| Deploy to Railway         | @devops-agent   | Specialty: infrastructure & deployment     |
| Write E2E tests           | @qa-agent       | Specialty: testing & quality verification  |
| Create Papa Legba prompt  | @ai-agent       | Specialty: advisor personalities & prompts |
| Fix API response time     | @backend-agent  | Backend performance optimization           |
| Fix mobile responsiveness | @frontend-agent | Frontend/UX optimization                   |
| Set up monitoring         | @devops-agent   | Infrastructure monitoring                  |
| Find UI accessibility bug | @qa-agent       | Testing & accessibility                    |
| Refine advisor tone       | @ai-agent       | Prompt engineering & personality           |

---

## 💬 Agent Interaction Patterns

### Pattern 1: Single Agent Task

**Scenario**: Simple, contained work for one specialist

```
@backend-agent: Create a PostgreSQL schema for user profiles with:
- id (UUID primary key)
- name, email, birth_date
- created_at, updated_at timestamps
- Include indexes on email

Backend Agent: [Responds with CREATE TABLE statement and explanation]
```

### Pattern 2: Dependency Chain

**Scenario**: Task requires multiple agents in sequence

```
Step 1 - @backend-agent designs the API:
"Create a POST /api/v1/readings endpoint that accepts birth data
and returns astrological calculations"

Backend Agent: [Creates API specification]

Step 2 - @frontend-agent builds the UI:
"I have the API ready at /api/v1/readings. Build a form that
collects birth data and displays results"

Frontend Agent: [Creates React component that calls the API]

Step 3 - @qa-agent tests the flow:
"Here's the form and API. Write E2E tests that verify a user can
submit birth data and see astrological results"

QA Agent: [Writes Playwright E2E tests]

Step 4 - @devops-agent deploys:
"Both are ready to go. Deploy backend to Railway and frontend to
Vercel, ensure API_URL env var is configured"

DevOps Agent: [Handles deployment and monitoring]
```

### Pattern 3: Parallel Tasks

**Scenario**: Multiple agents work simultaneously on different features

```
@backend-agent: Start building the auth system (JWT endpoints)

@frontend-agent: Start building the signup page (will use auth API later)

@qa-agent: Prepare test strategy for both auth system and signup flow

[All work in parallel, coordinate when dependencies arise]
```

---

## 🎯 Daily Workflow Example (Nov 5)

**Morning** (9 AM):

```
You: @backend-agent: Let's start building. First, create the database
schema for users, readings, advisors with appropriate relationships.

Backend Agent: [Creates schema, explains design decisions, asks clarifying Qs]
```

**Mid-Morning** (11 AM):

```
You: @frontend-agent: Backend schema is ready. Build the signup form
that collects name, email, password, birth date.

Frontend Agent: [Creates responsive form component with validation]
```

**Afternoon** (2 PM):

```
You: @devops-agent: Both backend and frontend scaffolds are ready.
Deploy backend to Railway and frontend to Vercel.

DevOps Agent: [Sets up deployments, env vars, monitoring]
```

**Late Afternoon** (4 PM):

```
You: @qa-agent: Both apps are deployed. Write E2E tests for signup flow
(enter data → success message → redirected to dashboard).

QA Agent: [Writes comprehensive Playwright E2E tests]
```

**End of Day** (5 PM):

```
You: All agents, report status. Any blockers?

All Agents: [Report completed work, confirm no blockers, ready for tomorrow]
```

---

## ⚠️ Common Mistakes to Avoid

### Mistake 1: Mixing Responsibilities

**WRONG**:

```
@backend-agent: Build the login page UI and create the JWT endpoint

Backend Agent is now trying to do frontend + backend work
```

**RIGHT**:

```
@backend-agent: Create the JWT authentication endpoint

@frontend-agent: Build the login page UI that calls the JWT endpoint
```

### Mistake 2: Ignoring Agent Expertise

**WRONG**:

```
@qa-agent: Implement the user authentication system

QA Agent is not a developer, they verify quality
```

**RIGHT**:

```
@backend-agent: Implement JWT authentication

@qa-agent: Write tests for the authentication system to ensure it works
```

### Mistake 3: Breaking Character Mid-Conversation

**WRONG**:

```
@backend-agent: Create database schema for readings

Backend Agent: [Creates schema]

You: Now build the React component for displaying readings

Backend Agent: [Suddenly switches to React code - WRONG DOMAIN]
```

**RIGHT**:

```
@backend-agent: Create database schema for readings

Backend Agent: [Creates schema, returns to backend specialty]

You: @frontend-agent: Backend created the readings table. Now build
the React component to display readings.

Frontend Agent: [Builds React component - CORRECT DOMAIN]
```

### Mistake 4: Unclear Requests

**WRONG**:

```
@backend-agent: Make the system better

Backend Agent: [Confused - what needs improvement?]
```

**RIGHT**:

```
@backend-agent: Optimize the /api/v1/readings endpoint. Currently
taking 2 seconds, we need it under 500ms. Profile the database queries
and suggest indexes.

Backend Agent: [Clear task, specific performance target, actionable]
```

---

## 📞 When Agents Need to Communicate

Agents automatically communicate when work depends on each other:

**Example Dependency**:

```
Backend Agent (done): "I've created the /api/v1/chart endpoint.
It expects POST with { birth_data } and returns { chart_json }"

Frontend Agent (waiting): "Waiting for the API spec from Backend"
↓ Backend provides spec ↓
Frontend Agent (now proceeds): "Now I can build the form that calls this API"

QA Agent (waiting): "Waiting for both API and UI to be done"
↓ Both are ready ↓
QA Agent (now proceeds): "Now I can write E2E tests for the full flow"

DevOps Agent (waiting): "Waiting for everything to be tested"
↓ Tests pass ↓
DevOps Agent (now proceeds): "Now I can deploy to production"
```

**How to Trigger This**:

Simply tell each agent when the previous step is complete:

```
@backend-agent: Create database schema [WAITING]
[Backend finishes]
@frontend-agent: I have the schema. Build the signup form [NOW GO]
[Frontend finishes]
@qa-agent: I have form + backend. Write E2E tests [NOW GO]
```

---

## ✅ Staying on Track: The 5-Day Sprint

### Day 1 (Nov 5): Scaffolds

```
✅ Backend Agent: Database + base API endpoints
✅ Frontend Agent: Next.js setup + basic pages
✅ DevOps Agent: Deployment infrastructure ready
```

### Day 2 (Nov 6): Authentication

```
✅ Backend Agent: JWT auth endpoints complete
✅ Frontend Agent: Login/signup pages complete
✅ QA Agent: Auth flow E2E tests
```

### Day 3 (Nov 7): Birth Chart

```
✅ Backend Agent: Chart calculation endpoint
✅ Frontend Agent: Chart display component
✅ QA Agent: Chart feature tests
```

### Day 4 (Nov 8): Dasha Timer

```
✅ Backend Agent: Dasha calculation endpoint
✅ Frontend Agent: Timer UI component
✅ QA Agent: Dasha feature tests
```

### Day 5 (Nov 9): Notifications

```
✅ Backend Agent: Notification endpoints
✅ Frontend Agent: Notification UI
✅ QA Agent: Notification tests
✅ DevOps Agent: Production deployment
```

---

## 🎓 Tips for Best Results

1. **Be Specific**: The more detailed your request, the better the response
2. **Stay Focused**: One feature per request, not multiple at once
3. **Use the Right Agent**: Always route to the appropriate specialist
4. **Provide Context**: Mention related work that's already done
5. **Request Explanations**: Ask agents to explain their decisions
6. **Check Quality**: Review code/work before moving to the next task
7. **Ask for Dependencies**: When work connects, explicitly mention it
8. **Keep Character**: Let each agent stay in their specialty zone

---

## 📚 Reference Documents

Keep these open for quick reference:

- **AI_AGENT_TEAM.md** - Full agent specs (what you pasted into Perplexity)
- **COPILOT_PROMPT_LIBRARY.md** - 21 prompts with @agent-name routing
- **BMAD_AGENT_QUICK_START.md** - Quick workflow reference
- **BMAD_PROMPT_LIBRARY_INDEX.md** - Find any prompt by date/agent

---

## 🎯 Success Definition

By Nov 15, with this agent team:

✅ **Backend Agent**: Database + 12 API endpoints complete  
✅ **Frontend Agent**: 8 pages + components built & deployed  
✅ **DevOps Agent**: Vercel + Railway setup, monitoring active  
✅ **QA Agent**: 90%+ E2E test coverage, quality verified  
✅ **AI Agent**: Papa Legba + 3 advisor personalities working

**Result**: Dasha Timer MVP live with 50-100 beta users

---

**Document Version**: 1.0  
**Last Updated**: November 4, 2025  
**Next Step**: Copy AI_AGENT_TEAM.md → Create Perplexity Collection → Start using agents!
