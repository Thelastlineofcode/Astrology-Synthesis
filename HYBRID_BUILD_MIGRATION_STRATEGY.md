# DATA MIGRATION & INTEGRATION STRATEGY

## From Isolated MVPs → Unified Platform

**Duration**: 2 weeks (Dec 3-17, 2025)  
**Timeline**: Weeks 3-4 of hybrid execution  
**Team**: Backend Lead + DevOps + (1 Frontend for testing)  
**Objective**: Seamlessly merge Dasha Timer + Compatibility into single platform without data loss or downtime

---

## OVERVIEW

### Current State (End of Week 2)

```
Dasha Timer MVP:
├── 500+ active users
├── 1000+ signups total
├── PostgreSQL database (schema_dasha)
├── Backend API running on Railway
├── Frontend on Vercel
└── Revenue: $100-200 MRR

Compatibility MVP:
├── 2000+ active users
├── 3000+ signups total
├── PostgreSQL database (schema_compat)
├── Backend API running on Railway
├── Frontend on Vercel
└── Revenue: $300-500 MRR

Total: 4000+ signups, $400-700 MRR, 2 separate systems
```

### Target State (End of Week 4)

```
Unified Mula Platform:
├── 4000+ users (migrated from both apps)
├── 1 database (unified schema)
├── 1 backend (extended FastAPI)
├── 1 frontend (both features visible)
├── 1 auth system (federated logins)
├── 1 payment system (Stripe unified)
├── 1 notification system (FCM unified)
└── Revenue: $400-700 MRR (maintained, not increased yet)

Plus: Ready for features #3-5 in Week 5+
```

---

## PHASE 1: PREPARATION (Days 1-3)

### Day 1: Assessment & Planning

**Tasks:**

```
Backend Lead:
├── Analyze current schema_dasha (PostgreSQL)
├── Analyze current schema_compat (PostgreSQL)
├── Identify data conflicts/duplicates
├── Create unified schema design
├── Document all differences
└── Plan rollback strategy

DevOps:
├── Backup all data (both databases)
├── Create snapshot of both systems
├── Setup staging environment
├── Create migration test database
└── Setup rollback automation

Frontend Lead:
├── Audit current frontend for Dasha Timer
├── Audit current frontend for Compatibility
├── Identify shared components
├── Plan unified navigation
└── Create feature flags for gradual rollout
```

### Unified Database Schema

```sql
-- New unified schema

-- Users (merged, deduplicated)
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100),
    oauth_provider VARCHAR(50),
    oauth_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    INDEX (email),
    INDEX (oauth_provider, oauth_id)
);

-- Birth Charts (merged)
CREATE TABLE birth_charts (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    birth_date TIMESTAMP NOT NULL,
    birth_time VARCHAR(8),
    birth_location_lat FLOAT,
    birth_location_lng FLOAT,
    birth_location_name VARCHAR(255),
    timezone_offset INT,
    chart_data JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    is_default BOOLEAN DEFAULT false,
    INDEX (user_id, created_at),
    INDEX (user_id, is_default)
);

-- Dasha Data (from Dasha Timer)
CREATE TABLE dasha_data (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    chart_id UUID NOT NULL REFERENCES birth_charts(id),
    current_dasha VARCHAR(50),
    current_dasha_start DATE,
    current_dasha_end DATE,
    dasha_sequence JSONB,
    calculated_at TIMESTAMP DEFAULT NOW(),
    INDEX (user_id, updated_at)
);

-- Compatibility Results (from Compatibility Checker)
CREATE TABLE compatibility_results (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    chart1_id UUID NOT NULL REFERENCES birth_charts(id),
    chart2_id UUID REFERENCES birth_charts(id),
    overall_score INT,
    venus_score INT,
    mars_score INT,
    moon_score INT,
    sun_score INT,
    detailed_breakdown JSONB,
    share_code VARCHAR(20) UNIQUE,
    calculated_at TIMESTAMP DEFAULT NOW(),
    view_count INT DEFAULT 0,
    INDEX (user_id, calculated_at),
    INDEX (share_code)
);

-- Subscriptions (unified)
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    stripe_subscription_id VARCHAR(255) UNIQUE,
    plan_name VARCHAR(50),  -- 'free', 'basic', 'premium'
    status VARCHAR(50),
    started_at TIMESTAMP DEFAULT NOW(),
    next_billing_at TIMESTAMP,
    INDEX (user_id, status)
);

-- FCM Tokens (unified)
CREATE TABLE fcm_tokens (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    token VARCHAR(500) NOT NULL,
    device_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true,
    UNIQUE (user_id, token)
);

-- User Preferences (unified)
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) UNIQUE,
    notifications_enabled BOOLEAN DEFAULT true,
    daily_dasha_reminder BOOLEAN DEFAULT true,
    email_enabled BOOLEAN DEFAULT true,
    marketing_emails BOOLEAN DEFAULT false,
    daily_reminder_time TIME DEFAULT '09:00',
    timezone VARCHAR(50) DEFAULT 'UTC',
    data JSONB DEFAULT '{}',
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Activity Log (new for analytics)
CREATE TABLE activity_log (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id),
    action VARCHAR(100),  -- 'viewed_dasha', 'calculated_compat', etc
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX (user_id, created_at),
    INDEX (created_at)
);
```

