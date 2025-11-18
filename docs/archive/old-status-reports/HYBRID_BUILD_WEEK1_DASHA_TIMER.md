# WEEK 1 BUILD SPECIFICATION

## Daily Dasha Timer MVP

**Duration**: 10 working days (Nov 8-22)  
**Team**: 2-3 developers (1 Backend, 1 Frontend, 0.5 DevOps)  
**Budget**: $8K-12K  
**Target Launch**: Nov 22, 2025

---

## PROJECT OVERVIEW

### What Is It?

Daily countdown timer showing when user's Dasha (planetary period) changes + what it means.

**Core Flow:**

1. User enters birth data (date, time, place) OR signs in with existing chart
2. System calculates current Dasha period
3. Display: "You are in Jupiter Dasha for X days" (big visual countdown)
4. Show what Jupiter Dasha means (personality traits, opportunities)
5. Notify user when Dasha changes (daily pushes + email)
6. Optional: Subscribe for detailed daily guidance ($5/month)

### Why This First?

✅ **Technical**: Uses existing Mula Dasha engine (already built, tested)  
✅ **Fast**: 2-week build (reuses 60% of existing backend code)  
✅ **Monetizable**: Clear freemium + premium path  
✅ **Engaging**: Daily notification = daily engagement  
✅ **Learnings**: Real user data informs future features

---

## TECH STACK

```
Frontend:
├── Framework: Next.js 16 (React 19, TypeScript)
├── Styling: Tailwind CSS + Shadcn/ui components
├── State: React Query (server state)
├── Deployment: Vercel (auto-deploy from GitHub)
└── PWA: Workbox (offline support, install-to-home)

Backend:
├── Framework: FastAPI (Python 3.11)
├── Database: PostgreSQL (new isolated DB for MVP)
├── Auth: JWT + Google OAuth + Apple Sign-In
├── Caching: Redis (Dasha calculations, user state)
├── APIs Used: Existing Mula backend (dasha_engine)
└── Deployment: Railway or Render (auto-deploy from GitHub)

Real-Time & Notifications:
├── Notifications: Firebase Cloud Messaging (FCM)
├── Email: SendGrid (welcome, dasha changes, reminders)
├── WebSocket: For real-time timer updates
└── Scheduler: APScheduler (cron jobs for daily notifications)

Integrations:
├── Payments: Stripe (subscriptions)
├── Analytics: Plausible (privacy-first tracking)
├── Monitoring: Sentry (error tracking)
└── Existing: Mula backend /api/dasha/* endpoints
```

---

## DETAILED ARCHITECTURE

### Frontend Structure

```
frontend-dasha-timer/
├── app/
│   ├── layout.tsx (global layout, providers)
│   ├── page.tsx (landing page)
│   ├── auth/
│   │   ├── login/page.tsx
│   │   ├── signup/page.tsx
│   │   ├── callback/page.tsx (OAuth redirect)
│   │   └── logout/route.ts
│   ├── dashboard/
│   │   ├── layout.tsx
│   │   ├── page.tsx (main dasha timer display)
│   │   ├── chart/page.tsx (birth chart input/edit)
│   │   └── settings/page.tsx (notifications, premium)
│   └── premium/
│       ├── page.tsx (upgrade page)
│       └── success/page.tsx (payment success)
├── components/
│   ├── DashaTimer.tsx (main countdown component)
│   ├── DashaInfo.tsx (meaning + characteristics)
│   ├── BirthChartForm.tsx (input form)
│   ├── NotificationSettings.tsx (push/email prefs)
│   ├── PremiumCard.tsx (upgrade CTA)
│   └── Navbar.tsx (top navigation)
├── hooks/
│   ├── useDashaData.ts (fetch + refetch dasha info)
│   ├── useAuth.ts (auth context)
│   └── useNotifications.ts (FCM registration)
├── services/
│   ├── api.ts (API client, axios)
│   ├── auth.ts (JWT management)
│   └── stripe.ts (premium checkout)
├── lib/
│   ├── constants.ts (API URLs, dasha meanings)
│   ├── utils.ts (formatting, dates)
│   └── dasha-descriptions.ts (full meanings, career/health/love)
├── styles/
│   └── globals.css (Tailwind config)
├── public/
│   ├── manifest.json (PWA config)
│   ├── service-worker.js (offline support)
│   └── icons/ (app icons)
└── package.json + next.config.js + tsconfig.json
```

