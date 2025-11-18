# Visual Guide: Frontend Backend Integration

## 📁 File Structure Created

```
frontend/
├── src/
│   ├── services/
│   │   ├── auth.ts ✨ NEW
│   │   │   ├── AuthService class (180 lines)
│   │   │   ├── register(email, password, firstName, lastName)
│   │   │   ├── login(email, password)
│   │   │   ├── getAccessToken()
│   │   │   ├── getCurrentUser()
│   │   │   ├── isAuthenticated()
│   │   │   └── logout()
│   │   │
│   │   └── chart.ts ✨ NEW
│   │       ├── ChartService class (85 lines)
│   │       ├── generateChart(birthData)
│   │       └── getChart(chartId)
│   │
│   └── app/
│       ├── auth/
│       │   └── login/
│       │       ├── page.tsx ✨ NEW (150 lines)
│       │       │   ├── Dual-mode login/register
│       │       │   ├── Form validation
│       │       │   ├── Success/error messages
│       │       │   └── Demo credentials display
│       │       │
│       │       └── login.css ✨ NEW (200 lines)
│       │           ├── Form styling
│       │           ├── Responsive design
│       │           ├── Design tokens integration
│       │           └── Animations
│       │
│       └── readings/
│           └── new/
│               └── page.tsx 🔄 UPDATED
│                   ├── Auth check on mount
│                   ├── Real API integration
│                   ├── Error handling
│                   └── Real chart data display
```

## 🔐 Authentication Flow (User's Perspective)

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER JOURNEY                                │
└─────────────────────────────────────────────────────────────────┘

REGISTRATION:
┌───────────────┐
│ Landing Page  │
│   (Public)    │
└───────┬───────┘
        │ Click "Start Reading"
        ↓
┌──────────────────────┐
│   /auth/login Page   │
│  (Default: Login)    │
└───────┬──────────────┘
        │ Click "Sign Up"
        ↓
┌──────────────────────────────────────────────┐
│         Registration Form                    │
│  ├─ Email: test@example.com                  │
│  ├─ First Name: John                         │
│  ├─ Last Name: Doe                           │
│  ├─ Password: StrongPass123                  │
│  └─ [Create Account]                         │
└───────┬────────────────────────────────────────┘
        │ ✅ Account created, tokens stored
        │ ✅ Auto-redirect 1.5 seconds
        ↓
┌──────────────────────────────────┐
│   /readings/new Chart Page       │
│  (Protected: Auth Required)      │
│                                  │
│  ├─ User: John Doe               │
│  ├─ Birth data form ready        │
│  └─ [Generate Chart] button      │
└──────────────────────────────────┘


LOGIN:
┌───────────────┐
│ Landing Page  │
│   (Public)    │
└───────┬───────┘
        │ Click "Sign In"
        ↓
┌──────────────────────────────────────────────┐
│         Login Form                           │
│  ├─ Email: laplace@mula.app                  │
│  ├─ Password: Mula2025!Astrology             │
│  └─ [Sign In]                                │
└───────┬────────────────────────────────────────┘
        │ ✅ Auth successful, tokens stored
        │ ✅ Auto-redirect 1.5 seconds
        ↓