### Day 2: Migration Scripts

**Create Python migration scripts:**

```python
# migration/migrate_users.py

import psycopg2
from uuid import uuid4
from datetime import datetime

def migrate_users():
    """
    Migrate users from both old schemas to new unified schema.
    Deduplicate by email.
    """

    dasha_conn = psycopg2.connect(os.getenv('DASHA_DATABASE_URL'))
    compat_conn = psycopg2.connect(os.getenv('COMPAT_DATABASE_URL'))
    unified_conn = psycopg2.connect(os.getenv('UNIFIED_DATABASE_URL'))

    dasha_cursor = dasha_conn.cursor()
    compat_cursor = compat_conn.cursor()
    unified_cursor = unified_conn.cursor()

    try:
        # Get all users from Dasha app
        dasha_cursor.execute("SELECT id, email, username, created_at FROM users")
        dasha_users = dasha_cursor.fetchall()

        # Get all users from Compat app
        compat_cursor.execute("SELECT id, email, username, created_at FROM users")
        compat_users = compat_cursor.fetchall()

        # Track mappings for later (old_id -> new_id)
        migrations = {
            'dasha': {},
            'compat': {}
        }

        # Merge users, deduplicating by email
        seen_emails = set()
        all_users = []

        for user in dasha_users:
            if user['email'] not in seen_emails:
                all_users.append(('dasha', user))
                seen_emails.add(user['email'])

        for user in compat_users:
            if user['email'] not in seen_emails:
                all_users.append(('compat', user))
                seen_emails.add(user['email'])

        # Insert into unified database
        for source, user in all_users:
            new_id = str(uuid4())

            unified_cursor.execute("""
                INSERT INTO users (id, email, username, created_at)
                VALUES (%s, %s, %s, %s)
            """, (new_id, user['email'], user['username'], user['created_at']))

            migrations[source][user['id']] = new_id

        unified_conn.commit()

        print(f"✅ Migrated {len(all_users)} users")
        return migrations

    except Exception as e:
        print(f"❌ Error migrating users: {e}")
        unified_conn.rollback()
        raise
    finally:
        dasha_cursor.close()
        compat_cursor.close()
        unified_cursor.close()
        dasha_conn.close()
        compat_conn.close()
        unified_conn.close()
```

