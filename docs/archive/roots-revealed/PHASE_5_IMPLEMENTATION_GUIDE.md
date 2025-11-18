# Phase 5 Implementation Guide

## LLM Integration with Perplexity API

**Target:** Agent 3  
**Timeline:** 4 weeks  
**Status:** Ready to Execute

---

## Quick Start (For Agent 3)

### 1. Environment Setup

```bash
# Add to .env file
PERPLEXITY_API_KEY=your-api-key-here
REDIS_URL=redis://localhost:6379
FAISS_INDEX_PATH=./vector_store
MONTHLY_BUDGET=5.0
TEMPERATURE=0.7
TOP_P=0.9
LOG_LEVEL=INFO
```

### 2. Install Dependencies

```bash
pip install requests redis faiss-cpu sentence-transformers
```

### 3. Start Redis

```bash
redis-server
# Or with Docker:
docker run -p 6379:6379 redis:7-alpine
```

---

## Week 1: Foundation Phase

### Task 1.1: Create PerplexityLLMService

**File:** `backend/services/perplexity_llm_service.py`

**Key Features:**

- Initialize with API key
- Generate interpretations
- Track costs & tokens
- Handle errors gracefully
- Retry on timeout

**Tests to Write:**

1. `test_init_with_valid_key()`
2. `test_init_without_key_raises()`
3. `test_cost_calculation()`
4. `test_budget_tracking()`
5. `test_is_available()`

**Success Criteria:**

- ✅ All 5 tests passing
- ✅ API connectivity verified
- ✅ Cost tracking accurate

---

### Task 1.2: Create CachedPerplexityService

**File:** `backend/services/cached_perplexity_service.py`

**Key Features:**

- Extend PerplexityLLMService
- Redis caching layer
- 30-day TTL
- Cache statistics

**Tests:**

1. `test_cache_miss()`
2. `test_cache_hit()`
3. `test_cache_ttl()`

---

## Week 2: Vector Database Phase

### Task 2.1: Create EmbeddingService

**File:** `backend/services/embedding_service.py`

**Model:** all-MiniLM-L6-v2 (384 dimensions)

```python
class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def encode(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts)

    def embed_single(self, text: str) -> np.ndarray:
        return self.model.encode(text)
```

**Tests:**

1. `test_embedding_dimension()`
2. `test_batch_encoding()`
3. `test_similarity()`

---

### Task 2.2: Create FAISSVectorStore

**File:** `backend/services/faiss_vector_store.py`

**Key Features:**

- FAISS IndexFlatL2
- Metadata tracking
- Category weighting
- Persistence

**Category Weights:**

```python
WEIGHTS = {
    "01_voodoo_spiritual_apex": 1.5,
    "02_vedic_core": 1.3,
    "03_vedic_advanced": 1.3,
    "04_dasha_timing": 1.2,
    "15_ayurveda_medicine": 1.2,
}
```

**Tests:**

1. `test_add_texts()`
2. `test_search_basic()`
3. `test_search_with_category_filter()`
4. `test_weight_application()`
5. `test_persistence()`

---

### Task 2.3: Index Knowledge Base

**Script:** `scripts/index_knowledge_base.py`

```python
from pathlib import Path
from backend.services.embedding_service import EmbeddingService
from backend.services.faiss_vector_store import FAISSVectorStore

# Load all 82 KB texts
kb_path = Path("knowledge_base/texts")
texts = []
metadata = []

for category_dir in kb_path.iterdir():
    if category_dir.is_dir():
        for text_file in category_dir.glob("*"):
            with open(text_file) as f:
                texts.append(f.read())
            metadata.append({
                "category": category_dir.name,
                "source": text_file.name
            })

# Create vector store and add texts
vs = FAISSVectorStore()
vs.add_texts(texts, metadata)
vs.save()

print(f"✅ Indexed {len(texts)} texts")
```

---

## Week 3: Hybrid Strategy Phase

### Task 3.1: Create HybridInterpretationService

**File:** `backend/services/hybrid_interpretation_service.py`

**Strategy Selection Logic:**

```python
class HybridInterpretationService:
    def __init__(self,
                 llm_service,
                 vector_store,
                 kb_service,
                 interpretation_service):
        self.llm = llm_service
        self.vs = vector_store
        self.kb = kb_service
        self.interp = interpretation_service

    def interpret(self, chart_data, interp_type, strategy="auto"):
        if strategy == "auto":
            strategy = self._select_strategy()

        if strategy == "llm":
            return self._strategy_llm(chart_data, interp_type)
        elif strategy == "kb":
            return self._strategy_kb(chart_data, interp_type)
        else:
            return self._strategy_template(chart_data, interp_type)

    def _select_strategy(self):
        budget = self.llm.get_budget_remaining()

        if budget["cost_remaining"] > 0.01:
            return "llm"
        elif self.vs.index:
            return "kb"
        else:
            return "template"
```

**Tests:**

1. `test_strategy_selection_with_budget()`
2. `test_strategy_selection_without_budget()`
3. `test_llm_fallback()`
4. `test_kb_fallback()`
5. `test_template_fallback()`
6. `test_end_to_end()`
7. `test_quality_scoring()`
8. `test_performance()`

---

### Task 3.2: Create API Endpoints

