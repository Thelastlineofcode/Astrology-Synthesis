# Chart Generation Integration - Complete Implementation

## Current Status

✅ **Backend API Ready:**

- `POST /api/v1/chart` - Generate birth chart (requires auth)
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User authentication
- Running on port 8001

⚠️ **Frontend Issues:**

- Mock data used in `/readings/new/page.tsx`
- Authentication commented out
- No token storage/retrieval
- No actual API calls

---

## Step 1: User Registration & Authentication

### Backend User Registration

**Endpoint:** `POST /api/v1/auth/register`

**Request:**

```json
{
  "email": "laplace@mula.app",
  "password": "Mula2025!Astrology",
  "first_name": "The",
  "last_name": "Last of Laplace"
}
```

**Response:**

```json
{
  "user_id": "uuid-string",
  "email": "laplace@mula.app",
  "first_name": "The",
  "last_name": "Last of Laplace",
  "created_at": "2025-11-03T...",
  "api_key": "api-key-string",
  "access_token": "jwt-token-string",
  "refresh_token": "refresh-token-string",
  "token_type": "bearer"
}
```

### Backend User Login

**Endpoint:** `POST /api/v1/auth/login`

**Request:**

```json
{
  "email": "laplace@mula.app",
  "password": "Mula2025!Astrology"
}
```

**Response:** Same as registration (with tokens)

---

## Step 2: Chart Generation API

**Endpoint:** `POST /api/v1/chart`

**Headers:**

```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request:**

```json
{
  "birth_data": {
    "date": "1984-12-19",
    "time": "12:00:00",
    "latitude": 29.9844,
    "longitude": -90.1547,
    "timezone": "America/Chicago",
    "location_name": "Metairie, LA"
  },
  "ayanamsa": "LAHIRI",
  "house_system": "PLACIDUS"
}
```

**Response:**

```json
{
  "chart_id": "uuid-string",
  "user_id": "uuid-string",
  "chart_data": {
    "planets": [...],
    "houses": [...],
    "aspects": [...],
    "ayanamsa": "LAHIRI"
  },
  "created_at": "2025-11-03T...",
  "birth_location": "Metairie, LA"
}
```

---

## Step 3: Frontend Authentication Service

Create `/frontend/src/services/auth.ts`:

```typescript
interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

interface User {
  user_id: string;
  email: string;
  first_name: string;
  last_name: string;
}

class AuthService {
  private API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";

  async register(
    email: string,
    password: string,
    firstName: string,
    lastName: string
  ): Promise<{ user: User; tokens: AuthTokens }> {
    const response = await fetch(`${this.API_URL}/api/v1/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        password,
        first_name: firstName,
        last_name: lastName,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Registration failed");
    }

    const data = await response.json();

    // Store tokens in localStorage
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    localStorage.setItem(
      "user",
      JSON.stringify({
        user_id: data.user_id,
        email: data.email,
        first_name: data.first_name,
        last_name: data.last_name,
      })
    );

    return {
      user: {
        user_id: data.user_id,
        email: data.email,
        first_name: data.first_name,
        last_name: data.last_name,
      },
      tokens: {
        access_token: data.access_token,
        refresh_token: data.refresh_token,
        token_type: data.token_type,
      },
    };
  }

  async login(
    email: string,
    password: string
  ): Promise<{ user: User; tokens: AuthTokens }> {
    const response = await fetch(`${this.API_URL}/api/v1/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Login failed");
    }

    const data = await response.json();

    // Store tokens
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);
    localStorage.setItem(
      "user",
      JSON.stringify({
        user_id: data.user_id,
        email: data.email,
        first_name: data.first_name,
        last_name: data.last_name,
      })
    );

    return {
      user: {
        user_id: data.user_id,
        email: data.email,
        first_name: data.first_name,
        last_name: data.last_name,
      },
      tokens: {
        access_token: data.access_token,
        refresh_token: data.refresh_token,
        token_type: data.token_type,
      },
    };
  }

  getAccessToken(): string | null {
    return localStorage.getItem("access_token");
  }

  getCurrentUser(): User | null {
    const user = localStorage.getItem("user");
    return user ? JSON.parse(user) : null;
  }

  logout(): void {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
  }

  isAuthenticated(): boolean {
    return !!this.getAccessToken();
  }
}

export default new AuthService();
```

---

## Step 4: Chart API Service

Create `/frontend/src/services/chart.ts`:

```typescript
interface BirthData {
  date: string;
  time: string;
  latitude: number;
  longitude: number;
  timezone: string;
  location_name: string;
}

interface ChartResponse {
  chart_id: string;
  user_id: string;
  chart_data: any;
  created_at: string;
  birth_location: string;
}

class ChartService {
  private API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";

  async generateChart(birthData: BirthData): Promise<ChartResponse> {
    const accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
      throw new Error("Not authenticated. Please login first.");
    }

