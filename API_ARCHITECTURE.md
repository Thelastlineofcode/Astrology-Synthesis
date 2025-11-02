# API Architecture Design - Phase 3

## Astrology-Synthesis Syncretic Prediction Engine

**Document Date:** November 1, 2025  
**Phase:** 3 (API Architecture & Integration)  
**Agent:** @architect  
**Status:** 🎯 DESIGN PHASE

---

## 1. Executive Overview

The API Architecture provides RESTful endpoints for the complete syncretic prediction engine, integrating KP Astrology, Vimshottari Dasha, Transit Analysis, and Swiss Ephemeris calculations into a unified service.

### 1.1 Design Principles

- **Syncretic Synthesis**: Multi-tradition predictions with confidence scoring
- **Real-Time Accuracy**: Live ephemeris data + historical analysis
- **Scalability**: Horizontal scaling for high-volume predictions
- **Security**: JWT authentication, API keys, rate limiting, GDPR compliance
- **Performance**: <500ms latency for single prediction, <2s for full analysis
- **Extensibility**: Easy addition of new traditions (Vedic, Vodou, Rosicrucian, Arabic)

### 1.2 Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT APPLICATIONS                      │
│          (Web, Mobile, Desktop, Third-party APIs)           │
└──────────────┬──────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────┐
│                  API GATEWAY & ROUTING                      │
│         (Authentication, Rate Limiting, Caching)            │
└──────────────┬──────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────┐
│              CORE API ENDPOINTS (REST)                      │
│  /predict | /chart | /transits | /remedies | /health       │
└──────────────┬──────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────┐
│           CALCULATION ENGINES (SERVICE LAYER)               │
│  KP | Dasha | Transit | Ephemeris | Synthesis              │
└──────────────┬──────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────┐
│              DATA & KNOWLEDGE LAYER                         │
│  Database | Cache | Ephemeris | Knowledge Base              │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. RESTful Endpoint Specification

### 2.1 Authentication Endpoints

#### POST `/api/v1/auth/register`

Register a new user account.

**Request:**

```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "name": "User Name"
}
```

**Response (201):**

```json
{
  "user_id": "uuid-string",
  "email": "user@example.com",
  "name": "User Name",
  "created_at": "2025-11-01T12:00:00Z",
  "api_key": "sk_live_xxxxxxxxxxxxx"
}
```

#### POST `/api/v1/auth/login`

Authenticate and receive JWT token.

**Request:**

```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response (200):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

#### POST `/api/v1/auth/refresh`

Refresh expired access token using refresh token.

**Request:**

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (200):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600
}
```

---

### 2.2 Prediction Endpoints

#### POST `/api/v1/predict`

Get comprehensive astrological predictions (primary endpoint).

**Request:**

```json
{
  "birth_data": {
    "date": "1995-06-15",
    "time": "14:30:00",
    "timezone": "America/New_York",
    "latitude": 40.7128,
    "longitude": -74.006
  },
  "query": "When will I experience major life changes?",
  "traditions": ["kp", "vedic", "vedou"],
  "confidence_threshold": 0.65,
  "time_range": {
    "start": "2025-11-01",
    "end": "2026-11-01"
  },
  "include_remedies": true
}
```

**Response (200):**

