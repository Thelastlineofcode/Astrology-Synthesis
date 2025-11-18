# Personal Development Insights Tool

A flexible B2B personal development platform using numerology and astrology for coaching, team building, and wellness programs.

## Critical Legal Positioning

**⚠️ COMPLIANCE NOTICE**

This tool is designed EXCLUSIVELY for:
- Personal development coaching
- Team building activities
- Wellness program integration
- Self-awareness exercises
- Communication style mapping

This tool is **NOT** intended for and must **NOT** be used for:
- Hiring decisions
- Promotion decisions
- Performance evaluation
- Employee assessment
- Compensation decisions
- Any employment-related decisions

Misuse for employment decisions may violate employment discrimination laws (Title VII, EEOC guidelines).

## The Pain Point: HR-Compliant Astrology/Numerology

### Market Problem

Corporate HR departments are interested in personality insights tools but face legal constraints:
- Myers-Briggs, DISC → Used in hiring (legal gray area)
- Astrology/Numerology → More "mystical," potentially safer legally
- **BUT**: Still risky if positioned as "assessment" or used in employment decisions

### Our Solution: Strategic Positioning

We **explicitly disclaim** use for employment decisions and position as:

1. **Personal Development Tool** - For self-awareness and growth
2. **Coaching Facilitator** - Conversation starter for coaching relationships
3. **Team Building** - Understanding communication styles and strengths
4. **Wellness Integration** - Part of holistic employee wellness programs

### Key Differentiator: Flexible Input

**Works with ANY level of birth information:**

| Data Level | What You Need | What You Get |
|------------|---------------|--------------|
| **Minimal** | Just birth date | Life path number, day of week insights, basic strengths |
| **Basic** | Date + name | Full numerology (destiny, soul urge, personality) |
| **Enhanced** | Date + time | Numerology + sun sign interpretation |
| **Complete** | Date + time + location | Full numerology + complete astrological chart |

**This is unique**: Most astrology tools require full birth data. We provide value at **every level**, making it viable for B2B where employees may not want to share complete birth info.

## Architecture

```
Personal Development System
├── Calculation Engines
│   ├── numerology_engine.py
│   │   ├── Life path calculation
│   │   ├── Destiny/soul urge/personality numbers
│   │   └── Day of week insights
│   ├── personal_development_engine.py
│   │   ├── FlexibleBirthData (adaptive input)
│   │   ├── PersonalDevelopmentReading (output)
│   │   └── FlexibleInsightsEngine (orchestrator)
│   └── team_dynamics_engine.py
│       ├── Team compatibility scoring
│       ├── Communication matrix
│       └── Pairwise synergy analysis
├── AI Agents
│   ├── personal_development_agent.py
│   │   ├── LangChain ReAct agent
│   │   ├── Coaching conversation support
│   │   └── Budget-aware LLM usage
│   └── personal_development_tools.py
│       └── LangChain tools for numerology/astrology
└── API Endpoints
    └── api/v1/personal_development.py
        ├── POST /reading (flexible input)
        ├── POST /numerology (quick calc)
        ├── POST /team/analyze (team dynamics)
        └── POST /agent/coaching (AI coaching)
```

## Features

### 1. Flexible Birth Data Input

Works with ANY level of completeness:

```python
from backend.calculations.personal_development_engine import (
    FlexibleBirthData,
    FlexibleInsightsEngine,
)
from datetime import date

# Example 1: Minimal data (date only)
birth_data_minimal = FlexibleBirthData(
    birth_date=date(1990, 6, 15)
)

# Example 2: With name (adds numerology)
birth_data_with_name = FlexibleBirthData(
    birth_date=date(1990, 6, 15),
    full_name="Jane Doe"
)

# Example 3: Complete data (full astrology)
birth_data_complete = FlexibleBirthData(
    birth_date=date(1990, 6, 15),
    birth_time="14:30:00",
    latitude=40.7128,
    longitude=-74.0060,
    timezone="America/New_York",
    full_name="Jane Doe"
)

# Generate reading
engine = FlexibleInsightsEngine()
reading = engine.generate_reading(birth_data_complete)

print(f"Data completeness: {reading.data_completeness.value}")
print(f"Life path: {reading.life_path_number}")
print(f"Available analyses: {reading.available_analyses}")
```

