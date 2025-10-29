# Interpretation System API Specification

## Document Overview

**Version**: 1.0  
**Date**: October 29, 2025  
**Status**: Design Phase  
**Related**: INTERPRETATION_SYSTEM_ARCHITECTURE.md

## Base URL

```
Production: https://api.rootsrevealed.com/v1
Development: http://localhost:5000/api/v1
```

## Authentication

All interpretation endpoints require JWT authentication via Bearer token:

```http
Authorization: Bearer {jwt_token}
```

## API Endpoints

### 1. Generate Full Interpretation

**Endpoint**: `POST /charts/:chartId/interpretation`

**Description**: Generate or regenerate a complete interpretation for a chart with specified options.

**Request**:
```http
POST /api/v1/charts/550e8400-e29b-41d4-a716-446655440000/interpretation
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "style": "modern",
  "culturalFramework": "western",
  "sections": [
    "planets_in_signs",
    "planets_in_houses",
    "aspects",
    "angles",
    "patterns",
    "themes"
  ],
  "options": {
    "includeAspects": true,
    "includeBMAD": true,
    "includeSymbolon": true,
    "includeMinorAspects": false
  }
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "interpretationId": "int_7f3d4c2a-9e1b-4a5c-8d7f-2e3a4b5c6d7e",
    "chartId": "550e8400-e29b-41d4-a716-446655440000",
    "userId": "usr_123abc",
    "style": "modern",
    "culturalFramework": "western",
    "sections": {
      "planetsInSigns": [
        {
          "planet": "sun",
          "sign": "aries",
          "text": "With your Sun in Aries, you embody the archetype...",
          "keywords": ["initiative", "courage", "independence"],
          "strength": 0.92
        },
        {
          "planet": "moon",
          "sign": "cancer",
          "text": "Your Moon in Cancer creates a deeply nurturing...",
          "keywords": ["nurturing", "emotional", "protective"],
          "strength": 0.88
        }
      ],
      "planetsInHouses": [
        {
          "planet": "sun",
          "house": 10,
          "text": "Your Sun in the 10th House illuminates...",
          "keywords": ["career", "public", "achievement"],
          "strength": 0.85
        }
      ],
      "aspects": [
        {
          "planet1": "sun",
          "planet2": "moon",
          "aspectType": "square",
          "orb": 2.3,
          "text": "The square between your Sun and Moon...",
          "isHarmonious": false,
          "strength": 0.78
        }
      ],
      "angles": [
        {
          "angle": "ascendant",
          "sign": "scorpio",
          "text": "With Scorpio rising, you project an aura...",
          "keywords": ["intensity", "depth", "transformation"]
        }
      ],
      "patterns": [
        {
          "patternType": "grand_trine",
          "element": "water",
          "planets": ["moon", "neptune", "pluto"],
          "text": "Your Grand Trine in Water signs creates...",
          "keywords": ["emotional flow", "intuition", "gifts"]
        }
      ]
    },
    "themeSynthesis": {
      "dominantThemes": [
        {
          "name": "Leadership and Independence",
          "description": "A strong emphasis on autonomy and pioneering...",
          "elements": ["sun_aries", "sun_house10", "mars_aspects"],
          "priority": 1
        },
        {
          "name": "Emotional Depth and Transformation",
          "description": "Water Grand Trine combined with Scorpio rising...",
          "elements": ["water_trine", "scorpio_asc", "pluto_aspects"],
          "priority": 2
        }
      ],
      "overallNarrative": "Your chart reveals a powerful combination of fiery independence and watery emotional depth...",
      "keyInsights": [
        "Natural leadership abilities combined with profound emotional intelligence",
        "Career and public life are central to your life purpose",
        "Internal tension between action and feeling creates growth"
      ],
      "strengths": [
        "Courage and initiative",
        "Deep emotional understanding",
        "Transformative capacity"
      ],
      "challenges": [
        "Balancing independence with emotional needs",
        "Managing intensity in relationships",
        "Patience with slower processes"
      ],
      "growthOpportunities": [
        "Integrate action-oriented and emotional sides",
        "Channel intensity into creative or healing work",
        "Develop patience alongside initiative"
      ]
    },
    "bmadIntegration": {
      "dimensionMappings": [
        {
          "dimension": "emotionalRegulation",
          "relatedPlacements": ["moon_cancer", "water_trine"],
          "correlation": 0.85,
          "insights": [
            "Strong natural emotional intelligence",
            "May need to balance depth with healthy boundaries"
          ]
        }
      ],
      "behavioralSynthesis": "Your BMAD profile shows high scores in emotional and interpersonal dimensions..."
    },
    "symbolonIntegration": {
      "relevantCards": [
        {
          "cardId": "sym_15",
          "cardName": "The Warrior",
          "relevanceScore": 0.89,
          "matchingElements": ["sun_aries", "mars_aspects"],
          "archetypalMeaning": "The warrior archetype resonates strongly..."
        }
      ],
      "archetypalThemes": ["Warrior", "Healer", "Transformer"],
      "connections": "Your chart's combination of Aries energy and Water emphasis..."
    },
    "metadata": {
      "version": "1.0",
      "generatedAt": "2025-10-29T16:30:00Z",
      "cacheKey": "interp_550e8400_modern_western",
      "generationTimeMs": 1847
    }
  },
  "message": "Interpretation generated successfully",
  "cached": false
}
```

