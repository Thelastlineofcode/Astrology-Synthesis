# Detailed Database Schema - Phase 3

## Astrology-Synthesis API Database

**Date:** November 1, 2025  
**Database:** PostgreSQL 14+  
**Status:** 🎯 SCHEMA READY FOR IMPLEMENTATION

---

## 1. Database Design Principles

- **Normalization:** 3NF for transactional data
- **Auditability:** Complete audit trail for all changes
- **Performance:** Indexing strategy for common queries
- **Security:** Encryption at rest for sensitive data
- **Scalability:** Horizontal scaling with read replicas
- **GDPR Compliance:** Data retention policies, right to deletion

---

## 2. User & Authentication Schema

### 2.1 users Table

```sql
CREATE TABLE users (
  user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  email_verified BOOLEAN DEFAULT FALSE,
  email_verified_at TIMESTAMP NULL,
  password_hash VARCHAR(255) NOT NULL,
  password_changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  -- Profile Information
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  phone_number VARCHAR(20),
  timezone VARCHAR(50) DEFAULT 'UTC',
  language VARCHAR(10) DEFAULT 'en',

  -- Subscription
  subscription_tier VARCHAR(50) DEFAULT 'free',
  -- Tiers: free, basic, pro, enterprise
  subscription_started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  subscription_expires_at TIMESTAMP NULL,
  subscription_cancelled_at TIMESTAMP NULL,

  -- API Access
  api_key_hash VARCHAR(255) UNIQUE,
  api_key_created_at TIMESTAMP NULL,

  -- Account Status
  is_active BOOLEAN DEFAULT TRUE,
  is_admin BOOLEAN DEFAULT FALSE,
  is_verified BOOLEAN DEFAULT FALSE,

  -- Metadata
  last_login_at TIMESTAMP NULL,
  login_count INTEGER DEFAULT 0,
  failed_login_attempts INTEGER DEFAULT 0,
  locked_until TIMESTAMP NULL,

  -- Audit
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL, -- Soft delete for GDPR

  CONSTRAINT email_format CHECK (email ~ '^[^@]+@[^@]+\.[^@]+$'),
  CONSTRAINT valid_subscription FOREIGN KEY (subscription_tier)
    REFERENCES subscription_tiers(tier_name)
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_api_key_hash ON users(api_key_hash);
CREATE INDEX idx_users_created_at ON users(created_at DESC);
CREATE INDEX idx_users_is_active ON users(is_active);
```

### 2.2 subscription_tiers Table

```sql
CREATE TABLE subscription_tiers (
  tier_name VARCHAR(50) PRIMARY KEY,
  display_name VARCHAR(255) NOT NULL,
  description TEXT,
  monthly_price DECIMAL(10, 2),
  annual_price DECIMAL(10, 2),

  -- Rate Limits
  predictions_per_hour INTEGER,
  charts_per_hour INTEGER,
  transits_queries_per_hour INTEGER,
  max_concurrent_requests INTEGER,

  -- Features
  includes_remedies BOOLEAN DEFAULT FALSE,
  includes_multitradition BOOLEAN DEFAULT FALSE,
  includes_api_access BOOLEAN DEFAULT FALSE,
  includes_batch_predictions BOOLEAN DEFAULT FALSE,
  includes_historical_data BOOLEAN DEFAULT FALSE,

  -- Support
  email_support BOOLEAN DEFAULT FALSE,
  priority_support BOOLEAN DEFAULT FALSE,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO subscription_tiers VALUES
('free', 'Free Plan', 'Basic predictions', 0, 0, 5, 3, 10, 1, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE),
('basic', 'Basic Plan', 'Enhanced features', 9.99, 99.90, 50, 20, 100, 5, TRUE, FALSE, TRUE, FALSE, FALSE, TRUE, FALSE),
('pro', 'Pro Plan', 'Professional features', 29.99, 299.90, 500, 200, 1000, 20, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE),
('enterprise', 'Enterprise', 'Custom solutions', NULL, NULL, NULL, NULL, NULL, NULL, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE);
```

