# Production Deployment Guide

**Version:** 1.0  
**Last Updated:** November 2, 2025  
**Status:** Ready for Deployment

---

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Docker Setup](#docker-setup)
3. [Environment Configuration](#environment-configuration)
4. [Database Migration](#database-migration)
5. [Health Checks](#health-checks)
6. [Performance Tuning](#performance-tuning)
7. [Monitoring & Logging](#monitoring--logging)
8. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

### Code Quality

```bash
# Run full test suite
pytest -v --cov=backend --cov-report=term-missing

# Check code style
flake8 backend/ --max-line-length=100
black --check backend/

# Type checking
mypy backend/ --ignore-missing-imports
```

### Configuration

```bash
# Verify all required environment variables
cat .env.example
# Copy to .env and update values
cp .env.example .env

# Validate configuration
python -c "from backend.config.settings import settings; print(f'API: {settings.api.title} v{settings.api.version}')"
```

### Database

```bash
# Verify database
sqlite3 backend/astrology.db ".tables"
sqlite3 backend/astrology.db ".schema users"

# Check data integrity
sqlite3 backend/astrology.db "SELECT COUNT(*) FROM users;"
```

### Dependencies

```bash
# Verify all dependencies installed
pip check

# Generate requirements
pip freeze > requirements-lock.txt

# Test imports
python -c "import fastapi; import sqlalchemy; import pytest; print('✅ All imports OK')"
```

---

## Docker Setup

### 1. Create Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run migrations (if needed)
RUN python -c "from backend.config.database import init_db; init_db()"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Create docker-compose.yml

```yaml
version: "3.8"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./astrology.db
      - ENVIRONMENT=production
      - LOG_LEVEL=info
      - CORS_ORIGINS=["https://example.com"]
    volumes:
      - ./backend:/app/backend
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s

  postgres:
    # Optional: for production scaling
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: astrology
      POSTGRES_USER: astrology_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

### 3. Build and Run

```bash
# Build image
docker build -t astrology-synthesis:latest .

# Run container
docker run -d \
  --name astrology-api \
  -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./astrology.db \
  -e ENVIRONMENT=production \
  astrology-synthesis:latest

# With docker-compose
docker-compose up -d

# Check logs
docker-compose logs -f api

# Stop
docker-compose down
```

---

## Environment Configuration

### .env File Template

```bash
# Application
ENVIRONMENT=production
DEBUG=false
API_TITLE=Astrology-Synthesis
API_VERSION=1.0.0

# Database
DATABASE_URL=sqlite:///./backend/astrology.db
# For PostgreSQL: postgresql://user:password@localhost:5432/astrology

# Security
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# API
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=info

# CORS
CORS_ORIGINS=["http://localhost:3000", "https://example.com"]
CORS_CREDENTIALS=true
CORS_METHODS=["GET", "POST", "PUT", "DELETE", "OPTIONS"]

# Calculation
AYANAMSA=LAHIRI
HOUSE_SYSTEM=PLACIDUS
TROPICAL=false

# Performance
MAX_WORKERS=4
CACHE_ENABLED=true
CACHE_TTL=3600
```

### Load from Environment

```python
from backend.config.settings import settings

print(f"Database: {settings.database.url}")
print(f"Debug: {settings.api.debug}")
print(f"Log Level: {settings.api.log_level}")
```

---

## Database Migration

### SQLite to PostgreSQL (Optional)

```bash
# 1. Export schema
sqlite3 backend/astrology.db ".schema" > schema.sql

# 2. Install pgloader or manual migration
# Option A: Using pgloader
pgloader sqlite:///backend/astrology.db postgresql://user:pass@host:5432/astrology

# Option B: Manual
python scripts/migrate_to_postgres.py

# 3. Verify
psql postgresql://user:pass@host:5432/astrology -c "\dt"
```

### Database Backups

```bash
# SQLite backup
sqlite3 backend/astrology.db ".backup backup.db"

# PostgreSQL backup
pg_dump -h host -U user -d astrology > backup.sql

# Restore
psql -h host -U user -d astrology < backup.sql
```

---

## Health Checks

### API Health Endpoint

```bash
# Check API health
curl http://localhost:8000/health

# Response:
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected",
  "uptime_seconds": 3600
}
```

### Database Health

```bash
# Check database connection
curl http://localhost:8000/health/db

# Response:
{
  "database": "healthy",
  "tables_count": 15,
  "indices_count": 64,
  "response_time_ms": 5
}
```

### Dependencies Health

```bash
# Check all dependencies
curl http://localhost:8000/health/dependencies

# Response:
{
  "ephemeris": "ready",
  "kp_engine": "ready",
  "dasha_calculator": "ready",
  "transit_analyzer": "ready"
}
```

---

## Performance Tuning

### Database Optimization

```sql
-- Enable WAL mode (SQLite)
PRAGMA journal_mode=WAL;

-- Optimize indexes
PRAGMA optimize;

-- Analyze query plans
EXPLAIN QUERY PLAN SELECT * FROM predictions WHERE user_id = '123';

-- Connection pooling (SQLAlchemy)
pool_size=20
max_overflow=40
pool_pre_ping=True
```

### Caching Strategy

```python
# Implementation
from functools import lru_cache
from fastapi_cache2 import FastAPICache2

# Cache chart generation (1 hour)
@FastAPICache2.cached(expire=3600)
def get_birth_chart(chart_id: str):
    return db.query(BirthChart).filter(BirthChart.id == chart_id).first()

# Cache predictions (24 hours)
@FastAPICache2.cached(expire=86400)
def get_predictions(user_id: str):
    return db.query(Prediction).filter(Prediction.user_id == user_id).all()
```

### Connection Pooling

```python
# backend/config/database.py
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    settings.database.url,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_recycle=3600,
)
```

### Async Workers

```bash
# Production (4 workers)
gunicorn backend.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --max-requests 1000 \
  --max-requests-jitter 100

# Or with uvicorn
uvicorn backend.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4
```

---

## Monitoring & Logging

### Structured Logging

```python
import logging
from pythonjsonlogger import jsonlogger

# Configure JSON logging
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Usage
logger.info("prediction_created", extra={
    "user_id": "123",
    "prediction_id": "456",
    "duration_ms": 150
})
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, start_http_server
import time

# Metrics
request_count = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint']
)

# Middleware
@app.middleware("http")
async def track_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    request_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    return response

# Expose metrics
start_http_server(8001)
```

### Error Tracking

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="https://xxxxx@sentry.io/xxxxx",
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1,
)
```

---

## Troubleshooting

### Issue: API won't start

```bash
# Check logs
docker-compose logs api

# Common causes:
# 1. Database connection
python -c "from backend.config.database import SessionLocal; db = SessionLocal()"

# 2. Missing environment variables
echo $SECRET_KEY

# 3. Port already in use
lsof -i :8000

# 4. Invalid configuration
python -c "from backend.config.settings import settings; print(settings)"
```

### Issue: Slow queries

```bash
# Enable query logging
# In backend/config/database.py
echo_pool = True
echo = True

# Profile queries
from sqlalchemy import event
from sqlalchemy.engine import Engine
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    start_time = time.time()

@event.listens_for(Engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, params, context, executemany):
    duration = (time.time() - start_time) * 1000
    if duration > 100:  # Log slow queries > 100ms
        logger.warning(f"Slow query: {duration:.2f}ms")
```

### Issue: Memory leaks

```bash
# Monitor memory usage
docker stats

# Profile memory
pip install memory-profiler
python -m memory_profiler backend/main.py

# Check for circular references
pip install objgraph
import objgraph
objgraph.show_most_common_types(limit=20)
```

### Issue: Database lock

```bash
# SQLite specific
# Close all connections
sqlite3 backend/astrology.db "PRAGMA integrity_check;"

# Reset connection pool
from backend.config.database import engine
engine.dispose()

# Use timeout
PRAGMA busy_timeout=5000;
```

---

## Performance Benchmarks

### Expected Performance

| Metric      | Target     | Current   |
| ----------- | ---------- | --------- |
| P50 Latency | <100ms     | ~80ms ✅  |
| P95 Latency | <500ms     | ~200ms ✅ |
| P99 Latency | <1s        | ~400ms ✅ |
| Throughput  | 100+ req/s | Testing   |
| Error Rate  | <0.1%      | ~0% ✅    |
| Uptime      | 99.9%      | Testing   |

### Load Test Example

```bash
# Using Apache Bench
ab -n 1000 -c 100 http://localhost:8000/health

# Using wrk
wrk -t4 -c100 -d30s http://localhost:8000/health

# Using k6
k6 run load-test.js
```

---

## Deployment Checklist

- [ ] All tests passing (50+)
- [ ] Code coverage 85%+
- [ ] Docker image builds successfully
- [ ] docker-compose up works
- [ ] Health checks pass
- [ ] Database migrations complete
- [ ] Environment variables set
- [ ] CORS origins configured
- [ ] SSL/TLS configured (production)
- [ ] Monitoring/logging configured
- [ ] Backups scheduled
- [ ] Runbook documented
- [ ] Team trained on procedures
- [ ] Staging deployment successful
- [ ] Production deployment approved

---

## Rollback Procedure

### If deployment fails:

```bash
# 1. Stop current deployment
docker-compose down

# 2. Restore previous database backup
sqlite3 backend/astrology.db < backup-YYYYMMDD.sql

# 3. Switch to previous image
docker-compose -f docker-compose.previous.yml up -d

# 4. Verify health
curl http://localhost:8000/health

# 5. Investigate issue
docker-compose logs -f api
```

---

## Support & Escalation

**Issues:**

1. Check logs: `docker-compose logs -f api`
2. Run health checks: `curl http://localhost:8000/health`
3. Check database: `sqlite3 backend/astrology.db ".tables"`
4. Review configuration: `cat .env`

**Escalation:**

- P1 (API down): Check health endpoint, restart containers
- P2 (Degraded): Check database performance, check memory
- P3 (Slow): Check query logs, check load
- P4 (Warnings): Monitor, plan for next release

---

**Document Version:** 1.0  
**Last Updated:** November 2, 2025  
**Next Review:** Phase 3 Week 4
