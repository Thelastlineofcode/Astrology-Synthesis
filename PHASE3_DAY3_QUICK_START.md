# Phase 3 Quick Start - Database Deployment (Day 3)

## Deploy in 30 Minutes

### Prerequisites Check

```bash
# Verify you have everything
brew --version                    # Homebrew (macOS)
git --version                      # Git
python3 --version                 # Python 3.14+
```

### Step 1: Install PostgreSQL (5 min)

```bash
# Install PostgreSQL 14
brew install postgresql@14

# Start PostgreSQL service
brew services start postgresql@14

# Verify installation
psql --version
# Expected: psql (PostgreSQL) 14.x
```

### Step 2: Create Database (3 min)

```bash
# Create database
createdb astrology_synthesis

# Create database user
createuser astrology_user --createdb

# Verify creation
psql -l | grep astrology_synthesis
```

### Step 3: Deploy Schema (10 min)

```bash
# Navigate to project
cd /Users/houseofobi/Documents/GitHub/Astrology-Synthesis

# Deploy schema
psql -d astrology_synthesis -f database_init.sql

# Expected output: CREATE TABLE (multiple lines)
```

### Step 4: Verify Deployment (5 min)

```bash
# List all tables (should show 15)
psql -d astrology_synthesis -c "\dt"

# Count tables
psql -d astrology_synthesis -c "
SELECT COUNT(*) as table_count FROM information_schema.tables
WHERE table_schema = 'public';"

# Expected: 15

# List indices (should show 40+)
psql -d astrology_synthesis -c "\di"

# Check constants were loaded
psql -d astrology_synthesis -c "SELECT COUNT(*) FROM astrological_constants;"
# Expected: 9
```

### Step 5: Update Environment (2 min)

Edit `.env` file:

```
DATABASE_URL=postgresql://astrology_user@localhost/astrology_synthesis
```

Verify .env:

```bash
cat .env | grep DATABASE_URL
```

### Step 6: Test Backend Connection (5 min)

```bash
cd backend

# Verify database connection
python -c "
from config.database import engine
print('Testing connection...')
try:
    with engine.connect() as conn:
        result = conn.execute('SELECT NOW()')
        print('✅ Database connected:', result.fetchone()[0])
except Exception as e:
    print('❌ Connection failed:', e)
"
```

---

## What Was Just Deployed

### 15 Tables Created

| Layer     | Tables                                                                     | Purpose               |
| --------- | -------------------------------------------------------------------------- | --------------------- |
| Auth      | users, api_keys                                                            | User authentication   |
| Data      | birth_charts, predictions, transits                                        | Chart & analysis data |
| Calc      | kp_calculations, dasha_calculations, transit_calculations, ephemeris_cache | Engine result caching |
| Knowledge | remedies, interpretations, event_patterns, astrological_constants          | Domain knowledge      |
| System    | audit_logs, system_settings                                                | Compliance & config   |

### 40+ Indices

All tables have optimized indices on:

- User IDs (for quick lookups)
- Dates (for time-range queries)
- Key columns (for searches)

### Features Enabled

- UUID primary keys (no sequential ID leakage)
- Foreign key constraints (referential integrity)
- Soft deletes (GDPR compliance)
- Auto-timestamps (created_at, updated_at)
- Check constraints (data validation)

---

## Troubleshooting

### PostgreSQL Won't Start

```bash
# Check if already running
lsof -i :5432

# If port 5432 is in use, restart
brew services restart postgresql@14

# Check status
brew services list | grep postgresql
```

### Database Already Exists

```bash
# Drop and recreate
dropdb astrology_synthesis
createdb astrology_synthesis
psql -d astrology_synthesis -f database_init.sql
```

### Connection Refused

```bash
# Start PostgreSQL
brew services start postgresql@14

# Test connection
psql -d astrology_synthesis -c "SELECT NOW();"
```

### Schema Not Imported

```bash
# Check if file exists
ls -la database_init.sql

# Try again with verbose
psql -d astrology_synthesis -f database_init.sql -v ON_ERROR_STOP=1

# Check what tables exist
psql -d astrology_synthesis -c "\dt"
```