**File:** `backend/api/v1/perplexity_endpoints.py`

```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1", tags=["perplexity"])

class ChartData(BaseModel):
    sun: str
    moon: str
    ascendant: str
    time_of_birth: str = None
    location: str = None

class InterpretationRequest(BaseModel):
    chart_data: ChartData
    type: str
    strategy: str = "auto"

@router.post("/interpretations/hybrid")
async def hybrid_interpretation(request: InterpretationRequest):
    """Generate interpretation with hybrid strategy"""
    # Implementation

@router.post("/interpretations/llm")
async def llm_interpretation(request: InterpretationRequest):
    """Generate interpretation with LLM only"""
    # Implementation

@router.get("/budget")
async def get_budget():
    """Check remaining budget"""
    # Implementation

@router.get("/health")
async def health_check():
    """System health check"""
    # Implementation
```

---

## Week 4: Integration & Deployment Phase

### Task 4.1: Integrate with Phase 4

**Update:** `backend/services/interpretation_service.py`

```python
class InterpretationService:
    def __init__(self, use_llm=True, use_cache=True):
        self.templates = {}
        self.knowledge_service = KnowledgeService()

        if use_llm:
            from backend.services.cached_perplexity_service import CachedPerplexityService
            api_key = os.getenv("PERPLEXITY_API_KEY")
            self.llm_service = CachedPerplexityService(api_key)
        else:
            self.llm_service = None

    def generate_sun_sign_interpretation(self, sun_sign, strategy="hybrid"):
        """Generate with hybrid strategy support"""
        chart_data = {"sun": sun_sign}

        if strategy in ["hybrid", "llm"] and self.llm_service:
            try:
                return self.llm_service.generate_interpretation(
                    chart_data, "sun"
                )
            except:
                pass

        # Fallback to Phase 4
        return self._get_template_interpretation(sun_sign, "sun")
```

### Task 4.2: Comprehensive Testing

**Write 7 E2E Tests:**

1. Full workflow: LLM → cache → KB → template
2. Budget exhaustion scenario
3. API failure scenarios
4. Performance benchmarks
5. Cache effectiveness
6. Cost accuracy
7. Multi-user concurrency

### Task 4.3: Documentation

**Create Files:**

1. PHASE_5_IMPLEMENTATION_SUMMARY.md
2. API_PHASE_5_DOCS.md
3. TROUBLESHOOTING_GUIDE.md
4. COST_ANALYSIS_REPORT.md

### Task 4.4: Deployment

**Update Dockerfile:**

```dockerfile
# Add Phase 5 services
COPY backend/services/perplexity_llm_service.py
COPY backend/services/faiss_vector_store.py
COPY backend/services/embedding_service.py
COPY backend/services/cached_perplexity_service.py

# Set environment
ENV PERPLEXITY_API_KEY=${PERPLEXITY_API_KEY}
ENV REDIS_URL=redis://localhost:6379
```

---

## Testing Checklist

### Unit Tests (10)

- [ ] Cost calculation (±0.0001%)
- [ ] Budget tracking
- [ ] Token counting
- [ ] Cache operations
- [ ] Vector indexing
- [ ] Category weighting
- [ ] Embedding quality
- [ ] Strategy selection
- [ ] Error handling
- [ ] Fallback paths

### Integration Tests (8)

- [ ] LLM API connectivity
- [ ] Redis cache
- [ ] FAISS search
- [ ] Fallback chain
- [ ] Budget monitoring
- [ ] Performance <100ms
- [ ] Cost accuracy
- [ ] Concurrent requests

### E2E Tests (4)

- [ ] Full interpretation flow
- [ ] All strategies working
- [ ] Cache effectiveness
- [ ] Production readiness

---

## Performance Benchmarks

### Target Metrics

| Metric           | Target | Acceptable | Failing |
| ---------------- | ------ | ---------- | ------- |
| LLM Response     | <2s    | <3s        | >3s     |
| Vector Search    | <100ms | <150ms     | >150ms  |
| Cache Hit Rate   | >60%   | >50%       | <50%    |
| API Availability | 99.9%  | >99%       | <99%    |
| Cost Accuracy    | ±0.01% | ±0.1%      | >0.1%   |

---

## Deployment Checklist

- [ ] All tests passing
- [ ] Code review completed
- [ ] API documented
- [ ] Environment variables configured
- [ ] Redis deployed
- [ ] FAISS index created
- [ ] Health checks passing
- [ ] Performance validated
- [ ] Cost tracking verified
- [ ] Fallback paths tested
- [ ] Monitoring configured
- [ ] Ready for production

---

## Success Criteria

✅ **Phase 5 Complete When:**

1. 1200+ lines of production code written
2. 20+ tests written and 100% passing
3. LLM service fully integrated
4. Vector DB indexed with all 82 texts
5. Hybrid strategy tested and working
6. API endpoints fully functional
7. Budget tracking accurate
8. Documentation complete
9. Performance targets met
10. Zero critical issues

---

## Next Steps After Phase 5

Once Phase 5 complete:

1. Agent 5 starts Phase 6 (Frontend) in parallel
2. System runs in production with hybrid strategy
3. Monitor usage and optimize costs
4. Gather user feedback on interpretation quality
5. Prepare for Phase 6 integration