### 2.3 sessions Table

```sql
CREATE TABLE sessions (
  session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,

  access_token_hash VARCHAR(255) UNIQUE NOT NULL,
  refresh_token_hash VARCHAR(255) UNIQUE NOT NULL,

  -- Token Metadata
  access_token_expires_at TIMESTAMP NOT NULL,
  refresh_token_expires_at TIMESTAMP NOT NULL,

  -- Session Details
  ip_address INET,
  user_agent TEXT,
  device_type VARCHAR(50), -- mobile, desktop, tablet, other
  device_os VARCHAR(50),   -- ios, android, windows, macos, linux

  is_valid BOOLEAN DEFAULT TRUE,
  revoked_at TIMESTAMP NULL,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_access_token_hash ON sessions(access_token_hash);
CREATE INDEX idx_sessions_is_valid ON sessions(is_valid);
CREATE INDEX idx_sessions_created_at ON sessions(created_at DESC);
```

---

## 3. Birth Chart Schema

### 3.1 birth_charts Table

```sql
CREATE TABLE birth_charts (
  chart_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,

  -- Birth Information
  subject_name VARCHAR(255),
  birth_date DATE NOT NULL,
  birth_time TIME NOT NULL,
  timezone VARCHAR(50) NOT NULL,
  latitude DECIMAL(10, 6) NOT NULL,
  longitude DECIMAL(10, 6) NOT NULL,

  -- Chart Configuration
  house_system VARCHAR(10) DEFAULT 'placidus',
  ayanamsa VARCHAR(50) DEFAULT 'lahiri',

  -- Calculated Data (stored as JSON for flexibility)
  planetary_positions JSONB NOT NULL,  -- Array of PlanetPosition objects
  house_cusps JSONB NOT NULL,          -- HouseCusps object
  aspects JSONB,                        -- Array of AspectData objects

  -- Additional Data
  nakshatras_info JSONB,               -- Nakshatra information
  dasha_info JSONB,                    -- Dasha positions and timeline

  -- Metadata
  is_birth_time_rectified BOOLEAN DEFAULT FALSE,
  notes TEXT,

  -- Audit
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_birth_charts_user_id ON birth_charts(user_id);
CREATE INDEX idx_birth_charts_created_at ON birth_charts(created_at DESC);
CREATE INDEX idx_birth_charts_birth_date ON birth_charts(birth_date);
```

### 3.2 chart_compatibility Table

```sql
CREATE TABLE chart_compatibility (
  compatibility_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,

  chart1_id UUID NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,
  chart2_id UUID NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,

  relationship_type VARCHAR(50), -- marriage, business, friendship

  -- Compatibility Scores
  overall_score DECIMAL(3, 2),
  emotional_score DECIMAL(3, 2),
  intellectual_score DECIMAL(3, 2),
  spiritual_score DECIMAL(3, 2),
  physical_score DECIMAL(3, 2),

  -- Analysis Data
  synastry_aspects JSONB,
  strengths TEXT,
  challenges TEXT,
  recommendations TEXT,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL,

  CONSTRAINT different_charts CHECK (chart1_id != chart2_id)
);

CREATE INDEX idx_compatibility_user_id ON chart_compatibility(user_id);
CREATE INDEX idx_compatibility_chart1_id ON chart_compatibility(chart1_id);
CREATE INDEX idx_compatibility_chart2_id ON chart_compatibility(chart2_id);
```

---

## 4. Prediction Schema

### 4.1 predictions Table