### Backend Structure

```
backend-dasha-timer/
├── app.py (FastAPI app initialization)
├── config.py (environment, database URL, secrets)
├── routes/
│   ├── auth.py (POST /auth/login, /auth/signup, /auth/logout)
│   ├── user.py (GET /user/profile, PUT /user/profile)
│   ├── chart.py (POST /chart/create, GET /chart, PUT /chart)
│   ├── dasha.py (GET /dasha/current, POST /dasha/calculate)
│   ├── subscription.py (POST /subscription/create, GET /subscription/status)
│   └── webhook.py (POST /webhook/stripe, /webhook/fcm)
├── models/
│   ├── user.py (User, UserPreferences)
│   ├── chart.py (BirthChart)
│   ├── dasha.py (DashaData, DashaResponse)
│   └── subscription.py (Subscription, Plan)
├── services/
│   ├── auth_service.py (JWT creation, OAuth verification)
│   ├── chart_service.py (validate birth data, store)
│   ├── dasha_service.py (call Mula engine, format response)
│   ├── notification_service.py (FCM + SendGrid)
│   ├── stripe_service.py (create subscription, webhooks)
│   └── scheduler.py (daily dasha change notifications)
├── db/
│   ├── models.py (SQLAlchemy models for User, Chart, Subscription)
│   ├── database.py (connection pool, migrations)
│   └── migrations/ (Alembic migrations)
├── middleware/
│   ├── auth.py (JWT verification)
│   ├── cors.py (allow frontend origin)
│   └── error_handler.py (global error handling)
├── tests/
│   ├── test_auth.py
│   ├── test_dasha.py
│   ├── test_chart.py
│   └── test_subscription.py
├── requirements.txt (dependencies)
├── docker-compose.yml (local dev DB + Redis)
└── .env.example
```

---

## DATABASE SCHEMA

### Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100),
    password_hash VARCHAR(255),  -- nullable (OAuth only)
    oauth_provider VARCHAR(50),   -- 'google', 'apple', null
    oauth_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    preferences JSONB DEFAULT '{}',  -- notification preferences
    INDEX (email),
    INDEX (oauth_provider, oauth_id)
);
```

### Birth Charts Table

```sql
CREATE TABLE birth_charts (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    birth_date TIMESTAMP NOT NULL,
    birth_time VARCHAR(8),  -- HH:MM:SS or null if exact time unknown
    birth_location_lat FLOAT,
    birth_location_lng FLOAT,
    birth_location_name VARCHAR(255),
    timezone_offset INT,  -- minutes from UTC
    chart_data JSONB,  -- full calculated chart (planet positions, etc)
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_default BOOLEAN DEFAULT true,
    INDEX (user_id),
    INDEX (user_id, is_default)
);
```

### Dasha Data Table

```sql
CREATE TABLE dasha_data (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    chart_id UUID NOT NULL REFERENCES birth_charts(id) ON DELETE CASCADE,
    current_dasha VARCHAR(50),  -- e.g., 'Jupiter'
    current_dasha_start DATE,
    current_dasha_end DATE,
    current_dasha_days_remaining INT,
    next_dasha VARCHAR(50),
    next_dasha_start DATE,
    dasha_balance_at_birth INT,  -- years
    full_dasha_sequence JSONB,  -- array of all dashas with dates
    calculated_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    INDEX (user_id),
    INDEX (user_id, updated_at)
);
```

### Subscriptions Table

```sql
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    stripe_subscription_id VARCHAR(255) UNIQUE,
    plan_name VARCHAR(50),  -- 'free', 'daily_guide', 'premium'
    price_cents INT,  -- $5/month = 500
    billing_cycle VARCHAR(50),  -- 'monthly', 'yearly'
    status VARCHAR(50),  -- 'active', 'cancelled', 'past_due'
    started_at TIMESTAMP DEFAULT NOW(),
    next_billing_at TIMESTAMP,
    cancelled_at TIMESTAMP,
    INDEX (user_id),
    INDEX (stripe_subscription_id)
);
```

### FCM Tokens Table (for notifications)

```sql
CREATE TABLE fcm_tokens (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(500) NOT NULL,
    device_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    last_used TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    INDEX (user_id),
    UNIQUE (user_id, token)
);
```

### Dasha Change Events (for tracking notifications sent)

```sql
CREATE TABLE dasha_events (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    event_type VARCHAR(50),  -- 'dasha_change', 'dasha_milestone'
    old_dasha VARCHAR(50),
    new_dasha VARCHAR(50),
    event_date TIMESTAMP,
    notification_sent BOOLEAN DEFAULT false,
    sent_at TIMESTAMP,
    INDEX (user_id, event_date)
);
```

---

## API ENDPOINTS

### Authentication

```
POST /api/auth/signup
├── Body: { email, password, name }
├── Response: { user_id, token, expires_in }
└── Creates user + JWT token

