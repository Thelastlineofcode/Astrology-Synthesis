# BMAD AGENT PROMPT LIBRARY FOR MILESTONE 1

## Copy-Paste Ready - Direct To Your BMAD Agent Team

**Use this document**: Open each section, copy the prompt, paste into the appropriate BMAD agent chat

**Agent Reference**:

- `@backend-agent` - Backend/API development (FastAPI, Python, databases)
- `@frontend-agent` - Frontend/UI (Next.js, React, TypeScript, components)
- `@devops-agent` - Deployment, infrastructure, CI/CD (Railway, Vercel)
- `@qa-agent` - Testing, quality assurance, performance
- `@ai-agent` - AI/LLM integration, prompts, knowledge bases

---

## 📦 TODO #3: GITHUB REPOS & SKELETON DEPLOY

### PROMPT #3.1: Next.js Frontend Scaffold

**Copy this entire prompt and paste into @frontend-agent:**

```
@frontend-agent

Create a Next.js 16 project scaffold with:
- React 19 + TypeScript
- Tailwind CSS configured globally
- Shadcn/ui components library installed
- ESLint + Prettier configured
- Basic folder structure:
  - app/
    - auth/
      - signup/
      - login/
    - dashboard/
  - components/
  - lib/
  - styles/
- .env.example with required variables
- .gitignore configured
- Vercel deployment ready (vercel.json)
- package.json with all scripts

This is for Mula, an astrology platform focused on Dasha timer calculations.
Include a README with setup instructions.
```

**Your action**:

1. Copy prompt above
2. Open BMAD chat in Perplexity or your agent interface
3. Paste to @frontend-agent
4. Wait for response with generated files
5. Create new Next.js project: `npx create-next-app@latest mula-dasha-timer-web`
6. Copy @frontend-agent output into project
7. Run: `npm run dev`
8. Notify @devops-agent for Vercel deployment

---

### PROMPT #3.2: FastAPI Backend Scaffold

**Copy this entire prompt and paste into @backend-agent:**

```
@backend-agent

Create a FastAPI Python project scaffold with:
- Python 3.11 compatible
- Pydantic v2 models for validation
- SQLAlchemy ORM setup
- PostgreSQL connection pooling (psycopg2)
- JWT authentication (PyJWT + python-jose)
- CORS middleware configured (allow localhost:3000)
- Error handling + logging setup
- Folder structure:
  - app/
    - models/
    - schemas/
    - routers/
    - services/
    - database.py
    - config.py
    - main.py
  - tests/
  - .env.example
  - requirements.txt
  - Procfile (Railway deployment)

Features:
- Basic health check endpoint: GET /health
- JWT token creation + validation
- Database connection string from env
- Error handling middleware
- CORS for frontend

Include setup instructions in README.
```

**Your action**:

1. Copy prompt above
2. Open BMAD chat in Perplexity or your agent interface
3. Paste to @backend-agent
4. Wait for response with generated files
5. Create directory: `mkdir mula-dasha-timer-api && cd mula-dasha-timer-api`
6. Copy @backend-agent output files
7. Create venv: `python3 -m venv venv && source venv/bin/activate`
8. Install deps: `pip install -r requirements.txt`
9. Run: `python3 -m uvicorn app.main:app --reload`
10. Notify @devops-agent for Railway deployment

---

## 🔐 TODO #4: AUTH SYSTEM

### PROMPT #4.1: Next.js Signup Page

**Copy this entire prompt and paste into @frontend-agent:**

```
@frontend-agent

Create a React page component at app/auth/signup/page.tsx with:

Form fields:
- Email input (type="email")
- Password input (type="password", min 8 chars)
- Confirm Password input (must match password)
- Submit button ("Sign Up")
- Link to login page (/auth/login)

Validation:
- Email: valid email format (regex or validator)
- Password: minimum 8 characters
- Passwords: must match
- Show error messages for each field
- Disable submit button while submitting

API integration:
- On submit: POST to process.env.NEXT_PUBLIC_API_URL/api/v1/auth/signup
- Body: {email, password}
- Response: {user_id, email, token}
- On success: Save token to localStorage, redirect to /dashboard
- On error: Show error message

Styling:
- Tailwind CSS
- Dark mode support
- Mobile responsive
- Professional looking form
- Center aligned on page

Include:
- Loading spinner while submitting
- Success message before redirect
- Link to "Already have an account? Login"
- Accessibility labels (for each input)

Don't use any external auth libraries (we'll use custom JWT).
```