---

## Quick Verification Commands

```bash
# Show all tables with row count
psql -d astrology_synthesis -c "
SELECT schemaname, tablename, n_live_tup
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;"

# Show all indices
psql -d astrology_synthesis -c "\di"

# Show database size
psql -d astrology_synthesis -c "
SELECT pg_size_pretty(pg_database_size('astrology_synthesis'));"

# Show foreign keys
psql -d astrology_synthesis -c "
SELECT constraint_name, table_name, column_name
FROM information_schema.key_column_usage
WHERE table_schema = 'public'
ORDER BY table_name;"
```

---

## Next Steps (Days 4-5)

After database is deployed:

1. **Implement User Registration**
   - Create user registration endpoint
   - Add password hashing (BCrypt)
   - Add email validation

2. **Implement JWT Authentication**
   - Create JWT token generation
   - Add token verification
   - Create login endpoint

3. **Add API Key Management**
   - Generate API keys
   - Verify API key headers
   - Add API key endpoints

4. **Write Tests**
   - Auth service tests (4-5 tests)
   - Auth endpoint tests (4-5 tests)

---

## Success Criteria (Day 3)

After completing these steps, you should have:

✅ PostgreSQL running locally  
✅ Database `astrology_synthesis` created  
✅ 15 tables deployed  
✅ 40+ indices created  
✅ Backend can connect to database  
✅ `.env` configured with DATABASE_URL  
✅ Schema verification passed

**Estimated Time:** 30 minutes  
**Difficulty:** Easy (all steps are straightforward)  
**Risk:** Very low (rollback is simple: just drop database)

---

## Quick Test After Deployment

```bash
# Full verification script
psql -d astrology_synthesis << EOF
-- Count tables
\echo '=== Table Count ==='
SELECT COUNT(*) as "Total Tables" FROM information_schema.tables WHERE table_schema = 'public';

-- List all tables
\echo '=== All Tables ==='
SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;

-- Count indices
\echo '=== Index Count ==='
SELECT COUNT(*) as "Total Indices" FROM pg_indexes WHERE schemaname = 'public';

-- Count records in constants
\echo '=== Constants Loaded ==='
SELECT COUNT(*) as "Constants" FROM astrological_constants;

-- Count settings loaded
\echo '=== Settings Loaded ==='
SELECT COUNT(*) as "Settings" FROM system_settings;

-- Database size
\echo '=== Database Size ==='
SELECT pg_size_pretty(pg_database_size('astrology_synthesis'));

\echo '✅ Deployment Verification Complete'
EOF
```

---

## Dashboard After Deployment

```
Schema Deployment Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ PostgreSQL installed
✅ Database created
✅ 15 tables deployed
✅ 40+ indices created
✅ Foreign keys active
✅ 9 constants loaded
✅ 10 settings loaded
✅ Soft deletes enabled
✅ Audit logging ready
✅ Backend connected

Status: READY FOR AUTHENTICATION IMPLEMENTATION
Time to Complete: ~30 minutes
Deployment Date: November 1, 2025
```

---

## Don't Forget

After schema deployment:

1. ✅ Commit database_init.sql to git
2. ✅ Update .env in backend
3. ✅ Document deployment in your notes
4. ✅ Test connection from Python backend
5. ✅ Ready to proceed to authentication (Days 4-5)

---

**Command Summary (Copy & Paste Ready)**

```bash
# 1. Install PostgreSQL
brew install postgresql@14 && brew services start postgresql@14

# 2. Create database
createdb astrology_synthesis && createuser astrology_user --createdb

# 3. Deploy schema
cd /Users/houseofobi/Documents/GitHub/Astrology-Synthesis
psql -d astrology_synthesis -f database_init.sql

# 4. Verify
psql -d astrology_synthesis -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"

# 5. Test backend connection
cd backend && python -c "from config.database import engine; print('✅ Connected' if engine.connect() else '❌ Failed')"
```

**Total Time:** ~30 minutes  
**Next:** Authentication system (Days 4-5)