### 2. Numerology Insights (Always Available)

Even with just a birth date, you get:
- **Life Path Number**: Core life purpose and natural tendencies
- **Day of Week**: Planetary influence based on birth day
- **Interpretation**: Work style, strengths, growth areas

```python
from backend.calculations.numerology_engine import NumerologyCalculator
from datetime import date

calc = NumerologyCalculator()

# Calculate
life_path = calc.calculate_life_path_number(date(1990, 6, 15))
interpretation = calc.interpret_life_path_number(life_path)

print(f"Life Path {life_path}: {interpretation}")

# With name, get more numbers
numbers = calc.get_all_numbers(date(1990, 6, 15), "Jane Doe")
# Returns: life_path, destiny, soul_urge, personality
```

### 3. Astrological Insights (When Data Available)

If birth time and location provided:
- **Sun Sign**: Core identity and self-expression
- **Moon Sign**: Emotional style and inner needs
- **Rising Sign**: First impression and approach to life
- **Planetary Positions**: Complete birth chart analysis

### 4. Team Dynamics Analysis

Analyze entire teams for collaboration insights:

```python
from backend.calculations.team_dynamics_engine import TeamDynamicsEngine

engine = TeamDynamicsEngine()

team_members = [
    {
        "id": "alice",
        "name": "Alice",
        "birth_date": "1990-06-15",
        "full_name": "Alice Smith",
        "role": "Product Manager"
    },
    {
        "id": "bob",
        "name": "Bob",
        "birth_date": "1988-03-22",
        "full_name": "Bob Johnson"
    },
    {
        "id": "charlie",
        "name": "Charlie",
        "birth_date": "1992-11-08",
        "full_name": "Charlie Davis"
    }
]

analysis = engine.analyze_team(team_members, team_name="Product Team")

print(f"Overall synergy: {analysis.compatibility_score.overall_synergy}/100")
print(f"Team strengths: {analysis.compatibility_score.team_strengths}")
print(f"Communication tips: {analysis.compatibility_score.communication_tips}")
```

### 5. AI-Powered Coaching (Optional)

LangChain agent for conversational coaching:

```python
from backend.agents.personal_development_agent import PersonalDevelopmentAgent

agent = PersonalDevelopmentAgent(api_key="your-perplexity-key", verbose=True)

# Get personalized coaching
result = agent.get_personal_insights(
    birth_date="1990-06-15",
    full_name="Jane Doe",
    focus_area="leadership development"
)

print(result["analysis"])
print(f"Cost: ${result['cost']:.6f}")
```

## API Usage

### 1. Personal Development Reading (Flexible Input)

**Minimal data (date only):**

```bash
curl -X POST "http://localhost:8000/api/v1/personal-development/reading" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1990-06-15"
  }'
```

**Response:**
```json
{
  "status": "success",
  "data_completeness": "date_only",
  "available_analyses": ["life_path_number", "day_of_week_insights"],
  "life_path_number": 9,
  "life_path_interpretation": "Humanitarian visionary...",
  "day_of_week": "Friday",
  "day_of_week_insights": "Born on Venus' day...",
  "strengths_themes": ["Strong empathy and collaboration skills"],
  "growth_opportunities": ["Setting healthy boundaries"],
  "reflection_prompts": [
    "What patterns in your work style resonate with your numerological insights?"
  ],
  "disclaimer": "This reading is for personal development and self-reflection purposes only..."
}
```

**With name (full numerology):**

```bash
curl -X POST "http://localhost:8000/api/v1/personal-development/reading" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1990-06-15",
    "full_name": "Jane Doe"
  }'
```

**Complete data (full astrology):**

```bash
curl -X POST "http://localhost:8000/api/v1/personal-development/reading" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1990-06-15",
    "birth_time": "14:30:00",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timezone": "America/New_York",
    "full_name": "Jane Doe",
    "include_coaching_prompts": true
  }'
```

### 2. Quick Numerology (Fastest)

```bash
curl -X POST "http://localhost:8000/api/v1/personal-development/numerology" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1990-06-15",
    "full_name": "Jane Doe"
  }'
```