```json
{
  "prediction_id": "pred_123456",
  "query": "When will I experience major life changes?",
  "generated_at": "2025-11-01T12:00:00Z",
  "predictions": [
    {
      "event_type": "marriage",
      "timeframe": {
        "start": "2026-01-15",
        "end": "2026-03-30",
        "peak": "2026-02-15"
      },
      "confidence": 0.71,
      "confidence_breakdown": {
        "kp": 0.7,
        "dasha": 0.75,
        "transit": 0.68,
        "syncretic": 0.71
      },
      "tradition_insights": {
        "kp": "Venus transiting in 7th house significator...",
        "vedic": "Exalted Venus in marriage houses...",
        "vodou": "Erzulie Freda (love lwa) activated..."
      },
      "planetary_support": {
        "benefics": ["Venus", "Jupiter"],
        "malefics": [],
        "neutral": ["Mercury"]
      },
      "dasha_support": {
        "current": "Venus Mahadasha",
        "timing_factor": 0.8
      },
      "remedies": [
        {
          "tradition": "vedic",
          "type": "mantra",
          "description": "Chant Shukra Beej Mantra 108 times",
          "duration": "40 days",
          "effectiveness": 0.75
        }
      ]
    }
  ],
  "overall_confidence": 0.71,
  "analysis_summary": "Strong indicators for major life transition in Q1 2026..."
}
```

---

#### GET `/api/v1/predict/{prediction_id}`

Retrieve a specific prediction.

**Response (200):** Same structure as POST response

**Response (404):**

```json
{
  "error": "prediction_not_found",
  "message": "Prediction with ID 'pred_123456' not found",
  "timestamp": "2025-11-01T12:00:00Z"
}
```

---

#### POST `/api/v1/predict/batch`

Get multiple predictions for comparison.

**Request:**

```json
{
  "predictions": [
    {
      "birth_data": {...},
      "query": "Career question?"
    },
    {
      "birth_data": {...},
      "query": "Relationship question?"
    }
  ]
}
```

**Response (200):**

```json
{
  "batch_id": "batch_456789",
  "predictions": [...]
}
```

---

### 2.3 Birth Chart Endpoints

#### POST `/api/v1/chart`

Generate complete birth chart with all calculations.

**Request:**

```json
{
  "birth_data": {
    "date": "1995-06-15",
    "time": "14:30:00",
    "timezone": "America/New_York",
    "latitude": 40.7128,
    "longitude": -74.006
  },
  "house_system": "placidus",
  "ayanamsa": "lahiri",
  "include_aspects": true,
  "include_nakshatras": true
}
```

**Response (200):**

```json
{
  "chart_id": "chart_789012",
  "birth_data": {...},
  "planetary_positions": [
    {
      "planet": "Sun",
      "longitude": 60.24,
      "latitude": 0.0,
      "sign": "Gemini",
      "degree_in_sign": 0.24,
      "nakshatra": "Mrigashira",
      "nakshatra_pada": 2,
      "house": 10,
      "retrograde": false,
      "speed": 1.02
    }
  ],
  "house_cusps": {
    "1": 145.98,
    "2": 168.58,
    "3": 196.33,
    "4": 229.35,
    "5": 264.64,
    "6": 297.46,
    "7": 325.98,
    "8": 348.58,
    "9": 16.33,
    "10": 49.35,
    "11": 84.64,
    "12": 117.46
  },
  "aspects": [
    {
      "planet1": "Mercury",
      "planet2": "Venus",
      "aspect": "Conjunction",
      "orb": 3.92,
      "strength": 0.50,
      "applying": true
    }
  ],
  "dasha_info": {
    "current_mahadasha": "Venus",
    "remaining_years": 12,
    "antardasha": "Saturn",
    "dasha_timeline": [...]
  }
}
```

---

#### GET `/api/v1/chart/{chart_id}`

Retrieve a stored birth chart.

**Response (200):** Same structure as POST response

---

#### POST `/api/v1/chart/comparison`

Compare two birth charts for compatibility.

**Request:**

```json
{
  "chart1_id": "chart_123",
  "chart2_id": "chart_456",
  "relationship_type": "marriage"
}
```

**Response (200):**

```json
{
  "comparison_id": "comp_345678",
  "charts": [
    {"chart_id": "chart_123", ...},
    {"chart_id": "chart_456", ...}
  ],
  "compatibility": {
    "overall_score": 0.78,
    "dimensions": {
      "emotional": 0.82,
      "intellectual": 0.71,
      "spiritual": 0.76,
      "physical": 0.75
    },
    "strengths": ["Strong Venus connection", "Complementary Mars positions"],
    "challenges": ["Saturn square suggests commitment challenges"],
    "synastry_aspects": [...]
  }
}
```

