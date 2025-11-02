-- ============================================================================
-- ASTROLOGY SYNTHESIS DATABASE SCHEMA
-- PostgreSQL DDL for Phase 3 Implementation
-- Generated: November 1, 2025
-- ============================================================================

-- ============================================================================
-- AUTHENTICATION LAYER (2 tables)
-- ============================================================================

-- Users table - User accounts with authentication
CREATE TABLE IF NOT EXISTS users (
  user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  password_hash VARCHAR(255) NOT NULL,
  api_key VARCHAR(255) UNIQUE,
  is_active BOOLEAN DEFAULT true,
  is_verified BOOLEAN DEFAULT false,
  verification_code VARCHAR(100),
  failed_login_attempts INTEGER DEFAULT 0,
  locked_until TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP,
  CONSTRAINT email_format CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_api_key ON users(api_key);
CREATE INDEX idx_users_created_at ON users(created_at);
CREATE INDEX idx_users_is_active ON users(is_active);
CREATE INDEX idx_users_deleted_at ON users(deleted_at);

-- API Keys table - Programmatic access for integrations
CREATE TABLE IF NOT EXISTS api_keys (
  key_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  key_name VARCHAR(100) NOT NULL,
  api_key_hash VARCHAR(255) UNIQUE NOT NULL,
  is_active BOOLEAN DEFAULT true,
  last_used_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE INDEX idx_api_keys_user ON api_keys(user_id);
CREATE INDEX idx_api_keys_hash ON api_keys(api_key_hash);
CREATE INDEX idx_api_keys_active ON api_keys(is_active);

-- ============================================================================
-- DATA LAYER (3 tables)
-- ============================================================================

-- Birth Charts table - Complete birth chart data
CREATE TABLE IF NOT EXISTS birth_charts (
  chart_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  birth_date DATE NOT NULL,
  birth_time TIME,
  birth_timezone VARCHAR(50) NOT NULL,
  birth_latitude NUMERIC(10, 8) NOT NULL CHECK (birth_latitude >= -90 AND birth_latitude <= 90),
  birth_longitude NUMERIC(11, 8) NOT NULL CHECK (birth_longitude >= -180 AND birth_longitude <= 180),
  birth_location_name VARCHAR(255),
  chart_name VARCHAR(255),
  chart_notes TEXT,
  chart_data JSONB NOT NULL,
  ayanamsa_mode VARCHAR(50) DEFAULT 'Lahiri',
  house_system VARCHAR(50) DEFAULT 'Placidus',
  is_default BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE INDEX idx_charts_user ON birth_charts(user_id);
CREATE INDEX idx_charts_date ON birth_charts(birth_date);
CREATE INDEX idx_charts_created ON birth_charts(created_at);
CREATE INDEX idx_charts_location ON birth_charts(birth_latitude, birth_longitude);
CREATE INDEX idx_charts_deleted_at ON birth_charts(deleted_at);

-- Predictions table - Prediction results from engines
CREATE TABLE IF NOT EXISTS predictions (
  prediction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chart_id UUID NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  prediction_type VARCHAR(50) NOT NULL,
  prediction_category VARCHAR(50),
  prediction_date DATE NOT NULL,
  prediction_window_start DATE,
  prediction_window_end DATE,
  prediction_data JSONB NOT NULL,
  confidence_score NUMERIC(5, 2) CHECK (confidence_score >= 0 AND confidence_score <= 100),
  accuracy_estimate VARCHAR(50),
  prediction_strength VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE INDEX idx_predictions_chart ON predictions(chart_id);
CREATE INDEX idx_predictions_user ON predictions(user_id);
CREATE INDEX idx_predictions_date ON predictions(prediction_date);
CREATE INDEX idx_predictions_type ON predictions(prediction_type);
CREATE INDEX idx_predictions_confidence ON predictions(confidence_score);

-- Transits table - Transit analysis results
CREATE TABLE IF NOT EXISTS transits (
  transit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chart_id UUID NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,
  transit_planet VARCHAR(50) NOT NULL,
  natal_planet VARCHAR(50),
  aspect_type VARCHAR(50),
  transit_date DATE NOT NULL,
  transit_start_date DATE,
  transit_end_date DATE,
  orb NUMERIC(10, 5),
  transit_strength VARCHAR(50),
  interpretation TEXT,
  transit_data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE INDEX idx_transits_chart ON transits(chart_id);
CREATE INDEX idx_transits_date ON transits(transit_date);
CREATE INDEX idx_transits_planet ON transits(transit_planet);
CREATE INDEX idx_transits_period ON transits(transit_start_date, transit_end_date);

-- ============================================================================
-- CALCULATION LAYER (4 tables)
-- ============================================================================

-- KP Calculations cache - KP engine results
CREATE TABLE IF NOT EXISTS kp_calculations (
  calc_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chart_id UUID NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,
  sub_lord VARCHAR(50),
  cusp_number INTEGER CHECK (cusp_number >= 1 AND cusp_number <= 12),
  calculation_data JSONB NOT NULL,
  significance_level NUMERIC(5, 2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP
);

CREATE INDEX idx_kp_chart ON kp_calculations(chart_id);
CREATE INDEX idx_kp_sub_lord ON kp_calculations(sub_lord);
CREATE INDEX idx_kp_cusp ON kp_calculations(cusp_number);

-- Dasha Calculations cache - Dasha period calculations
CREATE TABLE IF NOT EXISTS dasha_calculations (
  calc_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chart_id UUID NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,
  mahadasha_lord VARCHAR(50) NOT NULL,
  antardasha_lord VARCHAR(50),
  pratyantardasha_lord VARCHAR(50),
  dasha_start DATE NOT NULL,
  dasha_end DATE NOT NULL,
  dasha_duration_years NUMERIC(10, 5),
  calculation_data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP
);

CREATE INDEX idx_dasha_chart ON dasha_calculations(chart_id);
CREATE INDEX idx_dasha_lords ON dasha_calculations(mahadasha_lord, antardasha_lord);
CREATE INDEX idx_dasha_dates ON dasha_calculations(dasha_start, dasha_end);

-- Transit Calculations cache - Transit event calculations
CREATE TABLE IF NOT EXISTS transit_calculations (
  calc_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chart_id UUID NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,
  event_type VARCHAR(100),
  event_date DATE NOT NULL,
  event_strength VARCHAR(50),
  event_probability NUMERIC(5, 2),
  calculation_data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP
);

CREATE INDEX idx_transit_calc_chart ON transit_calculations(chart_id);
CREATE INDEX idx_transit_calc_date ON transit_calculations(event_date);
CREATE INDEX idx_transit_calc_type ON transit_calculations(event_type);

-- Ephemeris Cache - Planetary position cache
CREATE TABLE IF NOT EXISTS ephemeris_cache (
  cache_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  calculation_date DATE NOT NULL,
  planet_data JSONB NOT NULL,
  house_data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP
);

CREATE INDEX idx_ephemeris_date ON ephemeris_cache(calculation_date);
CREATE INDEX idx_ephemeris_expires ON ephemeris_cache(expires_at);

-- ============================================================================
-- KNOWLEDGE LAYER (4 tables)
-- ============================================================================

-- Remedies table - Astrological remedies and recommendations
CREATE TABLE IF NOT EXISTS remedies (
  remedy_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chart_id UUID REFERENCES birth_charts(chart_id) ON DELETE SET NULL,
  user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
  remedy_type VARCHAR(100) NOT NULL,
  remedy_name VARCHAR(255) NOT NULL,
  remedy_description TEXT,
  remedy_category VARCHAR(100),
  remedy_strength NUMERIC(5, 2),
  planet_associated VARCHAR(50),
  cost_estimate NUMERIC(10, 2),
  recommended_date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE INDEX idx_remedies_chart ON remedies(chart_id);
CREATE INDEX idx_remedies_user ON remedies(user_id);
CREATE INDEX idx_remedies_type ON remedies(remedy_type);
CREATE INDEX idx_remedies_planet ON remedies(planet_associated);

-- Interpretations table - Pre-computed interpretations
CREATE TABLE IF NOT EXISTS interpretations (
  interp_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chart_id UUID NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,
  interpretation_type VARCHAR(100),
  subject_area VARCHAR(100),
  interpretation_text TEXT,
  confidence_level NUMERIC(5, 2),
  is_verified BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE INDEX idx_interp_chart ON interpretations(chart_id);
CREATE INDEX idx_interp_type ON interpretations(interpretation_type);
CREATE INDEX idx_interp_area ON interpretations(subject_area);

-- Event Patterns table - Historical event patterns for validation
CREATE TABLE IF NOT EXISTS event_patterns (
  pattern_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  pattern_name VARCHAR(255),
  pattern_description TEXT,
  astrological_indicators JSONB,
  historical_accuracy NUMERIC(5, 2),
  sample_size INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_patterns_name ON event_patterns(pattern_name);
CREATE INDEX idx_patterns_accuracy ON event_patterns(historical_accuracy);

-- Astrological Constants table - System configuration constants
CREATE TABLE IF NOT EXISTS astrological_constants (
  const_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  const_name VARCHAR(255) UNIQUE NOT NULL,
  const_value TEXT,
  const_category VARCHAR(100),
  const_type VARCHAR(50),
  description TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_constants_name ON astrological_constants(const_name);
CREATE INDEX idx_constants_category ON astrological_constants(const_category);

-- ============================================================================
-- SYSTEM LAYER (2 tables)
-- ============================================================================

-- Audit Logs table - For compliance and debugging
CREATE TABLE IF NOT EXISTS audit_logs (
  log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
  action VARCHAR(100) NOT NULL,
  resource_type VARCHAR(100),
  resource_id UUID,
  details JSONB,
  ip_address VARCHAR(45),
  user_agent TEXT,
  status VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_audit_date ON audit_logs(created_at);
CREATE INDEX idx_audit_resource ON audit_logs(resource_type, resource_id);

-- System Settings table - Application configuration
CREATE TABLE IF NOT EXISTS system_settings (
  setting_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  setting_key VARCHAR(255) UNIQUE NOT NULL,
  setting_value TEXT,
  setting_type VARCHAR(50),
  setting_category VARCHAR(100),
  description TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by UUID REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE INDEX idx_settings_key ON system_settings(setting_key);
CREATE INDEX idx_settings_category ON system_settings(setting_category);

-- ============================================================================
-- INITIALIZATION DATA
-- ============================================================================

-- Insert default astrological constants
INSERT INTO astrological_constants (const_name, const_value, const_category, const_type, description)
VALUES 
  ('ZODIAC_SIGNS_COUNT', '12', 'ASTROLOGY', 'integer', 'Number of zodiac signs'),
  ('PLANETS_COUNT', '10', 'ASTROLOGY', 'integer', 'Number of planets (including Rahu/Ketu)'),
  ('HOUSES_COUNT', '12', 'ASTROLOGY', 'integer', 'Number of houses in natal chart'),
  ('NAKSHATRAS_COUNT', '27', 'ASTROLOGY', 'integer', 'Number of nakshatras (lunar mansions)'),
  ('DASHA_YEARS', '120', 'ASTROLOGY', 'integer', 'Total years in Vimshottari Dasha'),
  ('AYANAMSA_LAHIRI', '24.27', 'ASTROLOGY', 'decimal', 'Lahiri ayanamsa value for 2025'),
  ('KP_ACCURACY_RANGE', '70-80', 'PREDICTION', 'string', 'Expected accuracy range for KP predictions'),
  ('DASHA_ACCURACY_RANGE', '85-90', 'PREDICTION', 'string', 'Expected accuracy range for Dasha predictions'),
  ('TRANSIT_ACCURACY_RANGE', '75-85', 'PREDICTION', 'string', 'Expected accuracy range for Transit predictions')
ON CONFLICT (const_name) DO NOTHING;

-- Insert default system settings
INSERT INTO system_settings (setting_key, setting_value, setting_type, setting_category, description)
VALUES
  ('API_RATE_LIMIT', '100', 'integer', 'SECURITY', 'API requests per minute per user'),
  ('JWT_EXPIRY_SECONDS', '3600', 'integer', 'SECURITY', 'JWT token expiration in seconds'),
  ('REFRESH_TOKEN_EXPIRY_DAYS', '30', 'integer', 'SECURITY', 'Refresh token expiration in days'),
  ('MAX_LOGIN_ATTEMPTS', '5', 'integer', 'SECURITY', 'Maximum failed login attempts before lockout'),
  ('LOCKOUT_DURATION_MINUTES', '15', 'integer', 'SECURITY', 'Account lockout duration in minutes'),
  ('DATABASE_BACKUP_ENABLED', 'true', 'boolean', 'BACKUP', 'Enable automatic database backups'),
  ('CACHE_DURATION_HOURS', '24', 'integer', 'CACHE', 'How long to cache calculation results'),
  ('PREDICTION_HORIZON_DAYS', '365', 'integer', 'PREDICTION', 'Maximum days ahead for predictions'),
  ('GDPR_COMPLIANCE_ENABLED', 'true', 'boolean', 'COMPLIANCE', 'Enable GDPR soft delete feature'),
  ('AUDIT_LOGGING_ENABLED', 'true', 'boolean', 'COMPLIANCE', 'Enable comprehensive audit logging')
ON CONFLICT (setting_key) DO NOTHING;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Show created tables
-- SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;

-- Show created indices
-- SELECT indexname FROM pg_indexes WHERE schemaname = 'public' ORDER BY indexname;

-- Show table constraints
-- SELECT constraint_name, table_name FROM information_schema.table_constraints WHERE table_schema = 'public' ORDER BY constraint_name;

-- ============================================================================
-- DATABASE INITIALIZATION COMPLETE
-- Total Tables: 15
-- Total Indices: 40+
-- Status: READY FOR USE
-- ============================================================================