**Response:**
```json
{
  "status": "success",
  "numbers": {
    "life_path": 9,
    "destiny": 7,
    "soul_urge": 5,
    "personality": 2
  },
  "interpretations": {
    "life_path": "Humanitarian visionary and integrator...",
    "destiny": "Destined to analyze, understand, and seek truth...",
    "soul_urge": "Deep desire for freedom, variety, and adventure...",
    "personality": "Appears gentle, diplomatic, and sensitive..."
  }
}
```

### 3. Team Dynamics Analysis

```bash
curl -X POST "http://localhost:8000/api/v1/personal-development/team/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "team_name": "Product Team",
    "team_members": [
      {"birth_date": "1990-06-15", "full_name": "Alice", "role": "PM"},
      {"birth_date": "1988-03-22", "full_name": "Bob", "role": "Engineer"},
      {"birth_date": "1992-11-08", "full_name": "Charlie", "role": "Designer"}
    ],
    "include_pairwise_analysis": true
  }'
```

**Response:**
```json
{
  "status": "success",
  "team_name": "Product Team",
  "member_count": 3,
  "overall_synergy": 78.5,
  "communication_compatibility": 82.3,
  "strengths_diversity": 75.0,
  "team_strengths": [
    "Excellent team collaboration and empathy",
    "Strong creative and innovative capacity"
  ],
  "growth_areas": [
    "Strengthening processes and organizational structure"
  ],
  "communication_tips": [
    "Create space for different communication styles",
    "Balance between decisive leadership and collaborative consensus-building"
  ],
  "life_path_distribution": {
    "1": 1,
    "6": 1,
    "9": 1
  },
  "top_synergies": [
    {"person1": "Alice", "person2": "Bob", "synergy_score": 85.0},
    {"person1": "Bob", "person2": "Charlie", "synergy_score": 80.0}
  ],
  "team_coaching_prompts": [
    "How do your individual strengths complement each other on this team?",
    "What communication patterns have you noticed in team interactions?"
  ]
}
```

### 4. AI Coaching Session

```bash
curl -X POST "http://localhost:8000/api/v1/personal-development/agent/coaching" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1990-06-15",
    "full_name": "Jane Doe",
    "coaching_query": "How can I develop stronger leadership skills while honoring my natural communication style?"
  }'
```

**Response:**
```json
{
  "status": "success",
  "coaching_insights": "Based on your Life Path 9 energy...",
  "cost": 0.000234,
  "model": "sonar-small",
  "disclaimer": "This coaching insight is for personal development...",
  "compliance_notice": "IMPORTANT: This tool is for personal development..."
}
```

## Life Path Number Interpretations

| Number | Archetype | Strengths | Communication Style |
|--------|-----------|-----------|---------------------|
| **1** | Leader & Pioneer | Independent thinking, courage | Direct & decisive |
| **2** | Diplomat & Mediator | Empathy, collaboration | Gentle & receptive |
| **3** | Creative Communicator | Self-expression, optimism | Expressive & entertaining |
| **4** | Builder & Organizer | Reliability, structure | Systematic & practical |
| **5** | Change Agent | Versatility, adaptability | Dynamic & persuasive |
| **6** | Nurturer & Teacher | Responsibility, service | Warm & supportive |
| **7** | Analyst & Seeker | Wisdom, depth | Reserved & thoughtful |
| **8** | Executive & Manifestor | Leadership, ambition | Authoritative & confident |
| **9** | Humanitarian & Integrator | Compassion, inclusivity | Empathetic & inspiring |
| **11** | Intuitive Visionary (Master) | Inspiration, sensitivity | Charismatic & uplifting |
| **22** | Master Builder (Master) | Practical vision | Grounded & ambitious |
| **33** | Master Teacher (Master) | Healing, compassion | Loving & mentoring |

## Use Cases

### 1. Corporate Wellness Programs

**Integration Example:**

```python
# Wellness platform integration
def onboard_wellness_participant(employee_id, birth_date, consent=True):
    """
    Onboard employee to wellness program.

    NOTE: Requires explicit consent, data encrypted,
    results only visible to employee unless they choose to share.
    """
    if not consent:
        return {"error": "Consent required"}

    # Generate reading
    reading = get_personal_reading(birth_date)

    # Store encrypted
    store_encrypted_reading(employee_id, reading)

    # Employee-only access
    return {
        "success": True,
        "message": "Your personal development insights are ready!",
        "view_url": f"/wellness/insights/{employee_id}"
    }
```

