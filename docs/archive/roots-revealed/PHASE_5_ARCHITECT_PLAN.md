# Phase 5: LLM Integration & Vector Database - Architect Plan

**Date:** November 2, 2025  
**Agent:** Architect (Planning for Agent 3)  
**Status:** Ready for Implementation

---

## 1. EXECUTIVE VISION

### Objective

Implement production-ready Phase 5 with Perplexity API ($5/month) + Free stack for semantic search and enhanced interpretations.

### Success Criteria

- ✅ 1200+ lines of production code
- ✅ 20+ integration tests (100% passing)
- ✅ Hybrid fallback strategy (LLM → KB → Templates)
- ✅ Budget monitoring & cost tracking
- ✅ 47,000+ monthly interpretation capacity
- ✅ <100ms vector search latency
- ✅ 60-70% cache hit rate

### Cost Structure

- **LLM:** Perplexity API (sonar-small): $5/month ✓ (You have budget!)
- **Vector DB:** FAISS: $0 (free)
- **Embeddings:** Sentence Transformers: $0 (free)
- **Cache:** Redis: $0 (free)
- **Total:** $5/month (already budgeted)

---

## 2. SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER REQUEST                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────▼──────────────────┐
        │   API Gateway (FastAPI)            │
        │   • Authentication                 │
        │   • Rate Limiting                  │
        │   • Request Validation             │
        └────────────────┬──────────────────┘
                         │
        ┌────────────────▼──────────────────────────────┐
        │   Interpretation Service                       │
        │   (Orchestration Layer)                        │
        └────────────────┬──────────────────────────────┘
                         │
        ┌────────────────┴──────────────────────────────┐
        │                                               │
        ▼                                               ▼
┌──────────────────┐                          ┌──────────────────┐
│ Strategy Router  │                          │ Cache Check      │
│ (Hybrid Impl.)   │◄─────Hit?────────────────│ (Redis)          │
└────────┬─────────┘                          └──────────────────┘
         │
    ┌────┴──────────────────────────────────────────┐
    │                                               │
    ▼                                               ▼
┌──────────────────┐                        ┌──────────────────┐
│ LLM Strategy 1   │                        │ KB Strategy 2    │
│ Perplexity API   │                        │ FAISS + Search   │
│ (sonar-small)    │──Fail?──────┐         │ (Semantic)       │
│ • Research focus │             │         │ • Cost: $0       │
│ • Citations      │             │         │ • Quality: 80%+  │
│ • $0.0001/interp │             │         └──────┬───────────┘
└─────────────────┘              │                │
                                 │         ┌──────▼────────┐
                                 │         │ Template 3    │
                                 │         │ (Phase 4)     │
                                 │         │ • Cost: $0    │
                                 │         │ • Quality: 70%│
                                 └────────►└──────────────┘
                                                │
                                                ▼
                                        ┌──────────────────┐
                                        │ Response Cache   │
                                        │ (Redis)          │
                                        │ TTL: 30 days     │
                                        └──────────────────┘
