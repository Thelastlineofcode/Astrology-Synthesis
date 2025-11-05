# BMAD AGENT TEAM - QUICK START

## Your 5-Agent Development Team

You have 5 specialized BMAD agents ready to build Milestone 1. Here's how to use them:

---

## 🎯 Agent Quick Reference

| Agent               | Role             | Skills                                  | When to Use                                         |
| ------------------- | ---------------- | --------------------------------------- | --------------------------------------------------- |
| **@frontend-agent** | UI/Frontend      | Next.js, React, TypeScript, Components  | Building pages, forms, UI components                |
| **@backend-agent**  | Backend/API      | FastAPI, Python, Databases, APIs        | Building endpoints, database models, business logic |
| **@devops-agent**   | Deployment/Infra | Railway, Vercel, CI/CD, Monitoring      | Deploying to production, setup infrastructure       |
| **@qa-agent**       | Testing/QA       | Playwright, Jest, pytest, Accessibility | Writing tests, performance testing, quality checks  |
| **@ai-agent**       | AI/LLM           | Claude API, Prompts, RAG                | AI features, LLM integration, knowledge bases       |

---

## 📋 Milestone 1 Feature Breakdown

### TODO #3: GitHub Repos & Deploy Skeleton

- **Prompts**: #3.1 (Frontend), #3.2 (Backend)
- **Frontend Agent**: Creates Next.js scaffold
- **Backend Agent**: Creates FastAPI scaffold
- **DevOps Agent**: Deploys to Vercel + Railway
- **You**: Review → Copy → Test locally → Deploy

### TODO #4: Auth System (Nov 5-6)

- **Prompts**: #4.1-#4.5
- **Frontend Agent** generates: Signup page, Login page, Auth context hook
- **Backend Agent** generates: Signup endpoint, Login endpoint
- **You**: Test, iterate, deploy

### TODO #5: Birth Chart Form (Nov 7-8)

- **Prompts**: #5.1-#5.2
- **Frontend Agent**: Form with date/time/location inputs
- **Backend Agent**: Database models + API endpoints
- **You**: Validate accuracy, test, deploy

### TODO #6: Dasha Display & Timer (Nov 9-10)

- **Prompts**: #6.1-#6.4
- **Frontend Agent**: Display component + timer component + dashboard
- **Backend Agent**: Dasha calculation endpoint
- **You**: Verify calculations correct, test, deploy

### TODO #7: Notifications (Nov 11-12)

- **Prompts**: #7.1-#7.3
- **Frontend Agent**: Notification settings UI
- **Backend Agent**: API endpoints + SendGrid integration
- **You**: Test email delivery, deploy

### TODO #8: Testing & Deploy (Nov 13-15)

- **Prompts**: #8.1-#8.4
- **QA Agent**: Unit tests + Component tests + E2E tests
- **DevOps Agent**: Production deployment checklist
- **You**: Run test suite, fix bugs, deploy

---

## 🚀 How to Use BMAD Agents

### Step 1: Open BMAD Chat

- Go to Perplexity or your BMAD agent interface
- Find chat with your agent team

### Step 2: Select the Right Agent

- For UI/React: Use **@frontend-agent**
- For API/Python: Use **@backend-agent**
- For Deploy/Infra: Use **@devops-agent**
- For Tests: Use **@qa-agent**
- For AI features: Use **@ai-agent**

### Step 3: Paste Prompt

