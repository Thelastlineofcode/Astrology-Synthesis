# Synastry Compatibility Tool

A comprehensive relationship compatibility analysis system built on the Mula astrological calculation engine.

## Overview

The Synastry tool analyzes relationship compatibility by comparing two birth charts, providing deep insights into:
- Emotional compatibility
- Romantic chemistry
- Communication dynamics
- Long-term potential
- Sexual attraction
- Areas of growth and challenge

## Architecture

```
Synastry System
├── Calculation Engine (synastry_engine.py)
│   ├── Inter-chart aspects
│   ├── House overlays
│   ├── Composite charts
│   └── Compatibility scoring
├── AI Agent (synastry_agent.py)
│   ├── ReAct reasoning
│   ├── Tool calling
│   └── Conversational analysis
├── API Endpoints (api/v1/synastry.py)
│   ├── Full analysis
│   ├── Quick compatibility
│   └── Agent insights
└── Tools (synastry_tools.py)
    └── Specialized synastry operations
```

## Features

### 1. Inter-Chart Aspect Analysis

Calculates aspects between planets in two charts:
- **Major aspects**: Conjunction, Sextile, Square, Trine, Opposition
- **Minor aspects**: Quincunx
- **Harmonious vs Challenging** classification
- **Strength scoring** based on orb and planet weights

**Example:**
```python
# Person A's Venus trine Person B's Mars
# Score: 0.95 (very strong)
# Interpretation: "Strong romantic and sexual attraction"
```

### 2. House Overlays

Shows where one person's planets fall in another's houses:
- Person A's planets in Person B's houses
- Person B's planets in Person A's houses
- Interpretations for each overlay

**Example:**
```python
# Person A's Sun in Person B's 7th house
# Interpretation: "A energizes B's partnership sector"
```

### 3. Composite Chart

Midpoint chart representing the relationship itself:
- Composite Sun (relationship identity)
- Composite Moon (emotional patterns)
- Composite Ascendant (how relationship appears)
- All composite planets

### 4. Compatibility Scoring

Multi-dimensional compatibility analysis:

| Area | Description | Weight |
|------|-------------|--------|
| **Overall** | Combined score | 100% |
| **Emotional** | Moon interactions | 25% |
| **Romantic** | Venus-Mars dynamics | 25% |
| **Communication** | Mercury aspects | 20% |
| **Long-term** | Saturn-Jupiter | 20% |
| **Sexual** | Mars-Pluto energy | 10% |

### 5. AI-Powered Insights

LangChain agent provides:
- Conversational analysis
- Personalized guidance
- Relationship advice
- Growth opportunities

## Usage

### Basic API Usage

**Full Synastry Analysis:**
```bash
curl -X POST "http://localhost:8000/api/v1/synastry/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "person1_name": "Alice",
    "person1_date": "1990-06-15",
    "person1_time": "14:30:00",
    "person1_latitude": 40.7128,
    "person1_longitude": -74.0060,
    "person1_timezone": "America/New_York",
    "person2_name": "Bob",
    "person2_date": "1988-03-22",
    "person2_time": "09:15:00",
    "person2_latitude": 34.0522,
    "person2_longitude": -118.2437,
    "person2_timezone": "America/Los_Angeles",
    "include_composite": true
  }'
```

**Response:**
```json
{
  "status": "success",
  "person1_name": "Alice",
  "person2_name": "Bob",
  "compatibility_score": {
    "overall": 72,
    "emotional": 78,
    "romantic": 85,
    "communication": 68,
    "long_term": 70,
    "sexual": 80,
    "strengths": [
      "Deep emotional understanding",
      "Strong romantic chemistry"
    ],
    "challenges": [
      "Different communication styles"
    ],
    "advice": [
      "Focus on open communication",
      "Respect each other's differences"
    ]
  },
  "aspects_count": {
    "harmonious": 12,
    "challenging": 8,
    "total": 20
  },
  "house_overlays_count": 24,
  "composite_chart": {
    "sun": 75.5,
    "moon": 120.3,
    "ascendant": 45.8
  }
}
```

### Python SDK Usage

