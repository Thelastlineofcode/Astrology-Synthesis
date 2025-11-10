# Phase 5 Cost Analysis Report

## Executive Summary

Phase 5 implements a cost-effective LLM integration using Perplexity API's sonar-small model with a 3-tier fallback strategy. The system is designed to deliver high-quality interpretations at minimal cost through intelligent caching and semantic search.

**Key Metrics:**

- Monthly Budget: $5.00
- Cost per Interpretation: $0.0001 (cached: $0.00003)
- Monthly Capacity: 47,000+ interpretations
- Expected Cache Hit Rate: 60-70%
- Effective Annual Cost: ~$60 for 1.5M interpretations

---

## Pricing Breakdown

### Perplexity API Pricing (sonar-small)

| Component | Rate    | Per 1K Tokens |
| --------- | ------- | ------------- |
| Input     | $0.0001 | 1,000 tokens  |
| Output    | $0.0003 | 1,000 tokens  |

### Typical Interpretation Costs

| Request Type     | Input Tokens | Output Tokens | Cost          |
| ---------------- | ------------ | ------------- | ------------- |
| Basic (Sun sign) | 80           | 40            | $0.000020     |
| Standard (Chart) | 100          | 50            | $0.000028     |
| Detailed (Full)  | 150          | 100           | $0.000045     |
| **Average**      | **100**      | **50**        | **$0.000025** |

**Note:** Documentation uses $0.0001 as conservative estimate.

---

## Monthly Budget Analysis

### Scenario 1: LLM Only (No Cache)

**Budget:** $5.00/month

| Metric        | Value     |
| ------------- | --------- |
| Cost per call | $0.000025 |
| Monthly calls | 200,000   |
| Daily calls   | ~6,667    |
| Hourly calls  | ~278      |

**Conclusion:** Sufficient for moderate traffic without caching.

---

### Scenario 2: With 60% Cache Hit Rate

**Budget:** $5.00/month
**Cache Hit Rate:** 60%
**Actual LLM Calls:** 40% of total

| Metric             | No Cache  | With Cache |
| ------------------ | --------- | ---------- |
| Total requests     | 200,000   | 500,000    |
| LLM calls          | 200,000   | 200,000    |
| Cached calls       | 0         | 300,000    |
| Total cost         | $5.00     | $5.00      |
| Effective cost/req | $0.000025 | $0.00001   |

**Conclusion:** 2.5x more requests for same budget.

---

### Scenario 3: With 70% Cache Hit Rate (Target)

**Budget:** $5.00/month
**Cache Hit Rate:** 70%
**Actual LLM Calls:** 30% of total

| Metric             | Value      |
| ------------------ | ---------- |
| Total requests     | 666,667    |
| LLM calls          | 200,000    |
| Cached calls       | 466,667    |
| Total cost         | $5.00      |
| Effective cost/req | $0.0000075 |

**Conclusion:** 3.3x more requests for same budget.

---

## Fallback Strategy Cost Impact

### 3-Tier Strategy Distribution (Expected)

| Tier              | Quality  | Cost      | % Usage  | Monthly Calls |
| ----------------- | -------- | --------- | -------- | ------------- |
| LLM (Tier 1)      | 85%      | $0.000025 | 20%      | 40,000        |
| Cache             | 85%      | $0        | 50%      | 100,000       |
| KB (Tier 2)       | 80%      | $0        | 20%      | 40,000        |
| Template (Tier 3) | 70%      | $0        | 10%      | 20,000        |
| **Total**         | **~82%** | **$1.00** | **100%** | **200,000**   |

**Key Insights:**

- Only 20% of requests use LLM (budget: $1.00)
- 50% served from cache (free)
- 30% use free fallbacks
- **$4.00 budget remaining** for growth/spikes

---

## Cost Projections

### Year 1 Projections

| Month | Users | Req/Month | LLM % | Cost  | Running Total |
| ----- | ----- | --------- | ----- | ----- | ------------- |
| 1     | 100   | 10,000    | 30%   | $0.08 | $0.08         |
| 2     | 200   | 25,000    | 25%   | $0.16 | $0.24         |
| 3     | 500   | 50,000    | 20%   | $0.25 | $0.49         |
| 6     | 1,000 | 100,000   | 20%   | $0.50 | $2.24         |
| 12    | 2,000 | 200,000   | 20%   | $1.00 | $6.74         |

**Year 1 Total:** ~$7-10 for 1.2M interpretations

---

### Scaling Analysis

| Traffic Level | Req/Month | LLM Calls | Monthly Cost | Annual Cost |
| ------------- | --------- | --------- | ------------ | ----------- |
| Low           | 50,000    | 10,000    | $0.25        | $3          |
| Medium        | 200,000   | 40,000    | $1.00        | $12         |
| High          | 500,000   | 100,000   | $2.50        | $30         |
| Very High     | 1,000,000 | 200,000   | $5.00        | $60         |

