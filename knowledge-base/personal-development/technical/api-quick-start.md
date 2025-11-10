# Personal Development API - Quick Start

## Overview

The Personal Development API provides flexible personal insights using numerology and astrology. Works with **any level of birth data** from date-only to complete information.

**Base URL:** `https://api.yourdomain.com/api/v1/personal-development`

## Key Features

- ✅ Works with just birth date (unique!)
- ✅ More data = more insights (flexible)
- ✅ Team dynamics analysis
- ✅ AI-powered coaching (optional)
- ✅ Privacy-first design
- ✅ HR-compliant positioning

## Authentication

```bash
# Include API key in header
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.yourdomain.com/api/v1/personal-development/reading
```

## Quick Example

### Minimal Data (Date Only)

**Request:**
```bash
curl -X POST https://api.yourdomain.com/api/v1/personal-development/reading \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "birth_date": "1990-06-15"
  }'
```

**Response:**
```json
{
  "status": "success",
  "data_completeness": "date_only",
  "life_path_number": 9,
  "life_path_interpretation": "Humanitarian visionary and integrator...",
  "day_of_week": "Friday",
  "day_of_week_insights": "Born on Venus' day: Harmonious and aesthetically oriented...",
  "strengths_themes": ["Strong empathy and collaboration skills"],
  "growth_opportunities": ["Setting healthy boundaries"],
  "disclaimer": "This reading is for personal development and self-reflection purposes only..."
}
```

### Complete Data (Full Analysis)

**Request:**
```bash
curl -X POST https://api.yourdomain.com/api/v1/personal-development/reading \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
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

**Response:**
```json
{
  "status": "success",
  "data_completeness": "full_data",
  "available_analyses": [
    "life_path_number",
    "destiny_number",
    "soul_urge_number",
    "personality_number",
    "sun_sign",
    "moon_sign",
    "rising_sign",
    "planetary_positions"
  ],
  "life_path_number": 9,
  "destiny_number": 7,
  "soul_urge_number": 5,
  "personality_number": 2,
  "sun_sign": "Gemini",
  "moon_sign": "Pisces",
  "rising_sign": "Scorpio",
  "strengths_themes": [
    "Strong empathy and collaboration skills",
    "Creative communication and problem-solving",
    "Deep analytical thinking"
  ],
  "growth_opportunities": [
    "Setting healthy boundaries",
    "Practical application of insights",
    "Balancing idealism with reality"
  ],
  "communication_style": "Empathetic & Relational",
  "reflection_prompts": [
    "How does your natural empathy show up in your work?",
    "What boundaries would support your growth?"
  ]
}
```

## Core Endpoints

### 1. Get Personal Reading
`POST /reading`

Flexible personal development reading.

**Parameters:**
- `birth_date` (required): YYYY-MM-DD
- `full_name` (optional): For name-based numerology
- `birth_time` (optional): HH:MM:SS for astrology
- `latitude` (optional): For complete birth chart
- `longitude` (optional): For complete birth chart
- `timezone` (optional): e.g., "America/New_York"
- `include_coaching_prompts` (optional): Boolean, default true

### 2. Quick Numerology
`POST /numerology`

Fast numerology-only calculation.

**Parameters:**
- `birth_date` (required): YYYY-MM-DD
- `full_name` (optional): For full numerology

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
    "life_path": "Humanitarian visionary...",
    "destiny": "Destined to analyze and seek truth...",
    ...
  }
}
```

### 3. Team Analysis
`POST /team/analyze`

Analyze team dynamics and compatibility.

**Parameters:**
- `team_name` (required): String
- `team_members` (required): Array of member objects
- `include_pairwise_analysis` (optional): Boolean

**Example:**
```json
{
  "team_name": "Product Team",
  "team_members": [
    {"birth_date": "1990-06-15", "full_name": "Alice", "role": "PM"},
    {"birth_date": "1988-03-22", "full_name": "Bob", "role": "Engineer"},
    {"birth_date": "1992-11-08", "full_name": "Charlie", "role": "Designer"}
  ],
  "include_pairwise_analysis": true
}
```

**Response:**
```json
{
  "status": "success",
  "team_name": "Product Team",
  "member_count": 3,
  "overall_synergy": 78.5,
  "communication_compatibility": 82.3,
  "team_strengths": [
    "Excellent team collaboration and empathy",
    "Strong creative and innovative capacity"
  ],
  "growth_areas": [
    "Strengthening processes and organizational structure"
  ],
  "top_synergies": [
    {"person1": "Alice", "person2": "Bob", "synergy_score": 85.0}
  ]
}
```

### 4. AI Coaching
`POST /agent/coaching`

AI-powered coaching session (requires PERPLEXITY_API_KEY).

**Parameters:**
- `birth_date` (required): YYYY-MM-DD
- `full_name` (optional): String
- `coaching_query` (required): Specific question or topic

**Example:**
```json
{
  "birth_date": "1990-06-15",
  "full_name": "Jane Doe",
  "coaching_query": "How can I develop stronger leadership skills while honoring my natural communication style?"
}
```

## Data Levels Explained

| Level | What You Need | What You Get | Use Case |
|-------|---------------|--------------|----------|
| **Minimal** | Birth date only | Life path, day of week | Privacy-conscious users |
| **Basic** | Date + name | Full numerology | Personal branding |
| **Enhanced** | Date + time | Numerology + sun sign | Light astrology interest |
| **Complete** | Date + time + location | Full numerology + complete chart | Deep personal work |

## Rate Limits

- **Free tier:** 100 requests/day
- **Starter:** 1,000 requests/day
- **Professional:** 10,000 requests/day
- **Enterprise:** Custom

## Error Handling

```json
{
  "error": "Invalid birth date format",
  "details": "Expected YYYY-MM-DD, got '06/15/1990'",
  "status_code": 400
}
```

**Common Errors:**
- `400` - Invalid input format
- `401` - Invalid API key
- `429` - Rate limit exceeded
- `500` - Server error
- `503` - AI coaching unavailable

## Compliance Notice

**IMPORTANT:** This API provides personal development insights ONLY. It is NOT intended for hiring, promotion, performance evaluation, or any employment decisions.

All responses include compliance disclaimers. Ensure your application displays these prominently.

## Next Steps

- [Complete API Reference](./api-reference.md)
- [Integration Examples](./integration-examples.md)
- [Compliance Guide](../compliance/legal-positioning.md)
- [Numerology Interpretations](../interpretations/life-path-numbers.md)

## Support

- **Documentation:** https://docs.yourdomain.com
- **Email:** support@yourdomain.com
- **Community:** https://community.yourdomain.com
