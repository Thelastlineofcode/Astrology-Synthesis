# API Structure Documentation

## Overview

The frontend now has a complete, type-safe API structure for communicating with the backend. This includes:

- **Core API Client**: Handles all HTTP requests with error handling and authentication
- **Service Modules**: Organized by feature (auth, charts, predictions, transits, knowledge, LLM)
- **TypeScript Types**: Complete type definitions for all requests and responses
- **React Hooks**: Custom hooks for data fetching with loading/error states

## Usage Examples

### 1. Using API Services Directly

```typescript
import { api } from "@/lib/api";

// Login
const response = await api.auth.login({
  email: "user@example.com",
  password: "password123",
});

// Create a birth chart
const chart = await api.charts.create({
  name: "My Chart",
  birth_date: "1990-01-01",
  birth_time: "12:00:00",
  latitude: 40.7128,
  longitude: -74.006,
  timezone: "America/New_York",
  birth_location: "New York, NY",
  house_system: "placidus",
});

// Search knowledge base
const results = await api.knowledge.search({
  query: "mars in aries",
  limit: 10,
});
```

### 2. Using React Hooks

```typescript
'use client';

import { useAPI } from '@/lib/hooks';
import { api } from '@/lib/api';

function MyComponent() {
  const { data, loading, error, execute } = useAPI(
    api.auth.getCurrentUser,
    {
      onSuccess: (user) => console.log('User loaded:', user),
      onError: (err) => console.error('Error:', err)
    }
  );

  const handleLogin = async () => {
    await execute();
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!data) return <button onClick={handleLogin}>Load User</button>;

  return <div>Welcome, {data.first_name}!</div>;
}
```

### 3. Paginated Data

```typescript
import { usePaginatedAPI } from '@/lib/hooks';
import { api } from '@/lib/api';

function ChartsList() {
  const { data, loading, hasMore, loadMore } = usePaginatedAPI(
    (page, limit) => api.charts.list({ page, limit }),
    20
  );

  return (
    <div>
      {data.map(chart => (
        <div key={chart.id}>{chart.name}</div>
      ))}
      {hasMore && (
        <button onClick={loadMore} disabled={loading}>
          {loading ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  );
}
```

### 4. With Caching

```typescript
import { useCachedAPI } from "@/lib/hooks";
import { api } from "@/lib/api";

function CachedComponent() {
  const { data, loading, execute } = useCachedAPI(
    api.knowledge.getCategories,
    "knowledge-categories",
    { cacheDuration: 10 * 60 * 1000 } // 10 minutes
  );

  // Data will be cached for 10 minutes
  // Subsequent calls will use cached data
}
```

## Available Services

### Authentication (`api.auth`)

- `login(credentials)` - Login user
- `register(userData)` - Register new user
- `logout()` - Logout current user
- `getCurrentUser()` - Get current user profile
- `refreshToken()` - Refresh access token
- `changePassword(current, new)` - Change password

### Charts (`api.charts`)

- `create(data)` - Create new birth chart
- `getById(id)` - Get chart by ID
- `list(params)` - List all charts
- `update(id, data)` - Update chart
- `delete(id)` - Delete chart
- `calculate(data)` - Calculate chart without saving

### Predictions (`api.predictions`)

- `create(data)` - Create new prediction
- `getById(id)` - Get prediction by ID
- `listByChart(chartId, params)` - List predictions for chart
- `list(params)` - List all predictions
- `delete(id)` - Delete prediction

### Transits (`api.transits`)

- `calculate(data)` - Calculate transits
- `getById(id)` - Get transit by ID
- `listByChart(chartId, params)` - List transits for chart
- `getCurrent(chartId)` - Get current transits
- `delete(id)` - Delete transit

### Knowledge Base (`api.knowledge`) - Phase 5

- `search(params)` - Search knowledge base
- `getCategories()` - List all categories
- `getCategoryInfo(name)` - Get category details
- `healthCheck()` - Check KB health

### LLM (`api.llm`) - Phase 5

- `generateInterpretation(request)` - Generate interpretation
- `getBudget()` - Get LLM budget status
- `getStats()` - Get LLM statistics
- `healthCheck()` - Check LLM health

### Health (`api.health`)

- `getHealth()` - Get system health
- `getVersion()` - Get API version

## Error Handling

All API calls return errors as `APIError` instances with:

- `message`: Error message
- `status`: HTTP status code
- `code`: Error code (if provided by API)
- `details`: Additional error details

```typescript
try {
  const chart = await api.charts.create(data);
} catch (error) {
  if (error instanceof APIError) {
    console.error(`Error ${error.status}: ${error.message}`);
    if (error.code) {
      console.error(`Code: ${error.code}`);
    }
  }
}
```

## Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1
```

## File Structure

```
frontend/src/lib/
├── api/
│   ├── client.ts           # Core API client
│   ├── types.ts            # TypeScript types
│   ├── index.ts            # Main export
│   └── services/
│       ├── auth.ts         # Auth service
│       ├── charts.ts       # Charts service
│       ├── predictions.ts  # Predictions service
│       ├── transits.ts     # Transits service
│       ├── knowledge.ts    # Knowledge Base service
│       ├── llm.ts          # LLM service
│       └── health.ts       # Health service
└── hooks/
    ├── useAPI.ts           # API hooks
    └── index.ts            # Hooks export
```