```python
# migration/migrate_birth_charts.py

def migrate_birth_charts(user_mappings):
    """Migrate birth charts from both apps."""

    dasha_conn = psycopg2.connect(os.getenv('DASHA_DATABASE_URL'))
    compat_conn = psycopg2.connect(os.getenv('COMPAT_DATABASE_URL'))
    unified_conn = psycopg2.connect(os.getenv('UNIFIED_DATABASE_URL'))

    dasha_cursor = dasha_conn.cursor()
    compat_cursor = compat_conn.cursor()
    unified_cursor = unified_conn.cursor()

    try:
        chart_mappings = {'dasha': {}, 'compat': {}}

        # Migrate Dasha app charts
        dasha_cursor.execute("SELECT * FROM birth_charts")
        dasha_charts = dasha_cursor.fetchall()

        for chart in dasha_charts:
            new_id = str(uuid4())
            new_user_id = user_mappings['dasha'].get(chart['user_id'])

            if not new_user_id:
                print(f"⚠️  User {chart['user_id']} not found, skipping chart")
                continue

            unified_cursor.execute("""
                INSERT INTO birth_charts
                (id, user_id, birth_date, birth_time, birth_location_lat,
                 birth_location_lng, birth_location_name, timezone_offset,
                 chart_data, created_at, is_default)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (new_id, new_user_id, chart['birth_date'], chart['birth_time'],
                  chart['birth_location_lat'], chart['birth_location_lng'],
                  chart['birth_location_name'], chart['timezone_offset'],
                  json.dumps(chart['chart_data']), chart['created_at'],
                  chart['is_default']))

            chart_mappings['dasha'][chart['id']] = new_id

        # Migrate Compat app charts (same process)
        compat_cursor.execute("SELECT * FROM birth_charts")
        compat_charts = compat_cursor.fetchall()

        for chart in compat_charts:
            # Same logic as above but for compat
            pass

        unified_conn.commit()
        print(f"✅ Migrated {len(dasha_charts) + len(compat_charts)} birth charts")
        return chart_mappings

    except Exception as e:
        print(f"❌ Error migrating charts: {e}")
        unified_conn.rollback()
        raise
```

### Day 3: Test Migration & Validation

```python
# migration/validate_migration.py

def validate_migration():
    """Verify migration integrity."""

    unified_conn = psycopg2.connect(os.getenv('UNIFIED_DATABASE_URL'))
    cursor = unified_conn.cursor()

    checks = {
        'users': 0,
        'birth_charts': 0,
        'dasha_data': 0,
        'compatibility_results': 0,
        'errors': []
    }

    # Check users
    cursor.execute("SELECT COUNT(*) FROM users")
    checks['users'] = cursor.fetchone()[0]
    print(f"✅ {checks['users']} users migrated")

    # Check for NULL user_ids (orphaned records)
    cursor.execute("""
        SELECT COUNT(*) FROM birth_charts WHERE user_id IS NULL
    """)
    orphaned = cursor.fetchone()[0]
    if orphaned > 0:
        checks['errors'].append(f"⚠️  {orphaned} orphaned birth_charts")

    # Check for duplicate emails
    cursor.execute("""
        SELECT email, COUNT(*) as count
        FROM users
        GROUP BY email
        HAVING COUNT(*) > 1
    """)
    duplicates = cursor.fetchall()
    if duplicates:
        checks['errors'].append(f"⚠️  {len(duplicates)} duplicate emails found")

    # Verify data integrity
    cursor.execute("""
        SELECT COUNT(*) FROM birth_charts WHERE chart_data IS NULL
    """)
    null_charts = cursor.fetchone()[0]
    if null_charts > 0:
        checks['errors'].append(f"⚠️  {null_charts} charts with NULL data")

    return checks

# Run migration
print("Starting migration...")
user_maps = migrate_users()
chart_maps = migrate_birth_charts(user_maps)
dasha_maps = migrate_dasha_data(user_maps, chart_maps)
compat_maps = migrate_compatibility_results(user_maps, chart_maps)

# Validate
validation = validate_migration()
print(f"Migration validation: {validation}")
```

---

## PHASE 2: CUTOVER (Days 4-7)

### Day 4: Staging Test

**Test in staging environment first:**

```
1. Deploy unified database to staging
2. Deploy migrated data
3. Deploy new unified backend (FastAPI)
4. Deploy new unified frontend
5. QA tests:
   ├── Login with old credentials (federated)
   ├── View Dasha Timer data
   ├── View Compatibility results
   ├── Calculate new compatibility
   ├── Update preferences
   ├── Make purchase (Stripe)
   └── Send notifications (FCM)
6. Load testing: 500 concurrent users
7── Rollback test (verify backups work)
```