```sql
CREATE TABLE predictions (
  prediction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  chart_id UUID NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,

  -- Query
  query_text TEXT NOT NULL,
  event_types TEXT[], -- marriage, career, health, finances, etc.

  -- Prediction Data
  prediction_data JSONB NOT NULL, -- Full prediction object

  -- Confidence Scores
  overall_confidence DECIMAL(3, 2),
  kp_confidence DECIMAL(3, 2),
  dasha_confidence DECIMAL(3, 2),
  transit_confidence DECIMAL(3, 2),
  syncretic_confidence DECIMAL(3, 2),

  -- Traditions Analyzed
  traditions_analyzed TEXT[], -- kp, vedic, vodou, etc.

  -- Timeframe
  timeframe_start DATE,
  timeframe_end DATE,
  peak_date DATE,

  -- Status
  is_verified BOOLEAN DEFAULT FALSE,
  actual_outcome VARCHAR(50), -- accurate, inaccurate, null, pending
  outcome_verified_at TIMESTAMP NULL,

  -- User Feedback
  feedback_score INTEGER,          -- 1-5 stars
  feedback_text TEXT,
  feedback_submitted_at TIMESTAMP NULL,

  -- Audit
  generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP,
  deleted_at TIMESTAMP NULL
);

CREATE INDEX idx_predictions_user_id ON predictions(user_id);
CREATE INDEX idx_predictions_chart_id ON predictions(chart_id);
CREATE INDEX idx_predictions_timeframe_start ON predictions(timeframe_start);
CREATE INDEX idx_predictions_overall_confidence ON predictions(overall_confidence DESC);
CREATE INDEX idx_predictions_generated_at ON predictions(generated_at DESC);
```

### 4.2 prediction_events Table (Detailed Events)

```sql
CREATE TABLE prediction_events (
  event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  prediction_id UUID NOT NULL REFERENCES predictions(prediction_id) ON DELETE CASCADE,

  event_type VARCHAR(50) NOT NULL,
  event_data JSONB NOT NULL,

  event_start DATE,
  event_end DATE,
  event_peak DATE,

  confidence DECIMAL(3, 2),
  planetary_support JSONB,
  dasha_support JSONB,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_prediction_events_prediction_id ON prediction_events(prediction_id);
CREATE INDEX idx_prediction_events_event_type ON prediction_events(event_type);
```

---

## 5. Transit Analysis Schema

### 5.1 transits Table

```sql
CREATE TABLE transits (
  transit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chart_id UUID NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,

  -- Transit Information
  planet_name VARCHAR(50) NOT NULL,
  transit_date DATE NOT NULL,

  -- Position Data
  longitude DECIMAL(8, 4),
  latitude DECIMAL(8, 4),
  sign VARCHAR(20),
  house INTEGER,

  -- Aspects
  aspects_to_natal JSONB,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transits_chart_id ON transits(chart_id);
CREATE INDEX idx_transits_transit_date ON transits(transit_date);
CREATE INDEX idx_transits_planet_name ON transits(planet_name);
```

### 5.2 transit_windows Table

```sql
CREATE TABLE transit_windows (
  window_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chart_id UUID NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,

  -- Window Information
  event_type VARCHAR(50),
  window_start DATE,
  window_end DATE,
  peak_date DATE,

  -- Confidence & Analysis
  confidence DECIMAL(3, 2),
  confidence_kp DECIMAL(3, 2),
  confidence_dasha DECIMAL(3, 2),
  confidence_transit DECIMAL(3, 2),

  -- Details
  planetary_activations TEXT[],
  dasha_support VARCHAR(100),
  interpretation TEXT,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transit_windows_chart_id ON transit_windows(chart_id);
CREATE INDEX idx_transit_windows_window_start ON transit_windows(window_start);
CREATE INDEX idx_transit_windows_confidence ON transit_windows(confidence DESC);
```

---

## 6. Remedies Schema

### 6.1 remedies Table

```sql
CREATE TABLE remedies (
  remedy_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  tradition VARCHAR(50) NOT NULL,  -- vedic, vodou, rosicrucian, arabic
  remedy_type VARCHAR(50) NOT NULL, -- mantra, gemstone, ritual, color, etc.

  -- Remedy Details
  name VARCHAR(255) NOT NULL,
  description TEXT,
  detailed_instructions TEXT,

  -- Effectiveness
  effectiveness_score DECIMAL(3, 2),
  difficulty_level VARCHAR(20), -- easy, moderate, hard
  cost_level VARCHAR(20),        -- low, medium, high
  duration_days INTEGER,

  -- Associations
  associated_planets TEXT[],
  associated_houses INTEGER[],

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_remedies_tradition ON remedies(tradition);
CREATE INDEX idx_remedies_remedy_type ON remedies(remedy_type);
```