    const response = await fetch(`${this.API_URL}/api/v1/chart`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({
        birth_data: {
          ...birthData,
          time: birthData.time.includes(":")
            ? birthData.time + ":00"
            : birthData.time,
        },
        ayanamsa: "LAHIRI",
        house_system: "PLACIDUS",
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Chart generation failed");
    }

    return await response.json();
  }
}

export default new ChartService();
```

---

## Step 5: Update Chart Reading Page

Update `/frontend/src/app/readings/new/page.tsx`:

1. Import auth and chart services
2. Add authentication check on page load
3. Uncomment API call in `handleGenerateChart`
4. Use real chart data from API

```typescript
import authService from "@/services/auth";
import chartService from "@/services/chart";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function NewChartReadingPage() {
  const router = useRouter();
  const [chartData, setChartData] = useState(mockChartData);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check authentication on load
    if (!authService.isAuthenticated()) {
      // Redirect to login or show login prompt
      console.warn("Not authenticated - redirecting to login");
      // router.push('/auth/login');
    } else {
      setIsAuthenticated(true);
    }
  }, [router]);

  const handleGenerateChart = async () => {
    if (!isAuthenticated) {
      setError("Please login first to generate charts");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Call backend API
      const response = await chartService.generateChart(birthData);

      // Use real chart data from backend
      setChartData(response.chart_data);

      console.log("Chart generated successfully:", response);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to generate chart";
      setError(errorMessage);
      console.error("Chart generation error:", err);
    } finally {
      setLoading(false);
    }
  };

  // ... rest of component
}
```

---

## Step 6: Create Auth/Login Page

Create `/frontend/src/app/auth/login/page.tsx`:

```typescript
"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import authService from '@/services/auth';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('laplace@mula.app');
  const [password, setPassword] = useState('Mula2025!Astrology');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await authService.login(email, password);
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await authService.register(email, password, 'The', 'Last of Laplace');
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '4rem auto', padding: '2rem' }}>
      <h1>Login / Register</h1>

      {error && <div style={{ color: 'var(--color-error)', marginBottom: '1rem' }}>{error}</div>}

      <form onSubmit={handleLogin}>
        <div style={{ marginBottom: '1rem' }}>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{ width: '100%', padding: '0.5rem' }}
          />
        </div>

        <div style={{ marginBottom: '1.5rem' }}>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: '100%', padding: '0.5rem' }}
          />
        </div>

        <button type="submit" disabled={loading} style={{ marginRight: '1rem', padding: '0.5rem 1rem' }}>
          {loading ? 'Loading...' : 'Login'}
        </button>
        <button type="button" onClick={handleRegister} disabled={loading} style={{ padding: '0.5rem 1rem' }}>
          {loading ? 'Loading...' : 'Register'}
        </button>
      </form>
    </div>
  );
}
```

---

## Step 7: Implementation Checklist

- [ ] Create `/frontend/src/services/auth.ts` - Authentication service
- [ ] Create `/frontend/src/services/chart.ts` - Chart generation service
- [ ] Create `/frontend/src/app/auth/login/page.tsx` - Login/register page
- [ ] Update `/frontend/src/app/readings/new/page.tsx` - Enable API calls
- [ ] Test user registration via API
- [ ] Test user login via API
- [ ] Test chart generation with real backend
- [ ] Verify chart data renders in ChartCanvas component
- [ ] Test predictions and notes saving
- [ ] Complete responsive design testing

---

## Step 8: Quick Start Commands

### Terminal 1: Backend

```bash
cd /Users/houseofobi/Documents/GitHub/Mula
PORT=8001 python -m uvicorn backend.main:app --host 0.0.0.0 --port 8001 --reload
```

### Terminal 2: Frontend

```bash
cd /Users/houseofobi/Documents/GitHub/Mula/frontend
npm run dev  # Runs on port 3001
```

### Test Flow

1. Visit `http://localhost:3001/auth/login`
2. Click "Register" to create account
3. Get redirected to `/dashboard`
4. Visit `/readings/new`
5. Click "Generate Chart"
6. See real chart data from backend

---

## Error Handling

Common errors and solutions:

**"Not authenticated"**

- User hasn't registered/logged in
- Token not stored in localStorage
- Solution: Redirect to `/auth/login`

**"Chart generation failed"**

- Backend API is down
- Invalid birth data format
- Authentication token expired
- Solution: Check backend is running, refresh token

**"CORS error"**

- Frontend making cross-origin request to backend
- Solution: Backend should have CORS enabled (usually is)

---

## Next Phase: Data Persistence

After basic flow works:

1. Save generated charts to database
2. List previously generated charts
3. Load and view old charts
4. Add predictions to charts
5. Export chart data (PDF, image)

---

## Files to Create/Update

| File                                      | Status    | Purpose                          |
| ----------------------------------------- | --------- | -------------------------------- |
| `/frontend/src/services/auth.ts`          | 🆕 Create | Auth service with login/register |
| `/frontend/src/services/chart.ts`         | 🆕 Create | Chart generation service         |
| `/frontend/src/app/auth/login/page.tsx`   | 🆕 Create | Login/register UI                |
| `/frontend/src/app/readings/new/page.tsx` | ✏️ Update | Enable real API calls            |

---

## Status: Ready to Implement ✅

All pieces are in place. Backend is ready, frontend structure exists. Just need to wire them together!