### Day 5: Pre-Launch Prep

**Prepare users for transition:**

```
1. Send email: "We're launching an improved Mula platform!"
2. Inform users:
   ├── All data will be preserved
   ├── New features coming soon
   ├── No action needed from them
   ├── Scheduled maintenance (1 hour downtime)
   └── New login might be required (but old credentials still work)

3. Create FAQ:
   ├── "Will I lose my data?" → No, all migrated
   ├── "Do I need new account?" → No, federated login
   ├── "Why the downtime?" → Consolidating systems
   ├── "When can I use new features?" → Coming in Week 5
   └── "Support email" → Support link

4. Prepare support team:
   ├── Brief on what's changing
   ├── Common issues + solutions
   ├── Escalation procedures
   └── Go/no-go meeting
```

### Day 6: Production Cutover

**Execute migration to production (minimal downtime):**

```
Timeline (assume 4 AM UTC = least active time):

3:45 AM: Send notifications
├── "Maintenance starting in 15 minutes"
├── Push notification + Email
└── Display banner on app

4:00 AM: Take both services offline
├── Dasha Timer → Maintenance page
├── Compatibility Checker → Maintenance page
├── Set DNS to static maintenance pages
└── Verify traffic redirects

4:05 AM: Stop all active processes
├── Shutdown Dasha Timer backend
├── Shutdown Compatibility backend
├── Drain in-flight requests
└── Wait for cleanup

4:10 AM: Run migration scripts
├── Execute migrate_users.py (3-5 min)
├── Execute migrate_birth_charts.py (5-10 min)
├── Execute migrate_dasha_data.py (2-3 min)
├── Execute migrate_compatibility_results.py (2-3 min)
├── Validate migration (3-5 min)
└── Total: ~20 minutes

4:35 AM: Deploy unified platform
├── Deploy backend to Railway (new container)
├── Deploy frontend to Vercel (new deployment)
├── Run database migrations
├── Verify health checks
└── Confirm services up

4:50 AM: Test in production
├── Test login (federated)
├── Verify user data visible
├── Check Dasha calculations
├── Verify Compatibility results
├── Test Stripe integration
└── Test FCM notifications

5:00 AM: Go live
├── Remove maintenance pages
├── Update DNS to production
├── Send "We're back!" notification
├── Monitor error tracking (Sentry)
└── Monitor performance (Plausible)

Expected downtime: 45-60 minutes
```

### Day 7: Post-Launch Monitoring

```
Continuous monitoring:
├── Sentry: Check for errors (target: <1% error rate)
├── Plausible: Monitor traffic patterns
├── Database: Monitor performance, query times
├── API response times: Target <500ms p95
├── Notifications: Verify FCM delivery
└── Payments: Verify Stripe working

User support:
├── Monitor support email for issues
├── Have rollback procedure ready
├── Document any issues + fixes
└── Daily standup sync
```

---

## PHASE 3: FEDERATION & UNIFICATION (Days 8-14)

### Day 8-9: Federated Auth Implementation

**Users can now login with credentials from either old system:**