---

### 2.4 Transit Endpoints

#### GET `/api/v1/transits`

Get current and upcoming transits for a birth chart.

**Query Parameters:**

- `chart_id`: Birth chart UUID (required)
- `days_ahead`: Number of days to analyze (default: 365)
- `min_confidence`: Minimum confidence threshold (default: 0.65)

**Response (200):**

```json
{
  "chart_id": "chart_123",
  "current_date": "2025-11-01",
  "analysis_period": {
    "start": "2025-11-01",
    "end": "2026-11-01"
  },
  "active_transits": [
    {
      "planet": "Venus",
      "position": 179.69,
      "sign": "Virgo",
      "house": 7,
      "aspects": [
        {
          "planet": "natal_venus",
          "aspect": "Conjunction",
          "orb": 0.5
        }
      ]
    }
  ],
  "upcoming_windows": [
    {
      "event_type": "marriage",
      "start": "2026-01-15",
      "end": "2026-03-30",
      "peak": "2026-02-15",
      "confidence": 0.71,
      "description": "Venus-7th house activation with strong dasha support..."
    }
  ]
}
```

---

#### POST `/api/v1/transits/analyze`

Analyze transits for specific event types.

**Request:**

```json
{
  "chart_id": "chart_123",
  "event_types": ["marriage", "career", "health", "finances"],
  "time_range": {
    "start": "2025-11-01",
    "end": "2026-11-01"
  }
}
```

**Response (200):** Analysis for each event type with confidence scores

---

### 2.5 Remedies Endpoints

#### GET `/api/v1/remedies/{prediction_id}`

Get recommended remedies for a prediction.

**Response (200):**

```json
{
  "prediction_id": "pred_123456",
  "remedies": [
    {
      "tradition": "vedic",
      "category": "mantra",
      "description": "Chant Shukra Beej Mantra",
      "mantra": "ॐ द्रां द्रीं द्रौं सः शुक्राय नमः",
      "duration": "40 days",
      "frequency": "108 times daily",
      "best_time": "Friday morning",
      "effectiveness_score": 0.75,
      "difficulty": "easy"
    },
    {
      "tradition": "vedic",
      "category": "gemstone",
      "description": "Wear White Diamond or Opal",
      "stone": "Diamond",
      "carat_weight": "1-3 carats",
      "metal": "Gold or Platinum",
      "finger": "Ring finger (right)",
      "effectiveness_score": 0.82,
      "cost": "high"
    },
    {
      "tradition": "vodou",
      "category": "ritual",
      "description": "Offer to Erzulie Freda (love goddess)",
      "ritual": "Light pink candles, offer honey and rum",
      "duration": "3 days",
      "effectiveness_score": 0.68
    }
  ]
}
```

---

### 2.6 Health & Status Endpoints

#### GET `/api/v1/health`

Service health status.

**Response (200):**

```json
{
  "status": "healthy",
  "timestamp": "2025-11-01T12:00:00Z",
  "components": {
    "database": "healthy",
    "ephemeris_cache": "healthy",
    "calculation_engines": "healthy",
    "knowledge_base": "healthy"
  },
  "uptime_hours": 168.5,
  "response_times_ms": {
    "p50": 120,
    "p95": 450,
    "p99": 890
  }
}
```

---

#### GET `/api/v1/status`

Current system status and statistics.

**Response (200):**

```json
{
  "status": "operational",
  "version": "1.0.0",
  "statistics": {
    "total_predictions": 15234,
    "total_charts": 8932,
    "active_users": 1205,
    "average_response_time_ms": 280,
    "accuracy_metrics": {
      "kp": 0.75,
      "dasha": 0.87,
      "transit": 0.71,
      "syncretic": 0.78
    }
  }
}
```