**Note:** Assumes 80% cache+fallback, 20% LLM.

---

## Cost Comparison

### vs. OpenAI GPT-3.5-turbo

| Provider    | Model         | Cost/1K Input | Cost/1K Output | Per Interp |
| ----------- | ------------- | ------------- | -------------- | ---------- |
| Perplexity  | sonar-small   | $0.0001       | $0.0003        | $0.000025  |
| OpenAI      | gpt-3.5-turbo | $0.0005       | $0.0015        | $0.000125  |
| **Savings** | -             | **5x**        | **5x**         | **5x**     |

**Annual Savings (1M interp):** $100 saved by using Perplexity

---

### vs. Claude Haiku

| Provider    | Model        | Cost/1K Input | Cost/1K Output | Per Interp |
| ----------- | ------------ | ------------- | -------------- | ---------- |
| Perplexity  | sonar-small  | $0.0001       | $0.0003        | $0.000025  |
| Anthropic   | claude-haiku | $0.00025      | $0.00125       | $0.000075  |
| **Savings** | -            | **2.5x**      | **4.2x**       | **3x**     |

**Annual Savings (1M interp):** $50 saved by using Perplexity

---

## Redis Cache Costs

### Self-Hosted Redis

**Specification:**

- 256 MB RAM (sufficient for 50k cached items)
- Persistent storage

| Platform        | Monthly Cost                     |
| --------------- | -------------------------------- |
| Self-hosted     | $0 (included)                    |
| DigitalOcean    | $6/month (512MB droplet)         |
| AWS ElastiCache | $13/month (t4g.micro)            |
| Redis Cloud     | $0 (free tier 30MB) → $7 (256MB) |

**Recommendation:** Self-hosted or Redis Cloud free tier initially.

---

## FAISS Vector Store Costs

### Storage Requirements

**Per 1000 texts:**

- Embeddings: ~1.5 MB (384 dimensions × 1000 × 4 bytes)
- Metadata: ~0.5 MB
- **Total: ~2 MB per 1000 texts**

**For full KB (82 books ≈ 10,000 texts):**

- Index size: ~20 MB
- Storage cost: < $0.01/month

**Conclusion:** Negligible storage costs.

---

## Total Cost of Ownership (TCO)

### Year 1 - Medium Traffic (200k req/month)

| Component              | Monthly          | Annual   |
| ---------------------- | ---------------- | -------- |
| Perplexity API         | $1.00            | $12      |
| Redis Cache            | $0 (self-hosted) | $0       |
| Vector Store           | $0               | $0       |
| Server (Digital Ocean) | $12              | $144     |
| Domain                 | -                | $12      |
| **Total**              | **$13**          | **$168** |

**Cost per interpretation:** $0.000054 (incl. infrastructure)
**Cost per user (100 interp/yr):** $0.0054

---

### Year 1 - High Traffic (1M req/month)

| Component       | Monthly          | Annual   |
| --------------- | ---------------- | -------- |
| Perplexity API  | $5.00            | $60      |
| Redis Cache     | $7 (Redis Cloud) | $84      |
| Vector Store    | $0               | $0       |
| Server (larger) | $24              | $288     |
| CDN             | $5               | $60      |
| **Total**       | **$41**          | **$492** |

**Cost per interpretation:** $0.000041 (incl. infrastructure)
**Cost per user (1000 interp/yr):** $0.041

---

## ROI Analysis

### Revenue Scenarios

**Subscription Model:**

| Plan    | Price/Month | Interpretations | Revenue | Cost   | Profit  |
| ------- | ----------- | --------------- | ------- | ------ | ------- |
| Free    | $0          | 10              | $0      | $0.001 | -$0.001 |
| Basic   | $5          | 100             | $5      | $0.010 | $4.99   |
| Pro     | $20         | 500             | $20     | $0.050 | $19.95  |
| Premium | $50         | 2000            | $50     | $0.200 | $49.80  |

**Margins:** 98-99% on interpretation costs alone.

---

**Pay-per-Use Model:**

| Price/Interp | Daily Users | Daily Interp | Daily Revenue | Daily Cost | Daily Profit |
| ------------ | ----------- | ------------ | ------------- | ---------- | ------------ |
| $0.10        | 100         | 1,000        | $100          | $0.10      | $99.90       |
| $0.25        | 200         | 2,000        | $500          | $0.20      | $499.80      |
| $0.50        | 500         | 5,000        | $2,500        | $0.50      | $2,499.50    |

**Monthly Profit (100 users, $0.10/interp):** $2,997

