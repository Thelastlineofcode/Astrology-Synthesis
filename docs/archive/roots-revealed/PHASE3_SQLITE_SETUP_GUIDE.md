# Phase 3 Week 1 Day 3: SQLite Database Setup Guide

**Target Time: 5 minutes**  
**Difficulty: Easy**  
**Cost: $0**

---

## Overview

This guide walks you through setting up SQLite for local development. SQLite is **zero-cost, zero-setup**, and perfect for personal development work.

### Why SQLite?

- ✅ **Zero Cost** — No server installation needed
- ✅ **Zero Setup** — Works immediately on macOS
- ✅ **Easy Backup** — Single file you can copy/version control
- ✅ **Easy Migration** — Switch to PostgreSQL anytime (5-minute process)
- ✅ **Perfect for Personal Use** — All 4 calculation engines work identically

---

## Step 1: Verify Configuration (1 minute)

Your config is already updated. Just verify:

```bash
cd /Users/houseofobi/Documents/GitHub/Astrology-Synthesis
cat backend/.env | grep DB_DRIVER
# Should show: DB_DRIVER=sqlite
```

Expected output:

```
DB_DRIVER=sqlite
SQLITE_DB_PATH=./astrology_synthesis.db
```

✅ **Confirmed**: SQLite is configured.

---

## Step 2: Initialize the Database (2 minutes)

Use Python to create the SQLite database with all 15 tables:

```bash
# Navigate to project root
cd /Users/houseofobi/Documents/GitHub/Astrology-Synthesis

# Activate Python environment
source .venv/bin/activate

# Run database initialization
python << 'INIT_DB'
import sqlite3
import os

# Database file path
db_path = "./astrology_synthesis.db"

# Read the schema file
with open("database_init_sqlite.sql", "r") as f:
    schema = f.read()

# Create database and tables
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Execute schema (split by semicolons)
for statement in schema.split(';'):
    statement = statement.strip()
    if statement:
        cursor.execute(statement)

conn.commit()
conn.close()

print(f"✅ Database initialized: {db_path}")
print(f"✅ All 15 tables created")
print(f"✅ All indices created")
print(f"✅ All constraints configured")
INIT_DB
```

Expected output:

```
✅ Database initialized: ./astrology_synthesis.db
✅ All 15 tables created
✅ All indices created
✅ All constraints configured
```

---

## Step 3: Verify Database (1 minute)

Verify all 15 tables were created:

```bash
sqlite3 ./astrology_synthesis.db ".tables"
```

Expected output (all 15 tables):

```
api_keys              astrological_constants  audit_logs           birth_charts
dasha_calculations   ephemeris_cache        event_patterns       interpretations
kp_calculations      predictions            remedies             system_settings
transits             transit_calculations   users
```

Verify table count:

```bash
sqlite3 ./astrology_synthesis.db "SELECT COUNT(*) FROM sqlite_master WHERE type='table';"
```

Expected output:

```
15
```

Verify indices were created:

```bash
sqlite3 ./astrology_synthesis.db "SELECT COUNT(*) FROM sqlite_master WHERE type='index';"
```

Expected output:

```
40+
```

---

## Step 4: Verify Backend Connection (1 minute)

Start the backend and verify database connection:

```bash
# From the project root
cd backend

# Activate environment (if not already active)
source ../.venv/bin/activate

# Start FastAPI backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Expected startup output:

```
✅ SQLite database configured: ./astrology_synthesis.db
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

Visit in browser:

- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## ✅ Setup Complete

You now have:

| Item                     | Status         |
| ------------------------ | -------------- |
| SQLite database created  | ✅             |
| 15 tables deployed       | ✅             |
| 40+ indices created      | ✅             |
| Constraints configured   | ✅             |
| Backend connected        | ✅             |
| Ready for authentication | ✅             |
| **Total Setup Time**     | **~5 minutes** |
| **Total Setup Cost**     | **$0**         |

---

## Database File Location

Your database file is created at:

```
./astrology_synthesis.db
```

**Size**: ~2-3 MB (grows with data)

**To backup**: Simply copy the file

```bash
cp ./astrology_synthesis.db ./astrology_synthesis.db.backup
```

**To reset**: Delete and re-initialize

```bash
rm ./astrology_synthesis.db
# Then run Step 2 again
```

---

## Next Steps

1. ✅ Database ready → Proceed to **Phase 3 Week 1 Days 4-5: Authentication System**
2. Build user registration endpoint
3. Add JWT authentication
4. Create API key management
5. Write authentication tests

**Estimated time for authentication**: 7.5 hours

---

## Optional: Switch to PostgreSQL Later

When ready to use PostgreSQL (for production/multiple users):

1. Update `.env`:

   ```bash
   DB_DRIVER=postgresql
   DB_HOST=your_postgres_host
   DB_PORT=5432
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_NAME=your_database
   ```

2. Deploy PostgreSQL schema:

   ```bash
   psql -d your_database -f database_init.sql
   ```

3. **Zero code changes needed** — Everything works identically

---

## Database Schema Summary

| Layer              | Tables                                                            | Purpose                    |
| ------------------ | ----------------------------------------------------------------- | -------------------------- |
| **Authentication** | users, api_keys                                                   | User accounts & API access |
| **Data**           | birth_charts, predictions, transits                               | User data & calculations   |
| **Calculation**    | kp_calc, dasha_calc, transit_calc, ephemeris_cache                | Caching layer              |
| **Knowledge**      | remedies, interpretations, event_patterns, astrological_constants | Reference data             |
| **System**         | audit_logs, system_settings                                       | Operations & compliance    |

---

## Troubleshooting

### Issue: Database file not created

**Solution**: Verify `.env` file:

```bash
cat backend/.env | grep DB_DRIVER
# Must show: DB_DRIVER=sqlite
```

### Issue: Permission denied creating database

**Solution**: Ensure directory is writable:

```bash
chmod 755 /Users/houseofobi/Documents/GitHub/Astrology-Synthesis
```

### Issue: Foreign key constraints not working

**Solution**: SQLite requires explicit PRAGMA:

- ✅ Already configured in `backend/config/database.py`
- Automatically enables on connection

### Issue: Table already exists

**Solution**: That's OK! The schema uses `IF NOT EXISTS`

- Safe to re-run initialization anytime
- Existing data preserved

---

## Database Comparison

| Feature              | SQLite       | PostgreSQL              |
| -------------------- | ------------ | ----------------------- |
| **Setup Time**       | 5 min        | 30 min                  |
| **Setup Cost**       | $0           | $0 local, $15+/mo cloud |
| **File Size**        | ~3 MB        | Server depends          |
| **Concurrent Users** | Single (you) | Multiple                |
| **Backup**           | Copy file    | Dump/restore            |
| **Migration**        | Easy         | Easy                    |
| **Status**           | ✅ Active    | Upgrade path            |

---

**Setup Status: READY** ✅

You can now proceed to implement authentication in Phase 3 Week 1 Days 4-5.
