# BMAD Pattern Recognition System

## Overview

The BMAD (Birthday, Month, and Day) Pattern Recognition System is a sophisticated algorithm for identifying and analyzing astrological patterns in birth data. It detects significant numerological patterns, master numbers, harmonic relationships, and symbolic configurations in birth dates.

## Features

### Pattern Detection Categories

1. **Master Numbers** (11, 22, 33)
   - Identifies spiritually significant master numbers
   - High-weight patterns with elevated confidence scores
   - Detects master numbers in day, month, and year components

2. **Harmonic Patterns**
   - Matching day and month values
   - Numerical balance (Fibonacci-related sums)
   - Life path harmony alignments

3. **Sequential Patterns**
   - Consecutive numbers in birth data
   - Natural progression indicators
   - Step-by-step development markers

4. **Cyclic Patterns**
   - Multiple relationships between components
   - Rhythmic life cycle indicators
   - Recurring theme markers

5. **Repetitive Patterns**
   - Repeated digits in birth day
   - Intensified energy indicators
   - Focused life area markers

6. **Symbolic Patterns**
   - Prime numbers (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31)
   - Powers of two (1, 2, 4, 8, 16)
   - Unique and indivisible configurations

7. **Numeric Patterns**
   - Life path number alignments
   - Numerological harmonies
   - Digit sum relationships

## API Endpoints

### Analyze Birth Data
```http
POST /api/bmad/analyze
Content-Type: application/json

{
  "year": 1990,
  "month": 11,
  "day": 11,
  "hour": 14,
  "minute": 30
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "birthData": { ... },
    "patterns": [ ... ],
    "totalScore": 87,
    "dominantCategories": ["master_number", "harmonic"],
    "summary": "Birth date 11/11/1990 reveals 5 significant patterns...",
    "timestamp": "2025-10-29T06:19:32.071Z"
  }
}
```

### Detect Patterns Only
```http
POST /api/bmad/detect
Content-Type: application/json

{
  "year": 1990,
  "month": 7,
  "day": 7
}
```

### Filter by Category
```http
POST /api/bmad/patterns/category
Content-Type: application/json

{
  "year": 1990,
  "month": 11,
  "day": 11,
  "category": "master_number"
}
```

### Compare Birth Dates
```http
POST /api/bmad/compare
Content-Type: application/json

{
  "birthData1": {
    "year": 1990,
    "month": 11,
    "day": 11
  },
  "birthData2": {
    "year": 1992,
    "month": 11,
    "day": 22
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "birthData1": { ... },
    "birthData2": { ... },
    "comparison": {
      "commonPatterns": ["Master Number Day", "Prime Number Day"],
      "uniqueTo1": ["Pattern A"],
      "uniqueTo2": ["Pattern B"],
      "compatibilityScore": 75
    }
  }
}
```

### High Confidence Patterns
```http
POST /api/bmad/high-confidence
Content-Type: application/json

{
  "year": 1990,
  "month": 11,
  "day": 11,
  "minConfidence": 0.9
}
```

### Get Available Categories
```http
GET /api/bmad/categories
```

## Pattern Structure

Each detected pattern includes:

```typescript
{
  id: string;              // Unique identifier
  name: string;            // Pattern name
  description: string;     // Specific description for this birth data
  category: PatternCategory; // Pattern category
  score: number;           // 0-100 score based on weight and confidence
  weight: number;          // 0-1 base weight of pattern type
  confidence: number;      // 0-1 confidence in detection
  elements: PatternElement[]; // Contributing elements
  interpretation: string;  // Astrological interpretation
}
```

## Pattern Scoring System

### Weight Distribution
- **Master Numbers**: 0.80-0.95 (highest priority)
- **Sequential Patterns**: 0.85
- **Harmonic Patterns**: 0.75-0.80
- **Repetitive Patterns**: 0.75
- **Symbolic Patterns**: 0.60-0.70
- **Cyclic Patterns**: 0.65
- **Numeric Patterns**: 0.70

### Confidence Calculation
- Base confidence: 0.85
- Master number patterns: 0.95
- Sequential patterns: 0.90
- Harmonic patterns: 0.88

### Final Score
```
Score = Weight × Confidence × 100
```

## Validation

The system includes comprehensive validation:

- **Year**: 1900-2100
- **Month**: 1-12
- **Day**: 1-31 (validated against month)
- **Hour**: 0-23 (optional)
- **Minute**: 0-59 (optional)
- **Leap year handling**: Automatic
- **Month-specific day limits**: Enforced

## Usage Examples

### TypeScript/Node.js
```typescript
import { BMADPatternRecognizer } from './services/bmad';

const recognizer = new BMADPatternRecognizer();

const birthData = {
  year: 1990,
  month: 11,
  day: 11
};

// Full analysis
const analysis = recognizer.analyze(birthData);
console.log(analysis.summary);

// Detect patterns only
const patterns = recognizer.detectPatterns(birthData);

// Filter by category
const masterPatterns = recognizer.getPatternsByCategory(
  birthData,
  PatternCategory.MASTER_NUMBER
);

// High confidence only
const highConfPatterns = recognizer.getHighConfidencePatterns(birthData, 0.9);

// Compare dates
const comparison = recognizer.comparePatterns(birthData1, birthData2);
```

### REST API with cURL
```bash
# Analyze birth data
curl -X POST http://localhost:5000/api/bmad/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "year": 1990,
    "month": 11,
    "day": 11
  }'

# Get categories
curl http://localhost:5000/api/bmad/categories
```

## Testing

The system includes comprehensive unit tests covering:

- Helper function correctness (digitSum, isMasterNumber, etc.)
- Birth data validation (all edge cases)
- Pattern detection accuracy
- Analysis completeness
- Filtering capabilities
- Comparison functionality
- Edge case handling
- Scoring system validation

Run tests:
```bash
cd backend
npm test
```

## Integration

### With Express Application

```typescript
import express from 'express';
import bmadRouter from './routes/bmad';

const app = express();
app.use(express.json());
app.use('/api/bmad', bmadRouter);
```

### With Frontend

```javascript
async function analyzeBirthDate(year, month, day) {
  const response = await fetch('http://localhost:5000/api/bmad/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ year, month, day })
  });
  
  const result = await response.json();
  return result.data;
}
```

## Performance

- Average pattern detection: <10ms
- Full analysis including scoring: <20ms
- Comparison of two dates: <30ms
- Zero external API calls required
- All calculations done in-memory

## Security

- Input validation on all parameters
- Type-safe TypeScript implementation
- No SQL injection vulnerabilities
- No external data sources
- Deterministic results (no randomness)

## Future Enhancements

Potential future additions:
- Additional pattern types (Fibonacci sequences, golden ratio, etc.)
- Machine learning for pattern weight optimization
- Historical pattern correlation analysis
- Extended time-based patterns (hours, minutes)
- Cultural pattern variations
- Pattern strength trends over time

## License

Part of the Roots Revealed astrology application.
