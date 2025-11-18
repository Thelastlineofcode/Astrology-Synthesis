# TODO #3: GITHUB REPOS + SKELETON DEPLOY

## Detailed Execution - Nov 5 (2-3 hours)

**Status**: IN-PROGRESS  
**Started**: Nov 4 evening  
**Deadline**: Nov 5 evening  
**Your time**: 2-3 hours  
**Copilot time**: ~10 hours (scaffold generation)

---

## 🎯 GOAL

By end of Nov 5, have:

- ✅ 2 GitHub repos created (frontend + backend)
- ✅ Frontend deployed on Vercel (live URL)
- ✅ Backend deployed on Railway (live API)
- ✅ Both functional (can access URLs)
- ✅ Ready for next todo (Auth system)

---

## 📋 STEP-BY-STEP CHECKLIST

### PART A: FRONTEND REPO + VERCEL DEPLOY (1-1.5 hours your time)

#### Step 1: Create GitHub Repository (5 min)

- [ ] Go to github.com
- [ ] Click: New repository
- [ ] Name: `mula-dasha-timer-web`
- [ ] Description: "Dasha Timer - Astrology app frontend"
- [ ] Public (for now, can be private later)
- [ ] Initialize with: None (we'll add code)
- [ ] Click: Create repository
- [ ] Copy the HTTPS URL
  ```
  https://github.com/yourusername/mula-dasha-timer-web.git
  ```

#### Step 2: Create Local Frontend Project (10 min)

```bash
# In terminal, navigate to your workspace
cd /Users/houseofobi/Documents/GitHub

# Clone the empty repo
git clone https://github.com/yourusername/mula-dasha-timer-web.git
cd mula-dasha-timer-web

# Create Next.js project IN THIS DIRECTORY
# (This will create app/, components/, etc. inside the repo)
npx create-next-app@latest . --typescript --tailwind --eslint

# When prompted:
# - "Would you like to use ESLint?" → Y
# - "Would you like to use Tailwind CSS?" → Y
# - "Would you like your code inside a `src/` directory?" → Y
# - "Would you like to use App Router?" → Y
# - "Would you like to customize the import alias?" → N

# Verify it worked
ls -la
# Should see: app/, public/, src/, package.json, tsconfig.json, etc.
```

#### Step 3: Generate Next.js Scaffold with Copilot (15 min)

**Open VS Code**

```bash
code .
```

**Open Copilot Chat**

- Mac: Cmd+I
- Windows: Ctrl+I

**Copy & Paste This Prompt:**

```
Create a Next.js 16 project scaffold for a Vedic astrology platform (Mula).

Already started with create-next-app.
Now add:

Project structure:
- app/
  - layout.tsx (main layout with header/footer)
  - page.tsx (landing/home page)
  - auth/
    - signup/
      - page.tsx (signup page - create, don't have yet)
    - login/
      - page.tsx (login page - create, don't have yet)
  - dashboard/
    - page.tsx (dashboard - create, don't have yet)
- components/
  - Header.tsx
  - Footer.tsx
  - Navigation.tsx
  - (more components will be added)
- lib/
  - utils.ts
  - api.ts (API client for backend calls)
  - auth.ts (auth helper functions)
- styles/
  - globals.css
  - (global Tailwind styles)

Key files to create/update:
1. .env.example - Template for environment variables:
   NEXT_PUBLIC_API_URL=http://localhost:8000

2. .gitignore - Add: node_modules/, .next/, .env.local

3. tailwind.config.ts - Already configured by create-next-app

4. tsconfig.json - Path aliases configured

5. next.config.js - For API routing and middleware

Include:
- Dark mode support (Tailwind dark: class)
- Professional styling (clean, modern)
- Responsive design (mobile-first)
- Error boundaries
- Loading states
- Basic navigation

Output complete Next.js project ready for:
- Local development: npm run dev
- Vercel deployment: npm run build
- Feature development (we'll add pages/components)

Make it production-ready but not over-engineered.
```

**Copilot will generate:**

- Updated files for existing ones (tailwind.config.ts, tsconfig.json)
- New files (components/, lib/, etc.)

#### Step 4: Review Generated Files (5 min)

Copilot will show you generated code. Review:

- ✅ No sensitive data exposed
- ✅ Error handling present
- ✅ Dark mode support
- ✅ Mobile responsive

#### Step 5: Copy Generated Files to Project (10 min)

For each generated file:

1. Copy from Copilot output
2. Create/update in your project directory
3. File structure should match what Copilot generated

#### Step 6: Install Dependencies & Test Locally (15 min)

```bash
# Install if needed (should already be done by create-next-app)
npm install

# Test locally
npm run dev

# Open browser: http://localhost:3000
# Should see: Next.js page loading
# No errors in console
# Page responsive on mobile view
```

#### Step 7: Commit to GitHub (5 min)

```bash
# Stage all files
git add .

# Commit
git commit -m "Initial Next.js scaffold for Mula Dasha Timer"

# Push to GitHub
git push -u origin main
# Or if your default branch is 'master':
git push -u origin master
```

#### Step 8: Deploy to Vercel (10 min)

```bash
# Install Vercel CLI (if not already installed)
npm i -g vercel

# Deploy from your project directory
npx vercel

# Follow prompts:
# - "Which scope do you want to deploy to?" → your account
# - "Link to existing project?" → N (create new)
# - "What's your project's name?" → mula-dasha-timer-web
# - "In which directory is your code?" → ./ (current directory)
# - "Want to modify vercel.json?" → N
# - Wait... deployment happens
# - Vercel will show: https://mula-dasha-timer-web.vercel.app (or similar)
```

**Save this URL: This is your FRONTEND production URL**

#### Step 9: Test Production Deployment (5 min)

```bash
# Visit the URL Vercel gave you
# Example: https://mula-dasha-timer-web.vercel.app

# Verify:
✅ Page loads (no 404)
✅ No console errors
✅ Mobile responsive
✅ Dark mode toggle works (if you added it)
```

#### Step 10: Create .env File (5 min)

```bash
# In your local project directory
touch .env.local

# Add this line (will update with actual API URL after backend deploy)
NEXT_PUBLIC_API_URL=http://localhost:8000

# (For production: will be https://mula-api.railway.app)
```

**✅ FRONTEND DONE**

---

### PART B: BACKEND REPO + RAILWAY DEPLOY (1-1.5 hours your time)

#### Step 1: Create GitHub Repository (5 min)

- [ ] Go to github.com
- [ ] Click: New repository
- [ ] Name: `mula-dasha-timer-api`
- [ ] Description: "Dasha Timer - Astrology app backend API"
- [ ] Public
- [ ] Initialize with: None
- [ ] Click: Create repository
- [ ] Copy the HTTPS URL
  ```
  https://github.com/yourusername/mula-dasha-timer-api.git
  ```

#### Step 2: Create Local Backend Project (10 min)

```bash
# In terminal, navigate to workspace
cd /Users/houseofobi/Documents/GitHub

# Clone the empty repo
git clone https://github.com/yourusername/mula-dasha-timer-api.git
cd mula-dasha-timer-api

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Create initial folder structure
mkdir app
mkdir tests
touch app/__init__.py
touch app/main.py
touch requirements.txt
touch .env.example
touch .gitignore
touch Procfile
touch README.md
```

#### Step 3: Generate FastAPI Scaffold with Copilot (15 min)

**Open VS Code**

```bash
code .
```

**Open Copilot Chat** (Cmd+I or Ctrl+I)

**Copy & Paste This Prompt:**

```
Create a FastAPI Python 3.11 project scaffold for Vedic astrology API.

Project structure:
- app/
  - __init__.py (empty)
  - main.py (main app entry point)
  - models/
    - __init__.py (empty)
    - user.py (User model)
    - birth_chart.py (BirthChart model - create)
  - schemas/
    - __init__.py (empty)
    - (Pydantic schemas for API requests/responses)
  - routers/
    - __init__.py (empty)
    - auth.py (Auth endpoints - create later)
  - database.py (PostgreSQL connection setup)
  - config.py (Environment variables)
- tests/
  - __init__.py (empty)
  - conftest.py (pytest fixtures)
- requirements.txt (Python dependencies)
- .env.example (Template for environment variables)
- .gitignore (Version control exclusions)
- Procfile (Railway deployment configuration)
- README.md (Setup instructions)

Key features:
1. FastAPI setup with:
   - Pydantic v2 for validation
   - SQLAlchemy ORM
   - PostgreSQL adapter
   - JWT authentication (PyJWT + python-jose)
   - CORS middleware
   - Error handling

2. .env.example should include:
   DATABASE_URL=postgresql://user:password@localhost:5432/mula_db
   JWT_SECRET=your-secret-key-change-this
   ENVIRONMENT=development

3. requirements.txt should include:
   - fastapi
   - uvicorn
   - sqlalchemy
   - psycopg2-binary
   - pydantic
   - python-dotenv
   - pyjwt
   - python-jose
   - bcrypt
   - pytest
   - httpx

4. main.py should have:
   - FastAPI app initialization
   - CORS configuration
   - Health check endpoint: GET /health
   - Database connection setup
   - Router includes (will add later)

5. database.py should have:
   - PostgreSQL connection string from env
   - SQLAlchemy engine + session
   - Base model for ORM

6. Procfile for Railway:
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT

Output complete FastAPI project ready for:
- Local development: python3 -m uvicorn app.main:app --reload
- Railway deployment
- Feature development (we'll add endpoints)

Make it production-ready but not over-engineered.
```

#### Step 4: Review Generated Files (5 min)

Copilot shows generated code. Review:

- ✅ No secrets hardcoded
- ✅ CORS configured
- ✅ Database connection pooling
- ✅ JWT setup
- ✅ Error handling

#### Step 5: Copy Generated Files to Project (10 min)

For each file Copilot generated:

1. Copy content
2. Create/update in your project
3. Match structure exactly

#### Step 6: Install Dependencies & Test Locally (15 min)

```bash
# Activate virtual environment (if not already)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env.local with test database
cp .env.example .env.local

# For local testing, you can use SQLite temporarily:
# DATABASE_URL=sqlite:///./test.db

# Test the app
python3 -m uvicorn app.main:app --reload

# Should see output like:
# Uvicorn running on http://127.0.0.1:8000
# Press CTRL+C to quit

# In another terminal, test health check:
curl http://localhost:8000/health

# Should return: {"status": "ok"} or similar
```

#### Step 7: Commit to GitHub (5 min)

```bash
# Add .gitignore
echo "venv/" >> .gitignore
echo ".env.local" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".pytest_cache/" >> .gitignore
echo "*.pyc" >> .gitignore

# Stage files
git add .

# Commit
git commit -m "Initial FastAPI scaffold for Mula Dasha Timer API"

# Push
git push -u origin main
# (or 'master' if default branch is master)
```

#### Step 8: Deploy to Railway (15 min)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login
# Opens browser to authenticate with GitHub

# Navigate to backend project directory
cd /Users/houseofobi/Documents/GitHub/mula-dasha-timer-api

# Link project to Railway
railway init

# When prompted:
# - "Would you like to start a new project?" → Y
# - "Project name?" → mula-dasha-timer-api
# - "Create and deploy?" → Y (if asked)

# Add PostgreSQL database to Railway
railway add --plugin postgres

# Follow prompts to create PostgreSQL instance

# Create railway.json (if needed)
# Railway should auto-detect Python project

# Deploy
railway up
# Wait... this deploys your code

# Get your Railway app URL
railway status

# Or view in Railway dashboard: railway.app
# URL will be like: https://mula-api-prod.railway.app (specific to your project)
```

**Save this URL: This is your BACKEND production API URL**

#### Step 9: Test Production Deployment (5 min)

```bash
# Test health check on production
curl https://mula-api-prod.railway.app/health
# Should return: {"status": "ok"}

# Verify no errors:
# - No 500 errors
# - Health check responds quickly
# - Database connected (check Railway dashboard logs)
```

#### Step 10: Get Database Connection String (5 min)

In Railway dashboard:

1. Click your PostgreSQL plugin
2. Copy connection string (looks like: `postgresql://...`)
3. Add to Railway secrets: `DATABASE_URL=...`
4. Backend will automatically use it

**✅ BACKEND DONE**

---

## 🎯 ACCEPTANCE CRITERIA

### Frontend

- [ ] Repo created on GitHub
- [ ] Next.js project deployed on Vercel
- [ ] Vercel URL accessible (shows home page)
- [ ] No 404 errors
- [ ] Mobile responsive
- [ ] Dark mode works (if included)
- [ ] Ready for auth pages (next todo)

### Backend

- [ ] Repo created on GitHub
- [ ] FastAPI project deployed on Railway
- [ ] Railway URL accessible
- [ ] Health check returns 200 OK
- [ ] PostgreSQL database connected
- [ ] Ready for auth endpoints (next todo)

### Both

- [ ] GitHub repos linked to deployments (auto-deploy on push)
- [ ] .env files created locally
- [ ] Environment variables configured
- [ ] Both URLs documented (save them!)

---

## 📝 DOCUMENTATION: Save These URLs

Create a file `MILESTONE1_DEPLOYMENT_URLS.txt`:

```
FRONTEND (Vercel)
URL: https://mula-dasha-timer-web.vercel.app
GitHub: https://github.com/yourusername/mula-dasha-timer-web
Local: http://localhost:3000
Build: npm run build
Deploy: git push origin main (auto)

BACKEND (Railway)
URL: https://mula-api-prod.railway.app
GitHub: https://github.com/yourusername/mula-dasha-timer-api
Local: http://localhost:8000 (python3 -m uvicorn app.main:app --reload)
Database: PostgreSQL (on Railway)
Deploy: git push origin main (auto)

Environment Variables:
Frontend (.env.local):
- NEXT_PUBLIC_API_URL=https://mula-api-prod.railway.app

Backend (Railway Secrets):
- DATABASE_URL=[PostgreSQL connection string]
- JWT_SECRET=[Your secret key]
```

---

## ⏱️ TIME ESTIMATE

```
Frontend Setup:
- Create repo: 5 min
- Local project: 10 min
- Copilot scaffold: 15 min
- Review: 5 min
- Copy files: 10 min
- Test locally: 15 min
- GitHub commit: 5 min
- Vercel deploy: 10 min
- Prod test: 5 min
TOTAL: ~90 min (1.5 hours)

Backend Setup:
- Create repo: 5 min
- Local project: 10 min
- Copilot scaffold: 15 min
- Review: 5 min
- Copy files: 10 min
- Install deps: 5 min
- Test locally: 10 min
- GitHub commit: 5 min
- Railway deploy: 15 min
- Prod test: 5 min
TOTAL: ~85 min (1.5 hours)

COMBINED: 2-3 hours total
```

---

## ✅ YOU'RE READY

You have:

- ✅ Copilot prompts (copy-paste ready)
- ✅ Step-by-step instructions
- ✅ Checkboxes to track progress
- ✅ Time estimates

Next action:

1. **Open Terminal**
2. **Navigate to workspace**: `cd /Users/houseofobi/Documents/GitHub`
3. **Start with Frontend**: Create GitHub repo `mula-dasha-timer-web`
4. **Follow steps A1-A10 above**
5. **Then Backend**: Create GitHub repo `mula-dasha-timer-api`
6. **Follow steps B1-B10 above**
7. **By tonight**: Both deployed + working

---

**Go time. Start with creating the frontend GitHub repo right now.**
