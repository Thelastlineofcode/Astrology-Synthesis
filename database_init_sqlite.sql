-- ============================================================================
-- ASTROLOGY SYNTHESIS DATABASE SCHEMA
-- SQLite DDL for Phase 3 Implementation (Personal Development)
-- Generated: November 1, 2025
-- ============================================================================
-- NOTE: This SQLite schema is equivalent to PostgreSQL but optimized for
-- local development. Easily migrate to PostgreSQL later without code changes.
-- ============================================================================

-- ============================================================================
-- AUTHENTICATION LAYER (2 tables)
-- ============================================================================

-- Users table - User accounts with authentication
CREATE TABLE IF NOT EXISTS users (
  user_id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  first_name TEXT,
  last_name TEXT,
  password_hash TEXT NOT NULL,
  api_key TEXT UNIQUE,
  is_active BOOLEAN DEFAULT 1,
  is_verified BOOLEAN DEFAULT 0,
  verification_code TEXT,
  failed_login_attempts INTEGER DEFAULT 0,
  locked_until TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP,
  CHECK (email LIKE '%@%.%')
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_api_key ON users(api_key);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_users_deleted_at ON users(deleted_at);

-- API Keys table - Programmatic access for integrations
CREATE TABLE IF NOT EXISTS api_keys (
  key_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  key_name TEXT NOT NULL,
  api_key_hash TEXT UNIQUE NOT NULL,
  is_active BOOLEAN DEFAULT 1,
  last_used_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_api_keys_user ON api_keys(user_id);
CREATE INDEX IF NOT EXISTS idx_api_keys_hash ON api_keys(api_key_hash);
CREATE INDEX IF NOT EXISTS idx_api_keys_is_active ON api_keys(is_active);

-- ============================================================================
-- DATA LAYER (3 tables)
-- ============================================================================

-- Birth Charts table - User's astrological birth charts
CREATE TABLE IF NOT EXISTS birth_charts (
  chart_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  birth_date DATE NOT NULL,
  birth_time TIME,
  birth_latitude REAL NOT NULL,
  birth_longitude REAL NOT NULL,
  birth_location VARCHAR(255),
  timezone TEXT,
  chart_data JSON,
  ayanamsa TEXT DEFAULT 'LAHIRI',
  house_system TEXT DEFAULT 'PLACIDUS',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP,
  CHECK (birth_latitude >= -90 AND birth_latitude <= 90),
  CHECK (birth_longitude >= -180 AND birth_longitude <= 180)
);

CREATE INDEX IF NOT EXISTS idx_birth_charts_user ON birth_charts(user_id);
CREATE INDEX IF NOT EXISTS idx_birth_charts_birth_date ON birth_charts(birth_date);
CREATE INDEX IF NOT EXISTS idx_birth_charts_created_at ON birth_charts(created_at);
CREATE INDEX IF NOT EXISTS idx_birth_charts_deleted_at ON birth_charts(deleted_at);

-- Predictions table - Astrological predictions for users
CREATE TABLE IF NOT EXISTS predictions (
  prediction_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  chart_id TEXT REFERENCES birth_charts(chart_id) ON DELETE SET NULL,
  prediction_type TEXT NOT NULL,
  prediction_date_start DATE NOT NULL,
  prediction_date_end DATE,
  confidence_score INTEGER CHECK (confidence_score >= 0 AND confidence_score <= 100),
  strength_classification TEXT,
  prediction_data JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_predictions_user ON predictions(user_id);
CREATE INDEX IF NOT EXISTS idx_predictions_chart ON predictions(chart_id);
CREATE INDEX IF NOT EXISTS idx_predictions_type ON predictions(prediction_type);
CREATE INDEX IF NOT EXISTS idx_predictions_date_start ON predictions(prediction_date_start);
CREATE INDEX IF NOT EXISTS idx_predictions_deleted_at ON predictions(deleted_at);

-- Transits table - Planetary transits and their effects
CREATE TABLE IF NOT EXISTS transits (
  transit_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  chart_id TEXT REFERENCES birth_charts(chart_id) ON DELETE SET NULL,
  transit_planet TEXT NOT NULL,
  natal_planet TEXT NOT NULL,
  transit_date_start DATE NOT NULL,
  transit_date_end DATE,
  orb_degrees REAL,
  interpretation TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_transits_user ON transits(user_id);
CREATE INDEX IF NOT EXISTS idx_transits_chart ON transits(chart_id);
CREATE INDEX IF NOT EXISTS idx_transits_transit_planet ON transits(transit_planet);
CREATE INDEX IF NOT EXISTS idx_transits_natal_planet ON transits(natal_planet);
CREATE INDEX IF NOT EXISTS idx_transits_date_start ON transits(transit_date_start);

-- ============================================================================
-- CALCULATION LAYER - CACHING (4 tables)
-- ============================================================================

-- KP Calculations cache - Krishnamurthy Paddhati results
CREATE TABLE IF NOT EXISTS kp_calculations (
  calc_id TEXT PRIMARY KEY,
  chart_id TEXT NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,
  calculation_type TEXT NOT NULL,
  calculation_data JSON,
  confidence_score REAL,
  expires_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_kp_calculations_chart ON kp_calculations(chart_id);
CREATE INDEX IF NOT EXISTS idx_kp_calculations_expires_at ON kp_calculations(expires_at);

-- Dasha Calculations cache - Vimshottari Dasha periods
CREATE TABLE IF NOT EXISTS dasha_calculations (
  calc_id TEXT PRIMARY KEY,
  chart_id TEXT NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,
  mahadasha_lord TEXT,
  antardasha_lord TEXT,
  pratyantardasha_lord TEXT,
  period_start_date DATE,
  period_end_date DATE,
  calculation_data JSON,
  expires_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_dasha_calculations_chart ON dasha_calculations(chart_id);
CREATE INDEX IF NOT EXISTS idx_dasha_calculations_mahadasha ON dasha_calculations(mahadasha_lord);
CREATE INDEX IF NOT EXISTS idx_dasha_calculations_expires_at ON dasha_calculations(expires_at);

-- Transit Calculations cache - Transit analysis results
CREATE TABLE IF NOT EXISTS transit_calculations (
  calc_id TEXT PRIMARY KEY,
  chart_id TEXT NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,
  transit_date DATE NOT NULL,
  calculation_data JSON,
  event_probability REAL,
  expires_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_transit_calculations_chart ON transit_calculations(chart_id);
CREATE INDEX IF NOT EXISTS idx_transit_calculations_date ON transit_calculations(transit_date);
CREATE INDEX IF NOT EXISTS idx_transit_calculations_expires_at ON transit_calculations(expires_at);

-- Ephemeris cache - Planetary positions cache
CREATE TABLE IF NOT EXISTS ephemeris_cache (
  cache_id TEXT PRIMARY KEY,
  calculation_date DATE NOT NULL,
  body TEXT NOT NULL,
  position_data JSON,
  expires_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(calculation_date, body)
);

CREATE INDEX IF NOT EXISTS idx_ephemeris_cache_date ON ephemeris_cache(calculation_date);
CREATE INDEX IF NOT EXISTS idx_ephemeris_cache_body ON ephemeris_cache(body);
CREATE INDEX IF NOT EXISTS idx_ephemeris_cache_expires_at ON ephemeris_cache(expires_at);

-- ============================================================================
-- KNOWLEDGE LAYER (4 tables)
-- ============================================================================

-- Remedies table - Astrological remedies and recommendations
CREATE TABLE IF NOT EXISTS remedies (
  remedy_id TEXT PRIMARY KEY,
  remedy_name TEXT NOT NULL,
  remedy_type TEXT NOT NULL,
  associated_planet TEXT,
  associated_sign TEXT,
  cost_estimate_low INTEGER,
  cost_estimate_high INTEGER,
  description TEXT,
  recommendation_timing TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_remedies_type ON remedies(remedy_type);
CREATE INDEX IF NOT EXISTS idx_remedies_planet ON remedies(associated_planet);

-- Interpretations table - Astrological interpretations library
CREATE TABLE IF NOT EXISTS interpretations (
  interpretation_id TEXT PRIMARY KEY,
  interpretation_type TEXT NOT NULL,
  subject_area TEXT NOT NULL,
  interpretation_text TEXT,
  confidence_level REAL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_interpretations_type ON interpretations(interpretation_type);
CREATE INDEX IF NOT EXISTS idx_interpretations_subject ON interpretations(subject_area);

-- Event Patterns table - Historical event patterns for validation
CREATE TABLE IF NOT EXISTS event_patterns (
  pattern_id TEXT PRIMARY KEY,
  pattern_name TEXT NOT NULL,
  pattern_type TEXT NOT NULL,
  accuracy_percentage REAL,
  sample_size INTEGER,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_event_patterns_type ON event_patterns(pattern_type);

-- Astrological Constants table - System constants for calculations
CREATE TABLE IF NOT EXISTS astrological_constants (
  constant_id TEXT PRIMARY KEY,
  constant_name TEXT NOT NULL UNIQUE,
  constant_value TEXT NOT NULL,
  constant_type TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_astrological_constants_name ON astrological_constants(constant_name);

-- ============================================================================
-- SYSTEM LAYER (2 tables)
-- ============================================================================

-- Audit Logs table - Track all significant user actions
CREATE TABLE IF NOT EXISTS audit_logs (
  log_id TEXT PRIMARY KEY,
  user_id TEXT REFERENCES users(user_id) ON DELETE SET NULL,
  action_type TEXT NOT NULL,
  resource_type TEXT,
  resource_id TEXT,
  changes TEXT,
  ip_address TEXT,
  user_agent TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action_type);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

-- System Settings table - Configuration for API behavior
CREATE TABLE IF NOT EXISTS system_settings (
  setting_id TEXT PRIMARY KEY,
  setting_name TEXT NOT NULL UNIQUE,
  setting_value TEXT NOT NULL,
  setting_type TEXT NOT NULL,
  description TEXT,
  is_editable BOOLEAN DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_system_settings_name ON system_settings(setting_name);

-- ============================================================================
-- INITIALIZATION DATA
-- ============================================================================

-- Insert astrological constants
INSERT OR IGNORE INTO astrological_constants (constant_id, constant_name, constant_value, constant_type, description) VALUES
  ('const_001', 'zodiac_signs', '["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]', 'array', 'The 12 zodiac signs'),
  ('const_002', 'planets', '["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"]', 'array', 'The 9 planets in Vedic astrology'),
  ('const_003', 'houses', '["1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","11th","12th"]', 'array', 'The 12 houses'),
  ('const_004', 'nakshatras', '["Ashwini","Bharani","Krittika","Rohini","Mrigashirsha","Ardra","Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"]', 'array', 'The 27 nakshatras'),
  ('const_005', 'dasha_years', '{"Sun":6,"Moon":10,"Mars":7,"Mercury":17,"Jupiter":16,"Venus":20,"Saturn":19,"Rahu":18,"Ketu":7}', 'object', 'Vimshottari dasha years for each planet'),
  ('const_006', 'ayanamsa_lahiri', '24.04', 'number', 'Lahiri ayanamsa constant (degrees)'),
  ('const_007', 'prediction_accuracy_range', '{"low":0.7,"high":0.85}', 'object', 'Expected accuracy range for predictions'),
  ('const_008', 'cache_ttl_hours', '24', 'number', 'Default cache TTL in hours'),
  ('const_009', 'max_prediction_horizon_days', '365', 'number', 'Maximum prediction horizon in days');

-- Insert system settings
INSERT OR IGNORE INTO system_settings (setting_id, setting_name, setting_value, setting_type, description, is_editable) VALUES
  ('sys_001', 'api_rate_limit_requests', '100', 'number', 'Requests per minute per API key', 1),
  ('sys_002', 'jwt_expiration_hours', '24', 'number', 'JWT token expiration in hours', 1),
  ('sys_003', 'refresh_token_expiration_days', '30', 'number', 'Refresh token expiration in days', 1),
  ('sys_004', 'password_min_length', '8', 'number', 'Minimum password length', 0),
  ('sys_005', 'max_failed_login_attempts', '5', 'number', 'Max failed login attempts before lockout', 1),
  ('sys_006', 'account_lockout_minutes', '15', 'number', 'Account lockout duration in minutes', 1),
  ('sys_007', 'gdpr_enabled', 'true', 'boolean', 'Enable GDPR compliance features', 0),
  ('sys_008', 'soft_delete_enabled', 'true', 'boolean', 'Enable soft delete for data records', 0),
  ('sys_009', 'audit_logging_enabled', 'true', 'boolean', 'Enable audit logging for all actions', 0),
  ('sys_010', 'enable_api_key_auth', 'true', 'boolean', 'Enable API key authentication', 1);

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
-- This SQLite schema is fully compatible with SQLAlchemy ORM
-- All 15 tables with proper indices and constraints
-- Ready for development and testing
-- ============================================================================