```

---

## 3. IMPLEMENTATION ROADMAP

### Phase 5A: Foundation (Week 1)

**Goal:** Core LLM service + connectivity

**Deliverables:**

1. `backend/services/perplexity_llm_service.py` (200 lines)
   - PerplexityLLMService class
   - Cost tracking & budgeting
   - Error handling & fallbacks
   - API connectivity

2. `backend/services/cached_perplexity_service.py` (100 lines)
   - Redis caching layer
   - 30-day TTL
   - Cache hit statistics

3. Tests (5 tests)
   - API connectivity
   - Cost calculation
   - Budget tracking
   - Error handling

**Timeline:** 1 week
**Owner:** Agent 3
**Dependencies:** None

---

### Phase 5B: Vector Database (Week 2)

**Goal:** FAISS integration + semantic search

**Deliverables:**

1. `backend/services/faiss_vector_store.py` (200 lines)
   - FAISS index management
   - Text embedding integration
   - Similarity search
   - Category filtering with weights

2. `backend/services/embedding_service.py` (100 lines)
   - Sentence Transformers wrapper
   - Batch embedding capability
   - Embedding caching

3. Data loading (initial setup)
   - Index all 82 KB texts
   - Store embeddings
   - Verify search quality

**Timeline:** 1 week
**Owner:** Agent 3
**Dependencies:** Phase 5A

---

### Phase 5C: Hybrid Strategy (Week 3)

**Goal:** Orchestration + fallback logic

**Deliverables:**

1. `backend/services/hybrid_interpretation_service.py` (150 lines)
   - Strategy selection logic
   - Fallback handling
   - Quality scoring
   - Performance optimization

2. `backend/api/v1/perplexity_endpoints.py` (100 lines)
   - POST /api/v1/interpretations/hybrid
   - POST /api/v1/interpretations/llm
   - GET /api/v1/budget
   - GET /api/v1/health

3. Tests (8 tests)
   - Fallback paths
   - Strategy selection
   - Response quality
   - Performance

**Timeline:** 1 week
**Owner:** Agent 3
**Dependencies:** Phase 5A, 5B

---

### Phase 5D: Integration & Deployment (Week 4)

**Goal:** Full system integration + testing + deployment

**Deliverables:**

1. Integration with Phase 4
   - Update InterpretationService
   - Maintain backward compatibility
   - Add strategy parameter

2. Comprehensive tests (7 tests)
   - End-to-end workflows
   - Budget exhaustion scenarios
   - Cache performance
   - Fallback chains

3. Documentation
   - API documentation
   - Implementation guide
   - Troubleshooting guide
   - Cost analysis report

4. Deployment
   - Docker integration
   - Environment variables
   - Health checks
   - Monitoring

**Timeline:** 1 week
**Owner:** Agent 3
**Dependencies:** Phase 5A, 5B, 5C

---

## 4. TECHNICAL SPECIFICATIONS

### 4.1 Perplexity LLM Service

**File:** `backend/services/perplexity_llm_service.py`

```python
class PerplexityLLMService:
    """
    Production LLM Service using Perplexity API (sonar-small)

    Features:
    - Cost tracking per request
    - Budget monitoring ($5/month)
    - Error handling & retries
    - Structured output support
    - Research mode with citations
    """

    # Constants
    MODEL = "sonar-small"
    BASE_URL = "https://api.perplexity.ai"
    TIMEOUT = 30
    MAX_RETRIES = 3
    TEMPERATURE = 0.7
    TOP_P = 0.9

    # Pricing (per 1M tokens)
    PRICING = {
        "sonar-small": {"input": 0.0001, "output": 0.0003},
        "sonar": {"input": 0.002, "output": 0.006},
        "sonar-pro": {"input": 0.003, "output": 0.009}
    }

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.tokens_used = 0
        self.cost_used = 0.0

    def generate_interpretation(
        self,
        chart_data: Dict,
        interpretation_type: str,
        max_tokens: int = 500
    ) -> Dict:
        """Generate astrological interpretation with cost tracking"""

    def get_budget_remaining(self, monthly_budget: float = 5.0) -> Dict:
        """Calculate remaining budget and capacity"""

    def is_available(self) -> bool:
        """Health check for API availability"""
```

**Inputs:**

- chart_data: {sun, moon, ascendant, time_of_birth, location}
- interpretation_type: full|sun|moon|ascendant|vedic|health
- max_tokens: 200-1000

**Outputs:**

- interpretation: str (generated text)
- cost: float (USD spent)
- tokens_used: int
- success: bool
- timestamp: ISO 8601

**Error Handling:**

- Retry on network timeout (3 retries)
- Fallback on API error
- Cost tracking on all requests
- Logging of all failures

---

### 4.2 Vector Database Service

**File:** `backend/services/faiss_vector_store.py`

```python
class FAISSVectorStore:
    """
    Production Vector Store using FAISS

    Features:
    - Fast similarity search (<100ms)
    - Category-based filtering
    - Weight multipliers (1.5x for voodoo, 1.3x for vedic)
    - Metadata preservation
    - Persistence to disk
    """

    def __init__(self, dimension: int = 384, index_path: str = "./vector_store"):
        self.dimension = dimension  # all-MiniLM-L6-v2 outputs 384
        self.index_path = index_path
        self.index = None  # FAISS IndexFlatL2
        self.metadata = {}  # id -> {text, category, weight, source}

    def add_texts(
        self,
        texts: List[str],
        metadata_list: List[Dict]
    ) -> None:
        """Add texts to vector store with metadata"""

    def search(
        self,
        query: str,
        k: int = 5,
        category_filter: str = None
    ) -> List[Dict]:
        """Search with optional category filtering and weighting"""

    def save(self) -> None:
        """Persist index to disk"""

    def load(self) -> None:
        """Load persisted index"""
