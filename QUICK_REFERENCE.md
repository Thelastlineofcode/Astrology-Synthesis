# 🎯 QUICK REFERENCE CARD

## Start Here

```bash
# Terminal 1: Start Backend
cd /Users/houseofobi/Documents/GitHub/Mula
PORT=8001 python -m uvicorn backend.main:app --reload

# Terminal 2: Start Frontend
cd /Users/houseofobi/Documents/GitHub/Mula/frontend
npm run dev

# Browser: Visit
http://localhost:3001/auth/login
```

---

## Test Registration

```
1. Click "Sign Up" tab
2. Enter:
   - Email: test@example.com
   - First Name: Test
   - Last Name: User
   - Password: TestPass123
3. Click "Create Account"
4. ✅ Success message appears
5. ✅ Auto-redirect to /readings/new
```

---

## Test Login

```
1. Clear localStorage: localStorage.clear() (in console)
2. Refresh page → redirects to login
3. Click "Sign In" tab
4. Enter:
   - Email: laplace@mula.app
   - Password: Mula2025!Astrology
5. Click "Sign In"
6. ✅ Success message appears
7. ✅ Auto-redirect to /readings/new
```

---

## Test Chart Generation

```
1. On /readings/new page
2. Form pre-filled with:
   - Date: Dec 19, 1984
   - Time: 12:00
   - Location: Metairie, LA
3. Click "✨ Generate Birth Chart"
4. ✅ Button shows "Calculating..."
5. ✅ Chart displays with REAL data (not mock)
6. ✅ Check DevTools → Network → /api/v1/chart (200 OK)
```

---

## Files at a Glance

| File                                      | Purpose                | Status     |
| ----------------------------------------- | ---------------------- | ---------- |
| `/frontend/src/services/auth.ts`          | Authentication service | ✅ Created |
| `/frontend/src/services/chart.ts`         | Chart generation API   | ✅ Created |
| `/frontend/src/app/auth/login/page.tsx`   | Login/register page    | ✅ Created |
| `/frontend/src/app/auth/login/login.css`  | Auth styling           | ✅ Created |
| `/frontend/src/app/readings/new/page.tsx` | Chart page             | ✅ Updated |

---

## API Endpoints

```
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "password": "ValidPass123",
  "first_name": "John",
  "last_name": "Doe"
}
→ 200 {access_token, refresh_token, user_id, ...}

POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "ValidPass123"
}
→ 200 {access_token, refresh_token, user_id, ...}

POST /api/v1/chart
Headers: Authorization: Bearer {access_token}
Body: {
  "birth_data": {
    "birth_date": "1984-12-19",
    "birth_time": "12:00:00",
    "birth_location": "Metairie, LA",
    "latitude": 29.9844,
    "longitude": -90.1547,
    "timezone": "America/Chicago"
  }
}
→ 200 {chart_id, chart_data, created_at, ...}
```

---

## Service Usage

```typescript
// Import
import authService from "@/services/auth";
import chartService from "@/services/chart";

// Register
const response = await authService.register(
  "email@example.com",
  "Password123",
  "John",
  "Doe"
);

// Login
const response = await authService.login("email@example.com", "Password123");

// Check if authenticated
if (authService.isAuthenticated()) {
  // User is logged in
}

// Get current user
const user = authService.getCurrentUser();

// Generate chart (auto-includes token)
const chart = await chartService.generateChart({
  birth_date: "1984-12-19",
  birth_time: "12:00:00",
  birth_location: "Metairie, LA",
  latitude: 29.9844,
  longitude: -90.1547,
  timezone: "America/Chicago",
});

// Logout
authService.logout();
```

---

## localStorage After Auth

```javascript
localStorage = {
  access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  refresh_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  user: '{"user_id":"xxx","email":"user@example.com",...}',
};
```

---

## Errors & Solutions

| Error                 | Solution                               |
| --------------------- | -------------------------------------- |
| Port 3001 in use      | `lsof -ti:3001 \| xargs kill`          |
| Port 8001 in use      | `lsof -ti:8001 \| xargs kill`          |
| "Not authenticated"   | Go to /auth/login, register/login      |
| "Session expired"     | Login again                            |
| Can't generate chart  | Verify backend running on :8001        |
| CORS error            | Check backend CORS config              |
| Chart shows mock data | Backend API call failed, check console |

---

## Keyboard Shortcuts in Browser

| Action               | Command                                                 |
| -------------------- | ------------------------------------------------------- |
| Open DevTools        | F12                                                     |
| See Network requests | F12 → Network tab                                       |
| See Console errors   | F12 → Console tab                                       |
| Clear localStorage   | Type in console: `localStorage.clear()`                 |
| Get token            | Type in console: `localStorage.getItem('access_token')` |

---

## Directories Explained

```
/Mula                          (Root)
├── /frontend                  (Next.js app)
│   └── /src
│       ├── /services          (auth.ts, chart.ts) ← NEW
│       └── /app
│           ├── /auth/login    (login page) ← NEW
│           └── /readings/new  (chart page) ← UPDATED
│
└── /backend                   (FastAPI)
    └── /api/v1
        ├── auth_endpoints.py  (used by frontend)
        └── charts.py          (used by frontend)
```

---

## Key Environment Variables

```
# /frontend/.env.local
PORT=3001                                    # Frontend port
NODE_ENV=development                         # Dev mode
NEXT_PUBLIC_API_URL=http://localhost:8001   # Backend URL
NEXT_PUBLIC_DEBUG=true                       # Debug logging
```

---

## Component Dependencies

```
LoginPage
├── AuthService (import)
├── useRouter (import)
└── Uses: authService.register() / login()

ChartPage
├── AuthService (import)
├── ChartService (import)
├── useRouter (import)
├── useEffect: check auth
└── Uses: chartService.generateChart()

AuthService
├── Stores tokens in localStorage
└── Provides: getAccessToken(), isAuthenticated()

ChartService
├── Gets token from AuthService
└── Calls: POST /api/v1/chart with Bearer token
```

---

## Debugging Checklist

- [ ] Backend running? Check http://localhost:8001/docs
- [ ] Frontend running? Check http://localhost:3001
- [ ] Can reach login page? http://localhost:3001/auth/login
- [ ] Form submits? Check DevTools → Network
- [ ] Tokens stored? Check DevTools → Storage → localStorage
- [ ] Chart API called? Check DevTools → Network → /api/v1/chart
- [ ] Real data displays? Check response in DevTools

---

## Success Indicators ✅

- ✅ No TypeScript errors
- ✅ Can register new account
- ✅ Can login with registered account
- ✅ Can login with demo account
- ✅ Chart page shows real data (not mock)
- ✅ Tokens persist in localStorage
- ✅ Stay logged in after page refresh
- ✅ Logout clears tokens
- ✅ Error messages appear for invalid input
- ✅ Responsive on mobile (test at 375px width)

---

## Next: Detailed Guides

For more detailed information, see:

- **[QUICK_START_TESTING.md](./QUICK_START_TESTING.md)** - Full testing guide (5 min)
- **[IMPLEMENTATION_DETAILS.md](./IMPLEMENTATION_DETAILS.md)** - Technical details (15 min)
- **[VISUAL_GUIDE.md](./VISUAL_GUIDE.md)** - Visual explanations (10 min)
- **[BACKEND_INTEGRATION_COMPLETE.md](./BACKEND_INTEGRATION_COMPLETE.md)** - Complete reference (10 min)

---

## Status: READY TO TEST 🚀

All code compiled with zero errors.
All services implemented.
All documentation complete.

**Next step**: Start terminal commands above and test!