---

## 3. Data Models

### 3.1 Birth Data Model

```python
@dataclass
class BirthData:
    """Complete birth information."""
    date: str                    # "YYYY-MM-DD"
    time: str                    # "HH:MM:SS"
    timezone: str                # "Continent/City"
    latitude: float              # -90 to +90
    longitude: float             # -180 to +180
    name: Optional[str] = None
    gender: Optional[str] = None  # "M", "F", "Other"
```

### 3.2 Prediction Model

```python
@dataclass
class Prediction:
    """Complete astrological prediction."""
    prediction_id: str
    birth_data: BirthData
    query: str
    event_type: str
    timeframe: Dict[str, str]    # start, end, peak
    confidence: float             # 0.0 to 1.0
    confidence_breakdown: Dict    # kp, dasha, transit, syncretic
    tradition_insights: Dict      # insights per tradition
    planetary_support: Dict
    dasha_support: Dict
    remedies: List[Remedy]
    generated_at: datetime
```

### 3.3 Chart Model

```python
@dataclass
class BirthChart:
    """Complete astrological birth chart."""
    chart_id: str
    birth_data: BirthData
    planetary_positions: List[PlanetPosition]
    house_cusps: HouseCusps
    aspects: List[AspectData]
    dasha_info: DashaInfo
    nakshatras: List[NakshatraInfo]
    created_at: datetime
```

---

## 4. Authentication & Security

### 4.1 JWT Token Strategy

```
Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload:
{
  "sub": "user_id",
  "email": "user@example.com",
  "iat": 1698825600,
  "exp": 1698829200,
  "scopes": ["predictions:read", "charts:read", "charts:write"]
}
```

**Token Lifetime:**

- Access Token: 1 hour
- Refresh Token: 30 days

### 4.2 API Key Strategy

- Base64-encoded format: `sk_live_xxxxx` or `sk_test_xxxxx`
- Stored as SHA-256 hash in database
- Rate limiting per API key
- Revokable at any time

### 4.3 Security Headers

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
Content-Security-Policy: default-src 'self'
```

### 4.4 Rate Limiting

```
Global:
  - 1000 requests/minute per IP
  - 10000 requests/hour per IP

Per User (authenticated):
  - 100 predictions/hour
  - 50 charts/hour
  - 500 transits queries/hour

Per API Key (service):
  - 10000 requests/hour
  - Configurable per service tier
```

### 4.5 GDPR Compliance

- Right to access: GET `/api/v1/user/data`
- Right to deletion: DELETE `/api/v1/user/account`
- Right to portability: GET `/api/v1/user/export`
- Data retention policy: 90 days default, configurable
- Consent tracking: All predictions logged with consent
- PII encryption: AES-256 for birth data at rest

---

## 5. Caching Strategy

### 5.1 Cache Layers

```
┌──────────────────────────────────┐
│   CDN Cache (5 min)              │
│   Static responses, charts       │
└──────────────┬───────────────────┘
               │
┌──────────────▼───────────────────┐
│   Redis Cache (30 min)           │
│   Ephemeris, aspects, nakshatras │
└──────────────┬───────────────────┘
               │
┌──────────────▼───────────────────┐
│   Database Cache (persistent)    │
│   Charts, predictions, users     │
└──────────────────────────────────┘
```

### 5.2 Cache Keys

```
# Ephemeris data
ephemeris:{planet}:{date}:{system} = 30 min TTL

# Birth charts
chart:{chart_id} = 24 hours TTL

# Predictions
prediction:{prediction_id} = 48 hours TTL