**Your action**:

1. Copy prompt
2. Paste into @frontend-agent chat
3. Wait for component code
4. Create `app/auth/signup/page.tsx`
5. Copy @frontend-agent output
6. Test locally: `npm run dev` → go to http://localhost:3000/auth/signup
7. Verify form renders + validation works

---

### PROMPT #4.2: Next.js Login Page

**Copy this entire prompt and paste into @frontend-agent:**

```
@frontend-agent

Create a React page component at app/auth/login/page.tsx with:

Form fields:
- Email input (type="email")
- Password input (type="password")
- Remember me checkbox
- Submit button ("Log In")
- Link to signup page (/auth/signup)
- Link to forgot password (disabled for now, just show link)

Validation:
- Email: valid email format
- Password: required (not empty)
- Show error messages for each field
- Disable submit button while submitting

API integration:
- On submit: POST to process.env.NEXT_PUBLIC_API_URL/api/v1/auth/login
- Body: {email, password}
- Response: {user_id, email, token}
- On success: Save token to localStorage, redirect to /dashboard
- On error: Show error message (e.g., "Invalid credentials")

Styling:
- Tailwind CSS
- Dark mode support
- Mobile responsive
- Professional looking form
- Center aligned on page
- Consistent styling with signup page

Include:
- Loading spinner while submitting
- Remember me functionality (optional, can ignore for now)
- Link to "Don't have an account? Sign up"
- Accessibility labels

Match the design/styling of the signup page.
```

**Your action**:

1. Copy prompt
2. Paste into @frontend-agent chat
3. Create `app/auth/login/page.tsx`
4. Copy @frontend-agent output
5. Test locally → go to http://localhost:3000/auth/login
6. Verify form renders + validation works

---

### PROMPT #4.3: React Auth Context Hook

**Copy this entire prompt and paste into @frontend-agent:**

```
@frontend-agent

Create a React hook file at app/context/AuthContext.tsx with:

Context:
- currentUser: {user_id, email} or null
- isLoggedIn: boolean
- loading: boolean
- error: string or null

Hook (useAuth):
- useAuth() returns {currentUser, isLoggedIn, loading, error, signup, login, logout}

Methods:
- signup(email, password)
  - Calls POST /api/v1/auth/signup
  - Saves token to localStorage as "mula_token"
  - Sets currentUser
  - Returns {success, error}

- login(email, password)
  - Calls POST /api/v1/auth/login
  - Saves token to localStorage as "mula_token"
  - Sets currentUser
  - Returns {success, error}

- logout()
  - Removes token from localStorage
  - Clears currentUser
  - Redirects to /auth/login

- refreshAuthOnPageLoad()
  - Runs on app mount
  - Checks for token in localStorage
  - If token exists, verify it's valid
  - If valid, restore currentUser
  - If invalid, remove token

Error handling:
- Catch network errors
- Catch API errors (401, 422, etc)
- Set error message for display

Persistence:
- Save token to localStorage["mula_token"]
- Load token on app mount
- Remove token on logout

Use React Context API (not Redux).
API base URL from: process.env.NEXT_PUBLIC_API_URL
```

**Your action**:

1. Copy prompt
2. Paste into @frontend-agent chat
3. Create `app/context/AuthContext.tsx`
4. Copy @frontend-agent output
5. Wrap your app in AuthProvider (in `app/layout.tsx`)

---

### PROMPT #4.4: FastAPI Signup Endpoint

**Copy this entire prompt and paste into @backend-agent:**

```
@backend-agent

Create a FastAPI POST endpoint at app/routers/auth.py that:

Route: POST /api/v1/auth/signup

Request body (JSON):
{
  "email": "user@example.com",
  "password": "password123"
}

Validation:
- Email: valid email format, not already in database
- Password: minimum 8 characters
- Return 422 if validation fails

Processing:
- Hash password using bcrypt (use bcrypt.hashpw)
- Create new User in database with:
  - id (UUID)
  - email
  - password_hash
  - created_at (now)
  - is_active (true)
- Generate JWT token (expire in 24 hours)
- Use SECRET_KEY from environment variable

Response on success (200):
{
  "user_id": "uuid-string",
  "email": "user@example.com",
  "token": "jwt-token-string",
  "created_at": "2025-11-05T12:00:00Z"
}

Error responses:
- 409 Conflict: if email already exists (message: "Email already registered")
- 422 Unprocessable Entity: if validation fails
- 500 Internal Server Error: if database error

Dependencies:
- SQLAlchemy for database
- bcrypt for password hashing
- PyJWT for token generation
- Pydantic for validation

Include proper error messages and logging.
```