```python
# backend/services/federated_auth.py

class FederatedAuthService:
    """
    Allow users to login with:
    1. Email/password (new unified system)
    2. Old Dasha Timer OAuth token
    3. Old Compatibility OAuth token
    """

    def login_legacy_token(self, legacy_token: str) -> dict:
        """
        User provides old JWT token from either service.
        Validate it, verify source, create new unified token.
        """

        # Decode legacy token (from either service)
        try:
            # Try Dasha Timer key
            payload = jwt.decode(
                legacy_token,
                DASHA_JWT_SECRET,
                algorithms=['HS256']
            )
            legacy_source = 'dasha'
        except:
            try:
                # Try Compatibility key
                payload = jwt.decode(
                    legacy_token,
                    COMPAT_JWT_SECRET,
                    algorithms=['HS256']
                )
                legacy_source = 'compat'
            except:
                raise ValueError("Invalid token")

        # Get email from payload
        email = payload.get('email')
        old_user_id = payload.get('user_id')

        # Look up user in unified database
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError(f"User {email} not found in unified system")

        # Create new unified JWT token
        new_token = jwt.encode({
            'user_id': str(user.id),
            'email': user.email,
            'legacy_source': legacy_source,
            'legacy_user_id': old_user_id,
            'exp': datetime.utcnow() + timedelta(days=30)
        }, UNIFIED_JWT_SECRET, algorithm='HS256')

        # Log migration for analytics
        ActivityLog.create(
            user_id=user.id,
            action='legacy_login_migrated',
            metadata={'source': legacy_source}
        )

        return {
            'token': new_token,
            'user_id': str(user.id),
            'email': user.email,
            'message': 'Welcome to unified Mula platform!'
        }
```

### Day 10-11: Unified Dashboard

**Create single dashboard showing both features:**

```typescript
// frontend/app/dashboard/page.tsx

export default function DashboardPage() {
  const { user } = useAuth();
  const { data: dasha } = useDashaData();
  const { data: lastCompatibility } = useLastCompatibility();

  return (
    <div className="dashboard">
      {/* Header */}
      <header>
        <h1>Welcome, {user.name || user.email}</h1>
        <p>Your Personal Astrology Hub</p>
      </header>

      {/* Feature Cards */}
      <div className="feature-grid">
        {/* Dasha Timer Card */}
        <FeatureCard
          title="Daily Dasha Timer"
          icon="⏰"
          current={dasha?.current_dasha}
          daysRemaining={dasha?.days_remaining}
          onClick={() => router.push('/dasha')}
        />

        {/* Compatibility Card */}
        <FeatureCard
          title="Cosmic Compatibility"
          icon="💕"
          subtitle={lastCompatibility ? `${lastCompatibility.overall_score}% with ${lastCompatibility.partner_name}` : "Check yours"}
          onClick={() => router.push('/compatibility')}
        />

        {/* Coming Soon Cards */}
        <ComingSoonCard title="Moon Phase Rituals" icon="🌙" />
        <ComingSoonCard title="Remedy of the Day" icon="🔮" />
        <ComingSoonCard title="AI Oracle Chat" icon="✨" />
      </div>

      {/* Subscription Status */}
      <SubscriptionBanner />

      {/* Recent Activity */}
      <RecentActivity />
    </div>
  );
}
```

### Day 12-13: Unified Settings & Preferences

```typescript
// frontend/app/dashboard/settings/page.tsx

export default function SettingsPage() {
  return (
    <div className="settings">
      <h2>Settings</h2>

      <SettingsSection title="Notifications">
        <NotificationPreferences />
        {/* Options for all features */}
      </SettingsSection>

      <SettingsSection title="Birth Charts">
        <BirthChartManager />
        {/* Manage all charts from both services */}
      </SettingsSection>

      <SettingsSection title="Subscription">
        <SubscriptionManager />
      </SettingsSection>

      <SettingsSection title="Account">
        <AccountSettings />
        <DeleteAccount />
      </SettingsSection>
    </div>
  );
}
```

### Day 14: Completion & Handoff

```
Final checks:
├── ✅ All user data migrated
├── ✅ All logins working
├── ✅ Dashboard unified
├── ✅ Settings consolidated
├── ✅ Notifications still working
├── ✅ Payments still working
├── ✅ Analytics tracking
├── ✅ Documentation updated
└── ✅ Team trained on new system

Metrics:
├── 4000+ users unified
├── 1500+ birth charts migrated
├── 1000+ compatibility results preserved
├── $400-700 MRR maintained
├── <1% data loss
├── <2% failed logins
└── 100% uptime (post-migration)

Ready for Week 5: Build 3 new features (Rituals, Remedy, Oracle)
```

---

## ROLLBACK PROCEDURES

### If Something Goes Wrong

