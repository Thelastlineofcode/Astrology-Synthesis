# Phase 3 Implementation Kickoff - Week 1 Day 3+

## Overview

Phase 3 transforms the 4 production-ready calculation engines from Phase 2 into a live FastAPI backend API. This document guides the Day 3+ implementation starting with database deployment.

**Timeline:** November 1-22, 2025 (3 weeks)  
**Status:** BEGINNING NOW

---

## Phase 3 Structure

```
Phase 3 Week 1 (Days 1-5)
├─ Days 1-2: ✅ COMPLETE - Project scaffolding (17 files, 2,750 LOC)
├─ Day 3: ⏳ TODAY - Database schema deployment
└─ Days 4-5: ⏳ NEXT - Authentication system implementation

Phase 3 Week 2 (Days 1-5)
├─ Days 1-2: Service layer & engine integration
├─ Days 3-4: Core API endpoints implementation
└─ Day 5: Integration testing

Phase 3 Week 3 (Days 1-5)
├─ Days 1-3: Performance testing & optimization
├─ Days 4-5: Deployment & finalization
└─ Day 5: Production deployment
```

---

## Week 1 Day 3: Database Schema Deployment

### Objective

Deploy PostgreSQL schema to create production database with all 15 tables, indices, constraints, and relationships.

### Prerequisites

```bash
# Ensure PostgreSQL is installed
brew install postgresql@14
brew services start postgresql@14

# Create database and user
createdb astrology_synthesis
createuser astrology_user --createdb
```

### Step 1: Create Database Tables

The database schema has 15 tables organized into 5 layers:

#### Authentication Layer (2 tables)

- `users` - User accounts with hashed passwords
- `api_keys` - API keys for programmatic access

#### Data Layer (3 tables)

- `birth_charts` - Complete birth chart data (JSONB)
- `transits` - Transit analysis results
- `predictions` - Prediction results

#### Calculation Layer (4 tables)

- `kp_calculations` - KP engine results cache
- `dasha_calculations` - Dasha period calculations
- `transit_calculations` - Transit event data
- `ephemeris_cache` - Ephemeris data cache

#### Knowledge Layer (4 tables)

- `remedies` - Astrological remedies
- `interpretations` - Pre-computed interpretations
- `event_patterns` - Historical event patterns
- `astrological_constants` - System constants

#### System Layer (2 tables)

- `audit_logs` - User actions for compliance
- `system_settings` - Application configuration

### Step 2: Execute DDL

Create `database_init.sql`:

```sql
-- Users table
CREATE TABLE IF NOT EXISTS users (
  user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  password_hash VARCHAR(255) NOT NULL,
  api_key VARCHAR(255) UNIQUE,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP,
  CONSTRAINT email_not_null CHECK (email IS NOT NULL)
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_api_key ON users(api_key);
CREATE INDEX idx_users_created_at ON users(created_at);

-- API Keys table
CREATE TABLE IF NOT EXISTS api_keys (
  key_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  key_name VARCHAR(100),
  api_key VARCHAR(255) UNIQUE NOT NULL,
  is_active BOOLEAN DEFAULT true,
  last_used_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE INDEX idx_api_keys_user ON api_keys(user_id);
CREATE INDEX idx_api_keys_key ON api_keys(api_key);

-- Birth Charts table
CREATE TABLE IF NOT EXISTS birth_charts (
  chart_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  birth_date DATE NOT NULL,
  birth_time TIME,
  birth_timezone VARCHAR(50),
  birth_latitude NUMERIC(10, 8) NOT NULL,
  birth_longitude NUMERIC(11, 8) NOT NULL,
  birth_location_name VARCHAR(255),
  chart_name VARCHAR(255),
  chart_notes TEXT,
  chart_data JSONB NOT NULL,
  is_default BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE INDEX idx_charts_user ON birth_charts(user_id);
CREATE INDEX idx_charts_date ON birth_charts(birth_date);
CREATE INDEX idx_charts_created ON birth_charts(created_at);

-- Predictions table
CREATE TABLE IF NOT EXISTS predictions (
  prediction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chart_id UUID NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  prediction_type VARCHAR(50),
  prediction_date DATE NOT NULL,
  prediction_data JSONB NOT NULL,
  confidence_score NUMERIC(5, 2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE INDEX idx_predictions_chart ON predictions(chart_id);
CREATE INDEX idx_predictions_user ON predictions(user_id);
CREATE INDEX idx_predictions_date ON predictions(prediction_date);

-- Transits table
CREATE TABLE IF NOT EXISTS transits (
  transit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chart_id UUID NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,
  transit_planet VARCHAR(50),
  transit_date DATE NOT NULL,
  transit_data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE INDEX idx_transits_chart ON transits(chart_id);
CREATE INDEX idx_transits_date ON transits(transit_date);

-- Remedies table
CREATE TABLE IF NOT EXISTS remedies (
  remedy_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chart_id UUID REFERENCES birth_charts(chart_id) ON DELETE SET NULL,
  remedy_type VARCHAR(100),
  remedy_name VARCHAR(255),
  remedy_description TEXT,
  remedy_strength NUMERIC(5, 2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE INDEX idx_remedies_chart ON remedies(chart_id);
CREATE INDEX idx_remedies_type ON remedies(remedy_type);

-- KP Calculations cache table
CREATE TABLE IF NOT EXISTS kp_calculations (
  calc_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chart_id UUID NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,
  sub_lord VARCHAR(50),
  cusp_number INTEGER,
  calculation_data JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_kp_chart ON kp_calculations(chart_id);

-- Dasha Calculations cache table
CREATE TABLE IF NOT EXISTS dasha_calculations (
  calc_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chart_id UUID NOT NULL REFERENCES birth_charts(chart_id) ON DELETE CASCADE,
  mahadasha_lord VARCHAR(50),
  antardasha_lord VARCHAR(50),
  dasha_start DATE,
  dasha_end DATE,
  calculation_data JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_dasha_chart ON dasha_calculations(chart_id);
CREATE INDEX idx_dasha_dates ON dasha_calculations(dasha_start, dasha_end);

-- Audit Logs table
CREATE TABLE IF NOT EXISTS audit_logs (
  log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
  action VARCHAR(100),
  resource_type VARCHAR(100),
  resource_id UUID,
  details JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_audit_date ON audit_logs(created_at);

-- System Settings table
CREATE TABLE IF NOT EXISTS system_settings (
  setting_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  setting_key VARCHAR(255) UNIQUE NOT NULL,
  setting_value TEXT,
  setting_type VARCHAR(50),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_settings_key ON system_settings(setting_key);
```