### 2. Team Building Workshops

**Workshop Activity:**

1. **Pre-workshop**: Each team member gets their personal reading (optional, consent-based)
2. **Workshop**: Facilitator presents team dynamics analysis
3. **Activity**: Team discusses communication styles and strengths
4. **Outcome**: Increased understanding and trust

**Sample Workshop Agenda:**

```
Team Building Workshop: Understanding Team Dynamics
(2 hours)

1. Introduction (15 min)
   - Purpose: Build trust, not assess
   - Privacy: Participation optional
   - Framework: Numerology/astrology basics

2. Individual Reflection (20 min)
   - Review personal reading
   - Identify 2-3 key insights
   - Note: What resonates?

3. Team Sharing Circle (45 min)
   - Volunteers share insights
   - Discuss communication styles
   - Identify complementary strengths

4. Team Dynamics Review (30 min)
   - Present team compatibility analysis
   - Discuss synergies and growth areas
   - Collaboration opportunities

5. Action Planning (10 min)
   - How to leverage insights
   - Communication agreements
   - Follow-up activities
```

### 3. Executive Coaching

**Coaching Session Flow:**

```python
# Session 1: Discovery
coach_session_1 = agent.get_personal_insights(
    birth_date=client_birth_date,
    full_name=client_name,
    focus_area="leadership development"
)

# Session 2: Specific challenge
coach_session_2 = agent.get_coaching_session(
    reading_id=client_reading_id,
    specific_question="How can I delegate more effectively?"
)

# Session 3: Team dynamics
coach_session_3 = agent.get_team_insights(
    team_data=client_team,
    team_name=client_team_name
)
```

### 4. Communication Training

**Training Module: "Understanding Communication Styles"**

```python
def generate_communication_training_materials(team_data):
    """
    Generate training materials based on team composition.
    """
    analysis = team_engine.analyze_team(team_data)

    # Identify communication style distribution
    styles = analysis.communication_matrix

    # Generate custom exercises
    exercises = []

    # If team has mix of direct and empathetic communicators
    if has_style_diversity(styles, ["Direct & Expressive", "Empathetic & Relational"]):
        exercises.append({
            "title": "Bridge Building Exercise",
            "description": "Practice translating between direct and empathetic styles",
            "duration": "20 minutes"
        })

    return {
        "team_composition": styles,
        "training_modules": exercises,
        "communication_tips": analysis.compatibility_score.communication_tips
    }
```

## Privacy and Compliance

### Privacy-First Design

1. **Explicit Consent Required**
   ```python
   # Consent must be opt-in, not opt-out
   if not user_consent:
       return {"error": "Explicit consent required"}
   ```

2. **End-to-End Encryption**
   ```python
   # All birth data and readings encrypted at rest
   encrypted_data = encrypt(birth_data, user_key)
   store(encrypted_data)
   ```

3. **User-Controlled Access**
   ```python
   # Employee controls who sees their reading
   def share_reading(employee_id, recipient_id, reading_id):
       # Requires employee approval
       if not employee_approves_sharing(employee_id, recipient_id):
           return {"error": "Sharing not authorized"}

       share_with(recipient_id, reading_id)
   ```

4. **No HRIS Integration by Default**
   - Readings stored separately from HR systems
   - No automatic sync with employee records
   - No linkage to performance reviews

### Legal Compliance Checklist

- [ ] **Explicit positioning** as coaching tool, not assessment
- [ ] **Disclaimers** on every page/API response
- [ ] **Consent forms** for data collection
- [ ] **Privacy policy** specifically for this tool
- [ ] **Opt-in only** - never mandatory
- [ ] **Employee-controlled** sharing
- [ ] **Separate from HR** systems
- [ ] **Documentation** of intended use
- [ ] **Training** for facilitators on compliance
- [ ] **Regular audits** to prevent misuse

## Deployment

### Environment Variables

