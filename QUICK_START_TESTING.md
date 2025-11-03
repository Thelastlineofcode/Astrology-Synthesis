# Quick Start: Testing the Backend Integration

## Prerequisites

- Backend running: `http://localhost:8001`
- Frontend running: `http://localhost:3001`
- Port configuration already set in `package.json` and `.env.local`

## Files Created

| File                                     | Purpose                                    | Lines |
| ---------------------------------------- | ------------------------------------------ | ----- |
| `/frontend/src/services/auth.ts`         | Authentication service with register/login | 180   |
| `/frontend/src/services/chart.ts`        | Chart generation API service               | 85    |
| `/frontend/src/app/auth/login/page.tsx`  | Login/Register UI page                     | 150   |
| `/frontend/src/app/auth/login/login.css` | Auth page styling                          | 200   |

## What Changed in Existing Files

### `/frontend/src/app/readings/new/page.tsx`

- ✅ Added authentication check on mount
- ✅ Redirects to `/auth/login` if not authenticated
- ✅ Integrated `chartService.generateChart()` into button handler
- ✅ Replaced alert() with real API call
- ✅ Now displays real chart data from backend instead of mock data
- ✅ Handles session expiration gracefully

## Testing Flow (Copy & Paste)

### Terminal 1: Start Backend

```bash
cd /Users/houseofobi/Documents/GitHub/Mula
PORT=8001 python -m uvicorn backend.main:app --reload
```

Expected output:

```
INFO:     Uvicorn running on http://127.0.0.1:8001
```

### Terminal 2: Start Frontend

```bash
cd /Users/houseofobi/Documents/GitHub/Mula/frontend
npm run dev
```

Expected output:

```
> next dev -p 3001
▲ Next.js 16.x
```

### Browser: Test Registration (http://localhost:3001/auth/login)

1. Page loads with login form
2. Click "Sign Up" tab
3. Fill in:
   - Email: `test@example.com`
   - First Name: `Test`
   - Last Name: `User`
   - Password: `TestPass123`
4. Click "Create Account"
5. Success message shows
6. Auto-redirects to `/readings/new` in 1.5 seconds

### Browser: Test Chart Generation (http://localhost:3001/readings/new)

1. Page loads with chart form
2. Default birth data pre-filled:
   - Date: Dec 19, 1984
   - Time: 12:00
   - Location: Metairie, LA
   - Lat/Long: Already set
3. Click "✨ Generate Birth Chart"
4. Button shows "Calculating..." while loading
5. Backend generates real chart data
6. Chart displays with real data (not mock)

### Browser: Test Login with Demo Account

1. Logout: Open browser console, run: `localStorage.clear()`
2. Refresh page, redirects to login
3. Click "Sign In" tab
4. Fill in:
   - Email: `laplace@mula.app`
   - Password: `Mula2025!Astrology`
5. Click "Sign In"
6. Success message shows
7. Auto-redirects to chart page

## Verify It's Working

### Sign-up/Login Works If:

- ✅ No errors in browser console
- ✅ Success message appears (green bar)
- ✅ Auto-redirect happens after 1.5 seconds
- ✅ Can generate chart on /readings/new

### Chart Generation Works If:

- ✅ No "Not authenticated" error
- ✅ Button shows "Calculating..." while loading
- ✅ Real chart data displays (check browser dev tools Network tab)
- ✅ Chart shows actual planets, houses, aspects

### Check Network Requests

1. Open browser DevTools (F12)
2. Go to Network tab
3. Register/Login - should see:
   - `POST /api/v1/auth/register` → 200 OK
   - Response includes: `access_token`, `refresh_token`, `user_id`
4. Generate chart - should see:
   - `POST /api/v1/chart` → 200 OK
   - Response includes: `chart_data`, `chart_id`, `created_at`

## Troubleshooting

| Issue                     | Solution                                                                                     |
| ------------------------- | -------------------------------------------------------------------------------------------- |
| Backend not running       | Check Terminal 1, run: `PORT=8001 python -m uvicorn backend.main:app --reload`               |
| Frontend not running      | Check Terminal 2, run: `npm run dev` in `/frontend` directory                                |
| CORS errors               | Backend should handle CORS, verify in `/backend/main.py`                                     |
| 404 on /auth/login        | Verify Next.js built the route, check file exists at `/frontend/src/app/auth/login/page.tsx` |
| "Not authenticated" error | Clear localStorage: `localStorage.clear()`, then register/login                              |
| Chart generation fails    | Check backend console for calculation errors, verify birth data is valid                     |
| Port 3001 already in use  | Kill process: `lsof -ti:3001 \| xargs kill`                                                  |
| Port 8001 already in use  | Kill process: `lsof -ti:8001 \| xargs kill`                                                  |

## Key Endpoints Tested

### Backend Authentication

```
POST /api/v1/auth/register
{
  "email": "test@example.com",
  "password": "TestPass123",
  "first_name": "Test",
  "last_name": "User"
}

POST /api/v1/auth/login
{
  "email": "test@example.com",
  "password": "TestPass123"
}
```

### Backend Chart Generation

```
POST /api/v1/chart
Headers: Authorization: Bearer {access_token}
{
  "birth_data": {
    "birth_date": "1984-12-19",
    "birth_time": "12:00:00",
    "birth_location": "Metairie, LA",
    "latitude": 29.9844,
    "longitude": -90.1547,
    "timezone": "America/Chicago"
  }
}
```

## Success Indicators ✅

- ✅ No TypeScript errors in build
- ✅ Register creates new account with tokens
- ✅ Login retrieves existing account with tokens
- ✅ Tokens persist in localStorage
- ✅ Chart page redirects to login if not authenticated
- ✅ Chart generation calls real backend API
- ✅ Real chart data displays instead of mock
- ✅ Error messages are helpful
- ✅ Expired tokens trigger re-login prompt
- ✅ All forms styled with design tokens

## Next: Production Deployment

Once testing is complete:

1. Run all tests: `npm run test`
2. Build frontend: `npm run build`
3. Deploy to Railway/Vercel
4. Update backend environment variables in production
5. Test on production domain

---

**Duration**: ~15 minutes to test complete flow
**Difficulty**: Straightforward - just follow the browser flow
**Support**: Check console errors with F12 → Console tab