### 6.2 prediction_remedies Table (Junction)

```sql
CREATE TABLE prediction_remedies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  prediction_id UUID NOT NULL REFERENCES predictions(prediction_id) ON DELETE CASCADE,
  remedy_id UUID NOT NULL REFERENCES remedies(remedy_id) ON DELETE RESTRICT,

  recommended_effectiveness DECIMAL(3, 2),
  recommendation_notes TEXT,
  user_completed BOOLEAN DEFAULT FALSE,
  completion_notes TEXT,
  completed_at TIMESTAMP NULL,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  UNIQUE(prediction_id, remedy_id)
);

CREATE INDEX idx_prediction_remedies_prediction_id ON prediction_remedies(prediction_id);
CREATE INDEX idx_prediction_remedies_remedy_id ON prediction_remedies(remedy_id);
```

---

## 7. Ephemeris Cache Schema

### 7.1 ephemeris_cache Table

```sql
CREATE TABLE ephemeris_cache (
  cache_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Query Parameters
  planet_name VARCHAR(50) NOT NULL,
  query_date DATE NOT NULL,
  house_system VARCHAR(10) NOT NULL,
  ayanamsa VARCHAR(50) NOT NULL,

  -- Cached Data
  position_data JSONB NOT NULL, -- PlanetPosition object
  house_cusps_data JSONB,       -- HouseCusps object (if house-dependent)

  -- Metadata
  calculation_time_ms INTEGER,
  cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP,

  UNIQUE(planet_name, query_date, house_system, ayanamsa)
);

CREATE INDEX idx_ephemeris_cache_query_date ON ephemeris_cache(query_date);
CREATE INDEX idx_ephemeris_cache_planet_name ON ephemeris_cache(planet_name);
CREATE INDEX idx_ephemeris_cache_expires_at ON ephemeris_cache(expires_at);
```

### 7.2 ephemeris_batch_cache Table

```sql
CREATE TABLE ephemeris_batch_cache (
  batch_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  query_date DATE NOT NULL,
  house_system VARCHAR(10) NOT NULL,
  ayanamsa VARCHAR(50) NOT NULL,

  -- All planets data
  all_planets_data JSONB NOT NULL,

  cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP,

  UNIQUE(query_date, house_system, ayanamsa)
);

CREATE INDEX idx_ephemeris_batch_query_date ON ephemeris_batch_cache(query_date);
```

---

## 8. Audit & Logging Schema

### 8.1 audit_log Table

```sql
CREATE TABLE audit_log (
  log_id BIGSERIAL PRIMARY KEY,

  -- User Information
  user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,

  -- Action Details
  action VARCHAR(100) NOT NULL,
  resource_type VARCHAR(50),    -- chart, prediction, user, etc.
  resource_id VARCHAR(100),

  -- Changes
  old_values JSONB,
  new_values JSONB,
  change_summary TEXT,

  -- Request Info
  ip_address INET,
  user_agent TEXT,
  session_id UUID REFERENCES sessions(session_id) ON DELETE SET NULL,

  -- Status
  success BOOLEAN DEFAULT TRUE,
  error_message TEXT,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX idx_audit_log_resource_type_id ON audit_log(resource_type, resource_id);
CREATE INDEX idx_audit_log_action ON audit_log(action);
CREATE INDEX idx_audit_log_created_at ON audit_log(created_at DESC);
```

### 8.2 api_request_log Table

