# Database Schema Design

## Overview
This document outlines the proposed PostgreSQL database schema for the Astrology Synthesis application. The database will support user management, chart storage, and caching of calculations.

**Status**: 📋 Planned - Not yet implemented  
**Database**: PostgreSQL 14+  
**ORM**: SQLAlchemy (via Flask-SQLAlchemy)

## Schema Diagram

```
┌─────────────┐         ┌──────────────┐         ┌─────────────────┐
│    users    │────────<│    charts    │>────────│  chart_planets  │
└─────────────┘         └──────────────┘         └─────────────────┘
                              │  │
                              │  │
                        ┌─────┘  └─────┐
                        │                │
                  ┌───────────┐    ┌─────────────┐
                  │  aspects  │    │    houses   │
                  └───────────┘    └─────────────┘
```

## Tables

### users
Stores user account information.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    birth_date DATE,
    birth_time TIME,
    birth_latitude DECIMAL(10, 7),
    birth_longitude DECIMAL(10, 7),
    birth_location VARCHAR(255),
    timezone VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    email_verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    preferences JSONB DEFAULT '{}'
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_uuid ON users(uuid);
CREATE INDEX idx_users_created_at ON users(created_at);
```

**Fields**:
- `id`: Primary key
- `uuid`: Public identifier (safer to expose than id)
- `username`: Unique username
- `email`: User email address
- `password_hash`: Hashed password (bcrypt)
- `birth_date`, `birth_time`: User's birth info (optional)
- `birth_latitude`, `birth_longitude`: Birth coordinates
- `birth_location`: Birth place name
- `timezone`: User timezone
- `preferences`: JSON field for user settings (theme, default chart type, etc.)

### charts
Stores natal charts and calculations.

```sql
CREATE TABLE charts (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    chart_name VARCHAR(255),
    chart_type VARCHAR(50) DEFAULT 'natal',
    birth_date DATE NOT NULL,
    birth_time TIME NOT NULL,
    birth_latitude DECIMAL(10, 7) NOT NULL,
    birth_longitude DECIMAL(10, 7) NOT NULL,
    birth_location VARCHAR(255),
    timezone VARCHAR(50),
    zodiac_type VARCHAR(20) DEFAULT 'tropical',
    ayanamsa VARCHAR(50) DEFAULT 'LAHIRI',
    house_system VARCHAR(10) DEFAULT 'P',
    include_minor_aspects BOOLEAN DEFAULT FALSE,
    chart_data JSONB,
    calculation_metadata JSONB,
    is_public BOOLEAN DEFAULT FALSE,
    tags VARCHAR(100)[],
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    calculated_at TIMESTAMP,
    access_count INTEGER DEFAULT 0,
    last_accessed TIMESTAMP
);