- Open `COPILOT_PROMPT_LIBRARY.md`
- Find the prompt you need (e.g., #4.1 for signup)
- Copy the entire prompt (includes @agent mention)
- Paste into BMAD chat

### Step 4: Review Response

- Agent generates code/response
- Read through quality/security/best practices
- Ask for adjustments if needed

### Step 5: Implement

- Copy agent response
- Create/update files in your project
- Test locally
- Deploy to production

### Step 6: Document

- Note what agent did
- Update progress in todo list
- Next task

---

## 💬 Example: Build Signup Page

```
# Day: Nov 5, 2 PM

Step 1: Need signup page

Step 2: This is React/UI → Need @frontend-agent

Step 3: Open COPILOT_PROMPT_LIBRARY.md
        Find: PROMPT #4.1: Next.js Signup Page
        Copy entire prompt

Step 4: Paste into Perplexity with @frontend-agent:

@frontend-agent

Create a React page component at app/auth/signup/page.tsx with:
...
[entire prompt]
...

Step 5: Agent responds with code:

"I'll create a professional signup page for Mula with:
- Email and password validation
- Error handling
- Loading states
- Tailwind styling
- Mobile responsive

Here's the component..."

[Code response]

Step 6: Copy response → Create app/auth/signup/page.tsx

Step 7: Test locally:
npm run dev
→ go to http://localhost:3000/auth/signup
→ Form appears ✓
→ Validation works ✓

Step 8: Commit:
git add app/auth/signup/page.tsx
git commit -m "feat: add signup page (#4.1)"

Next: Build signup endpoint with @backend-agent
```

---

## 🎯 Today's Task: Repo Setup (Nov 5)

### Morning (9 AM)

```
PROMPT #3.1 (@frontend-agent): Next.js Scaffold
→ Copy prompt from COPILOT_PROMPT_LIBRARY.md
→ Paste to @frontend-agent
→ Get generated files
→ Create project: npx create-next-app@latest mula-dasha-timer-web
→ Integrate agent code
→ Test: npm run dev
→ Result: Frontend app running on localhost:3000
```

### Midday (11 AM)

```
PROMPT #3.2 (@backend-agent): FastAPI Scaffold
→ Copy prompt from COPILOT_PROMPT_LIBRARY.md
→ Paste to @backend-agent
→ Get generated files
→ Create project: mkdir mula-dasha-timer-api
→ Integrate agent code
→ Setup venv & deps
→ Test: python3 -m uvicorn app.main:app --reload
→ Result: Backend API running on localhost:8000
```

### Afternoon (2 PM)

```
PROMPT #8.4 (@devops-agent): Production Deployment
→ Copy prompt from COPILOT_PROMPT_LIBRARY.md
→ Paste to @devops-agent
→ Get deployment instructions
→ Deploy frontend to Vercel
→ Deploy backend to Railway
→ Test production URLs
→ Result: Both apps live on internet
```

### End of Day (5 PM)

✅ Todo #3 Complete: Both apps deployed and live

---

## 📚 Documentation Reference

| Document                                  | Purpose                | When to Use                         |
| ----------------------------------------- | ---------------------- | ----------------------------------- |
| **COPILOT_PROMPT_LIBRARY.md**             | All BMAD agent prompts | Daily - copy prompts for features   |
| **AI_AGENT_TEAM.md**                      | Agent descriptions     | Understanding agent capabilities    |
| **MILESTONE1_AI_AGENT_ASSIGNMENTS.md**    | Detailed handoffs      | Understanding context for each todo |
| **MILESTONE1_AGENT_ASSIGNMENT_MATRIX.md** | Quick reference table  | Quick lookup of who does what       |
| **TODO3_GITHUB_REPOS_DEPLOY.md**          | Step-by-step for Nov 5 | Today's detailed instructions       |

---

## ❓ FAQ

**Q: Can I use multiple agents for one task?**
A: Yes! @frontend-agent + @backend-agent work together. They coordinate well.

**Q: What if the agent code doesn't work?**
A: Describe the issue to the same agent, share the error, ask for fixes. Or ask another agent for second opinion.

**Q: How long does each agent take?**
A: Most responses: 30 seconds - 2 minutes. Complex tasks: 2-5 minutes.

**Q: Can I modify agent code?**
A: Absolutely! You're in control. Agent code is starting point, you review/adjust/test.

**Q: What if I don't like the generated code?**
A: Tell the agent! Ask for: simpler code, different approach, different library, etc. They'll adjust.

**Q: Can agents work in parallel?**
A: Yes! While @frontend-agent builds UI, @backend-agent can build API. Then @qa-agent tests both.

**Q: Do I need to manage agent state?**
A: No. Each prompt is independent. Reference previous work in prompt if needed.

---

## ✅ Success Criteria

By end of today (Nov 5):

- ✅ Frontend app deployed to Vercel
- ✅ Backend API deployed to Railway
- ✅ Both URLs live + accessible
- ✅ Todo #3 marked complete
- ✅ Ready for Todo #4 tomorrow (Auth system)

---

## 🎬 START NOW

**Pick one agent and start**:

1. Read COPILOT_PROMPT_LIBRARY.md → PROMPT #3.1
2. Copy the prompt (includes @frontend-agent)
3. Open BMAD chat
4. Paste: `@frontend-agent [entire prompt]`
5. Wait for response
6. Implement
7. Test
8. Deploy

**See you with two live apps. Let's go! 🚀**