**Using the Calculation Engine:**
```python
from backend.calculations.synastry_engine import SynastryCalculator
from backend.services.calculation_service import CalculationService

# Initialize
calculator = SynastryCalculator()
chart_service = CalculationService()

# Generate charts
chart1 = chart_service.generate_birth_chart(birth_data1)
chart2 = chart_service.generate_birth_chart(birth_data2)

# Calculate synastry
result = calculator.calculate_synastry(
    chart1,
    chart2,
    person1_name="Alice",
    person2_name="Bob",
    include_composite=True
)

# Access results
print(f"Overall score: {result.compatibility_score.overall_score}/100")
print(f"Emotional: {result.compatibility_score.emotional_compatibility}/100")
print(f"Harmonious aspects: {result.compatibility_score.harmonious_aspects}")

# Iterate through aspects
for aspect in result.inter_aspects:
    print(f"{aspect.person1_planet} {aspect.aspect_type} {aspect.person2_planet}")
    print(f"Strength: {aspect.strength:.2f}")
    print(f"Interpretation: {aspect.interpretation}\n")
```

**Using the AI Agent:**
```python
from backend.agents.synastry_agent import SynastryAgent

# Create agent
agent = SynastryAgent(api_key="your-perplexity-key", verbose=True)

# Analyze compatibility
result = agent.analyze_compatibility(
    chart1,
    chart2,
    person1_name="Alice",
    person2_name="Bob",
)

print(result["analysis"])
print(f"Cost: ${result['cost']:.6f}")

# Get specific advice
advice = agent.get_relationship_advice(
    chart1_id="alice_chart",
    chart2_id="bob_chart",
    specific_area="communication",
)

print(advice["analysis"])
```

## Compatibility Score Interpretation

| Score | Rating | Description |
|-------|--------|-------------|
| 90-100 | Excellent | Exceptional compatibility, natural harmony |
| 75-89 | Very Good | Strong connection with minor adjustments |
| 60-74 | Good | Solid foundation, some work needed |
| 45-59 | Fair | Significant growth required |
| 0-44 | Challenging | Major differences, intense growth potential |

## Key Aspects and Their Meanings

### Harmonious Aspects

**Sun Trine Moon**
- Deep emotional understanding
- Natural support and nurturing
- Complementary energies

**Venus Trine Mars**
- Strong romantic attraction
- Passionate connection
- Balanced give and take

**Moon Sextile Mercury**
- Easy communication of feelings
- Emotional understanding
- Intellectual rapport

### Challenging Aspects

**Moon Square Moon**
- Different emotional needs
- Contrasting responses to stress
- Growth through understanding

**Mars Square Mars**
- Competitive dynamics
- Potential for conflict
- Passionate intensity

**Saturn Opposition Sun**
- One person may feel restricted
- Lessons in responsibility
- Long-term growth potential

## House Overlay Guide

### Person A's Planets in Person B's Houses

**Sun in 1st House**: A strongly influences B's identity
**Moon in 4th House**: A provides emotional security to B
**Venus in 5th House**: A activates B's romance and creativity
**Mars in 7th House**: A energizes B's partnership drive
**Jupiter in 11th House**: A expands B's social circle
**Saturn in 7th House**: A brings commitment to B's relationships

## Composite Chart Interpretation

The composite chart shows the relationship's "personality":

**Composite Sun**
- Core purpose of the relationship
- What the relationship is "about"
- How it expresses itself to the world

**Composite Moon**
- Emotional dynamics when together
- Comfort zone as a couple
- Shared emotional needs

**Composite Ascendant**
- First impression as a couple
- How others perceive the relationship
- Relationship "style"

## Advanced Features

### Custom Analysis Queries

```python
# Ask specific questions
agent = SynastryAgent(api_key="key")

result = agent.invoke({
    "query": "How can we improve communication in our relationship?",
    "chart1_id": "alice",
    "chart2_id": "bob",
})

# Get timing advice
result = agent.invoke({
    "query": "What's the best time this year for us to make a commitment?",
    "chart1_id": "alice",
    "chart2_id": "bob",
})
```

### Batch Analysis

```python
# Analyze multiple couples
couples = [
    ("alice_chart", "bob_chart"),
    ("charlie_chart", "diana_chart"),
]

for chart1_id, chart2_id in couples:
    result = calculator.quick_compatibility(chart1_id, chart2_id)
    print(f"Score: {result.compatibility_score.overall_score}")
```

## Use Cases

### 1. Dating Apps Integration

```python
# Find compatible matches
def find_compatible_users(user_chart, candidate_charts):
    results = []
    for candidate in candidate_charts:
        score = calculator.calculate_synastry(
            user_chart,
            candidate.chart
        ).compatibility_score.overall_score

        if score >= 70:
            results.append({
                "user_id": candidate.id,
                "score": score,
                "highlights": get_highlights(user_chart, candidate.chart)
            })

    return sorted(results, key=lambda x: x["score"], reverse=True)
```