### Step 3: Deploy Schema

```bash
cd /Users/houseofobi/Documents/GitHub/Astrology-Synthesis

# Connect to database and execute DDL
psql -d astrology_synthesis -f database_init.sql

# Verify tables were created
psql -d astrology_synthesis -c "\dt"
```

### Step 4: Verify Deployment

```bash
# Check all tables exist
psql -d astrology_synthesis -c "
SELECT tablename FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;"

# Verify indices
psql -d astrology_synthesis -c "
SELECT indexname FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY indexname;"

# Check constraints
psql -d astrology_synthesis -c "
SELECT constraint_name FROM information_schema.table_constraints
WHERE table_schema = 'public'
ORDER BY constraint_name;"
```

### Step 5: Update Backend Environment

Edit `.env`:

```
DATABASE_URL=postgresql://astrology_user@localhost/astrology_synthesis
```

Update `backend/config/database.py`:

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    os.getenv("DATABASE_URL"),
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    echo=False
)
```

### Step 6: Initialize Session

```bash
cd backend
python -c "
from config.database import SessionLocal
from models.database import Base, engine

# Create all tables via ORM
Base.metadata.create_all(bind=engine)

# Verify connection
session = SessionLocal()
print('Database connection successful!')
session.close()
"
```

---

## Week 1 Days 4-5: Authentication System

### Objective

Implement JWT-based authentication with user registration, login, and API key management.

### Components to Build

#### 1. Password Hashing

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed: str) -> bool:
    return pwd_context.verify(plain_password, hashed)
```

#### 2. JWT Token Generation

```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def create_access_token(user_id: str, expires_in: int = 3600):
    payload = {
        "sub": user_id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

#### 3. Authentication Endpoints

**POST /api/v1/auth/register**

```python
@router.post("/register")
async def register(req: RegisterRequest):
    # Hash password
    # Create user
    # Return success
```

**POST /api/v1/auth/login**

```python
@router.post("/login")
async def login(req: LoginRequest):
    # Verify credentials
    # Generate JWT token
    # Return token
```

**POST /api/v1/auth/refresh**

```python
@router.post("/refresh")
async def refresh(token: str = Depends(oauth2_scheme)):
    # Verify existing token
    # Generate new token
    # Return new token
```

#### 4. Auth Middleware

```python
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    user_id = verify_token(token)
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=401)
    return user