```sql
CREATE TABLE api_request_log (
  request_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,

  -- Request Details
  method VARCHAR(10),
  endpoint VARCHAR(500),
  query_params TEXT,

  -- Response
  status_code INTEGER,
  response_time_ms INTEGER,
  response_size_bytes INTEGER,

  -- Error Info
  error_code VARCHAR(100),
  error_message TEXT,

  -- Request Context
  ip_address INET,
  user_agent TEXT,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_api_request_log_user_id ON api_request_log(user_id);
CREATE INDEX idx_api_request_log_endpoint ON api_request_log(endpoint);
CREATE INDEX idx_api_request_log_status_code ON api_request_log(status_code);
CREATE INDEX idx_api_request_log_created_at ON api_request_log(created_at DESC);
```

---

## 9. Data Retention & GDPR Schema

### 9.1 user_data_requests Table

```sql
CREATE TABLE user_data_requests (
  request_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,

  -- Request Type
  request_type VARCHAR(50) NOT NULL, -- access, deletion, portability, rectification

  -- Status
  status VARCHAR(50) DEFAULT 'pending', -- pending, approved, completed, rejected
  status_notes TEXT,

  -- Processing
  requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  due_date TIMESTAMP,
  completed_at TIMESTAMP NULL,

  -- Data Location
  data_file_url VARCHAR(500),

  CONSTRAINT valid_request_type CHECK (request_type IN ('access', 'deletion', 'portability', 'rectification'))
);

CREATE INDEX idx_user_data_requests_user_id ON user_data_requests(user_id);
CREATE INDEX idx_user_data_requests_status ON user_data_requests(status);
CREATE INDEX idx_user_data_requests_due_date ON user_data_requests(due_date);
```

### 9.2 data_retention_policy Table

```sql
CREATE TABLE data_retention_policy (
  policy_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  data_type VARCHAR(50) NOT NULL,
  retention_days INTEGER NOT NULL,

  -- Policy Details
  description TEXT,
  applies_to_deleted_users BOOLEAN DEFAULT TRUE,
  applies_to_inactive_users BOOLEAN DEFAULT FALSE,
  inactive_days_trigger INTEGER, -- days of inactivity before policy applies

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Default policies
INSERT INTO data_retention_policy (data_type, retention_days, description) VALUES
('application_logs', 30, 'Application event logs'),
('api_request_logs', 90, 'API request history'),
('audit_logs', 365, 'System audit trail'),
('ephemeris_cache', 90, 'Cached ephemeris calculations'),
('deleted_predictions', 30, 'Soft-deleted predictions'),
('deleted_charts', 30, 'Soft-deleted birth charts'),
('deleted_accounts', 90, 'Deleted user account data');
```

---

## 10. Notification Schema

### 10.1 notifications Table

```sql
CREATE TABLE notifications (
  notification_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,

  -- Notification Details
  type VARCHAR(50), -- prediction_ready, transit_alert, remedies_reminder
  title VARCHAR(255),
  message TEXT,

  -- Link to Resource
  resource_type VARCHAR(50),
  resource_id UUID,

  -- Status
  is_read BOOLEAN DEFAULT FALSE,
  read_at TIMESTAMP NULL,

  -- Delivery
  delivery_method VARCHAR(50), -- email, push, in_app
  delivered_at TIMESTAMP NULL,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);
```

---

## 11. Analytics Schema

### 11.1 analytics_events Table

```sql
CREATE TABLE analytics_events (
  event_id BIGSERIAL PRIMARY KEY,

  user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,

  event_name VARCHAR(100) NOT NULL,
  event_properties JSONB,

  page_url VARCHAR(500),
  referrer VARCHAR(500),

  session_id UUID,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_analytics_events_user_id ON analytics_events(user_id);
CREATE INDEX idx_analytics_events_event_name ON analytics_events(event_name);
CREATE INDEX idx_analytics_events_created_at ON analytics_events(created_at DESC);
```

### 11.2 daily_metrics Table