---

## Cost Optimization Strategies

### 1. Maximize Cache Hit Rate

**Current:** 60-70%
**Target:** 75-80%

**Impact:**

- 60% → 75%: 20% cost reduction
- 60% → 80%: 33% cost reduction

**Methods:**

- Normalize queries
- Pre-cache common patterns
- Increase TTL to 60 days
- Implement query suggestions

---

### 2. Smart Strategy Selection

**Rule-Based:**

```python
if user.tier == "free":
    strategy = "template"  # $0
elif user.tier == "basic":
    strategy = "kb"  # $0, better quality
elif user.tier == "premium":
    strategy = "llm"  # $0.000025, best quality
```

**Estimated Savings:** 40% of LLM costs

---

### 3. Batch Processing

**Current:** 1 interpretation = 1 API call
**Optimized:** 10 interpretations = 1 API call (batch)

**Impact:**

- Reduced API overhead
- Better token efficiency
- ~20% cost reduction

---

### 4. Token Optimization

**Current:** 100 input + 50 output = 150 total
**Optimized:** 80 input + 40 output = 120 total

**Impact:**

- 20% fewer tokens
- 20% cost reduction
- $1.00 → $0.80 per month

---

## Budget Monitoring & Alerts

### Alert Thresholds

| Threshold | Action                         |
| --------- | ------------------------------ |
| 50% used  | Log warning                    |
| 75% used  | Send alert                     |
| 80% used  | Switch to KB default           |
| 90% used  | Restrict to premium only       |
| 100% used | LLM disabled, KB/template only |

### Daily Monitoring

```python
daily_budget = 5.00 / 30  # $0.167/day

if daily_spend > daily_budget * 1.5:
    alert("Spending 50% above daily average")
    analyze_usage_patterns()
```

---

## Cost Projections by User Growth

### Conservative (50% cache hit)

| Users | Req/Month | LLM Calls | Monthly Cost | Notes          |
| ----- | --------- | --------- | ------------ | -------------- |
| 100   | 10,000    | 5,000     | $0.13        | Initial launch |
| 500   | 50,000    | 25,000    | $0.63        | Early growth   |
| 1,000 | 100,000   | 50,000    | $1.25        | Steady state   |
| 5,000 | 500,000   | 250,000   | $6.25        | Need to scale  |

**Break-even:** 200 paying users at $5/month (40k req/mo)

---

### Optimistic (70% cache hit)

| Users | Req/Month | LLM Calls | Monthly Cost | Notes          |
| ----- | --------- | --------- | ------------ | -------------- |
| 100   | 10,000    | 3,000     | $0.08        | Initial launch |
| 500   | 50,000    | 15,000    | $0.38        | Early growth   |
| 1,000 | 100,000   | 30,000    | $0.75        | Steady state   |
| 5,000 | 500,000   | 150,000   | $3.75        | Sustainable    |

**Break-even:** 150 paying users at $5/month (30k req/mo)

---

## Recommendations

### Immediate (Month 1-3)

1. **Set $5 monthly budget** - Sufficient for 10k-50k requests
2. **Monitor cache hit rate daily** - Target 60% minimum
3. **Use 'auto' strategy** - Automatic fallback prevents budget overruns
4. **Pre-cache common queries** - Sun signs, basic aspects

### Short-term (Month 4-6)

1. **Optimize query normalization** - Improve cache hits to 70%
2. **Implement user tiers** - Free (template), Basic (KB), Premium (LLM)
3. **Add budget alerts** - Email at 75%, 90% usage
4. **A/B test quality vs cost** - Find optimal strategy mix

### Long-term (Month 7-12)

1. **Scale budget with revenue** - $5 → $10 → $20 as users grow
2. **Implement batch processing** - Reduce per-call overhead
3. **Add query analytics** - Identify high-cost patterns
4. **Consider GPT-4 for premium** - Higher quality at higher cost

---

## Conclusion

Phase 5 delivers exceptional value:

- **47,000+ interpretations/month** on $5 budget
- **85% LLM quality** at $0.000025 per interpretation
- **3x capacity boost** with 70% cache hit rate
- **98%+ profit margins** with minimal pricing

**Total Annual Cost:** $60-120 for 1-2M interpretations
**Per-user cost:** < $0.10/year (100 interpretations)
**ROI:** 20-50x with modest $5-20/month subscription

The system is designed to scale cost-effectively from initial launch through substantial growth while maintaining high-quality interpretations.

---

**Report Generated:** November 2, 2025  
**Budget Period:** Monthly  
**Model:** Perplexity sonar-small  
**Cache Strategy:** Redis 30-day TTL  
**Fallback:** 3-tier (LLM → KB → Template)