**Your action**:

1. Copy prompt
2. Paste into @backend-agent chat
3. Create `app/routers/auth.py`
4. Copy @backend-agent output
5. Update `app/main.py` to include: `app.include_router(auth.router)`
6. Test:

```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}'
```

---

### PROMPT #4.5: FastAPI Login Endpoint

**Copy this entire prompt and paste into @backend-agent:**

```
@backend-agent

Create a FastAPI POST endpoint at app/routers/auth.py that:

Route: POST /api/v1/auth/login

Request body (JSON):
{
  "email": "user@example.com",
  "password": "password123"
}

Processing:
- Look up user by email in database
- If not found: return 404 with message "User not found"
- If found: verify password using bcrypt
- If password wrong: return 401 with message "Invalid credentials"
- If password correct: generate JWT token (expire 24 hours)

Response on success (200):
{
  "user_id": "uuid-string",
  "email": "user@example.com",
  "token": "jwt-token-string"
}

Error responses:
- 404 Not Found: user not found
- 401 Unauthorized: password incorrect
- 422 Unprocessable Entity: validation error
- 500 Internal Server Error: database error

Dependencies:
- SQLAlchemy for database queries
- bcrypt for password verification
- PyJWT for token generation

Include proper error messages and logging.
This endpoint should be in app/routers/auth.py (same file as signup).
```

**Your action**:

1. Copy prompt
2. Paste into @backend-agent chat
3. Add to `app/routers/auth.py`
4. Test:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123"}'
```

---

## 📋 TODO #5: BIRTH CHART FORM

### PROMPT #5.1: Birth Chart Form Component

**Copy this entire prompt and paste into @frontend-agent:**

```
@frontend-agent

Create a React page component at app/birth-chart/new/page.tsx with:

Form fields:
- Birth date:
  - Day dropdown (1-31)
  - Month dropdown (Jan-Dec)
  - Year dropdown (1900-2025)
- Birth time:
  - Hour dropdown (0-23)
  - Minute dropdown (0-59, increment 5)
  - AM/PM selector (for 12-hour format)
- Birth location:
  - Text input with autocomplete
  - Autocomplete suggestions from Google Places API or similar
  - Show: City, State/Province, Country
  - On select: Extract latitude + longitude

Validation:
- Birth date: cannot be in the future
- Birth date: must be reasonable (after 1900)
- Birth location: must be selected from autocomplete (not free text)
- Show error messages for invalid fields

API integration:
- On submit: POST to process.env.NEXT_PUBLIC_API_URL/api/v1/birth-charts
- Headers: Authorization: Bearer {token from localStorage["mula_token"]}
- Body: {birth_date, birth_time, location, latitude, longitude}
- On success: Show "Birth chart saved!" then redirect to /dashboard
- On error: Show error message

Styling:
- Tailwind CSS
- Dark mode support
- Mobile responsive
- Professional form layout
- Consistent with auth pages

Include:
- Loading spinner while submitting
- Form validation messages
- Link to go back to dashboard
- Accessibility labels
- Submit button disabled while submitting or if validation fails

Use @react-aria/combobox or similar for autocomplete.
```

**Your action**:

1. Copy prompt
2. Paste into @frontend-agent chat
3. Create `app/birth-chart/new/page.tsx`
4. Copy @frontend-agent output
5. Test locally
6. Note: May need to add Google Places API key to .env

---

### PROMPT #5.2: FastAPI Birth Chart Storage

**Copy this entire prompt and paste into @backend-agent:**

```
@backend-agent

Create SQLAlchemy models at app/models/birth_chart.py with:

Model: BirthChart
- id (UUID primary key)
- user_id (UUID foreign key to User)
- birth_date (date)
- birth_time (time)
- location (string, e.g., "New York, NY, USA")
- latitude (float)
- longitude (float)
- created_at (datetime)
- updated_at (datetime)
- Indexes: (user_id), (user_id, created_at)

And create FastAPI endpoints at app/routers/birth_charts.py:

Endpoint 1: POST /api/v1/birth-charts (Create birth chart)
- Requires JWT auth (extract user_id from token)
- Request body: {birth_date, birth_time, location, latitude, longitude}
- Validates all fields required
- Creates BirthChart in database
- Returns 201: {chart_id, user_id, birth_date, birth_time, location}
- Error 401: Unauthorized (invalid token)
- Error 422: Validation error

