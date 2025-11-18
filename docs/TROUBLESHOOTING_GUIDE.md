# Phase 5 Troubleshooting Guide

## Quick Diagnostics

### 1. Check System Health

```bash
curl http://localhost:5000/api/v1/perplexity/health
```

**Healthy Response:**

```json
{
  "status": "healthy",
  "services": {
    "llm": true,
    "cache": true,
    "vector_store": true,
    "knowledge_base": true
  }
}
```

---

## Common Issues & Solutions

### Issue 1: "PERPLEXITY_API_KEY is required"

**Symptom:** Server fails to start or LLM requests fail

**Cause:** API key not configured

**Solution:**

```bash
# Check if key is set
echo $PERPLEXITY_API_KEY

# Set in backend/.env
PERPLEXITY_API_KEY=pplx-your-key-here

# Or export in terminal
export PERPLEXITY_API_KEY=pplx-your-key-here
```

**Verification:**

```bash
# Test endpoint
curl -X POST http://localhost:5000/api/v1/interpretations/hybrid \
  -H "Content-Type: application/json" \
  -d '{"chart_data":{"sun":"Aries"},"type":"sun","strategy":"llm"}'
```

---

### Issue 2: 402 Payment Required - Budget Exhausted

**Symptom:**

```json
{
  "error": "Monthly budget exhausted",
  "budget_used": 5.0,
  "budget_remaining": 0.0
}
```

**Cause:** Monthly $5 budget consumed

**Solutions:**

**Option A: Use Fallback Strategy**

```bash
# Switch to auto (uses KB/template fallback)
curl -X POST http://localhost:5000/api/v1/interpretations/hybrid \
  -H "Content-Type": application/json" \
  -d '{"chart_data":{"sun":"Aries"},"type":"sun","strategy":"auto"}'
```

**Option B: Reset Budget (New Month)**

```python
from backend.services.perplexity_llm_service import PerplexityLLMService

service = PerplexityLLMService(api_key="your-key")
service.reset_budget_tracking()
```

**Option C: Increase Budget**

```bash
# In backend/.env
PERPLEXITY_MONTHLY_BUDGET=10.0
```

**Verification:**

```bash
curl http://localhost:5000/api/v1/perplexity/budget
```

---

### Issue 3: Redis Connection Refused

**Symptom:**

```
redis.exceptions.ConnectionError: Connection refused
```

**Cause:** Redis not running

**Solution:**

**Start Redis:**

```bash
# macOS
brew services start redis

# Linux
sudo systemctl start redis

# Docker
docker run -d -p 6379:6379 redis:alpine
```

**Verify Redis:**

```bash
redis-cli ping
# Should return: PONG
```

**Test Cache:**

```bash
curl http://localhost:5000/api/v1/perplexity/cache-stats
```

---

### Issue 4: FAISS "No module named 'faiss'"

**Symptom:**

```
ImportError: No module named 'faiss'
```

**Cause:** FAISS not installed

**Solution:**

```bash
# Install FAISS
pip install faiss-cpu

# Or for GPU support
pip install faiss-gpu
```

**Verification:**

```python
import faiss
print(faiss.__version__)
```

---

### Issue 5: Slow Response Times

**Symptom:** Interpretations taking > 5 seconds

**Diagnosis:**

```bash
# Check which tier is being used
curl http://localhost:5000/api/v1/perplexity/health

# Check cache hit rate
curl http://localhost:5000/api/v1/perplexity/cache-stats
```

**Solutions:**

**If LLM is slow (> 3s):**

- Reduce `max_tokens` in config (default: 512)
- Use `kb` strategy for faster responses
- Check Perplexity API status

**If KB search is slow (> 200ms):**

- Reduce result limit (default: 5)
- Rebuild FAISS index
- Check vector store size

**If cache is disabled:**

```bash
# Enable in backend/.env
REDIS_ENABLED=true
CACHE_ENABLED=true
```

---

### Issue 6: Poor Interpretation Quality

**Symptom:** Interpretations are generic or inaccurate

**Diagnosis:**

```bash
# Check which strategy was used
# Response includes: "strategy": "llm|kb|template"
```

**Solutions:**

**If using templates (70% quality):**

- Ensure LLM budget available
- Check `strategy` parameter is "auto" or "llm"
- Verify API key is valid

**If using KB (80% quality):**

- Index more knowledge base texts
- Improve query context
- Use LLM for critical interpretations

**If using LLM (85% quality):**

- Provide more context in request
- Refine interpretation type
- Check prompt engineering

---

### Issue 7: Vector Store Not Indexing

**Symptom:**

```json
{
  "status": "error",
  "message": "No texts found to index"
}
```

**Cause:** Knowledge base empty or not configured

**Solution:**

**Check KB Directory:**

```bash
ls -la backend/knowledge_base/
# Should contain JSON files with texts
```

**Index Knowledge Base:**

```bash
curl -X POST http://localhost:5000/api/v1/knowledge/index \
  -H "Content-Type: application/json" \
  -d '{"rebuild": true}'
```

**Verify Index:**

```bash
# Search should return results
curl -X POST http://localhost:5000/api/v1/knowledge/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Sun in Aries", "limit": 3}'
```

---

### Issue 8: High Costs / Budget Burning Fast

**Symptom:** Budget exhausted in < 1 week

**Diagnosis:**

```bash
# Check usage patterns
curl http://localhost:5000/api/v1/perplexity/budget

# Check cache hit rate
curl http://localhost:5000/api/v1/perplexity/cache-stats
```

**Solutions:**

**Improve Cache Hit Rate (Target: 60-70%):**

- Increase cache TTL (default: 30 days)
- Normalize query formats
- Cache warming for common queries