**Error Responses**:

```json
// 404 Not Found
{
  "success": false,
  "error": {
    "code": "CHART_NOT_FOUND",
    "message": "Chart with ID 550e8400-e29b-41d4-a716-446655440000 not found"
  }
}

// 403 Forbidden
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED_ACCESS",
    "message": "You don't have permission to access this chart"
  }
}

// 400 Bad Request
{
  "success": false,
  "error": {
    "code": "INVALID_PARAMETERS",
    "message": "Invalid interpretation style: 'custom'",
    "details": {
      "validStyles": ["traditional", "modern", "psychological"]
    }
  }
}
```

---

### 2. Get Cached Interpretation

**Endpoint**: `GET /charts/:chartId/interpretation`

**Description**: Retrieve existing interpretation from cache or database.

**Request**:
```http
GET /api/v1/charts/550e8400-e29b-41d4-a716-446655440000/interpretation?style=modern&refresh=false
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Query Parameters**:
- `style` (optional): `traditional` | `modern` | `psychological` (defaults to user preference)
- `culturalFramework` (optional): `western` | `vedic` | `chinese` | `african` | `custom`
- `refresh` (optional): `true` | `false` (bypass cache, regenerate)

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    // Same structure as POST response
  },
  "cached": true,
  "generatedAt": "2025-10-29T14:00:00Z"
}
```

**Response** (404 Not Found):
```json
{
  "success": false,
  "error": {
    "code": "INTERPRETATION_NOT_FOUND",
    "message": "No interpretation found for this chart. Generate one first.",
    "suggestion": "POST /api/v1/charts/:chartId/interpretation"
  }
}
```

---

### 3. Get Specific Section

**Endpoint**: `GET /charts/:chartId/interpretation/:section`

**Description**: Retrieve only a specific section of the interpretation for lazy loading.

**Request**:
```http
GET /api/v1/charts/550e8400-e29b-41d4-a716-446655440000/interpretation/planets-in-signs
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Valid Sections**:
- `planets-in-signs`
- `planets-in-houses`
- `aspects`
- `angles`
- `patterns`
- `themes`

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "section": "planets_in_signs",
    "chartId": "550e8400-e29b-41d4-a716-446655440000",
    "content": [
      {
        "planet": "sun",
        "sign": "aries",
        "text": "With your Sun in Aries...",
        "keywords": ["initiative", "courage", "independence"],
        "strength": 0.92
      },
      {
        "planet": "moon",
        "sign": "cancer",
        "text": "Your Moon in Cancer...",
        "keywords": ["nurturing", "emotional", "protective"],
        "strength": 0.88
      }
    ],
    "style": "modern",
    "generatedAt": "2025-10-29T14:00:00Z"
  },
  "cached": true
}
```