┌──────────────────────────────────┐
│   /readings/new Chart Page       │
│  (Protected: Auth Required)      │
│                                  │
│  ├─ User: Laplace                │
│  ├─ Birth data form ready        │
│  └─ [Generate Chart] button      │
└──────────────────────────────────┘
```

## 📡 API Communication Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                    FRONTEND ↔ BACKEND                             │
└──────────────────────────────────────────────────────────────────┘

LOGIN/REGISTER:
┌────────────────┐                    ┌──────────────────┐
│  Login Page    │                    │  Backend Port    │
│  :3001/auth    │                    │  8001            │
└───────┬────────┘                    └────────┬─────────┘
        │                                      │
        │ 1. User submits form                │
        ├─────────────────────────────────────→│
        │  POST /api/v1/auth/register or       │
        │       /api/v1/auth/login             │
        │  {email, password, first_name, ...}  │
        │                                      │
        │                            2. Validate
        │                            3. Create user OR
        │                               find user
        │                            4. Generate JWT
        │                                      │
        │ 5. Response with tokens ←──────────┤
        │←─────────────────────────────────────│
        │  200 OK {access_token, refresh_token}
        │                                      │
        └─ Store tokens in localStorage
        └─ Redirect to /readings/new
        └─ Set user session


CHART GENERATION:
┌────────────────────┐                ┌──────────────────┐
│  Chart Page        │                │  Backend Port    │
│  :3001/readings    │                │  8001            │
└───────┬────────────┘                └────────┬─────────┘
        │                                      │
        │ 1. User enters birth data            │
        │ 2. Click [Generate Chart]            │
        │                                      │
        │ 3. ChartService.generateChart()      │
        │    ├─ Get token from localStorage    │
        │    └─ Prepare request                │
        │                                      │
        ├─ POST /api/v1/chart ─────────────────→│
        │  Headers: {                          │
        │    Authorization: Bearer {token}     │ 4. Validate token
        │    Content-Type: application/json    │ 5. Get current user
        │  }                                   │ 6. Calculate chart
        │  Body: {                             │ 7. Store in DB
        │    birth_data: {                     │ 8. Return data
        │      birth_date,                     │
        │      birth_time,                     │
        │      latitude,                       │
        │      longitude,                      │
        │      timezone,                       │
        │      birth_location                  │
        │    }                                 │
        │  }                                   │
        │                                      │
        │ 9. Response with chart data ←───────┤
        │←─────────────────────────────────────│
        │  200 OK {chart_id, chart_data, ...}  │
        │                                      │
        └─ setChartData(real data)
        └─ ChartCanvas renders real birth chart
```

## 🔑 Token Lifecycle

```
REGISTRATION/LOGIN:
┌─────────────────────────────────────────────────────┐
│ Browser: http://localhost:3001/auth/login           │
│                                                      │
│ 1. User submits credentials                        │
│    ↓                                                 │
│ 2. AuthService.register() or login()               │
│    ↓                                                 │
│ 3. Backend sends back:                             │
│    - access_token (JWT)                            │
│    - refresh_token (JWT)                           │
│    - user data                                      │
│    ↓                                                 │
│ 4. AuthService.storeTokens()                       │
│    → localStorage['access_token'] = token          │
│    → localStorage['refresh_token'] = token         │
│    → localStorage['user'] = {...}                  │
│                                                      │
└─────────────────────────────────────────────────────┘

AUTHENTICATED REQUESTS:
┌─────────────────────────────────────────────────────┐
│ API Call: chartService.generateChart()              │
│                                                      │
│ 1. Get token from localStorage                      │
│    token = localStorage['access_token']             │
│                                                      │
│ 2. Add to request headers                           │
│    Authorization: `Bearer ${token}`                 │
│                                                      │
│ 3. Backend receives request                         │
│    - Validates token signature                      │
│    - Extracts user_id from token                   │
│    - Verifies token not expired                     │
│    - Generates chart for that user                 │
│                                                      │
│ 4. If valid → 200 OK with chart data               │
│    If expired → 401 Unauthorized                    │
│                ↓                                     │
│ 5. If 401:                                          │
│    - AuthService catches error                      │
│    - Calls authService.logout()                     │
│    - Clears localStorage                            │
│    - Shows: "Session expired. Please log in again"  │
│    - Redirects to /auth/login                       │
│                                                      │
└─────────────────────────────────────────────────────┘

LOGOUT:
┌─────────────────────────────────────────────────────┐
│ User clicks [Logout]                                │
│   ↓                                                  │
│ AuthService.logout()                               │
│   ├─ localStorage.removeItem('access_token')       │
│   ├─ localStorage.removeItem('refresh_token')      │
│   └─ localStorage.removeItem('user')               │
│   ↓                                                  │
│ Router redirects to /auth/login                     │
│   ↓                                                  │
│ Page loads, checks auth: isAuthenticated() = false  │
│ (because token missing from localStorage)           │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## 🛡️ Error Handling Tree

```
API Call → Error?
│
├─ NO → Success
│   └─ Update UI with response data
│
└─ YES → Check error type
    │
    ├─ Status 401 (Unauthorized)
    │   └─ Session expired
    │   └─ AuthService.logout()
    │   └─ Show: "Session expired. Please log in again."
    │   └─ Route to /auth/login
    │   └─ User must re-authenticate
    │
    ├─ Status 400 (Bad Request)
    │   └─ Invalid data submitted
    │   └─ Show: error.detail message
    │   └─ User can retry
    │
    ├─ Status 500 (Server Error)
    │   └─ Backend calculation error
    │   └─ Show: "Server error. Please try again."
    │   └─ User can retry or contact support
    │
    └─ Network Error
        └─ No internet or backend down
        └─ Show: "Connection error. Please check your internet."
        └─ User can retry when connection restored
