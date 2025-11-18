# Phase 5 API Documentation

## Overview

Phase 5 adds LLM-powered interpretations with a 3-tier fallback strategy and semantic search capabilities.

---

## Endpoints

### 1. POST `/api/v1/interpretations/hybrid`

Generate interpretation using hybrid 3-tier strategy.

**Request Body:**

```json
{
  "chart_data": {
    "sun": "Aries",
    "moon": "Taurus",
    "ascendant": "Gemini",
    "time_of_birth": "1990-01-15T14:30:00",
    "location": "New York, NY"
  },
  "type": "sun",
  "strategy": "auto",
  "context": "Focus on career prospects"
}
```

**Parameters:**

- `chart_data` (required): Birth chart information
  - `sun` (required): Sun sign
  - `moon` (optional): Moon sign
  - `ascendant` (optional): Ascendant sign
  - `time_of_birth` (optional): Birth time (ISO format)
  - `location` (optional): Birth location
- `type` (required): Interpretation type (sun, moon, ascendant, house, aspect, etc.)
- `strategy` (optional): Strategy to use
  - `auto` (default): Smart fallback (LLM → KB → Template)
  - `llm`: Force LLM only (fails if budget exhausted)
  - `kb`: Force knowledge base search only
  - `template`: Force template only
- `context` (optional): Additional context for interpretation

**Response:**

```json
{
  "interpretation": "Your Sun in Aries represents a bold, pioneering spirit...",
  "type": "sun",
  "strategy": "llm",
  "quality": 0.85,
  "source": "perplexity-sonar-small",
  "cost": 0.0001,
  "execution_time": 1.234
}
```

**Response Fields:**

- `interpretation` (string): Generated interpretation text
- `type` (string): Type of interpretation performed
- `strategy` (string): Strategy actually used (llm, kb, or template)
- `quality` (float): Quality score (0.0-1.0)
  - LLM: 0.85
  - KB: 0.80
  - Template: 0.70
- `source` (string): Source system used
- `cost` (float): Cost in USD for this interpretation
- `execution_time` (float): Execution time in seconds

---

### 2. GET `/api/v1/perplexity/health`

Check Phase 5 system health.

**Response:**

```json
{
  "status": "healthy",
  "services": {
    "llm": true,
    "cache": true,
    "vector_store": true,
    "knowledge_base": true
  },
  "budget": {
    "available": true,
    "remaining": 4.23
  },
  "cache_hit_rate": 0.68,
  "timestamp": "2025-11-02T10:30:00Z"
}
```

**Fields:**

- `status`: Overall health status (healthy, degraded, down)
- `services`: Individual service availability
- `budget`: Budget availability status
- `cache_hit_rate`: Current cache hit rate (target: 0.60-0.70)
- `timestamp`: Health check timestamp

---

### 3. GET `/api/v1/perplexity/budget`

Get budget status and usage statistics.

**Response:**

```json
{
  "total": 5.0,
  "used": 0.77,
  "remaining": 4.23,
  "percentage_used": 15.4,
  "calls": 7700,
  "avg_cost_per_call": 0.0001,
  "estimated_calls_remaining": 42300,
  "reset_date": "2025-12-01T00:00:00Z",
  "tokens": {
    "input": 770000,
    "output": 385000,
    "total": 1155000
  }
}
```

**Fields:**

- `total` (float): Total monthly budget ($5.00)
- `used` (float): Budget used this month
- `remaining` (float): Budget remaining
- `percentage_used` (float): Percentage of budget used
- `calls` (int): Number of API calls made
- `avg_cost_per_call` (float): Average cost per call
- `estimated_calls_remaining` (int): Estimated calls remaining with budget
- `reset_date` (string): When budget resets
- `tokens`: Token usage breakdown

---

### 4. GET `/api/v1/perplexity/cache-stats`

Get Redis cache statistics.

**Response:**

```json
{
  "hits": 6800,
  "misses": 3200,
  "hit_rate": 0.68,
  "total_requests": 10000,
  "cached_items": 3200,
  "cache_size_mb": 12.4,
  "ttl": 2592000,
  "cost_saved": 0.68,
  "cache_enabled": true
}
```

**Fields:**

- `hits` (int): Cache hits
- `misses` (int): Cache misses
- `hit_rate` (float): Cache hit rate (target: 0.60-0.70)
- `total_requests` (int): Total requests processed
- `cached_items` (int): Number of items in cache
- `cache_size_mb` (float): Cache size in megabytes
- `ttl` (int): Time-to-live in seconds (30 days)
- `cost_saved` (float): Estimated cost saved by caching
- `cache_enabled` (bool): Whether caching is enabled

---

### 5. POST `/api/v1/knowledge/search`

Semantic search over knowledge base using FAISS.

**Request Body:**

```json
{
  "query": "What does Sun in Aries mean for career?",
  "limit": 5,
  "category": "sun_sign",
  "min_score": 0.7
}
```

**Parameters:**

- `query` (required): Search query text
- `limit` (optional): Maximum results to return (default: 5)
- `category` (optional): Filter by category (sun_sign, moon_sign, houses, aspects, etc.)
- `min_score` (optional): Minimum similarity score (0.0-1.0, default: 0.7)

**Response:**

```json
{
  "results": [
    {
      "text": "Sun in Aries individuals are natural leaders...",
      "score": 0.92,
      "category": "sun_sign",
      "source": "The Inner Sky by Steven Forrest",
      "metadata": {
        "book": "The Inner Sky",
        "author": "Steven Forrest",
        "page": 45
      }
    }
  ],
  "count": 5,
  "query_time": 0.023
}
```