**Use KB Strategy More:**

```python
# For non-critical requests
{
  "strategy": "kb"  # Free, 80% quality
}
```

**Batch Requests:**

- Cache similar interpretations
- Avoid duplicate calculations

**Monitor Usage:**

```python
# Set alert at 80% budget
if budget_used >= 4.0:
    send_alert()
    switch_to_kb_strategy()
```

---

### Issue 9: Cache Misses Too High

**Symptom:** Cache hit rate < 50%

**Diagnosis:**

```bash
curl http://localhost:5000/api/v1/perplexity/cache-stats
```

**Causes & Solutions:**

**1. Query Variations:**

```python
# BAD: Different phrasings
"Sun in Aries"
"sun in aries"
"Aries Sun"

# GOOD: Normalized format
normalize_query("Sun in Aries")  # Always returns "sun_aries"
```

**2. Short TTL:**

```bash
# Increase in backend/.env
CACHE_TTL_SECONDS=2592000  # 30 days
```

**3. Cache Cleared Too Often:**

- Only clear cache when content updated
- Don't clear on restart

**4. Unique Requests:**

- Some queries naturally uncacheable
- Focus on caching common patterns

---

### Issue 10: Sentence Transformers Loading Slow

**Symptom:** First request takes > 30 seconds

**Cause:** Model downloading on first use

**Solution:**

**Pre-download Model:**

```python
from sentence_transformers import SentenceTransformer

# Downloads ~90MB model
model = SentenceTransformer('all-MiniLM-L6-v2')
```

**Or use Docker with model pre-loaded:**

```dockerfile
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

---

## Performance Tuning

### Optimize LLM Calls

```python
# Reduce tokens for speed
PerplexityLLMService(
    max_tokens=256,  # From 512 (faster, shorter)
    temperature=0.5,  # From 0.7 (more consistent)
)
```

### Optimize Vector Search

```python
# Reduce search space
FAISSVectorStore(
    index_type="IVF",  # Faster for large indexes
    nlist=100  # Number of clusters
)
```

### Optimize Cache

```python
# Use connection pool
redis_pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50
)
```

---

## Debugging Tools

### Enable Debug Logging

```python
# backend/main.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Monitor Metrics

```python
# Track every request
@router.post("/interpretations/hybrid")
async def interpret(request: InterpretationRequest):
    start_time = time.time()

    # ... process ...

    execution_time = time.time() - start_time
    logger.info(f"Strategy: {strategy}, Time: {execution_time:.2f}s, Cost: ${cost:.6f}")
```

### Test Fallback Chain

```python
# Force each tier
strategies = ["llm", "kb", "template"]

for strategy in strategies:
    response = client.post("/interpretations/hybrid", json={
        "chart_data": {"sun": "Aries"},
        "type": "sun",
        "strategy": strategy
    })
    print(f"{strategy}: {response.json()['quality']}")
```

---

## Health Check Checklist

Run these commands to verify system health:

```bash
# 1. Check all services
curl http://localhost:5000/api/v1/perplexity/health

# 2. Verify budget
curl http://localhost:5000/api/v1/perplexity/budget

# 3. Check cache
curl http://localhost:5000/api/v1/perplexity/cache-stats

# 4. Test LLM
curl -X POST http://localhost:5000/api/v1/interpretations/hybrid \
  -H "Content-Type: application/json" \
  -d '{"chart_data":{"sun":"Aries"},"type":"sun","strategy":"llm"}'

# 5. Test KB
curl -X POST http://localhost:5000/api/v1/knowledge/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Sun in Aries","limit":3}'

# 6. Test fallback
curl -X POST http://localhost:5000/api/v1/interpretations/hybrid \
  -H "Content-Type: application/json" \
  -d '{"chart_data":{"sun":"Aries"},"type":"sun","strategy":"auto"}'
```

All should return 200 OK with valid data.

---

## Emergency Procedures

### System Down - All Tiers Failing

**1. Check Backend:**

```bash
docker logs astrology-backend
# OR
tail -f backend/logs/app.log
```

**2. Restart Services:**

```bash
docker-compose restart
# OR
systemctl restart astrology-backend
```

**3. Fallback to Template Only:**

```python
# Temporary fix in code
FORCE_TEMPLATE_MODE = True
```

### Budget Exhausted - Critical Queries Only

**1. Switch to KB Strategy:**

```bash
# Update default strategy
DEFAULT_STRATEGY=kb
```

**2. Whitelist Critical Endpoints:**

```python
CRITICAL_PATHS = ["/premium-interpretation"]

if request.path in CRITICAL_PATHS:
    strategy = "llm"  # Allow LLM for premium
else:
    strategy = "kb"  # Force KB for others
```

---

## Contact & Support

**Phase 5 Issues:**

- Check logs: `backend/logs/phase5.log`
- Review metrics: `/api/v1/perplexity/health`
- Monitor budget: `/api/v1/perplexity/budget`

**Critical Issues:**

1. Switch to fallback strategy
2. Check system health endpoints
3. Review error logs
4. Restart affected services

**Performance Issues:**

1. Check cache hit rate (target: 60-70%)
2. Monitor response times
3. Review strategy distribution
4. Optimize queries

---

## Appendix: Error Codes

| Code | Meaning             | Solution                       |
| ---- | ------------------- | ------------------------------ |
| 400  | Bad Request         | Check request format           |
| 401  | Unauthorized        | Check API key                  |
| 402  | Payment Required    | Budget exhausted, use fallback |
| 500  | Server Error        | Check logs, restart services   |
| 503  | Service Unavailable | All tiers failed, investigate  |
| 504  | Timeout             | Reduce max_tokens or use KB    |

---

**Last Updated:** November 2, 2025