```

---

## Implementation Checklist for Week 1

### Day 3 Checklist - Database Deployment

- [ ] PostgreSQL installed and running
- [ ] Database `astrology_synthesis` created
- [ ] User `astrology_user` created
- [ ] DDL schema executed (15 tables)
- [ ] All indices created
- [ ] Foreign keys verified
- [ ] `.env` updated with DATABASE_URL
- [ ] Backend ORM connection tested
- [ ] Connection pool configured

### Days 4-5 Checklist - Authentication

- [ ] Password hashing implemented (BCrypt)
- [ ] JWT token generation working
- [ ] Token verification working
- [ ] /auth/register endpoint working
- [ ] /auth/login endpoint working
- [ ] /auth/refresh endpoint working
- [ ] Auth middleware implemented
- [ ] User model created in database
- [ ] Unit tests for auth (8-10 tests)
- [ ] Integration tests for auth endpoints
- [ ] Curl/Postman testing verified

---

## Verification Tests

### Database Tests

```bash
# Test connection
psql -d astrology_synthesis -c "SELECT NOW();"

# Count tables
psql -d astrology_synthesis -c "SELECT COUNT(*) FROM information_schema.tables;"

# Verify constraints
psql -d astrology_synthesis -c "SELECT * FROM information_schema.key_column_usage;"
```

### Authentication Tests

```bash
# Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# Get protected resource
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/health
```

---

## Files to Create/Update

### Day 3 Files

- [ ] `database_init.sql` - PostgreSQL DDL schema
- [ ] `.env` - Database URL configuration

### Days 4-5 Files

- [ ] `backend/services/auth_service.py` - Auth logic (password hashing, JWT)
- [ ] `backend/api/v1/auth.py` - Auth endpoints (register, login, refresh)
- [ ] `test_auth_service.py` - Auth service unit tests
- [ ] `test_auth_endpoints.py` - Auth endpoint integration tests

---

## Next Phase Preview

### Week 2: Service Layer & Endpoints

After authentication is working:

1. **Service Layer Integration**
   - Wrap all 4 Phase 2 engines in service classes
   - Create CalculationService orchestrator
   - Add error handling and caching

2. **Core Endpoints**
   - `POST /api/v1/charts` - Create birth chart
   - `GET /api/v1/charts/{id}` - Retrieve chart
   - `POST /api/v1/predict` - Generate prediction
   - `GET /api/v1/transits` - Get transit data
   - `GET /api/v1/remedies/{id}` - Get remedies

3. **Testing**
   - Unit tests for services (85%+ coverage)
   - Integration tests for endpoints
   - Load testing (100+ req/s target)

---

## Quick Start Command

```bash
cd /Users/houseofobi/Documents/GitHub/Astrology-Synthesis

# Start virtual environment
source .venv/bin/activate

# Ensure dependencies installed
pip install fastapi uvicorn sqlalchemy psycopg2-binary pyjwt passlib bcrypt

# Verify environment
python -c "import fastapi, sqlalchemy; print('OK')"

# Test database connection
python -c "from backend.config.database import engine; print(engine.connect())"

# Start server
python -m uvicorn backend.main:app --reload
```

Visit: http://localhost:8000/docs (Swagger UI)

---

## Success Criteria

By end of Week 1:

- ✅ Database schema deployed to PostgreSQL
- ✅ 15 tables with proper indices and constraints
- ✅ User registration working
- ✅ JWT authentication working
- ✅ API key generation working
- ✅ Protected endpoints accessible only with valid auth
- ✅ Auth unit tests passing (8+ tests)
- ✅ Auth integration tests passing (5+ tests)

---

## Timeline

| Phase | Week | Days | Milestone                | Status   |
| ----- | ---- | ---- | ------------------------ | -------- |
| 3     | 1    | 1-2  | ✅ Project scaffolding   | COMPLETE |
| 3     | 1    | 3    | ⏳ Database deployment   | TODAY    |
| 3     | 1    | 4-5  | ⏳ Authentication        | NEXT     |
| 3     | 2    | 1-2  | ⏳ Service layer         | WEEK 2   |
| 3     | 2    | 3-4  | ⏳ Core endpoints        | WEEK 2   |
| 3     | 3    | 1-3  | ⏳ Testing & performance | WEEK 3   |
| 3     | 3    | 4-5  | ⏳ Deployment            | WEEK 3   |

**Target Completion:** November 22, 2025

---

## Support Resources

- Fastapi docs: https://fastapi.tiangolo.com/
- SQLAlchemy docs: https://docs.sqlalchemy.org/
- PostgreSQL docs: https://www.postgresql.org/docs/
- JWT Guide: https://jwt.io/
- Phase 2 Test Report: `PHASE2_TEST_REPORT.md`
- Previous setup guide: `backend/API_SETUP_GUIDE.md`