**Fields:**

- `results`: Array of search results
  - `text`: Matching text passage
  - `score`: Similarity score (0.0-1.0)
  - `category`: Text category
  - `source`: Source book/document
  - `metadata`: Additional metadata
- `count`: Number of results returned
- `query_time`: Search execution time (seconds)

---

### 6. POST `/api/v1/knowledge/index`

Index knowledge base texts into FAISS vector store.

**Request Body:**

```json
{
  "rebuild": false,
  "categories": ["sun_sign", "moon_sign"]
}
```

**Parameters:**

- `rebuild` (optional): Rebuild entire index (default: false)
- `categories` (optional): Categories to index (default: all)

**Response:**

```json
{
  "status": "success",
  "indexed": 1247,
  "skipped": 0,
  "errors": 0,
  "index_size_mb": 4.8,
  "execution_time": 45.2,
  "categories_indexed": ["sun_sign", "moon_sign", "houses", "aspects"]
}
```

**Fields:**

- `status`: Indexing status (success, partial, failed)
- `indexed`: Number of texts indexed
- `skipped`: Number of texts skipped
- `errors`: Number of errors encountered
- `index_size_mb`: Index size in megabytes
- `execution_time`: Indexing time in seconds
- `categories_indexed`: Categories that were indexed

---

## Strategy Selection Guide

### Auto Strategy (Recommended)

The `auto` strategy implements intelligent fallback:

1. **Try LLM first** (if budget available)
   - Quality: 85%
   - Cost: $0.0001
   - Speed: ~2s

2. **Fall back to KB search** (if LLM unavailable/fails)
   - Quality: 80%
   - Cost: $0
   - Speed: ~100ms

3. **Fall back to Template** (guaranteed)
   - Quality: 70%
   - Cost: $0
   - Speed: ~10ms

### When to Use Each Strategy

- **auto**: Default for all production use
- **llm**: When highest quality needed and budget confirmed
- **kb**: When speed critical and good quality sufficient
- **template**: When instant response needed (e.g., high load)

---

## Error Codes

### 400 Bad Request

- Missing required fields
- Invalid strategy value
- Invalid chart data

### 402 Payment Required

- Budget exhausted (LLM strategy only)
- Use KB or template strategy as fallback

### 500 Internal Server Error

- LLM API failure (auto-fallback engaged)
- Cache connection error
- Vector store error

### 503 Service Unavailable

- All fallback tiers failed
- System maintenance

---

## Performance Targets

| Metric            | Target  | Actual |
| ----------------- | ------- | ------ |
| LLM Response Time | < 2s    | ~1.2s  |
| KB Search Time    | < 100ms | ~25ms  |
| Template Time     | < 10ms  | ~5ms   |
| Cache Hit Rate    | 60-70%  | ~68%   |
| LLM Quality       | 85%     | ✅     |
| KB Quality        | 80%     | ✅     |
| Cost per Interp   | $0.0001 | ✅     |

---

## Cost Analysis

### Monthly Budget: $5.00

- **LLM Calls:** 47,000+ interpretations/month
- **Cached Calls:** Unlimited (60-70% hit rate expected)
- **KB Searches:** Unlimited (free)
- **Templates:** Unlimited (free)

### Expected Distribution

- 30% LLM (fresh, high-value requests)
- 70% Cache/KB/Template (repeated, standard requests)

### Effective Cost

- **With 68% cache hit rate:** $0.000032 per interpretation
- **Annual budget needed:** ~$60/year for 1.5M interpretations

---

## Integration Examples

### Python Client

```python
import requests

# Generate interpretation
response = requests.post(
    "http://localhost:5000/api/v1/interpretations/hybrid",
    json={
        "chart_data": {
            "sun": "Aries",
            "moon": "Taurus",
            "ascendant": "Gemini"
        },
        "type": "sun",
        "strategy": "auto"
    }
)

interpretation = response.json()
print(f"Quality: {interpretation['quality']}")
print(f"Cost: ${interpretation['cost']:.6f}")
print(interpretation['interpretation'])
```

### JavaScript Client

```javascript
const response = await fetch(
  "http://localhost:5000/api/v1/interpretations/hybrid",
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chart_data: {
        sun: "Aries",
        moon: "Taurus",
        ascendant: "Gemini",
      },
      type: "sun",
      strategy: "auto",
    }),
  }
);

const interpretation = await response.json();
console.log(`Strategy used: ${interpretation.strategy}`);
console.log(interpretation.interpretation);
```

---

## Monitoring Endpoints

Check system health regularly:

```bash
# Health check
curl http://localhost:5000/api/v1/perplexity/health

# Budget status
curl http://localhost:5000/api/v1/perplexity/budget

# Cache performance
curl http://localhost:5000/api/v1/perplexity/cache-stats
```

---

## Best Practices

1. **Always use `auto` strategy** in production
2. **Monitor cache hit rate** (target: 60-70%)
3. **Check budget daily** during initial rollout
4. **Log all interpretation requests** for analysis
5. **A/B test quality** across strategies
6. **Index KB regularly** (weekly recommended)
7. **Clear cache monthly** for fresh interpretations

---

## Support

For issues or questions:

- Check TROUBLESHOOTING_GUIDE.md
- Review COST_ANALYSIS_REPORT.md
- Check logs: `backend/logs/phase5.log`
- Monitor metrics dashboard