---

### 4. Update Interpretation Style

**Endpoint**: `PATCH /charts/:chartId/interpretation`

**Description**: Update interpretation style or cultural framework, triggering regeneration.

**Request**:
```http
PATCH /api/v1/charts/550e8400-e29b-41d4-a716-446655440000/interpretation
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "style": "psychological",
  "culturalFramework": "vedic"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Interpretation updated and regenerated",
  "data": {
    // Full interpretation with new style
  },
  "changes": {
    "style": {
      "from": "modern",
      "to": "psychological"
    },
    "culturalFramework": {
      "from": "western",
      "to": "vedic"
    }
  },
  "regeneratedAt": "2025-10-29T16:35:00Z"
}
```

---

### 5. Toggle Section Visibility

**Endpoint**: `PATCH /charts/:chartId/interpretation/sections`

**Description**: Show or hide specific interpretation sections.

**Request**:
```http
PATCH /api/v1/charts/550e8400-e29b-41d4-a716-446655440000/interpretation/sections
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "hiddenSections": ["aspects", "patterns"]
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Section visibility updated",
  "data": {
    "hiddenSections": ["aspects", "patterns"],
    "visibleSections": ["planets_in_signs", "planets_in_houses", "angles", "themes"]
  }
}
```

---

### 6. Add User Note

**Endpoint**: `POST /charts/:chartId/interpretation/notes`

**Description**: Add personal notes to specific interpretation elements.

**Request**:
```http
POST /api/v1/charts/550e8400-e29b-41d4-a716-446655440000/interpretation/notes
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "section": "planets_in_signs",
  "element": "sun_aries",
  "note": "This really resonates with how I approach my career. I've always been the first to volunteer for new projects.",
  "isPrivate": true
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "message": "Note saved successfully",
  "data": {
    "noteId": "note_abc123",
    "section": "planets_in_signs",
    "element": "sun_aries",
    "note": "This really resonates...",
    "isPrivate": true,
    "createdAt": "2025-10-29T16:40:00Z"
  }
}
```

---

### 7. Get User Notes

**Endpoint**: `GET /charts/:chartId/interpretation/notes`

**Description**: Retrieve all notes for a chart's interpretation.

**Request**:
```http
GET /api/v1/charts/550e8400-e29b-41d4-a716-446655440000/interpretation/notes
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "notes": [
      {
        "noteId": "note_abc123",
        "section": "planets_in_signs",
        "element": "sun_aries",
        "note": "This really resonates...",
        "createdAt": "2025-10-29T16:40:00Z",
        "updatedAt": "2025-10-29T16:40:00Z"
      }
    ],
    "total": 1
  }
}
```

---

### 8. Share Interpretation

**Endpoint**: `POST /charts/:chartId/interpretation/share`

**Description**: Generate a shareable public link for the interpretation.

**Request**:
```http
POST /api/v1/charts/550e8400-e29b-41d4-a716-446655440000/interpretation/share
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "expiresIn": 604800,
  "allowComments": false,
  "includeSections": ["planets_in_signs", "themes"]
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "message": "Share link created",
  "data": {
    "shareId": "share_xyz789",
    "shareUrl": "https://rootsrevealed.com/shared/interpretation/share_xyz789",
    "expiresAt": "2025-11-05T16:45:00Z",
    "accessCount": 0,
    "allowComments": false
  }
}
```

---

### 9. Export Interpretation (PDF)

**Endpoint**: `GET /charts/:chartId/interpretation/export`

**Description**: Export interpretation as PDF document.