POST /api/auth/login
├── Body: { email, password }
├── Response: { user_id, token, expires_in }
└── 401 if invalid credentials

POST /api/auth/google
├── Body: { google_id_token }
├── Response: { user_id, token, expires_in }
└── OAuth flow, creates user if new

POST /api/auth/apple
├── Body: { apple_id_token, user_email }
├── Response: { user_id, token, expires_in }
└── OAuth flow, creates user if new

POST /api/auth/logout
├── Auth: Bearer token
├── Response: { success: true }
└── Invalidate token (add to blacklist)

POST /api/auth/refresh
├── Body: { refresh_token }
├── Response: { token, expires_in }
└── Get new access token
```

### User Profile

```
GET /api/user/profile
├── Auth: Bearer token
├── Response: { user_id, email, name, created_at, subscription_status }
└── Get current user info

PUT /api/user/profile
├── Auth: Bearer token
├── Body: { name, email, preferences }
├── Response: { success: true, user }
└── Update user info

GET /api/user/preferences
├── Auth: Bearer token
├── Response: { notifications_enabled, email_enabled, daily_time, timezone }
└── Get notification preferences

PUT /api/user/preferences
├── Auth: Bearer token
├── Body: { notifications_enabled, email_enabled, daily_time, timezone }
├── Response: { success: true }
└── Update notification preferences
```

### Birth Charts

```
POST /api/chart/create
├── Auth: Bearer token
├── Body: {
│   birth_date: "1990-08-15",
│   birth_time: "14:30:00",
│   birth_location_lat: 40.7128,
│   birth_location_lng: -74.0060,
│   birth_location_name: "New York, NY"
│ }
├── Response: { chart_id, is_default, created_at }
└── Create birth chart, validate against Mula engine

GET /api/chart
├── Auth: Bearer token
├── Response: { charts: [...], default_chart: { ... } }
└── Get all user's charts

GET /api/chart/:chart_id
├── Auth: Bearer token
├── Response: { chart_id, birth_date, chart_data, is_default }
└── Get specific chart details

PUT /api/chart/:chart_id/default
├── Auth: Bearer token
├── Response: { success: true, default_chart_id }
└── Set as default chart for dasha calculations
```

### Dasha Calculations

```
GET /api/dasha/current
├── Auth: Bearer token
├── Query: ?chart_id=<uuid> (optional, uses default if not provided)
├── Response: {
│   current_dasha: "Jupiter",
│   current_dasha_start: "2023-05-15",
│   current_dasha_end: "2025-09-20",
│   days_remaining: 287,
│   next_dasha: "Saturn",
│   next_dasha_start: "2025-09-20",
│   dasha_meaning: { ... },
│   last_calculated: "2025-11-04T12:30:00Z"
│ }
└── Get current Dasha info (calls Mula engine, caches 1 hour)

POST /api/dasha/calculate
├── Auth: Bearer token
├── Body: { chart_id }
├── Response: { full_sequence: [...], current: { ... }, next: { ... } }
└── Force recalculate all dashas (invalidate cache)

GET /api/dasha/meanings
├── Auth: NOT required
├── Response: {
│   "Sun": { keywords: [], career: [], health: [], relationships: [] },
│   "Moon": { ... },
│   ...
│ }
└── Get meanings for all dashas (static, cache forever)