Endpoint 2: GET /api/v1/birth-charts (List user's charts)
- Requires JWT auth
- Returns list of all charts for authenticated user
- Order by created_at desc
- Return 200: [{chart_id, birth_date, birth_time, location}, ...]
- Error 401: Unauthorized

Endpoint 3: GET /api/v1/birth-charts/{chart_id} (Get specific chart)
- Requires JWT auth
- Returns specific chart if user owns it
- Return 200: {chart_id, birth_date, birth_time, location, latitude, longitude}
- Error 401: Unauthorized
- Error 404: Chart not found

Include:
- Proper JWT token validation (extract user_id from token)
- Database error handling
- Logging for debugging
```

**Your action**:

1. Copy prompt
2. Paste into @backend-agent chat
3. Create `app/models/birth_chart.py`
4. Create `app/routers/birth_charts.py`
5. Update `app/main.py` to include router
6. Run database migration
7. Test endpoints with token

---

## 🌙 TODO #6: DASHA DISPLAY & TIMER

### PROMPT #6.1: Dasha Display Component

**Copy this entire prompt and paste into @frontend-agent:**

```
@frontend-agent

Create a React component at app/components/DashaDisplay.tsx that:

Props:
- dasha: {current_dasha, period_start, period_end, meaning}
- Example: {current_dasha: "Jupiter Dasha", period_start: "2023-01-15", period_end: "2033-01-15", meaning: "Growth and expansion..."}

Display:
- Heading: "Current Dasha"
- Mahadasha name (e.g., "Jupiter Dasha") - large, bold
- Period: "Start date - End date"
- Time remaining (calculated from end date to today)
- Meaning/interpretation (text, 2-3 sentences)
- Progress bar showing % of period completed
- Next dasha preview (optional: show name of next dasha)

Visual:
- Card layout with Tailwind
- Color coding by planet (Mercury=blue, Venus=pink, Mars=red, Jupiter=gold, Saturn=grey, etc.)
- Dark mode support
- Icons for each planet (optional)
- Responsive on mobile

No API calls (data comes from parent via props).
```

**Your action**:

1. Copy prompt
2. Paste into @frontend-agent chat
3. Create `app/components/DashaDisplay.tsx`
4. Copy @frontend-agent output
5. Will use in dashboard component

---

### PROMPT #6.2: Dasha Timer Component

**Copy this entire prompt and paste into @frontend-agent:**

```
@frontend-agent

Create a React component at app/components/DashaTimer.tsx that:

Purpose: Show real-time countdown to next dasha change

Props:
- dasha_end_date: ISO string (e.g., "2033-01-15T00:00:00Z")

Display:
- Shows current time (updates every second)
- Shows time remaining until dasha end
- Format: "X years, Y months, Z days remaining"
- Or: "X months, Y days remaining" (depending on remaining time)
- Or: "X days remaining" (if less than 1 month)

Functionality:
- setInterval to update every second
- useEffect to clean up interval on unmount
- Calculate remaining time: dasha_end_date - currentTime
- Format nicely for display

Visual:
- Tailwind CSS
- Large, easy-to-read display
- Dark mode support
- Animated (optional: pulse or fade effect)
- Show as: "Next dasha in: X years Y months Z days"

Example output:
"Next dasha in: 8 years 2 months 10 days"
```

**Your action**:

1. Copy prompt
2. Paste into @frontend-agent chat
3. Create `app/components/DashaTimer.tsx`
4. Copy @frontend-agent output
5. Test locally (verify updates every second)

---

### PROMPT #6.3: Dashboard Page with Dasha

**Copy this entire prompt and paste into @frontend-agent:**

```
@frontend-agent

Create a React page component at app/dashboard/page.tsx with:

Features:
- Requires JWT auth (redirect to login if not authenticated)
- Displays user's selected birth chart
- Shows current dasha (using DashaDisplay component)
- Shows countdown timer (using DashaTimer component)
- Action buttons: "Add new chart", "Settings", "Logout"

Layout:
- Header with user email + logout button
- Main content area showing current dasha
- DashaDisplay component (centered)
- DashaTimer component (below dasha display)
- Buttons: "Add new chart" (link to /birth-chart/new), "Settings"
- Footer with links

Data flow:
- On mount:
  - Check if user authenticated (token in localStorage["mula_token"])
  - Fetch user's latest birth chart from GET /api/v1/birth-charts
  - Fetch current dasha from GET /api/v1/dasha/{chart_id}
  - Display data in components
- Loading state while fetching
- Error state if fetch fails

Styling:
- Tailwind CSS
- Dark mode support
- Mobile responsive
- Professional dashboard layout

Include:
- Loading spinner while fetching
- Error message if data fetch fails
- Logout functionality (clear token, redirect to /auth/login)
- Accessibility labels
Use: process.env.NEXT_PUBLIC_API_URL for API base URL
```

**Your action**:

1. Copy prompt
2. Paste into @frontend-agent chat
3. Create `app/dashboard/page.tsx`
4. Copy @frontend-agent output
5. Update imports to use DashaDisplay and DashaTimer components
6. Test locally

---

### PROMPT #6.4: FastAPI Dasha Calculation Endpoint

**Copy this entire prompt and paste into @backend-agent:**

```
@backend-agent

Create a FastAPI endpoint at app/routers/dasha.py that:

Route: GET /api/v1/dasha/{chart_id}

Purpose: Calculate and return current dasha period for a birth chart

Processing:
- Extract user_id from JWT token
- Verify user owns the chart_id
- Fetch birth chart from database (date, time, longitude)
- Call existing dasha calculation function from your codebase
  - Function should calculate current mahadasha, antardasha, etc.
  - Returns: {mahadasha, mahadasha_start, mahadasha_end, antardasha, antardasha_start, antardasha_end}
- Format response

Response on success (200):
{
  "current_dasha": "Jupiter Dasha",
  "period_start": "2023-01-15",
  "period_end": "2033-01-15",
  "meaning": "Jupiter represents growth, expansion, wisdom. This is a favorable period for learning and expansion.",
  "antardasha": "Sun Antardasha",
  "antardasha_end": "2025-06-15"
}

Error responses:
- 401: Unauthorized (invalid token)
- 404: Chart not found or user doesn't own chart
- 500: Calculation error

Caching:
- Cache result for 24 hours (same user, same chart should return cached result)
- Use simple in-memory cache or Redis

Include:
- Proper JWT validation
- Error handling
- Logging
- Call to existing dasha calculation function
```

**Your action**:

1. Locate existing dasha calculation function in your codebase
2. Note the function name and path
3. Copy prompt (modify function name if needed)
4. Paste into @backend-agent chat
5. Create `app/routers/dasha.py`
6. Update `app/main.py` to include router
7. Test endpoint

---

## 📧 TODO #7: NOTIFICATIONS

### PROMPT #7.1: Notification Settings Component

**Copy this entire prompt and paste into @frontend-agent:**

```
@frontend-agent

Create a React component at app/components/NotificationSettings.tsx with:

Purpose: Let users control notification preferences

Form fields:
- Toggle: "Email notifications" (ON/OFF)
- Dropdown: Notification frequency
  - Options: "Daily", "Weekly", "Monthly", "Never"
- Submit button: "Save preferences"

Functionality:
- Requires JWT auth
- On mount: Fetch current preferences from GET /api/v1/notifications/preferences
- Show loading state while fetching
- On change: Update local state
- On submit: POST to /api/v1/notifications/subscribe or /api/v1/notifications/unsubscribe
- Show success/error message

Visual:
- Card layout with Tailwind
- Dark mode support
- Mobile responsive
- Clear labels and descriptions

Headers:
- Include: Authorization: Bearer {token from localStorage["mula_token"]}

Example flow:
1. User opens settings
2. Component fetches current preferences
3. User toggles "Email notifications" to OFF
4. User clicks "Save"
5. Component sends POST /api/v1/notifications/unsubscribe
6. Success message shown
API base URL: process.env.NEXT_PUBLIC_API_URL
```

**Your action**:

1. Copy prompt
2. Paste into @frontend-agent chat
3. Create `app/components/NotificationSettings.tsx`
4. Copy @frontend-agent output
5. Add to settings page

---

### PROMPT #7.2: FastAPI Notification Endpoints

**Copy this entire prompt and paste into @backend-agent:**

```
@backend-agent

Create FastAPI endpoints at app/routers/notifications.py for:

Endpoint 1: POST /api/v1/notifications/subscribe
- Requires JWT auth
- Sets user.notification_enabled = true in database
- Returns 200: {message: "Notifications enabled"}
- Error 401: Unauthorized

Endpoint 2: POST /api/v1/notifications/unsubscribe
- Requires JWT auth
- Sets user.notification_enabled = false in database
- Returns 200: {message: "Notifications disabled"}
- Error 401: Unauthorized

Endpoint 3: GET /api/v1/notifications/preferences
- Requires JWT auth
- Returns 200: {notification_enabled: boolean, frequency: "daily" or "weekly"}
- Error 401: Unauthorized

Background Task (APScheduler):
- Create function check_and_send_dasha_notifications()
- Runs every day at UTC midnight
- For each user where notification_enabled = true:
  - Get user's birth charts
  - For each chart, check if dasha has changed since last check
  - If changed: Send email via SendGrid
- Schedule: APScheduler with CronTrigger (every day at 00:00 UTC)

Error handling:
- Catch SendGrid errors (log but don't crash)
- Catch database errors
- Log all sends for debugging

Include:
- Proper JWT validation
- Database updates
- SendGrid integration (will implement separately)
```

**Your action**:

1. Copy prompt
2. Paste into @backend-agent chat
3. Create `app/routers/notifications.py`
4. Update database schema: Add notification_enabled and notification_frequency to User model
5. Update `app/main.py` to include router and schedule background task
6. Test endpoints

---

### PROMPT #7.3: SendGrid Email Service

**Copy this entire prompt and paste into @backend-agent:**

```
@backend-agent

Create SendGrid integration at app/services/notifications.py with:

Function: send_dasha_change_email(user_email, new_dasha, start_date, end_date)
- Initialize SendGrid client using SENDGRID_API_KEY from environment
- Create email using SendGrid Mail API
- From email: noreply@mulaastro.app
- To email: user_email
- Subject: "Your Dasha has changed! {new_dasha} begins"
- HTML body: Use HTML template with:
  - Greeting: "Hi [name or just 'there']"
  - Main message: "Your Mahadasha has changed to {new_dasha}"
  - Period info: "Dasha period: {start_date} to {end_date}"
  - Meaning: Brief description of the new dasha
  - Link to app: "View your chart"
  - Footer with unsubscribe link
- Plain text body: Simple text version of HTML
- Send email
- Return: {success: boolean, message: string}

Error handling:
- Try/catch SendGrid errors
- Log errors but don't crash
- Return {success: false, message: error message}

Example usage:
send_dasha_change_email("user@example.com", "Jupiter Dasha", "2023-01-15", "2033-01-15")

Include:
- Constants for SendGrid settings
- Clean HTML email template
- Error logging
```

**Your action**:

1. Get SendGrid API key (signup at sendgrid.com, free tier: 100/day)
2. Add to Railway secrets: SENDGRID_API_KEY
3. Copy prompt
4. Paste into @backend-agent chat
5. Create `app/services/notifications.py`
6. Test with: `send_dasha_change_email("test@example.com", "Jupiter Dasha", "2023-01-15", "2033-01-15")`

---

## ✅ TODO #8: TESTING & DEPLOY

### PROMPT #8.1: Backend Unit Tests (Auth)

**Copy this entire prompt and paste into @qa-agent:**

```
@qa-agent

Create pytest tests at tests/test_auth.py for auth endpoints:

Test signup endpoint:
- test_signup_success: Valid email + password → 201, returns user + token
- test_signup_invalid_email: Invalid email format → 422
- test_signup_weak_password: Password < 8 chars → 422
- test_signup_duplicate_email: Email already exists → 409
- test_signup_passwords_dont_match: Confirm password doesn't match → 422

Test login endpoint:
- test_login_success: Valid email + password → 200, returns token
- test_login_user_not_found: Email doesn't exist → 404
- test_login_wrong_password: Correct email, wrong password → 401

Setup:
- Use pytest fixtures for test database setup/teardown
- Use TestClient from FastAPI for making requests
- Clean database between tests

Example test:
```

def test_signup_success(client, db):
response = client.post("/api/v1/auth/signup", json={
"email": "test@example.com",
"password": "password123"
})
assert response.status_code == 201
data = response.json()
assert "token" in data
assert data["email"] == "test@example.com"

```

Run tests with: pytest tests/test_auth.py
```

**Your action**:

1. Copy prompt
2. Paste into @qa-agent chat
3. Create `tests/test_auth.py`
4. Create `tests/conftest.py` with fixtures
5. Run: `pytest tests/test_auth.py`
6. Fix any failures

---

### PROMPT #8.2: Frontend Component Tests

**Copy this entire prompt and paste into @qa-agent:**

```
@qa-agent

Create Jest tests at src/__tests__/auth.test.tsx for React components:

Test SignupPage component:
- test_signup_form_renders: Form with email + password fields renders
- test_signup_validation: Empty email shows error
- test_signup_weak_password: Password < 8 chars shows error
- test_signup_submit: Form submits and calls API

Test LoginPage component:
- test_login_form_renders: Form renders
- test_login_empty_email: Shows error if email empty
- test_login_submit: Form submits and calls API
- test_login_error: Shows error if login fails

Use:
- React Testing Library
- jest-mock-axios for API mocking
- @testing-library/user-event for user interactions

Example:
```

import { render, screen, fireEvent } from '@testing-library/react';
import SignupPage from '@/app/auth/signup/page';

test('signup form renders', () => {
render(<SignupPage />);
expect(screen.getByText('Sign Up')).toBeInTheDocument();
});

```

Run tests with: npm run test
```

**Your action**:

1. Copy prompt
2. Paste into @qa-agent chat
3. Create `src/__tests__/auth.test.tsx`
4. Run: `npm run test`
5. Fix any failures

---

### PROMPT #8.3: E2E Tests (Playwright)

**Copy this entire prompt and paste into @qa-agent:**

```
@qa-agent

Create Playwright E2E tests at e2e/auth-flow.spec.ts for full user flow:

Test full signup → login → dashboard flow:
- test_user_signup:
  1. Navigate to /auth/signup
  2. Fill email: "test-user@example.com"
  3. Fill password: "TestPassword123"
  4. Fill confirm password: "TestPassword123"
  5. Click submit
  6. Verify redirected to /dashboard
  7. Verify user email shown

- test_user_login:
  1. Navigate to /auth/login
  2. Fill email: "test-user@example.com"
  3. Fill password: "TestPassword123"
  4. Click submit
  5. Verify redirected to /dashboard

- test_add_birth_chart:
  1. Navigate to /dashboard
  2. Click "Add new chart"
  3. Fill birth date: 01/15/1990
  4. Fill birth time: 10:30 AM
  5. Fill location: "New York, NY, USA"
  6. Click submit
  7. Verify success message
  8. Verify returned to dashboard

Use:
- page.goto() to navigate
- page.fill() to input form fields
- page.click() to click buttons
- page.waitForNavigation() to wait for navigation
- expect() for assertions

Run tests with: npx playwright test
```

**Your action**:

1. Copy prompt
2. Paste into @qa-agent chat
3. Create `e2e/auth-flow.spec.ts`
4. Update `playwright.config.ts` if needed
5. Run: `npx playwright test`
6. Fix any failures

---

### PROMPT #8.4: Production Deployment

**Copy this entire prompt and paste into @devops-agent:**

```
@devops-agent

Perform production deployment for Mula Dasha Timer MVP:

Frontend Deployment (Next.js on Vercel):
- [ ] All tests passing: npm run test
- [ ] Build succeeds: npm run build
- [ ] No console errors or warnings
- [ ] Lighthouse score > 85
- [ ] Environment variables set:
  - NEXT_PUBLIC_API_URL = production API URL
- [ ] Favicon configured
- [ ] Metadata correct (title, description)
- [ ] Deploy: git push to main (auto-deploys to Vercel)

Backend Deployment (FastAPI on Railway):
- [ ] All tests passing: pytest tests/
- [ ] No console errors or warnings
- [ ] Database migrations run: alembic upgrade head
- [ ] Environment variables set in Railway:
  - DATABASE_URL
  - JWT_SECRET
  - SENDGRID_API_KEY
- [ ] CORS configured for production domain
- [ ] Rate limiting enabled
- [ ] Error logging configured (Sentry)
- [ ] Deploy: git push (Railway auto-deploys)

Post-Deployment Testing:
- [ ] Frontend URL loads without errors
- [ ] Backend health check works: GET /health
- [ ] Can signup new user via production frontend
- [ ] Can login via production frontend
- [ ] JWT tokens valid
- [ ] Dasha calculations working
- [ ] Emails sending (test notification)
- [ ] Performance metrics logged (Lighthouse, Sentry)

Smoke Test:
- [ ] Full user flow on production: signup → login → add chart → view dasha
- [ ] No critical errors
- [ ] Page load <3 seconds
- [ ] Mobile responsive
```

**Your action**:

1. Copy prompt
2. Paste into @devops-agent chat
3. Get detailed deployment checklist and scripts
4. Follow steps
5. Test production URLs
6. Document URLs in MILESTONE1_DEPLOYMENT_COMPLETE.md

---

## 📖 REFERENCE: Copy-Paste Quick Links

When you need to generate code, just:

1. Scroll to the relevant prompt below
2. Copy the entire prompt text (including @agent mention)
3. Open BMAD chat in your agent interface (Perplexity, etc.)
4. Paste prompt
5. Wait for agent to generate code/response
6. Review + copy to your project

**Prompts by agent**:

### @frontend-agent Prompts (React/Next.js):

- #3.1: Next.js scaffold
- #4.1: Signup page
- #4.2: Login page
- #4.3: Auth context hook
- #5.1: Birth chart form
- #6.1: Dasha display component
- #6.2: Dasha timer component
- #6.3: Dashboard page
- #7.1: Notification settings UI

### @backend-agent Prompts (FastAPI/Python):

- #3.2: FastAPI scaffold
- #4.4: Signup endpoint
- #4.5: Login endpoint
- #5.2: Birth chart storage + endpoints
- #6.4: Dasha calculation endpoint
- #7.2: Notification endpoints
- #7.3: SendGrid email service

### @qa-agent Prompts (Testing):

- #8.1: Backend unit tests
- #8.2: Frontend component tests
- #8.3: E2E tests (Playwright)

### @devops-agent Prompts (Deployment):

- #8.4: Production deployment

---

## 🎯 WORKFLOW: Using BMAD Agents Daily

**Morning Setup**:

1. Read today's todo from MILESTONE1_AI_AGENT_ASSIGNMENTS.md
2. Note which agents to engage (@frontend-agent, @backend-agent, etc.)
3. Open BMAD chat interface

**For Each Feature**:

1. Find prompt in this library (e.g., #4.1 for signup)
2. Copy prompt (starts with @agent name)
3. Paste into BMAD agent chat
4. Agent generates code/response
5. Review code for quality, security, best practices
6. Copy to your project
7. Test locally
8. Deploy

**Parallel Work**:

- @frontend-agent works on UI components
- @backend-agent works on API endpoints
- @qa-agent prepares tests
- @devops-agent prepares deployment
- You review all outputs and make final decisions

**Example Daily Flow**:

```
9 AM:  Task: "Build signup page" (#4.1)
       → Copy prompt
       → Paste to @frontend-agent
       → Get React component code
       → Create app/auth/signup/page.tsx
       → Test locally
       → Commit

2 PM:  Task: "Build signup endpoint" (#4.4)
       → Copy prompt
       → Paste to @backend-agent
       → Get FastAPI endpoint code
       → Create app/routers/auth.py
       → Test with curl
       → Commit

5 PM:  Task: "Test signup flow" (#8.1)
       → Copy prompt
       → Paste to @qa-agent
       → Get test code
       → Create tests/test_auth.py
       → Run pytest
       → Fix any issues

Result: Feature complete, tested, deployed to production same day
```

---

## 💡 KEY TIPS FOR BMAD AGENTS

1. **Be Specific**: More detail → Better code. Include examples.
2. **Include Context**: Tell agent about your stack, naming conventions, requirements
3. **Ask for Explanations**: If something unclear, ask agent to explain
4. **Request Modifications**: If code doesn't fit, ask agent to adjust (simpler, add feature, etc.)
5. **Use Previous Work**: Reference earlier prompts when building on them
6. **Test Everything**: Agent code is good starting point, but you verify + test
7. **Ask for Best Practices**: Agent can advise on architecture, security, performance
8. **Provide Feedback**: If code has issues, paste error to agent for fixes

---

## 🚀 NEXT STEPS

**Ready to build**?

1. Start with **Prompt #3.1** (@frontend-agent): Next.js scaffold
2. Then **Prompt #3.2** (@backend-agent): FastAPI scaffold
3. Then **Prompt #4.1** (@frontend-agent): Signup page
4. Follow the sequence in MILESTONE1_AI_AGENT_ASSIGNMENTS.md

**Questions about a prompt**?

1. Check MILESTONE1_INDEX_NAVIGATION_GUIDE.md for navigation help
2. Review MILESTONE1_AI_AGENT_ASSIGNMENTS.md for detailed context
3. Reference AI_AGENT_TEAM.md for agent capabilities
4. Ask @ai-agent for help understanding requirements

**Having issues with generated code**?

1. Describe the issue to the relevant agent
2. Share the error message or problematic code
3. Agent can debug and suggest fixes
4. Or ask a different agent for second opinion

---

**Let's ship this MVP! 🚀**

Start with @frontend-agent right now → Prompt #3.1 → Next.js scaffold