**Request**:
```http
GET /api/v1/charts/550e8400-e29b-41d4-a716-446655440000/interpretation/export?format=pdf
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Query Parameters**:
- `format`: `pdf` | `docx` | `txt`
- `sections`: Comma-separated list of sections to include

**Response** (200 OK):
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="chart-interpretation-2025-10-29.pdf"

[PDF binary data]
```

---

### 10. Get Interpretation Statistics

**Endpoint**: `GET /charts/:chartId/interpretation/stats`

**Description**: Get metadata and statistics about the interpretation.

**Request**:
```http
GET /api/v1/charts/550e8400-e29b-41d4-a716-446655440000/interpretation/stats
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "chartId": "550e8400-e29b-41d4-a716-446655440000",
    "firstGeneratedAt": "2025-10-20T10:00:00Z",
    "lastGeneratedAt": "2025-10-29T16:30:00Z",
    "viewCount": 42,
    "lastViewedAt": "2025-10-29T16:45:00Z",
    "noteCount": 3,
    "shareCount": 1,
    "currentStyle": "modern",
    "currentFramework": "western",
    "sections": {
      "planets_in_signs": { "items": 10, "avgStrength": 0.82 },
      "planets_in_houses": { "items": 10, "avgStrength": 0.78 },
      "aspects": { "items": 15, "avgStrength": 0.71 },
      "patterns": { "items": 2, "avgStrength": 0.88 }
    },
    "cacheStatus": {
      "inRedis": true,
      "inDatabase": true,
      "lastRefreshed": "2025-10-29T16:30:00Z"
    }
  }
}
```

---

## Data Flow Diagrams

### 1. Interpretation Generation Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │ POST /charts/:id/interpretation
     ▼
┌─────────────────────────────────────────┐
│   Interpretation Controller              │
│  1. Validate auth & permissions          │
│  2. Check parameters                     │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│   Check Cache (Redis)                   │
│  - Generate cache key                    │
│  - Try Redis lookup                      │
└────┬────────────────────────┬───────────┘
     │ Cache Miss             │ Cache Hit
     │                        │
     ▼                        ▼
┌─────────────────┐      ┌──────────────┐
│ Check Database  │      │ Return Cache │
│ interpretations │      │    Result    │
└────┬────────────┘      └──────────────┘
     │ Not Found or Refresh
     ▼
┌─────────────────────────────────────────┐
│   Fetch Chart Data                      │
│  - Get from charts table                 │
│  - Include planets, houses, aspects     │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│   Content Service                        │
│  - Load interpretation texts             │
│  - Apply style & framework filters      │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│   Interpretation Engine                  │
│  - Generate planet interpretations       │
│  - Generate aspect interpretations      │
│  - Generate pattern interpretations     │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│   Synthesis Engine                       │
│  - Identify themes                       │
│  - Generate narrative                    │
│  - Integrate BMAD & Symbolon            │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│   Cache Results                          │
│  - Save to Redis (24hr TTL)             │
│  - Save to Database (permanent)         │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│   Return Response                        │
│  - HTTP 200 with interpretation data    │
│  - Include metadata                      │
└─────────────────────────────────────────┘
```

### 2. Section Lazy Loading Flow

```
User scrolls → Section visible → Check loaded?
                                     │
                     ┌───────────────┴──────────────┐
                     │ No                            │ Yes
                     ▼                               ▼
         GET /interpretation/:section        Display cached
                     │
                     ▼
            Check component cache
                     │
         ┌───────────┴──────────┐
         │ Miss                  │ Hit
         ▼                       ▼
   Fetch from API          Return cached
         │
         ▼
   Store in component cache
         │
         ▼
      Render section
```

---

## Rate Limiting

```
Authenticated Users:
- 100 requests per minute per user
- 1000 requests per hour per user

Shared Links (Unauthenticated):
- 10 requests per minute per IP
- 100 requests per hour per IP