```sql
CREATE TABLE daily_metrics (
  metric_date DATE PRIMARY KEY,

  total_predictions INTEGER DEFAULT 0,
  total_charts INTEGER DEFAULT 0,
  total_comparisons INTEGER DEFAULT 0,
  active_users INTEGER DEFAULT 0,
  new_users INTEGER DEFAULT 0,

  average_confidence DECIMAL(3, 2),
  average_response_time_ms DECIMAL(7, 2),

  error_rate DECIMAL(5, 2),
  api_requests INTEGER DEFAULT 0,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_daily_metrics_metric_date ON daily_metrics(metric_date DESC);
```

---

## 12. Performance Optimization

### 12.1 Indexing Strategy

**Most Frequently Queried:**

- `users.email` (unique index)
- `predictions.user_id` (composite with created_at)
- `birth_charts.user_id` (composite with created_at)
- `transit_windows.chart_id` (composite with window_start)

**Analytical Queries:**

- `predictions.overall_confidence` (DESC)
- `predictions.generated_at` (DESC)
- `daily_metrics.metric_date` (DESC)

**Full-text Search (Future):**

```sql
CREATE INDEX idx_predictions_query_text_fts
  ON predictions
  USING GIN (to_tsvector('english', query_text));
```

### 12.2 Partitioning Strategy

**Partitioned Tables (for very large volumes):**

```sql
-- Partition predictions by year
CREATE TABLE predictions_2025 PARTITION OF predictions
  FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

-- Partition audit_log by month
CREATE TABLE audit_log_2025_11 PARTITION OF audit_log
  FOR VALUES FROM (202511) TO (202512);
```

---

## 13. Database Administration

### 13.1 Backup Strategy

```sql
-- Full backup (daily at 2 AM)
pg_dump -U postgres astrology_synthesis > backup_$(date +%Y%m%d).sql

-- PITR (Point-in-time recovery)
-- Store WAL archives for 30-day recovery window

-- Replication setup (standby server)
-- Primary → Standby (synchronous replication)
```

### 13.2 Maintenance

```sql
-- Weekly vacuum and analyze
VACUUM ANALYZE;

-- Monthly index maintenance
REINDEX INDEX CONCURRENTLY idx_predictions_user_id;

-- Quarterly constraint integrity check
ALTER TABLE predictions VALIDATE CONSTRAINT ...;
```

---

## 14. Security Measures

### 14.1 Column Encryption

```sql
-- Sensitive data encrypted at rest
ALTER TABLE users ADD COLUMN phone_number_encrypted bytea;
ALTER TABLE birth_charts ADD COLUMN latitude_encrypted bytea;

-- Encryption function using pgcrypto
SELECT pgp_sym_encrypt(phone_number, 'encryption_key')::bytea
  FROM users;
```

### 14.2 Row-Level Security (RLS)

```sql
-- Enable RLS
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own predictions
CREATE POLICY user_predictions_policy ON predictions
  USING (user_id = current_user_id());

CREATE POLICY user_predictions_policy ON predictions
  WITH CHECK (user_id = current_user_id());
```

---

## 15. Implementation Checklist

- [ ] Create PostgreSQL instance (RDS or self-managed)
- [ ] Create database `astrology_synthesis`
- [ ] Run all schema creation scripts
- [ ] Create default subscription tiers
- [ ] Create indices
- [ ] Configure backups and replication
- [ ] Enable RLS for multi-tenancy
- [ ] Test connection pooling
- [ ] Load initial data
- [ ] Run performance tests

---

## Appendix: Sample Queries

### Queries for Common Operations

**Get user's latest prediction:**

```sql
SELECT * FROM predictions
WHERE user_id = $1
ORDER BY generated_at DESC
LIMIT 1;
```

**Get upcoming transits for a chart:**

```sql
SELECT * FROM transit_windows
WHERE chart_id = $1
  AND window_start >= CURRENT_DATE
ORDER BY window_start ASC;
```

**User predictions per subscription tier:**

```sql
SELECT
  u.subscription_tier,
  COUNT(p.prediction_id) as prediction_count
FROM users u
LEFT JOIN predictions p ON u.user_id = p.user_id
GROUP BY u.subscription_tier;
```

---

**Database schema fully specified and ready for implementation.**