```
Level 1: Minor bugs (users can't login to one service)
├── Fix and redeploy
├── Notify affected users
└── Continue

Level 2: Data integrity issues (some users' data corrupted)
├── Identify affected users
├── Restore from backup
├── Redeploy with fix
├── Notify affected users
└── Full audit + retry

Level 3: Critical failure (services down, data loss)
├── ACTIVATE ROLLBACK PROCEDURE:
│   ├── Restore both old databases from backups
│   ├── Redeploy old Dasha Timer service
│   ├── Redeploy old Compatibility service
│   ├── Update DNS to point to old services
│   └── Notify all users
├── Post-mortem analysis
├── Fix issues in staging
└── Retry migration in 1 week

Estimated rollback time: 30-45 minutes to old state
```

---

## COMMUNICATION PLAN

### To Users

**Before Migration:**

```
Subject: "Mula Platform Upgrade - This Saturday at 4 AM UTC"

Hi [User],

We're consolidating Dasha Timer and Compatibility Checker into one unified Mula platform!

📅 What's happening:
- Short maintenance (45-60 minutes)
- All your data is preserved
- New features coming soon
- No action needed from you

✅ What you can expect:
- Faster performance
- Better notifications
- Unified preferences
- New features launching next week

⏰ Scheduled maintenance:
- Saturday, Dec 6, 4:00-5:00 AM UTC
- You'll see maintenance page
- Services back online after ~1 hour

Questions? Support@mula.app
```

**After Migration:**

```
Subject: "✨ Welcome to Unified Mula Platform"

Hi [User],

You're now on our new unified platform!

🎉 What's new:
- Single dashboard for all features
- Faster calculations
- Better notifications
- Seamless experience

🚀 Coming next week:
- Moon Phase Rituals
- Remedy of the Day
- AI Oracle Chat
- And more...

Enjoy exploring!
```

### To Team

**Pre-migration sync:**

- Engineering lead: reviews migration scripts
- QA: reviews test plan
- Support: briefs on issues + solutions
- Operations: confirms infrastructure ready

**Go/no-go meeting:**

- All leads present
- Review: staging test results
- Confirm: all systems ready
- Decision: proceed or delay?

---

## RISK MITIGATION

| Risk                    | Probability | Impact                  | Mitigation                                   |
| ----------------------- | ----------- | ----------------------- | -------------------------------------------- |
| Migration takes >1 hour | Medium      | User frustration        | Test staging thoroughly, have rollback ready |
| Users can't login       | High        | Service dead            | Federated auth tested beforehand             |
| Data corruption         | Low         | Data loss, legal issues | Backups, validation scripts, audit trail     |
| Performance degrades    | Medium      | Users leave             | Load test, optimize queries                  |
| Stripe breaks           | Low         | No revenue              | Test Stripe webhook before cutover           |

---

## SUCCESS CRITERIA

```
✅ Migration Complete When:
├── 4000+ users migrated
├── All data validated (100% integrity)
├── Federated login working
├── Dashboard unified
├── 0 critical bugs
├── <2% failed logins
├── Performance: p95 <500ms
├── 0 unplanned downtime
├── $400-700 MRR maintained
└── All users can see both features

Ready for Week 5:
├── Full platform architecture in place
├── 3 new features can be added easily
├── 10,000+ user capacity proven
└── $1M+ ARR roadmap enabled
```

---

## TIMELINE SUMMARY

```
Week 1 (Nov 8-15): Dasha Timer MVP launched
Week 2 (Nov 15-22): Compatibility Checker launched
Week 3 (Nov 22-29): Data Migration
├── Days 1-3: Preparation
├── Days 4-5: Testing
├── Days 6-7: Cutover
└── Days 8-14: Federation

Week 4 (Nov 29-Dec 6): Unified Dashboard
├── Days 1-3: Federated auth
├── Days 4-7: Dashboard + Settings
└── Days 8-10: Quality assurance

Week 5+ (Dec 9+): Build 3 New Features
├── Moon Phase Rituals
├── Remedy of the Day
├── AI Oracle Chat

Total: 4-week journey from "build first MVP" to "5-feature unified platform"
```

**Ready to execute?** 🚀