Heavy Operations (PDF Export):
- 5 requests per minute
- 20 requests per hour
```

**Rate Limit Headers**:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1698595200
```

**Rate Limit Exceeded (429)**:
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again in 42 seconds.",
    "retryAfter": 42
  }
}
```

---

## Error Codes Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `CHART_NOT_FOUND` | 404 | Chart ID doesn't exist |
| `INTERPRETATION_NOT_FOUND` | 404 | No interpretation exists yet |
| `UNAUTHORIZED_ACCESS` | 403 | User doesn't own this chart |
| `INVALID_PARAMETERS` | 400 | Invalid request parameters |
| `INVALID_SECTION` | 400 | Section name not recognized |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `GENERATION_FAILED` | 500 | Interpretation generation error |
| `CACHE_ERROR` | 500 | Cache service unavailable |
| `DATABASE_ERROR` | 500 | Database operation failed |

---

## Webhooks (Future Feature)

Register webhooks to receive notifications when interpretations are generated or updated.

**Endpoint**: `POST /webhooks/interpretation`

**Events**:
- `interpretation.generated`
- `interpretation.updated`
- `interpretation.viewed`
- `interpretation.shared`
- `note.added`

---

## SDK Examples

### JavaScript/TypeScript
```typescript
import { RootsRevealedClient } from '@roots-revealed/sdk';

const client = new RootsRevealedClient({
  apiKey: process.env.API_KEY,
  baseUrl: 'https://api.rootsrevealed.com/v1'
});

// Generate interpretation
const interpretation = await client.interpretations.generate(chartId, {
  style: 'modern',
  culturalFramework: 'western',
  includeBMAD: true
});

// Get specific section
const planets = await client.interpretations.getSection(
  chartId,
  'planets-in-signs'
);

// Add note
await client.interpretations.addNote(chartId, {
  section: 'planets_in_signs',
  element: 'sun_aries',
  note: 'This resonates with me...'
});
```

### Python
```python
from roots_revealed import Client

client = Client(
    api_key=os.environ['API_KEY'],
    base_url='https://api.rootsrevealed.com/v1'
)

# Generate interpretation
interpretation = client.interpretations.generate(
    chart_id=chart_id,
    style='modern',
    cultural_framework='western',
    include_bmad=True
)

# Get specific section
planets = client.interpretations.get_section(
    chart_id=chart_id,
    section='planets-in-signs'
)
```

---

## Testing Endpoints

### Development/Staging
```
Base URL: http://localhost:5000/api/v1
Test User: test@rootsrevealed.com
Test Chart ID: 550e8400-e29b-41d4-a716-446655440000
```

### Sample cURL Commands

```bash
# Generate interpretation
curl -X POST http://localhost:5000/api/v1/charts/550e8400-e29b-41d4-a716-446655440000/interpretation \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"style": "modern", "culturalFramework": "western"}'

# Get cached interpretation
curl -X GET http://localhost:5000/api/v1/charts/550e8400-e29b-41d4-a716-446655440000/interpretation \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get specific section
curl -X GET http://localhost:5000/api/v1/charts/550e8400-e29b-41d4-a716-446655440000/interpretation/planets-in-signs \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Changelog

### Version 1.0 (2025-10-29)
- Initial API specification
- 10 core endpoints defined
- Authentication and rate limiting specified
- Error codes documented

---

**Document Status**: Ready for Implementation  
**Next Steps**:
1. Review with backend development team
2. Set up endpoint stubs for testing
3. Implement authentication middleware
4. Create integration tests

**Related Documents**:
- [INTERPRETATION_SYSTEM_ARCHITECTURE.md](INTERPRETATION_SYSTEM_ARCHITECTURE.md)
- [INTERPRETATION_CONTENT_GUIDE.md](INTERPRETATION_CONTENT_GUIDE.md)
- [DATABASE_SCHEMA.md](../DATABASE_SCHEMA.md)
