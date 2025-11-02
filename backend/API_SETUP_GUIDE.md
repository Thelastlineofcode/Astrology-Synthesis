# Phase 3: FastAPI Backend Implementation

## Overview

Phase 3 implements a production-ready REST API that wraps all Phase 2 calculation engines (KP, Dasha, Transit, Ephemeris) into a unified service.

## Project Structure

```
backend/
├── main.py                    # FastAPI application entry point
├── requirements.txt          # Python dependencies
├── .env                      # Local environment configuration
├── .env.example             # Example environment variables
├── config/
│   ├── settings.py          # Configuration management
│   ├── database.py          # Database connection & session
│   └── __init__.py
├── models/
│   ├── database.py          # SQLAlchemy ORM models
│   └── __init__.py
├── schemas/
│   ├── __init__.py          # Pydantic request/response schemas
│   └── ... (schemas imported from main file)
├── services/
│   ├── auth_service.py      # Authentication & JWT tokens
│   ├── calculation_service.py # Orchestrates all 4 engines
│   └── __init__.py
├── api/
│   ├── v1/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── predictions.py   # Prediction endpoints
│   │   ├── charts.py        # Birth chart endpoints
│   │   ├── transits.py      # Transit analysis endpoints
│   │   ├── health.py        # Health check endpoints
│   │   ├── routes.py        # Route imports
│   │   └── __init__.py
│   └── __init__.py
├── middleware/              # Custom middleware
├── tests/                   # Test suite
├── calculations/            # Phase 2 engines (kp_engine.py, dasha_engine.py, etc.)
└── utils/                   # Utilities
```

## Installation & Setup

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Database Setup

#### PostgreSQL Installation (macOS)

```bash
# Using Homebrew
brew install postgresql@14

# Start PostgreSQL service
brew services start postgresql@14

# Create database
createdb astrology_synthesis

# Create user
psql astrology_synthesis -c "CREATE USER astrology_user WITH PASSWORD 'dev_password_12345';"
psql astrology_synthesis -c "ALTER USER astrology_user CREATEDB;"
psql astrology_synthesis -c "GRANT ALL PRIVILEGES ON DATABASE astrology_synthesis TO astrology_user;"
```

### 3. Configuration

The application reads from `.env` file (already created for development):

```bash
# Review/update environment variables
cat .env
```

### 4. Initialize Database Tables

Run the FastAPI app (tables auto-created on startup):

```bash
python -m uvicorn backend.main:app --reload
```

The database schema will be initialized automatically. Check logs for confirmation:

```
✅ Database initialized
```

## Running the API

### Development Mode (with auto-reload)

```bash
cd /Users/houseofobi/Documents/GitHub/Astrology-Synthesis
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: `http://localhost:8000`

**API Documentation:**

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Production Mode

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Create account
- `POST /api/v1/auth/login` - Get JWT token
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/auth/me` - Current user profile

### Predictions

- `POST /api/v1/predict` - Generate comprehensive prediction
- `GET /api/v1/predict/{id}` - Retrieve stored prediction
- `GET /api/v1/predict` - List user's predictions

### Charts

- `POST /api/v1/chart` - Generate birth chart
- `GET /api/v1/chart/{id}` - Retrieve stored chart
- `GET /api/v1/chart` - List user's charts

### Transits

- `POST /api/v1/transits` - Analyze current transits

### Health

- `GET /api/v1/health` - Service health status
- `GET /api/v1/health/stats` - System statistics (admin only)

## Authentication

### Using JWT Tokens

1. **Register:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

2. **Login:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 1800,
  "token_type": "Bearer"
}
```

3. **Use Token in Requests:**

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

### API Key Authentication

API keys are generated on registration. Can also be used in headers:

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "X-API-Key: sk_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

## Testing

### Run Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=backend --cov-report=html

# Specific test file
pytest tests/test_auth.py -v
```

### Load Testing

```bash
# Using Apache Bench
ab -n 100 -c 10 http://localhost:8000/api/v1/health

# Using wrk
wrk -t4 -c100 -d30s http://localhost:8000/api/v1/health
```

## Performance Targets

| Metric        | Target     | Status |
| ------------- | ---------- | ------ |
| P50 Latency   | < 200ms    | 🟡 TBD |
| P95 Latency   | < 500ms    | 🟡 TBD |
| P99 Latency   | < 1000ms   | 🟡 TBD |
| Throughput    | 100+ req/s | 🟡 TBD |
| Test Coverage | 85%+       | 🟡 TBD |
| Uptime        | 99.9%      | 🟡 TBD |

## Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
brew services list | grep postgresql

# Start PostgreSQL if needed
brew services start postgresql@14

# Test connection
psql -U astrology_user -d astrology_synthesis -c "SELECT 1;"
```

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Module Import Errors

```bash
# Verify Python path
export PYTHONPATH="${PYTHONPATH}:/Users/houseofobi/Documents/GitHub/Astrology-Synthesis"

# Reinstall packages
pip install -r requirements.txt --force-reinstall
```

## Next Steps

**Week 1 (Days 3-5):**

- ✅ FastAPI project setup
- ⏳ Database schema deployment
- ⏳ Authentication implementation

**Week 2 (Days 1-4):**

- ⏳ Service layer implementation
- ⏳ Core API endpoints
- ⏳ Caching layer setup

**Week 3 (Days 1-5):**

- ⏳ Testing & performance verification
- ⏳ Documentation & Swagger
- ⏳ Staging deployment

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JWT Authentication](https://tools.ietf.org/html/rfc7519)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Support

For issues or questions about the API:

1. Check the [API Documentation](http://localhost:8000/docs)
2. Review [PHASE3_KICKOFF.md](../PHASE3_KICKOFF.md)
3. Check [API_ARCHITECTURE.md](../API_ARCHITECTURE.md) for specification details