```bash
# Required for AI agent
export PERPLEXITY_API_KEY=your_key_here

# Optional
export PD_ENABLE_AI_COACHING=true
export PD_MONTHLY_BUDGET=5.0
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY backend/ ./backend/

# Expose port
EXPOSE 8000

# Run
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run
docker build -t personal-development-api .
docker run -p 8000:8000 \
  -e PERPLEXITY_API_KEY=your_key \
  personal-development-api
```

### As Standalone Service

```python
# main.py
from fastapi import FastAPI
from backend.api.v1.personal_development import router

app = FastAPI(
    title="Personal Development Insights API",
    description="Coaching and wellness tool using numerology and astrology",
    version="1.0.0"
)

# Add compliance notice to docs
app.add_api_route("/", lambda: {
    "message": "Personal Development Insights API",
    "compliance": "Coaching tool only - NOT for employment decisions"
})

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Performance

### Response Times

| Endpoint | Data Level | Avg Time | Notes |
|----------|-----------|----------|-------|
| `/numerology` | Date only | ~10ms | Fastest |
| `/reading` | Date only | ~20ms | Numerology + synthesis |
| `/reading` | Full data | ~100ms | Includes birth chart calculation |
| `/team/analyze` | 5 members | ~150ms | Team-wide analysis |
| `/agent/coaching` | Any | ~2-3s | LLM call |

### Caching

```python
# Calculations are cached
from functools import lru_cache

@lru_cache(maxsize=256)
def calculate_life_path_number(birth_date):
    # Cached for repeated queries
    pass
```

## Testing

```bash
# Run tests
pytest backend/tests/test_personal_development.py
pytest backend/tests/test_numerology.py
pytest backend/tests/test_team_dynamics.py

# Test specific functionality
pytest backend/tests/test_personal_development.py::test_flexible_input
pytest backend/tests/test_personal_development.py::test_minimal_data
pytest backend/tests/test_personal_development.py::test_team_analysis
```

## Sales Positioning

### Elevator Pitch

> "Personal development insights platform that works with ANY level of birth information. Unlike traditional astrology tools requiring complete data, we provide valuable numerology insights with just a birth date—perfect for B2B wellness programs where privacy matters. Explicitly positioned as a coaching facilitator, not an assessment tool, to stay compliant with employment law."

### Key Differentiators

1. **Flexible Input** - Works with date-only (unique in market)
2. **Legal Positioning** - Explicitly NOT for employment decisions
3. **Privacy-First** - User consent, encrypted, employee-controlled
4. **Multi-Modal** - Numerology + astrology + AI coaching
5. **Team Insights** - Not just individual, but team dynamics
6. **B2B Ready** - API-first, enterprise privacy, compliance docs

### Target Markets

1. **Corporate Wellness Platforms** - Integrate as wellness module
2. **Executive Coaching Firms** - Tool for coaches
3. **HR Tech (Carefully)** - Team building, NOT hiring
4. **Learning & Development** - Communication training
5. **Retreat Centers** - Team offsite activities

### Pricing Strategy

**Tiered based on features:**

- **Basic**: $99/month - Numerology only, up to 50 users
- **Professional**: $299/month - Numerology + astrology, up to 200 users
- **Enterprise**: $999/month - AI coaching, unlimited users, team dynamics
- **White-Label**: Custom - Full platform integration

## Roadmap

- [ ] Mobile app for easier data input
- [ ] Slack/Teams bot integration
- [ ] Vedic astrology option (for Indian market)
- [ ] Career path recommendations (carefully positioned)
- [ ] Compatibility for project team formation
- [ ] Multi-language support
- [ ] Anonymous team analysis (no PII required)
- [ ] Integration with popular wellness platforms

## Contributing

To extend the personal development tool:

1. Add new numerology interpretations in `numerology_engine.py`
2. Create custom tools in `personal_development_tools.py`
3. Extend the agent in `personal_development_agent.py`
4. Add API endpoints in `api/v1/personal_development.py`

## License

Part of the Mula astrological calculation engine.

## Credits

Built on:
- Swiss Ephemeris (planetary calculations)
- LangChain (AI agents)
- FastAPI (web framework)
- Pythagorean numerology (traditional system)

---

**COMPLIANCE REMINDER**: This tool is for personal development, coaching, and wellness purposes ONLY. It is NOT intended for hiring, promotion, performance evaluation, or any employment decisions.