```

## 💾 localStorage State Machine

```
┌─────────────────────────┐
│   INITIAL STATE         │
│  (Not Logged In)        │
│                         │
│  localStorage = {}      │
│                         │
│  isAuthenticated() = ❌ │
└────────┬────────────────┘
         │
         │ User registers/logs in
         ↓
┌─────────────────────────────────────┐
│   AUTHENTICATED STATE               │
│  (Logged In)                        │
│                                     │
│  localStorage = {                  │
│    'access_token': 'xyz...',       │
│    'refresh_token': 'abc...',      │
│    'user': '{...}'                 │
│  }                                  │
│                                     │
│  isAuthenticated() = ✅             │
└────────┬────────────────────────────┘
         │
         ├─ User refreshes page
         │  ↓
         │  ✅ Tokens still in localStorage
         │  ✅ User stays logged in
         │  ↓
         │  (Back to AUTHENTICATED STATE)
         │
         └─ User clicks logout
            ↓
┌─────────────────────────┐
│   LOGGED OUT STATE      │
│                         │
│  localStorage = {}      │
│  (all cleared)          │
│                         │
│  isAuthenticated() = ❌ │
└────────┬────────────────┘
         │
         │ User logs in again
         ↓
    AUTHENTICATED STATE...
```

## 📊 Component Communication

```
App Component Tree:
├── /
│   ├── Landing Page (public)
│   └── Link to /auth/login
│
├── /auth/login (public)
│   ├── LoginPage Component
│   ├── Uses: AuthService
│   ├─┬─ Login Mode
│   │ └─ Calls: authService.login()
│   └─┬─ Register Mode
│     └─ Calls: authService.register()
│
└── /readings/new (protected)
    ├── NewChartReadingPage Component
    ├── useEffect: Check auth
    │  ├─ authService.isAuthenticated()
    │  └─ If false → router.push('/auth/login')
    │
    ├── Form: Birth data input
    │
    ├── Button: Generate Chart
    │  └─ Calls: chartService.generateChart()
    │     ├─ ChartService gets token from localStorage
    │     ├─ Calls: fetch('/api/v1/chart', {
    │     │   Authorization: 'Bearer ' + token
    │     │ })
    │     └─ Returns: chart_data
    │
    └── ChartCanvas
        └─ Renders: Real chart data
```

## ✅ Testing Checklist

```
LOCAL TESTING:
□ Backend running on port 8001 (check http://localhost:8001/docs)
□ Frontend running on port 3001 (check terminal output)
□ Visit http://localhost:3001 - loads without errors
□ Click "Start" or navigate to /auth/login

REGISTRATION:
□ Click "Sign Up" tab
□ Fill in: email, first name, last name, password
□ Submit form
□ Success message appears (green bar)
□ Auto-redirect to /readings/new within 1.5 seconds
□ Tokens stored in localStorage (check DevTools → Storage)

LOGIN:
□ Logout (clear localStorage): localStorage.clear() in console
□ Visit /auth/login
□ Click "Sign In" tab
□ Fill in: laplace@mula.app and Mula2025!Astrology
□ Submit form
□ Success message appears
□ Auto-redirect to /readings/new

CHART GENERATION:
□ On /readings/new page
□ Form shows with pre-filled birth data
□ Click "✨ Generate Birth Chart"
□ Button shows "Calculating..." while loading
□ Chart displays with real data (not mock)
□ Check DevTools → Network:
  - Should see POST /api/v1/chart request
  - Status: 200 OK
  - Response includes chart_data

ERROR HANDLING:
□ Type wrong password → Error message shows
□ Clear tokens → Redirects to login automatically
□ Network offline → Friendly error message
□ Invalid birth data → Validation error shows
□ Session expired → "Please log in again" message

DESIGN:
□ Form styled with design tokens (cyan accents, modern look)
□ Responsive on mobile (test at 640px width)
□ All animations smooth (fade-in, slide-up)
□ Demo credentials visible in info box
□ No layout shifts or missing styles
```

## 🎯 Success Indicators

When everything works:
✅ Can register account
✅ Can login with registered account
✅ Can login with demo account
✅ Chart page shows real data (not mock)
✅ No console errors
✅ No network errors
✅ Responsive design works
✅ Token persists across page refresh
✅ Session expiration handled gracefully
✅ All forms styled consistently

---

**Everything is ready to test! Follow the flow above, and the integration will work seamlessly.**