```

**Supported Categories:**

- 01_voodoo_spiritual_apex (weight: 1.5x)
- 02_vedic_core (weight: 1.3x)
- 03_vedic_advanced (weight: 1.3x)
- 04_dasha_timing (weight: 1.2x)
- 15_ayurveda_medicine (weight: 1.2x)
- Others (weight: 1.0x)

---

### 4.3 Cached Service

**File:** `backend/services/cached_perplexity_service.py`

```python
class CachedPerplexityService(PerplexityLLMService):
    """
    Perplexity service with Redis caching

    Features:
    - 30-day cache TTL
    - Cache hit tracking
    - Automatic persistence
    - Cost savings on repeat requests
    """

    def __init__(self, api_key: str, redis_url: str = "redis://localhost:6379"):
        super().__init__(api_key)
        self.redis = redis.Redis.from_url(redis_url)
        self.cache_ttl = 86400 * 30  # 30 days

    def generate_interpretation(
        self,
        chart_data: Dict,
        interpretation_type: str,
        **kwargs
    ) -> Dict:
        """Generate with automatic caching"""
        # Check cache first
        # If miss: call API
        # Store result in cache
        # Return result
```

**Cache Keys:** `perplexity:sha256(chart_data + type)`
**TTL:** 30 days
**Storage:** Redis
**Eviction:** LRU if memory full

---

## 5. API ENDPOINTS

### Interpretation Endpoints

```
POST /api/v1/interpretations/hybrid
├─ Request:
│  ├─ chart_data: {sun, moon, ascendant, ...}
│  ├─ type: full|sun|moon|ascendant|vedic|health
│  └─ strategy: auto|llm_only|kb_only|template_only
│
└─ Response:
   ├─ interpretation: str
   ├─ strategy_used: string
   ├─ cost: float (USD)
   ├─ quality_score: float (0-1)
   └─ timestamp: ISO 8601

POST /api/v1/interpretations/llm
├─ Request: Same as hybrid
└─ Response: Same as hybrid (but LLM only)

GET /api/v1/budget
├─ Request: None
└─ Response:
   ├─ monthly_budget: 5.0
   ├─ cost_used: float
   ├─ cost_remaining: float
   ├─ tokens_used: int
   ├─ tokens_remaining: int
   ├─ budget_percent_used: float
   └─ interpretations_remaining: int

GET /api/v1/health
├─ Request: None
└─ Response:
   ├─ status: ok|error
   ├─ llm_available: bool
   ├─ vector_db_available: bool
   ├─ cache_available: bool
   └─ timestamp: ISO 8601
```

---

## 6. DATA FLOW

### Request Flow: Hybrid Interpretation

```
User Request
    ↓
API Gateway (validate JWT, rate limit)
    ↓
Cache Check (Redis)
    ├─ Hit? → Return cached response
    └─ Miss? → Continue
    ↓
Strategy Determination
    ├─ Check budget remaining
    ├─ Check LLM availability
    └─ Select strategy: LLM → KB → Template
    ↓
Execute Strategy
    ├─ LLM: Call Perplexity API
    │   ├─ Build prompt with KB context
    │   ├─ Call sonar-small model
    │   ├─ Track tokens & cost
    │   └─ On error: fallback to KB
    │
    ├─ KB: FAISS semantic search
    │   ├─ Embed query
    │   ├─ Search with category weighting
    │   ├─ Aggregate results
    │   └─ On error: fallback to template
    │
    └─ Template: Phase 4 templates
        └─ Return predefined text
    ↓
Response Caching (Redis)
    ├─ Store in cache (30-day TTL)
    └─ Continue
    ↓
Response Assembly
    ├─ interpretation: selected text
    ├─ strategy_used: which strategy was used
    ├─ cost: USD spent
    ├─ quality_score: confidence (0-1)
    └─ timestamp: ISO 8601
    ↓