# Transit analysis
transits:{chart_id}:{date_range} = 1 hour TTL
```

### 5.3 Cache Invalidation

- Time-based (TTL)
- Event-based (new prediction, chart update)
- Manual (admin override)

---

## 6. Database Schema

### 6.1 Core Tables

#### users

```sql
CREATE TABLE users (
  user_id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  api_key_hash VARCHAR(255) UNIQUE,
  is_active BOOLEAN DEFAULT TRUE,
  subscription_tier VARCHAR(50) DEFAULT 'free'
);
```

#### birth_charts

```sql
CREATE TABLE birth_charts (
  chart_id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(user_id),
  birth_date DATE NOT NULL,
  birth_time TIME NOT NULL,
  timezone VARCHAR(50) NOT NULL,
  latitude DECIMAL(10, 6) NOT NULL,
  longitude DECIMAL(10, 6) NOT NULL,
  name VARCHAR(255),
  chart_data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### predictions

```sql
CREATE TABLE predictions (
  prediction_id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(user_id),
  chart_id UUID NOT NULL REFERENCES birth_charts(chart_id),
  query TEXT NOT NULL,
  prediction_data JSONB NOT NULL,
  confidence DECIMAL(3, 2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP,
  is_accurate BOOLEAN,
  feedback TEXT
);
```

#### ephemeris_cache

```sql
CREATE TABLE ephemeris_cache (
  cache_id UUID PRIMARY KEY,
  planet VARCHAR(50) NOT NULL,
  query_date DATE NOT NULL,
  house_system VARCHAR(10),
  position_data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(planet, query_date, house_system)
);
```

#### audit_log

```sql
CREATE TABLE audit_log (
  log_id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(user_id),
  action VARCHAR(100) NOT NULL,
  resource_type VARCHAR(50),
  resource_id VARCHAR(100),
  details JSONB,
  ip_address INET,
  user_agent TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 7. Error Handling

### 7.1 Error Response Format

```json
{
  "error": "error_code",
  "message": "Human-readable message",
  "status_code": 400,
  "timestamp": "2025-11-01T12:00:00Z",
  "request_id": "req_123456",
  "details": {
    "field": "birth_date",
    "issue": "Invalid date format"
  }
}
```

### 7.2 Error Codes

| Code                   | Status | Description                    |
| ---------------------- | ------ | ------------------------------ |
| `invalid_request`      | 400    | Malformed request              |
| `invalid_birth_data`   | 400    | Birth data validation failed   |
| `unauthorized`         | 401    | Missing/invalid authentication |
| `forbidden`            | 403    | Insufficient permissions       |
| `not_found`            | 404    | Resource not found             |
| `rate_limit_exceeded`  | 429    | Too many requests              |
| `internal_error`       | 500    | Server error                   |
| `ephemeris_error`      | 503    | Ephemeris calculation failed   |
| `knowledge_base_error` | 503    | Knowledge base unavailable     |

---

## 8. Performance Targets

### 8.1 Response Time SLAs

| Endpoint    | Target | P95   | P99    |
| ----------- | ------ | ----- | ------ |
| `/predict`  | 400ms  | 800ms | 1500ms |
| `/chart`    | 300ms  | 600ms | 1200ms |
| `/transits` | 200ms  | 400ms | 800ms  |
| `/health`   | 50ms   | 100ms | 200ms  |

### 8.2 Throughput Targets

- 1000 predictions/second (with scaling)
- 500 charts/second
- 10000 transit queries/second
- <50ms p50 latency at scale

### 8.3 Availability Targets

- 99.9% uptime (43 minutes downtime/month)
- 99.99% during peak hours
- Automatic failover within 30 seconds

---

## 9. Deployment Architecture

### 9.1 Infrastructure Stack

```
┌────────────────────────────────────────────────┐
│          AWS / GCP / Azure Cloud               │
├────────────────────────────────────────────────┤
│                                                │
│  ┌──────────────────────────────────────────┐ │
│  │    CloudFront / CDN (Global)             │ │
│  └──────────────────────────────────────────┘ │
│                     │                         │
│  ┌──────────────────▼──────────────────────┐ │
│  │  Application Load Balancer               │ │
│  │  (Health checks, SSL/TLS termination)   │ │
│  └──────────────────▼──────────────────────┘ │
│                     │                         │
│  ┌──────────────────▼──────────────────────┐ │
│  │  Auto-scaling Group (API Servers)       │ │
│  │  • 2-20 instances (Docker containers)   │ │
│  │  • Python 3.14 + FastAPI                │ │
│  │  • Gunicorn workers (4 per instance)    │ │
│  └──────────────────┬──────────────────────┘ │
│                     │                         │
│  ┌──────────────────┼──────────────────────┐ │
│  │   Shared Services                       │ │
│  │   ├─ PostgreSQL (RDS)                   │ │
│  │   ├─ Redis (ElastiCache)                │ │
│  │   ├─ S3 (data storage)                  │ │
│  │   └─ CloudWatch (monitoring)            │ │
│  └──────────────────────────────────────────┘ │
│                                                │
└────────────────────────────────────────────────┘
```

### 9.2 Container Strategy

**Docker Image:**

- Base: `python:3.14-slim`
- Size: ~200MB
- Multi-stage build (optimize layers)

**Kubernetes Manifest:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: astrology-api
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: api
          image: astrology-synthesis:1.0.0
          ports:
            - containerPort: 8000
          resources:
            requests:
              memory: "512Mi"
              cpu: "500m"
            limits:
              memory: "1Gi"
              cpu: "1000m"
          livenessProbe:
            httpGet:
              path: /api/v1/health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
```

---

## 10. Monitoring & Observability

### 10.1 Metrics

**Application Metrics:**

- Request latency (p50, p95, p99)
- Error rates (by endpoint)
- Throughput (requests/second)
- Cache hit/miss ratios

**Business Metrics:**

- Predictions generated/day
- Charts created/day
- Average confidence scores
- User satisfaction (CSAT)

**Infrastructure Metrics:**

- CPU utilization
- Memory usage
- Disk I/O
- Network traffic

### 10.2 Logging Strategy

**Structured Logging (JSON):**

```json
{
  "timestamp": "2025-11-01T12:00:00Z",
  "level": "INFO",
  "request_id": "req_123456",
  "user_id": "user_789",
  "endpoint": "/api/v1/predict",
  "method": "POST",
  "status": 200,
  "duration_ms": 250,
  "message": "Prediction generated successfully"
}
```

**Log Levels:**

- DEBUG: Development/troubleshooting
- INFO: Normal operations
- WARNING: Degraded but functional
- ERROR: Errors with recovery
- CRITICAL: System failures

**Log Retention:**

- Application logs: 30 days
- Audit logs: 1 year
- Error logs: 90 days

### 10.3 Tracing

- Distributed tracing (Jaeger/Zipkin)
- Per-request unique ID
- Trace through all services
- Performance analysis

### 10.4 Alerting

**Alert Conditions:**

- Error rate > 5%
- Latency p95 > 1 second
- Database connection pool > 80%
- Redis eviction rate > 10%
- Uptime < 99.9%

**Alert Channels:**

- PagerDuty (critical)
- Slack (warnings)
- Email (digest)

---

## 11. API Versioning Strategy

### 11.1 Version Management

- Current: `v1`
- Pattern: `/api/v1/`, `/api/v2/` (future)
- Deprecation: 12-month notice before removal
- Sunset header: `Sunset: Sun, 15 Nov 2026 23:59:59 GMT`

### 11.2 Breaking Changes Policy

- Version bump for breaking changes
- Parallel support for multiple versions
- Mandatory migration path
- Clear migration guide per release

---

## 12. Development Roadmap

### Phase 3A (Weeks 1-2): Core API Implementation

- [ ] FastAPI project setup with middleware
- [ ] Authentication system (JWT + API keys)
- [ ] Database schema creation
- [ ] Core endpoints implementation (/predict, /chart, /transits)
- [ ] Error handling and validation
- [ ] Unit tests (85%+ coverage)

### Phase 3B (Weeks 2-3): Integration & Performance

- [ ] Calculation engine integration
- [ ] Caching layer (Redis)
- [ ] Performance optimization
- [ ] Load testing (1000 req/s target)
- [ ] Integration tests
- [ ] Documentation (API docs, postman collection)

### Phase 3C (Ongoing): Deployment & Monitoring

- [ ] Docker containerization
- [ ] Kubernetes manifests
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Monitoring setup (Prometheus/Grafana)
- [ ] Log aggregation (ELK stack)
- [ ] Production deployment

---

## 13. Integration Points

### 13.1 Calculation Engines (Existing)

```python
# From backend/calculations/
from kp_engine import get_significators_for_house, get_sub_lord
from dasha_engine import DashaCalculator, get_dasha_at_date
from transit_engine import TransitAnalyzer
from ephemeris import EphemerisCalculator
```

### 13.2 API Integration Layer

```python
# New: backend/api/services/
class PredictionService:
    def __init__(self):
        self.kp = KPEngine()
        self.dasha = DashaCalculator()
        self.transit = TransitAnalyzer()
        self.ephemeris = EphemerisCalculator()

    def predict(self, birth_data, query, traditions):
        # Orchestrate all engines
        # Return unified prediction
        pass
```

### 13.3 Database Integration

- ORM: SQLAlchemy
- Migrations: Alembic
- Connection pooling: 20-50 connections
- Read replicas for scaling

---

## 14. Success Criteria (Phase 3)

### 14.1 Functional Requirements

- ✓ All endpoints operational
- ✓ Authentication working
- ✓ Integration tests passing (95%+)
- ✓ Database schema normalized
- ✓ Caching reducing latency by 60%

### 14.2 Performance Requirements

- ✓ P50 latency: <200ms
- ✓ P95 latency: <500ms
- ✓ Error rate: <1%
- ✓ Throughput: 100+ req/s single instance

### 14.3 Quality Requirements

- ✓ Code coverage: 85%+
- ✓ API documentation: 100%
- ✓ Zero security vulnerabilities
- ✓ OWASP Top 10 compliance

### 14.4 Documentation Requirements

- ✓ API documentation (OpenAPI/Swagger)
- ✓ Architecture diagram
- ✓ Deployment guide
- ✓ Operations runbook

---

## 15. Next Steps

### Immediate (This Week)

1. Review and approve architecture
2. Set up FastAPI project scaffold
3. Initialize database
4. Begin authentication implementation

### Short-term (Week 2-3)

1. Implement core endpoints
2. Integration with calculation engines
3. Performance testing
4. Deploy staging environment

### Medium-term (Week 4+)

1. Production deployment
2. Unblock Phase 4 (Knowledge Base + AI)
3. Begin historical validation
4. Prepare security audit

---

## 16. Document Control

**Version:** 1.0 (Draft)  
**Date:** November 1, 2025  
**Author:** @architect Agent  
**Status:** 🎯 READY FOR IMPLEMENTATION  
**Next Review:** After Phase 3 completion

---

## Appendix A: OpenAPI Specification

See `openapi.yaml` for complete OpenAPI 3.0 specification with all request/response examples.

## Appendix B: Database Diagrams

See `DATABASE_SCHEMA.md` for detailed ER diagrams and normalization analysis.

## Appendix C: Security Audit Checklist

See `SECURITY_CHECKLIST.md` for comprehensive security implementation checklist.

---

**🚀 Phase 3 API Architecture Ready for Implementation**

This comprehensive design enables the Astrology-Synthesis engine to serve predictions at scale while maintaining accuracy, security, and performance. The modular design allows parallel work on:

- **Phase 3**: API Development (this phase)
- **Phase 4**: Knowledge Base + AI Synthesis (@data + @ai)
- **Phase 5**: Historical Validation (@qa)
- **Phase 6**: Security Hardening (@security)
- **Phase 7**: Production Deployment (@devops)
