# Implementation Overview

## Architecture

```
Frontend (Next.js 16 on :3001)
├── Services Layer
│   ├── AuthService (/frontend/src/services/auth.ts)
│   │   ├── register() → Backend /api/v1/auth/register
│   │   ├── login() → Backend /api/v1/auth/login
│   │   ├── getAccessToken() → localStorage
│   │   ├── getCurrentUser() → localStorage
│   │   ├── isAuthenticated() → boolean
│   │   └── logout() → clear tokens
│   │
│   └── ChartService (/frontend/src/services/chart.ts)
│       ├── generateChart() → Backend /api/v1/chart (requires auth)
│       └── getChart() → Backend /api/v1/chart/{id}
│
├── Pages
│   ├── /auth/login/page.tsx (Login/Register UI)
│   │   ├── Form state management
│   │   ├── Calls AuthService.register() or login()
│   │   ├── Stores tokens via AuthService
│   │   └── Redirects to /readings/new on success
│   │
│   └── /readings/new/page.tsx (Chart Generation)
│       ├── useEffect: Check auth, redirect if not authenticated
│       ├── handleGenerateChart()
│       │   ├── Checks isAuthenticated()
│       │   ├── Calls ChartService.generateChart()
│       │   ├── ChartService retrieves token from localStorage
│       │   ├── ChartService adds Authorization header
│       │   ├── Updates state with real chart data
│       │   └── Handles errors (shows message, redirects if expired)
│       └── Renders ChartCanvas with real data
│
└── Styles
    ├── globals.css (Design tokens)
    │   ├── Colors: --color-accent-primary, --color-text-primary, etc.
    │   ├── Fonts: --font-rubik, --font-inter
    │   ├── Spacing: Scale of 4px units
    │   └── Animations: fadeIn, slideUp, shimmer, etc.
    │
    └── auth/login/login.css (Auth page styles)
        ├── Mobile-first responsive design
        ├── Form inputs with focus states
        ├── Success/error message styling
        └── Demo credentials display
```

## Data Flow Diagrams

### Registration Flow

```
User Form
   ↓
LoginPage.handleSubmit()
   ↓
AuthService.register(email, password, firstName, lastName)
   ↓
fetch POST /api/v1/auth/register
   ↓
Backend validates & creates user
   ↓
Response: {user_id, email, first_name, last_name, access_token, refresh_token, token_type}
   ↓
AuthService.storeTokens() → localStorage
AuthService.storeUser() → localStorage
   ↓
useRouter.push('/readings/new')
```

### Chart Generation Flow

```
User enters birth data
   ↓
Chart page useEffect: Check auth → authService.isAuthenticated()
   ↓
User clicks "Generate Birth Chart"
   ↓
handleGenerateChart()
   ├─ Check: authService.isAuthenticated()
   └─ Yes → Continue
   │   └─ setLoading(true)
   │
ChartService.generateChart(birthData)
   ├─ getAccessToken() from localStorage
   └─ Construct request:
       POST /api/v1/chart
       Headers: Authorization: Bearer {token}
       Body: {birth_data: {...}}
   │
   ↓
Backend chart calculation
   │
   ↓
Response: {chart_id, user_id, chart_data, created_at, birth_location}
   │
   ↓
setChartData(response.chart_data)
   ↓
ChartCanvas renders real data
   ↓
setLoading(false)
```

### Token Lifecycle

```
Registration/Login
   ↓
Backend returns: {access_token, refresh_token}
   ↓
AuthService.storeTokens()
   → localStorage['access_token'] = token
   → localStorage['refresh_token'] = token
   │
   ↓
User navigates to /readings/new
   │
   ├─ Page loads
   ├─ useEffect checks: authService.isAuthenticated()
   │  → Checks localStorage['access_token'] exists
   │  → Yes: Allow page to load
   │  → No: router.push('/auth/login')
   │
   ├─ User generates chart
   ├─ chartService.generateChart() called
   ├─ getAccessToken() retrieves from localStorage
   ├─ Adds to Authorization header
   │
   ├─ Backend validates token
   │  → Valid: Generate chart
   │  → Invalid/Expired: Return 401
   │
   ├─ If 401: ChartService catches error
   │  → authService.logout()
   │  → Clear localStorage
   │  → Show error: "Session expired. Please log in again."
   │  → router.push('/auth/login')
   │
   └─ User logs back in, new token issued
```

## Component Integration Example

### LoginPage Component Structure

```tsx
export default function LoginPage() {
  const router = useRouter();
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    firstName: "",
    lastName: "",
  });

  const handleSubmit = async (e) => {
    try {
      if (isLogin) {
        const response = await authService.login(email, password);
        // response.user, response.tokens (already stored)
        router.push("/readings/new");
      } else {
        const response = await authService.register(
          email,
          password,
          firstName,
          lastName
        );
        // response.user, response.tokens (already stored)
        router.push("/readings/new");
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <button type="submit" disabled={loading}>
        {loading ? "Processing..." : isLogin ? "Sign In" : "Create Account"}
      </button>
    </form>
  );
}
```

### Chart Page Component Structure