-- Indexes
CREATE INDEX idx_charts_user_id ON charts(user_id);
CREATE INDEX idx_charts_uuid ON charts(uuid);
CREATE INDEX idx_charts_chart_type ON charts(chart_type);
CREATE INDEX idx_charts_created_at ON charts(created_at);
CREATE INDEX idx_charts_tags ON charts USING GIN(tags);
CREATE INDEX idx_charts_is_public ON charts(is_public);
```

**Fields**:
- `chart_type`: 'natal', 'transit', 'synastry', 'composite'
- `zodiac_type`: 'tropical', 'sidereal'
- `ayanamsa`: Sidereal calculation method
- `house_system`: House system code (P, K, W, E, R, etc.)
- `chart_data`: Full JSON chart data from calculation
- `calculation_metadata`: Performance metrics, version info
- `tags`: Array of tags for organization
- `is_public`: Whether chart can be shared

### chart_planets
Stores individual planet positions (normalized data).

```sql
CREATE TABLE chart_planets (
    id SERIAL PRIMARY KEY,
    chart_id INTEGER REFERENCES charts(id) ON DELETE CASCADE,
    planet_name VARCHAR(20) NOT NULL,
    planet_id INTEGER,
    longitude DECIMAL(10, 6) NOT NULL,
    latitude DECIMAL(10, 6),
    distance DECIMAL(15, 6),
    speed DECIMAL(10, 6),
    is_retrograde BOOLEAN DEFAULT FALSE,
    sign VARCHAR(20),
    sign_degree DECIMAL(5, 2),
    house INTEGER,
    nakshatra VARCHAR(50),
    nakshatra_pada INTEGER,
    dignity VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_chart_planets_chart_id ON chart_planets(chart_id);
CREATE INDEX idx_chart_planets_planet_name ON chart_planets(planet_name);
```

**Fields**:
- `longitude`: Zodiac longitude (0-360 degrees)
- `latitude`: Ecliptic latitude
- `distance`: Distance from Earth (AU)
- `speed`: Daily motion (degrees/day)
- `nakshatra`: Vedic lunar mansion
- `dignity`: Essential dignity (domicile, exaltation, etc.)

### houses
Stores house cusps and angles.

```sql
CREATE TABLE houses (
    id SERIAL PRIMARY KEY,
    chart_id INTEGER REFERENCES charts(id) ON DELETE CASCADE,
    house_number INTEGER NOT NULL CHECK (house_number BETWEEN 1 AND 12),
    cusp_longitude DECIMAL(10, 6) NOT NULL,
    sign VARCHAR(20),
    sign_degree DECIMAL(5, 2),
    is_angle BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_houses_chart_id ON houses(chart_id);
CREATE INDEX idx_houses_house_number ON houses(house_number);
```

### aspects
Stores planetary aspects.

```sql
CREATE TABLE aspects (
    id SERIAL PRIMARY KEY,
    chart_id INTEGER REFERENCES charts(id) ON DELETE CASCADE,
    planet1_name VARCHAR(20) NOT NULL,
    planet2_name VARCHAR(20) NOT NULL,
    aspect_type VARCHAR(20) NOT NULL,
    aspect_angle DECIMAL(5, 2) NOT NULL,
    orb DECIMAL(5, 2) NOT NULL,
    is_applying BOOLEAN,
    is_exact BOOLEAN DEFAULT FALSE,
    strength DECIMAL(3, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_aspects_chart_id ON aspects(chart_id);
CREATE INDEX idx_aspects_type ON aspects(aspect_type);
CREATE INDEX idx_aspects_planets ON aspects(planet1_name, planet2_name);
```

**Fields**:
- `aspect_type`: 'conjunction', 'opposition', 'trine', etc.
- `aspect_angle`: Theoretical angle (0, 60, 90, 120, 180, etc.)
- `orb`: Deviation from exact aspect
- `is_applying`: Whether aspect is applying or separating
- `strength`: Calculated aspect strength (0.0-1.0)

### sessions
User session management (for JWT tokens).

```sql
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    token_jti VARCHAR(36) UNIQUE NOT NULL,
    token_type VARCHAR(20) DEFAULT 'access',
    expires_at TIMESTAMP NOT NULL,
    ip_address INET,
    user_agent TEXT,
    is_revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    revoked_at TIMESTAMP
);

-- Indexes
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_token_jti ON sessions(token_jti);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);
```

### calculation_cache
Cache frequently requested calculations.

```sql
CREATE TABLE calculation_cache (
    id SERIAL PRIMARY KEY,
    cache_key VARCHAR(255) UNIQUE NOT NULL,
    cache_data JSONB NOT NULL,
    calculation_type VARCHAR(50),
    expires_at TIMESTAMP,
    hit_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP
);

-- Indexes
CREATE INDEX idx_cache_key ON calculation_cache(cache_key);
CREATE INDEX idx_cache_expires_at ON calculation_cache(expires_at);
CREATE INDEX idx_cache_type ON calculation_cache(calculation_type);
```

### bmad_analyses
Store BMAD personality analysis results.

```sql
CREATE TABLE bmad_analyses (
    id SERIAL PRIMARY KEY,
    chart_id INTEGER REFERENCES charts(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    analysis_type VARCHAR(50) NOT NULL,
    personality_profile JSONB,
    behavior_predictions JSONB,
    symbolon_cards JSONB,
    insights TEXT,
    confidence_score DECIMAL(3, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version VARCHAR(20)
);

-- Indexes
CREATE INDEX idx_bmad_chart_id ON bmad_analyses(chart_id);
CREATE INDEX idx_bmad_user_id ON bmad_analyses(user_id);
CREATE INDEX idx_bmad_type ON bmad_analyses(analysis_type);
```

## Relationships

### One-to-Many
- `users` → `charts`: A user can have multiple charts
- `charts` → `chart_planets`: A chart has multiple planets
- `charts` → `houses`: A chart has 12 houses
- `charts` → `aspects`: A chart has multiple aspects
- `users` → `sessions`: A user can have multiple sessions
- `charts` → `bmad_analyses`: A chart can have multiple analyses

### Many-to-Many (Future)
- `users` ↔ `charts`: Shared charts (via junction table)
- `charts` ↔ `tags`: Chart categorization

## Migrations

### Initial Migration
```bash
# Create migration
flask db init
flask db migrate -m "Initial schema"
flask db upgrade
```

### Adding New Fields
```bash
flask db migrate -m "Add preferences to users"
flask db upgrade
```

## Data Access Layer

### Models (SQLAlchemy)

```python
# models/user.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Relationships
    charts = db.relationship('Chart', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
```

## Queries

### Common Queries

```sql
-- Get user with all charts
SELECT u.*, c.* 
FROM users u
LEFT JOIN charts c ON u.id = c.user_id
WHERE u.email = 'user@example.com';

-- Find charts by location
SELECT * FROM charts
WHERE birth_location ILIKE '%New York%'
ORDER BY created_at DESC
LIMIT 10;

-- Get aspects for a chart
SELECT * FROM aspects
WHERE chart_id = 123
ORDER BY orb ASC;

-- Find retrograde planets
SELECT c.chart_name, cp.planet_name, cp.longitude
FROM charts c
JOIN chart_planets cp ON c.id = cp.chart_id
WHERE cp.is_retrograde = TRUE;

-- User chart statistics
SELECT u.username, COUNT(c.id) as chart_count
FROM users u
LEFT JOIN charts c ON u.id = c.user_id
GROUP BY u.id
ORDER BY chart_count DESC;
```

## Performance Optimization

### Indexes
- Primary keys on all tables
- Foreign key indexes
- Composite indexes for common queries
- GIN indexes for JSONB fields

### Partitioning
```sql
-- Partition charts by year (for large datasets)
CREATE TABLE charts_2025 PARTITION OF charts
FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
```

### Views
```sql
-- User statistics view
CREATE VIEW user_stats AS
SELECT 
    u.id,
    u.username,
    COUNT(DISTINCT c.id) as chart_count,
    COUNT(DISTINCT ba.id) as analysis_count,
    MAX(c.created_at) as last_chart_date
FROM users u
LEFT JOIN charts c ON u.id = c.user_id
LEFT JOIN bmad_analyses ba ON u.id = ba.user_id
GROUP BY u.id, u.username;
```

## Backup and Maintenance

### Backup
```bash
# Full backup
pg_dump -U astrology_user astrology_db > backup.sql

# Restore
psql -U astrology_user astrology_db < backup.sql
```

### Cleanup
```sql
-- Remove old cache entries
DELETE FROM calculation_cache
WHERE expires_at < NOW();

-- Remove revoked sessions
DELETE FROM sessions
WHERE is_revoked = TRUE AND revoked_at < NOW() - INTERVAL '30 days';
```

## Security Considerations

1. **Passwords**: Always store hashed (bcrypt, scrypt)
2. **SQL Injection**: Use parameterized queries (SQLAlchemy ORM)
3. **Sensitive Data**: Encrypt birth data if required
4. **Access Control**: Row-level security for multi-tenant
5. **Audit Log**: Track chart access and modifications

## Future Enhancements

- [ ] Add audit log table for tracking changes
- [ ] Implement soft deletes with `deleted_at` timestamps
- [ ] Add chart sharing and permissions table
- [ ] Create materialized views for complex queries
- [ ] Implement full-text search for chart notes
- [ ] Add webhook/notification tables
- [ ] Support for divisional charts (D9, D10, etc.)
- [ ] Transit tracking tables

---

**Last Updated**: October 28, 2025  
**Status**: Design Phase  
**Next Steps**: Implement models and migrations