GET /api/dasha/timeline
├── Auth: Bearer token
├── Query: ?years=10 (how many years to show)
├── Response: { timeline: [...], current_position: 45 }
└── Get full dasha timeline for visualization
```

### Subscriptions

```
POST /api/subscription/create
├── Auth: Bearer token
├── Body: { plan: "premium", billing: "monthly" }
├── Response: { stripe_session_id, session_url }
└── Create Stripe checkout session

GET /api/subscription/status
├── Auth: Bearer token
├── Response: { plan, status, expires_at, auto_renew }
└── Get current subscription status

POST /api/subscription/cancel
├── Auth: Bearer token
├── Response: { success: true, cancelled_at }
└── Cancel subscription (end of current period)

GET /api/subscription/plans
├── Auth: NOT required
├── Response: { plans: [{ name, price, features, popular: bool }] }
└── Get all available plans
```

### Webhooks (Backend → Frontend)

```
POST /api/webhook/stripe
├── Signature: X-Stripe-Signature header
├── Body: Stripe event (subscription created, updated, deleted)
├── Response: { success: true }
└── Update subscription status in DB

POST /api/webhook/dasha-change
├── Internal trigger (scheduled job)
├── Body: { user_id, old_dasha, new_dasha, event_date }
├── Response: { notifications_sent: <count> }
└── Trigger notifications when dasha changes
```

---

## FRONTEND COMPONENTS

### DashaTimer.tsx (Main Component)

```typescript
// frontend/components/DashaTimer.tsx

export interface DashaTimerProps {
  dasha: {
    current_dasha: string;
    current_dasha_end: string;
    days_remaining: number;
    next_dasha: string;
  };
}

export function DashaTimer({ dasha }: DashaTimerProps) {
  // Visual display:
  // ╔════════════════════════════════════════╗
  // ║   YOU ARE IN JUPITER DASHA             ║
  // ║                                        ║
  // ║   Countdown: 287 Days                  ║
  // ║   ████████████████████░░░░░░░░░░░░░░░  ║
  // ║                                        ║
  // ║   Until: Sep 20, 2025                  ║
  // ║   Then: Saturn Dasha                   ║
  // ╚════════════════════════════════════════╝

  return (
    <div className="dasha-timer-container">
      {/* Circular countdown visualization */}
      <CircularCountdown days={dasha.days_remaining} />

      {/* Current dasha name - large, bold */}
      <h1 className="text-4xl font-bold">
        {dasha.current_dasha} Dasha
      </h1>

      {/* Days remaining - primary metric */}
      <div className="text-5xl font-bold text-purple-600">
        {dasha.days_remaining}
      </div>
      <p className="text-gray-500">Days Remaining</p>

      {/* End date */}
      <div className="text-center mt-4">
        <p className="text-sm text-gray-500">Changes on</p>
        <p className="text-lg font-semibold">
          {formatDate(dasha.current_dasha_end)}
        </p>
      </div>

      {/* Next dasha preview */}
      <div className="mt-6 p-4 bg-purple-50 rounded-lg">
        <p className="text-sm text-gray-600">Next Period</p>
        <p className="text-lg font-semibold">{dasha.next_dasha} Dasha</p>
      </div>
    </div>
  );
}
```

### DashaInfo.tsx (Meaning + Details)

```typescript
// frontend/components/DashaInfo.tsx

interface DashaInfoProps {
  dasha: string;
  meanings: DashaMeaning;
}