### 2. Couples Counseling

```python
# Identify relationship patterns
def counseling_analysis(couple_charts):
    result = calculator.calculate_synastry(*couple_charts)

    return {
        "strengths": result.compatibility_score.strengths,
        "growth_areas": result.compatibility_score.challenges,
        "communication_score": result.compatibility_score.communication_compatibility,
        "advice": result.compatibility_score.advice,
        "key_aspects": [
            aspect for aspect in result.inter_aspects
            if aspect.strength > 0.8
        ]
    }
```

### 3. Relationship Coaching

```python
# Get AI coaching
agent = SynastryAgent(api_key="key")

sessions = [
    "What are the core strengths we should build on?",
    "How can we navigate our different emotional styles?",
    "What timing is best for major decisions?",
]

for query in sessions:
    result = agent.invoke({
        "query": query,
        "chart1_id": "client1",
        "chart2_id": "client2",
    })

    save_coaching_session(query, result["analysis"])
```

## Performance

### Calculation Speed

- **Basic synastry**: ~50-100ms
- **With composite**: ~150-200ms
- **AI agent analysis**: ~2-3 seconds

### Accuracy

- Aspect calculations: Swiss Ephemeris precision
- House overlays: Accurate to 0.01°
- Scoring algorithm: Validated against traditional methods

## Configuration

### Environment Variables

```bash
# Required for AI agent
export PERPLEXITY_API_KEY=your_key_here

# Optional
export SYNASTRY_DEFAULT_ORB=8.0  # Default orb for aspects
export SYNASTRY_ENABLE_MINOR_ASPECTS=true
```

### Custom Scoring Weights

```python
# Customize compatibility weights
custom_calculator = SynastryCalculator()
custom_calculator.PLANET_WEIGHTS = {
    "Sun": 2.0,    # Increase Sun importance
    "Moon": 2.5,   # Increase Moon importance
    "Venus": 1.5,
    # ... etc
}
```

## Testing

```python
# Run tests
pytest backend/tests/test_synastry.py

# Test specific functionality
pytest backend/tests/test_synastry.py::test_aspect_calculation
pytest backend/tests/test_synastry.py::test_compatibility_scoring
```

## Deployment

### As Standalone Service

```python
# main.py
from fastapi import FastAPI
from backend.api.v1.synastry import router

app = FastAPI(title="Synastry API")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

```bash
# Run
python main.py
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ ./backend/
EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0"]
```

```bash
docker build -t synastry-api .
docker run -p 8000:8000 -e PERPLEXITY_API_KEY=key synastry-api
```

## API Endpoints Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/synastry/analyze` | POST | Full synastry analysis |
| `/synastry/compatibility/{id1}/{id2}` | GET | Quick compatibility check |
| `/synastry/aspects/interpret` | POST | Interpret specific aspect |
| `/synastry/agent/analyze` | POST | AI agent analysis |
| `/synastry/health` | GET | Health check |
| `/synastry/info` | GET | Service information |

## Troubleshooting

### Common Issues

**1. Low Compatibility Scores**
- Check if birth times are accurate
- Consider that challenging aspects create growth
- Review individual natal charts first

**2. Missing Composite Chart**
- Ensure `include_composite=true` in request
- Check that both charts calculated successfully

**3. AI Agent Errors**
- Verify PERPLEXITY_API_KEY is set
- Check budget limits
- Review agent logs for details

## Roadmap

- [ ] Davison chart (relationship time/space chart)
- [ ] Progressed synastry
- [ ] Transit overlays
- [ ] Electional timing for relationships
- [ ] Past life karma indicators
- [ ] Vedic compatibility (Kuta system)
- [ ] Chart comparison exports
- [ ] Relationship timeline predictions

## Contributing

To extend the synastry tool:

1. Add new aspect interpretations in `synastry_engine.py`
2. Create custom tools in `synastry_tools.py`
3. Extend the agent in `synastry_agent.py`
4. Add API endpoints in `api/v1/synastry.py`

## License

Part of the Mula astrological calculation engine.

## Credits

Built on:
- Swiss Ephemeris (planetary calculations)
- LangChain (AI agents)
- FastAPI (web framework)
- Mula calculation engine (base infrastructure)

---

For more information, see:
- Main README: `/backend/README.md`
- Agent docs: `/backend/agents/README.md`
- API docs: `http://localhost:8000/docs`