User Response (JSON)
```

---

## 7. TESTING STRATEGY

### Test Categories (20+ tests)

**Unit Tests (10 tests)**

1. Cost calculation accuracy
2. Budget tracking correctness
3. Token counting validation
4. Model selection logic
5. Cache key generation
6. Vector search accuracy
7. Category filtering
8. Weight application
9. Metadata preservation
10. Error handling

**Integration Tests (8 tests)**

1. LLM API connectivity
2. Fallback chain execution
3. Cache hit/miss scenarios
4. End-to-end interpretation
5. Budget exhaustion handling
6. Performance: <100ms search
7. Performance: <2s LLM response
8. Cost tracking accuracy

**E2E Tests (4 tests)**

1. Full hybrid workflow
2. All fallback paths
3. Cache effectiveness
4. Budget monitoring

---

## 8. DEPLOYMENT ARCHITECTURE

### Docker Integration

```dockerfile
FROM python:3.11-slim

# Install dependencies
RUN apt-get install -y redis-server

# Copy Phase 5 code
COPY backend/services/perplexity_llm_service.py /app/backend/services/
COPY backend/services/faiss_vector_store.py /app/backend/services/
COPY backend/services/embedding_service.py /app/backend/services/
COPY backend/services/cached_perplexity_service.py /app/backend/services/

# Set environment variables
ENV PERPLEXITY_API_KEY=${PERPLEXITY_API_KEY}
ENV REDIS_URL=redis://localhost:6379

# Start services
CMD redis-server & python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Environment Variables

````bash
```bash
# Required
PERPLEXITY_API_KEY=your-api-key-here

# Optional
REDIS_URL=redis://localhost:6379
FAISS_INDEX_PATH=./vector_store
````

MONTHLY_BUDGET=5.0
TEMPERATURE=0.7
TOP_P=0.9
LOG_LEVEL=INFO

```

---

## 9. PERFORMANCE TARGETS

| Metric        | Target    | Method                  |
| ------------- | --------- | ----------------------- |
| LLM Response  | <2s       | async requests, caching |
| Vector Search | <100ms    | FAISS IndexFlatL2       |
| Cache Hit     | 60-70%    | 30-day TTL, smart keys  |
| Throughput    | 1,567/day | $5 ÷ $0.0001 per interp |
| Availability  | 99.9%     | Fallback chain          |
| Cost/Interp   | $0.0001   | sonar-small only        |

---

## 10. RISK MITIGATION

### Potential Issues & Solutions

| Issue                  | Probability | Impact | Solution                      |
| ---------------------- | ----------- | ------ | ----------------------------- |
| Perplexity API timeout | Medium      | High   | Fallback to KB immediately    |
| Budget exhaustion      | Low         | High   | Monitor usage, alert at 80%   |
| Vector DB corruption   | Low         | Medium | Backup daily, rebuild from KB |
| Cache memory full      | Low         | Medium | LRU eviction, tune TTL        |
| Embedding quality poor | Low         | Medium | Use all-mpnet-base-v2 backup  |

---

## 11. SUCCESS METRICS

### Phase 5 Completion Criteria

- ✅ 1200+ lines production code
- ✅ 20+ tests, 100% passing
- ✅ LLM integration working
- ✅ Vector search <100ms
- ✅ Cache hit rate >60%
- ✅ Budget tracking accurate
- ✅ All fallbacks functional
- ✅ Zero critical issues
- ✅ Documentation complete
- ✅ Ready for production

---

## 12. HANDOFF CHECKLIST FOR AGENT 3

- ✅ This architect plan created
- ✅ API key provided (see .env.phase5.template)
- ✅ Architecture validated
- ✅ Dependencies identified
- ✅ Test strategy defined
- ✅ Performance targets set

**Ready to hand off to Agent 3 for implementation!**

---

## Appendix A: File Structure

```

backend/
├── services/
│ ├── perplexity_llm_service.py (200 lines)
│ ├── cached_perplexity_service.py (100 lines)
│ ├── embedding_service.py (100 lines)
│ ├── faiss_vector_store.py (200 lines)
│ └── hybrid_interpretation_service.py (150 lines)
│
├── api/v1/
│ └── perplexity_endpoints.py (100 lines)
│
└── models/
└── perplexity_models.py (50 lines)

tests/
├── test_perplexity_service.py (100 lines)
├── test_faiss_vector_store.py (100 lines)
├── test_cached_service.py (80 lines)
├── test_hybrid_interpretation.py (100 lines)
└── test_perplexity_endpoints.py (150 lines)

TOTAL: ~1300+ lines of production + test code

```

```