```tsx
export default function NewChartReadingPage() {
  const router = useRouter();
  const [chartData, setChartData] = useState(mockChartData);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Check auth on mount
  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push("/auth/login");
    }
  }, [router]);

  const handleGenerateChart = async () => {
    try {
      // Check auth before API call
      if (!authService.isAuthenticated()) {
        router.push("/auth/login");
        return;
      }

      // Call API with auth token (automatic via ChartService)
      const response = await chartService.generateChart({
        birth_date: birthData.date,
        birth_time: `${birthData.time}:00`,
        birth_location: birthData.location_name,
        latitude: birthData.latitude,
        longitude: birthData.longitude,
        timezone: birthData.timezone,
      });

      // Update UI with real data
      setChartData(response.chart_data as typeof mockChartData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate chart");

      // Redirect if session expired
      if (
        err.message.includes("expired") ||
        err.message.includes("authenticated")
      ) {
        setTimeout(() => router.push("/auth/login"), 2000);
      }
    }
  };

  return (
    <div>
      {/* Form for birth data input */}
      <button onClick={handleGenerateChart} disabled={loading}>
        {loading ? "Calculating..." : "✨ Generate Birth Chart"}
      </button>

      {/* Display chart with real data */}
      <ChartCanvas chartData={chartData} />
    </div>
  );
}
```

## Service Layer Implementation

### AuthService Methods

```typescript
// Store tokens after auth
class AuthService {
  private storeTokens(accessToken: string, refreshToken: string) {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
  }

  private storeUser(user: User) {
    localStorage.setItem('user', JSON.stringify(user));
  }

  // Register new user
  async register(email, password, firstName, lastName) {
    const response = await fetch(`${API_URL}/api/v1/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, first_name: firstName, last_name: lastName })
    });
    const data = await response.json();
    this.storeTokens(data.access_token, data.refresh_token);
    this.storeUser(data);
    return { user: data, tokens: {...} };
  }

  // Get token for API calls
  getAccessToken() {
    return localStorage.getItem('access_token');
  }

  // Check if user is logged in
  isAuthenticated() {
    return !!this.getAccessToken();
  }

  // Clear session
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  }
}
```

### ChartService Implementation

```typescript
class ChartService {
  async generateChart(birthData) {
    const accessToken = authService.getAccessToken();

    if (!accessToken) {
      throw new Error("Not authenticated. Please log in first.");
    }

    const response = await fetch(`${API_URL}/api/v1/chart`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`, // ← Token added here
      },
      body: JSON.stringify({ birth_data: birthData }),
    });

    if (response.status === 401) {
      authService.logout();
      throw new Error("Session expired. Please log in again.");
    }

    return await response.json();
  }
}
```

## Authentication Flow Sequence

```
┌─────────────────┐         ┌──────────────────┐         ┌──────────────┐
│   Login Page    │         │  Auth Service    │         │   Backend    │
└────────┬────────┘         └────────┬─────────┘         └──────┬───────┘
         │                          │                          │
         │ register()               │                          │
         │─────────────────────────→│                          │
         │                          │ POST /auth/register      │
         │                          │─────────────────────────→│
         │                          │                          │
         │                          │ ← 200 {tokens, user}     │
         │                          │←─────────────────────────│
         │                          │                          │
         │                   storeTokens()                      │
         │                   localStorage                       │
         │                          │                          │
         │ ← response                │                          │
         │←─────────────────────────│                          │
         │                          │                          │
      redirect to
      /readings/new
         │                          │                          │

┌─────────────────┐         ┌──────────────────┐         ┌──────────────┐
│  Chart Page     │         │  Chart Service   │         │   Backend    │
└────────┬────────┘         └────────┬─────────┘         └──────┬───────┘
         │                          │                          │
   Mount page                       │                          │
   useEffect check auth             │                          │
   isAuthenticated()                │                          │
         │                          │                          │
         │ generateChart()          │                          │
         │─────────────────────────→│                          │
         │                          │ getAccessToken()         │
         │                          │ from localStorage        │
         │                          │                          │
         │                          │ POST /chart              │
         │                          │ + Bearer token           │
         │                          │─────────────────────────→│
         │                          │                          │
         │                          │ ← 200 {chart_data}       │
         │                          │←─────────────────────────│
         │                          │                          │
         │ ← response               │                          │
         │←─────────────────────────│                          │
         │                          │                          │
   setChartData()                    │                          │
   render with real data             │                          │
```

## Error Handling Chain

```
handleGenerateChart()
   ↓
chartService.generateChart()
   ├─ No token: throw "Not authenticated"
   │  ↓
   │  handleGenerateChart catches
   │  ↓
   │  Set error message
   │  route to /auth/login
   │
   ├─ API call fails: throw error
   │  ↓
   │  Check error message
   │  ├─ 401: logout() + "Session expired"
   │  ├─ 400: "Invalid data" (show to user)
   │  └─ 500: "Server error" (show to user)
   │
   └─ Success: return chart_data
       ↓
       setChartData(real data)
       ↓
       UI updates with real chart
```

## localStorage Structure

```javascript
// After successful registration/login:
localStorage = {
  access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  refresh_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  user: JSON.stringify({
    user_id: "uuid-123",
    email: "user@example.com",
    first_name: "John",
    last_name: "Doe",
  }),
};

// After logout:
localStorage = {};
```

## Summary

The implementation provides:

✅ **Type-safe** - Full TypeScript interfaces
✅ **Modular** - Services layer separates concerns
✅ **Reusable** - Services can be used anywhere
✅ **Secure** - Tokens in localStorage, headers for API
✅ **Robust** - Error handling for all scenarios
✅ **User-friendly** - Clear messages and redirects
✅ **Maintainable** - Well-commented, documented
✅ **Extensible** - Easy to add refresh token logic later