export function DashaInfo({ dasha, meanings }: DashaInfoProps) {
  // Display:
  // ╔═══════════════════════════════════════╗
  // ║  JUPITER DASHA - What It Means        ║
  // ├───────────────────────────────────────┤
  // ║  Keywords: Abundance, Growth, Wisdom  ║
  // ║                                       ║
  // ║  💼 Career                            ║
  // ║  → Promotions, expansion, learning   ║
  // ║                                       ║
  // ║  ❤️ Relationships                     ║
  // ║  → New connections, romance          ║
  // ║                                       ║
  // ║  🏥 Health                            ║
  // ║  → Good energy, recovery             ║
  // ╚═══════════════════════════════════════╝

  return (
    <div className="dasha-info-container">
      <h2 className="text-2xl font-bold">{dasha} Dasha</h2>
      <p className="text-gray-600">What It Means For You</p>

      {/* Keywords */}
      <div className="keywords mt-4">
        <div className="flex flex-wrap gap-2">
          {meanings.keywords.map(keyword => (
            <span key={keyword} className="badge">
              {keyword}
            </span>
          ))}
        </div>
      </div>

      {/* Career section */}
      <div className="section mt-6">
        <h3 className="flex items-center gap-2">
          <span>💼</span> Career & Ambition
        </h3>
        <p>{meanings.career}</p>
      </div>

      {/* Relationships section */}
      <div className="section mt-6">
        <h3 className="flex items-center gap-2">
          <span>❤️</span> Love & Relationships
        </h3>
        <p>{meanings.relationships}</p>
      </div>

      {/* Health section */}
      <div className="section mt-6">
        <h3 className="flex items-center gap-2">
          <span>🏥</span> Health & Wellness
        </h3>
        <p>{meanings.health}</p>
      </div>

      {/* Advice section */}
      <div className="section mt-6 bg-blue-50 p-4 rounded">
        <h3>💡 Best Uses of This Time</h3>
        <ul className="list-disc list-inside">
          {meanings.best_uses.map(use => (
            <li key={use}>{use}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

### BirthChartForm.tsx (Input)

```typescript
// frontend/components/BirthChartForm.tsx

interface FormData {
  birth_date: string;
  birth_time: string;
  birth_location_name: string;
  birth_location_lat: number;
  birth_location_lng: number;
}

export function BirthChartForm({ onSubmit }: { onSubmit: (data: FormData) => void }) {
  // Display:
  // ╔════════════════════════════════════════╗
  // ║  Enter Your Birth Information         ║
  // ├────────────────────────────────────────┤
  // ║  Date: [ Aug 15, 1990     ]           ║
  // ║  Time: [ 2:30 PM          ]           ║
  // ║  Location: [ New York, NY  ]          ║
  // ║  ┌──────────────────────────────┐    ║
  // ║  │                              │    ║
  // ║  │     (Map location picker)    │    ║
  // ║  │                              │    ║
  // ║  └──────────────────────────────┘    ║
  // ║  [ Calculate ] or [ Use Sample ]     ║
  // ╚════════════════════════════════════════╝

  return (
    <form onSubmit={handleSubmit} className="birth-chart-form">
      <h2>Enter Your Birth Information</h2>

      {/* Date input */}
      <div className="form-group">
        <label>Birth Date</label>
        <input type="date" required />
      </div>

      {/* Time input */}
      <div className="form-group">
        <label>Birth Time (or approximate)</label>
        <input type="time" />
        <p className="helper">Leave blank if unknown</p>
      </div>

      {/* Location input with map picker */}
      <div className="form-group">
        <label>Birth Location</label>
        <LocationPicker onChange={setLocation} />
      </div>

      {/* Buttons */}
      <div className="form-actions">
        <button type="submit" className="btn-primary">
          Calculate My Dasha
        </button>
        <button type="button" onClick={loadSample} className="btn-secondary">
          Use Sample Chart
        </button>
      </div>
    </form>
  );
}
```

---

## BACKEND SERVICES

### DashaService

```python
# backend/services/dasha_service.py

from datetime import datetime, timezone, timedelta
from typing import Optional

class DashaService:
    def __init__(self, mula_api_client):
        self.mula_client = mula_api_client
        self.cache = {}  # Simple cache (use Redis in production)

    def get_current_dasha(self, birth_chart: dict) -> dict:
        """
        Get current Dasha for user's birth chart.
        Calls Mula backend engine, caches 1 hour.
        """
        cache_key = f"dasha_{birth_chart['id']}"

        # Check cache
        if cache_key in self.cache:
            cached, timestamp = self.cache[cache_key]
            if datetime.now() - timestamp < timedelta(hours=1):
                return cached

        # Call Mula dasha engine
        dasha_response = self.mula_client.call_dasha_engine(
            birth_date=birth_chart['birth_date'],
            birth_location={'lat': birth_chart['lat'], 'lng': birth_chart['lng']},
            birth_time=birth_chart['birth_time']
        )

        # Parse response
        current_dasha = {
            'current_dasha': dasha_response['current_dasha_name'],
            'current_dasha_start': dasha_response['current_dasha_start'],
            'current_dasha_end': dasha_response['current_dasha_end'],
            'days_remaining': (
                dasha_response['current_dasha_end'] - datetime.now(timezone.utc)
            ).days,
            'next_dasha': dasha_response['next_dasha_name'],
            'next_dasha_start': dasha_response['current_dasha_end'],
            'dasha_meaning': self.get_dasha_meaning(dasha_response['current_dasha_name']),
            'full_sequence': dasha_response['full_sequence']
        }

        # Cache
        self.cache[cache_key] = (current_dasha, datetime.now())

        return current_dasha

    def get_dasha_meaning(self, dasha_name: str) -> dict:
        """Get meaning and interpretation for a dasha."""
        meanings = {
            'Sun': {
                'keywords': ['Authority', 'Leadership', 'Confidence'],
                'career': 'Promotion, recognition, leadership opportunities',
                'relationships': 'Personal magnetism, romantic success',
                'health': 'Vitality, strong energy, some heat conditions',
                'best_uses': ['Start new projects', 'Lead teams', 'Seek recognition']
            },
            'Moon': {
                'keywords': ['Emotions', 'Family', 'Nurturing'],
                'career': 'Collaboration, team work, emotional intelligence valued',
                'relationships': 'Family bonding, maternal connection, domestic harmony',
                'health': 'May have emotional sensitivity, focus on mental health',
                'best_uses': ['Build relationships', 'Family gatherings', 'Creative work']
            },
            'Mars': {
                'keywords': ['Energy', 'Courage', 'Action'],
                'career': 'Drive, competition, leadership, passion projects',
                'relationships': 'Passion, intensity, need for independence',
                'health': 'High energy, risk of accidents, inflammation',
                'best_uses': ['Competitive endeavors', 'Physical challenges', 'New initiatives']
            },
            # ... continue for all 9 dashas
        }
        return meanings.get(dasha_name, {})

    def get_dasha_timeline(self, birth_chart: dict, years: int = 10) -> dict:
        """Get full Dasha timeline for visualization."""
        # Call Mula engine to get full sequence
        sequence = self.mula_client.get_dasha_sequence(birth_chart)

        # Format for timeline visualization
        timeline = []
        for dasha in sequence:
            timeline.append({
                'name': dasha['name'],
                'start': dasha['start_date'],
                'end': dasha['end_date'],
                'duration_years': dasha['duration_years'],
                'is_current': dasha['is_current'],
                'color': self.get_dasha_color(dasha['name'])
            })

        return {
            'timeline': timeline[:years],
            'current_position': self._get_current_position(timeline),
            'current_dasha': sequence[0]['name']
        }

    def get_dasha_color(self, dasha: str) -> str:
        """Get color for dasha visualization."""
        colors = {
            'Sun': '#FDB813',      # Gold
            'Moon': '#F0F0F0',     # White
            'Mars': '#FF6B6B',     # Red
            'Mercury': '#FFD93D',  # Yellow
            'Jupiter': '#6BCF7F',  # Green
            'Venus': '#FF69B4',    # Pink
            'Saturn': '#4D4D4D',   # Gray
            'Rahu': '#1A1A2E',     # Dark Blue
            'Ketu': '#9D4EDD',     # Purple
        }
        return colors.get(dasha, '#999999')
```

### NotificationService

```python
# backend/services/notification_service.py

class NotificationService:
    def __init__(self, fcm_client, sendgrid_client):
        self.fcm = fcm_client
        self.sendgrid = sendgrid_client

    def send_dasha_change_notification(self, user_id: str,
                                       old_dasha: str,
                                       new_dasha: str):
        """Send notification when user's Dasha changes."""

        # Get user + preferences
        user = User.get(user_id)
        prefs = user.preferences

        # Send push notification
        if prefs.get('notifications_enabled'):
            self.fcm.send_multicast({
                'tokens': user.fcm_tokens,
                'notification': {
                    'title': f'Your Dasha Has Changed!',
                    'body': f'{old_dasha} → {new_dasha} Dasha',
                    'image': self._get_dasha_image(new_dasha)
                },
                'data': {
                    'action': 'dasha_changed',
                    'new_dasha': new_dasha,
                    'link': f'/app/dasha/{new_dasha}'
                }
            })

        # Send email
        if prefs.get('email_enabled'):
            meaning = self._get_dasha_meaning(new_dasha)
            self.sendgrid.send_email({
                'to': user.email,
                'subject': f'✨ Your Dasha Has Changed to {new_dasha}',
                'template_id': 'dasha_change_email',
                'dynamic_template_data': {
                    'new_dasha': new_dasha,
                    'meaning': meaning['short_description'],
                    'opportunities': meaning['opportunities']
                }
            })

    def send_daily_dasha_reminder(self, user_id: str):
        """Send daily reminder about current Dasha."""
        user = User.get(user_id)
        dasha_data = DashaData.query.filter_by(user_id=user_id).first()

        if not user.preferences.get('daily_reminder_enabled'):
            return

        self.fcm.send_multicast({
            'tokens': user.fcm_tokens,
            'notification': {
                'title': f'Your {dasha_data.current_dasha} Dasha',
                'body': f'{dasha_data.days_remaining} days remaining'
            }
        })
```

---

## DEPLOYMENT & DEVOPS

### Frontend Deployment (Vercel)

```yaml
# vercel.json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "env":
    {
      "NEXT_PUBLIC_API_URL": "@api_url",
      "NEXT_PUBLIC_GOOGLE_CLIENT_ID": "@google_client_id",
      "NEXT_PUBLIC_STRIPE_KEY": "@stripe_public_key",
    },
  "github":
    {
      "enabled": true,
      "production": "main",
      "preview": true,
      "autoAlias": true,
    },
  "regions": ["iad1", "lhr1"],
}
```

### Backend Deployment (Railway)

```yaml
# railway.toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "python -m uvicorn app:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 5

[env]
DATABASE_URL = "$DATABASE_URL"
REDIS_URL = "$REDIS_URL"
JWT_SECRET = "$JWT_SECRET"
STRIPE_SECRET = "$STRIPE_SECRET"
SENDGRID_API_KEY = "$SENDGRID_API_KEY"
FIREBASE_CREDENTIALS = "$FIREBASE_CREDENTIALS"
```

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy Dasha Timer

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: |
          railway up --service backend

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Vercel
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
        run: |
          npm run build
          vercel deploy --prod --token $VERCEL_TOKEN
```

---

## DAY-BY-DAY EXECUTION PLAN

### Days 1-2: Project Setup & Design

```
Frontend Lead (Day 1-2):
├── Create Next.js project (vercel/next.js template)
├── Install dependencies: React Query, TailwindCSS, Shadcn/UI
├── Setup auth context + API client
├── Create component structure
└── Figma design review → component specs

Backend Lead (Day 1-2):
├── Create FastAPI project (cookiecutter-fastapi)
├── Setup PostgreSQL + migrations
├── Install dependencies: SQLAlchemy, Pydantic, python-jose
├── Create models + database schema
├── Setup auth middleware
└── Create test suite structure

DevOps (Day 1-2):
├── Setup GitHub repos (frontend + backend)
├── Configure Vercel for frontend
├── Configure Railway for backend
├── Setup CI/CD pipelines
├── Create .env templates
└── Setup monitoring (Sentry)
```

### Days 3-4: Authentication

```
Frontend (Day 3-4):
├── Build login/signup forms (email + password)
├── Implement Google OAuth flow
├── Implement Apple Sign-In
├── Create auth context + hooks
├── Build protected routes
└── Test all auth flows

Backend (Day 3-4):
├── Implement JWT token generation
├── Setup OAuth providers (Google, Apple)
├── Create /auth/* endpoints
├── Implement refresh token logic
├── Create auth middleware
├── Write unit tests for auth
└── Test with frontend
```

### Days 5-6: Birth Chart Management

```
Frontend (Day 5-6):
├── Build birth date picker component
├── Build time input component
├── Build location picker (map integration)
├── Create BirthChartForm component
├── Build chart management UI
└── Connect to backend API

Backend (Day 5-6):
├── Create POST /chart/create endpoint
├── Validate birth data (date range, location)
├── Integrate with Mula chart generation
├── Create GET /chart endpoints
├── Implement default chart selection
├── Write tests for chart endpoints
└── Cache chart calculations
```

### Days 7-8: Dasha Display

```
Frontend (Day 7-8):
├── Build DashaTimer component (circular visualization)
├── Build DashaInfo component (meanings + details)
├── Create dashboard layout
├── Implement real-time countdown
├── Add PWA offline support
└── Style for dark mode support

Backend (Day 7-8):
├── Create GET /dasha/current endpoint
├── Create GET /dasha/timeline endpoint
├── Create GET /dasha/meanings endpoint
├── Implement caching (1-hour expiry)
├── Add Mula engine integration
├── Write comprehensive tests
└── Performance optimization
```

### Days 9-10: Notifications & Premium

```
Frontend (Day 9-10):
├── Setup Firebase Cloud Messaging
├── Build notification permission request
├── Build notification settings UI
├── Create notification preferences form
├── Build premium upgrade page
├── Integrate Stripe checkout
└── Test payment flow (test mode)

Backend (Day 9-10):
├── Create notification service
├── Setup Firebase credentials
├── Implement daily dasha reminder scheduler
├── Create Stripe webhook handler
├── Implement subscription status tracking
├── Create subscription endpoints
├── Test notification delivery
└── Setup email service (SendGrid)
```

### Day 10: Testing & Launch Prep

```
QA Lead:
├── End-to-end testing (auth → dashboard)
├── Test all browsers (Chrome, Safari, Firefox)
├── Mobile responsiveness check
├── Performance testing (lighthouse score)
├── Security review (JWT, HTTPS, CORS)
├── Load testing (100 concurrent users)
└── Fix critical bugs

Deployment:
├── Deploy to Vercel (frontend)
├── Deploy to Railway (backend)
├── Verify health checks
├── Test production endpoints
├── Setup monitoring + alerting
└── Ready for beta launch
```

---

## SUCCESS METRICS (Week 1 Target)

```
Launch Targets (Day 10):
├── ✅ MVP live at dasha-timer.app
├── ✅ 100 beta testers onboarded
├── ✅ <2s page load time
├── ✅ Zero critical bugs
├── ✅ Auth working smoothly
├── ✅ Notifications tested
└── ✅ Stripe sandbox working

Week 1-2 Goals (Post-launch):
├── 500+ signups (conservative)
├── 200+ daily active users
├── 30%+ D7 retention
├── 10+ paid subscribers ($50/mo MRR)
├── 0 critical production bugs
└── Positive user feedback
```

---

## BUDGET BREAKDOWN

```
Development Labor:
├── Backend Dev (10 days @ $200/day): $2,000
├── Frontend Dev (10 days @ $200/day): $2,000
├── DevOps/QA (5 days @ $150/day): $750
└── Subtotal: $4,750

Infrastructure & Services:
├── Railway (backend): $100
├── PostgreSQL (Railway): $100
├── Redis (caching): $50
├── Firebase (notifications): $25
├── SendGrid (email): $30
├── Stripe (2% transaction fee): $50
└── Subtotal: $355

Third-Party APIs:
├── Google OAuth: Free
├── Apple Sign-In: Free
├── Plausible Analytics: $20
├── Sentry (error tracking): $29/month (trial)
└── Subtotal: $49

Total: ~$5,150 (conservative, actual with overhead: $8K-12K)
```

---

## RISK MITIGATION

| Risk                          | Probability | Impact        | Mitigation                                   |
| ----------------------------- | ----------- | ------------- | -------------------------------------------- |
| Mula engine integration fails | Medium      | Blocks launch | Test integration early (days 3-4)            |
| Notification delivery issues  | Medium      | Poor UX       | Setup Firebase early, extensive testing      |
| Payment processing delays     | Low         | Revenue = 0   | Test Stripe sandbox before day 9             |
| Performance bottlenecks       | Medium      | Churn         | Load test at day 8, optimize DB queries      |
| Scope creep                   | High        | Timeline slip | Strict MVP scope, no new features mid-sprint |

---

## NEXT STEPS

1. **Today (Nov 4)**: Founder approves this spec
2. **Tomorrow (Nov 5)**: Team kickoff, GitHub repos created
3. **Nov 6**: Finalize API design, UI mockups
4. **Nov 8**: Development begins (Day 1)
5. **Nov 22**: Beta launch target (Day 10)

**Ready to build?** 🚀
