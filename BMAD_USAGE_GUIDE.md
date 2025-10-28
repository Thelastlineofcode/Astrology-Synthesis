# 🧠 BMAD Method Usage Guide

The **Behavioral Model and Data (BMAD)** framework is now fully integrated into your astrology application! Here are all the ways you can use it:

## 🚀 Quick Start

### Method 1: Standalone API Server (Recommended)
```bash
# Start the BMAD API server
python bmad_server.py

# Server runs on: http://localhost:5001
# Available endpoints: /api/bmad/*
```

### Method 2: Direct Python Integration
```bash
# Run analysis directly with Python script
python run_bmad_analysis.py
```

### Method 3: Integration with Main App
```bash
# Run your main Flask app (if Flask dependencies are installed)
python backend/app.py
```

## 📡 API Endpoints

### 🏥 Health Check
```http
GET http://localhost:5001/api/health
```

### 🧠 Personality Analysis Only
```http
POST http://localhost:5001/api/bmad/personality/analyze
Content-Type: application/json

{
  "chart_data": {
    "planets": {
      "Sun": {"sign": "Leo", "degree": 15.5, "house": 5},
      "Moon": {"sign": "Cancer", "degree": 22.3, "house": 4}
    },
    "houses": {
      "house_1": {"sign": "Aries", "degree": 12.0}
    },
    "aspects": []
  },
  "birth_data": {
    "year": 1990, "month": 8, "day": 15,
    "hour": 14, "minute": 30,
    "latitude": 40.7128, "longitude": -74.0060
  }
}
```

### 🎭 Behavioral Profile Only
```http
POST http://localhost:5001/api/bmad/behavior/profile
Content-Type: application/json

{
  "chart_data": { /* same as above */ },
  "birth_data": { /* same as above */ }
}
```

### 🎯 Complete BMAD Analysis
```http
POST http://localhost:5001/api/bmad/combined/full-analysis
Content-Type: application/json

{
  "chart_data": {
    "planets": {
      "Sun": {"sign": "Leo", "degree": 15.5, "house": 5},
      "Moon": {"sign": "Cancer", "degree": 22.3, "house": 4},
      "Mercury": {"sign": "Virgo", "degree": 8.1, "house": 6},
      "Venus": {"sign": "Leo", "degree": 28.7, "house": 5},
      "Mars": {"sign": "Gemini", "degree": 12.4, "house": 3}
    },
    "houses": {
      "house_1": {"sign": "Aries", "degree": 12.0},
      "house_4": {"sign": "Cancer", "degree": 12.0},
      "house_5": {"sign": "Leo", "degree": 12.0}
    },
    "aspects": [
      {"planet1": "Sun", "planet2": "Moon", "aspect": "sextile", "orb": 3.2},
      {"planet1": "Sun", "planet2": "Venus", "aspect": "conjunction", "orb": 1.8}
    ]
  },
  "birth_data": {
    "year": 1990, "month": 8, "day": 15,
    "hour": 14, "minute": 30,
    "latitude": 40.7128, "longitude": -74.0060
  },
  "person_name": "John Doe",
  "analysis_options": {
    "include_predictions": true,
    "prediction_months": 3
  }
}
```

## 📊 Response Format

### Successful Response
```json
{
  "success": true,
  "metadata": {
    "person_name": "John Doe",
    "analysis_date": "2025-10-28T16:53:19.123456",
    "analysis_timestamp": "2025-10-28T16:53:19.123456"
  },
  "personality_profile": {
    "traits": [
      {
        "name": "Creative Expression",
        "dimension": "openness",
        "intensity": 4,
        "description": "Strong inclination towards artistic and creative pursuits",
        "astrological_basis": ["Sun in Leo", "Venus in Leo"],
        "created_timestamp": "2025-10-28T16:53:19.123456"
      }
    ],
    "dominant_dimensions": ["openness", "extraversion"],
    "summary": "Profile shows strong creative and expressive tendencies...",
    "created_timestamp": "2025-10-28T16:53:19.123456"
  },
  "behavior_profile": {
    "current_indicators": [
      {
        "name": "Leadership Tendencies",
        "category": "social_interaction",
        "intensity": 3.8,
        "description": "Natural inclination to take charge in group situations",
        "confidence": 0.85,
        "astrological_basis": ["Sun in Leo", "Sun in house 5"]
      }
    ],
    "dominant_categories": ["social_interaction", "creative_expression"],
    "summary": "Behavioral profile indicates strong leadership and creative expression...",
    "last_updated": "2025-10-28T16:53:19.123456"
  },
  "future_predictions": [
    {
      "period": "2025-11",
      "description": "Increased focus on creative projects and self-expression",
      "intensity": 3.5,
      "category": "creative_expression",
      "confidence": 0.75,
      "astrological_basis": ["Progressed Sun aspects"]
    }
  ]
}
```

## 💻 Frontend Integration Examples

### JavaScript/React Example
```javascript
// Example function to call BMAD API
async function analyzeBMAD(chartData, birthData, personName) {
  const requestData = {
    chart_data: chartData,
    birth_data: birthData,
    person_name: personName,
    analysis_options: {
      include_predictions: true,
      prediction_months: 6
    }
  };

  try {
    const response = await fetch('http://localhost:5001/api/bmad/combined/full-analysis', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    });

    if (response.ok) {
      const result = await response.json();
      return result;
    } else {
      throw new Error(`API Error: ${response.status}`);
    }
  } catch (error) {
    console.error('BMAD Analysis Error:', error);
    throw error;
  }
}

// Usage in your component
const bmadResults = await analyzeBMAD(chartData, birthData, "Client Name");
console.log('Personality traits:', bmadResults.personality_profile.traits);
console.log('Behavioral indicators:', bmadResults.behavior_profile.current_indicators);
```

### Python Integration Example
```python
import requests

def analyze_with_bmad(chart_data, birth_data, person_name="Client"):
    """Integrate BMAD analysis into your Python application."""
    
    url = "http://localhost:5001/api/bmad/combined/full-analysis"
    
    payload = {
        "chart_data": chart_data,
        "birth_data": birth_data,
        "person_name": person_name,
        "analysis_options": {
            "include_predictions": True,
            "prediction_months": 3
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"BMAD API Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error calling BMAD API: {e}")
        return None

# Example usage
result = analyze_with_bmad(your_chart_data, your_birth_data, "Client Name")
if result:
    personality_traits = result['personality_profile']['traits']
    behavioral_indicators = result['behavior_profile']['current_indicators']
    predictions = result.get('future_predictions', [])
```

## 🎯 BMAD Analysis Features

### 🧠 Personality Dimensions (10 Total)
1. **Openness** - Creativity, curiosity, intellectual interests
2. **Conscientiousness** - Organization, discipline, goal-orientation
3. **Extraversion** - Social energy, assertiveness, enthusiasm
4. **Agreeableness** - Cooperation, trust, empathy
5. **Emotional Stability** - Stress management, emotional regulation
6. **Independence** - Self-reliance, autonomy
7. **Intuition** - Insight, pattern recognition, gut feelings
8. **Analytical Thinking** - Logic, systematic approach, critical analysis
9. **Empathy** - Understanding others, emotional intelligence
10. **Spiritual Orientation** - Connection to transcendent, meaning-seeking

### 🎭 Behavioral Categories (10 Total)
1. **Communication Style** - How they express and receive information
2. **Decision Making** - Their approach to choices and problem-solving
3. **Social Interaction** - Patterns in relationships and group dynamics
4. **Emotional Expression** - How they process and show emotions
5. **Creative Expression** - Artistic and innovative tendencies
6. **Leadership Style** - How they guide and influence others
7. **Learning Preferences** - Optimal ways they acquire knowledge
8. **Stress Response** - Reactions and coping mechanisms under pressure
9. **Goal Orientation** - How they set and pursue objectives
10. **Relationship Patterns** - Tendencies in forming and maintaining bonds

### 🔮 Future Predictions
- Behavioral trend forecasting based on astrological progressions
- Customizable prediction timeframes (1-12 months)
- Confidence ratings for each prediction
- Category-specific predictions

## 🔧 Configuration Options

### Analysis Options
```json
{
  "analysis_options": {
    "include_predictions": true,           // Enable future predictions
    "prediction_months": 6,               // How many months to predict
    "personality_threshold": 0.3,         // Minimum intensity for personality traits
    "behavior_threshold": 0.2,            // Minimum intensity for behavioral indicators
    "detailed_analysis": true,            // Include detailed descriptions
    "astrological_explanations": true     // Include astrological basis for each result
  }
}
```

## 🚀 Production Deployment

### For Production Use:
1. **Install production WSGI server:**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5001 bmad_server:app
   ```

3. **Environment Variables:**
   ```bash
   export BMAD_DEBUG=false
   export BMAD_PORT=5001
   export BMAD_HOST=0.0.0.0
   ```

## 🔍 Troubleshooting

### Common Issues:

1. **Server won't start:**
   ```bash
   # Check if port is in use
   lsof -i :5001
   
   # Kill existing processes
   pkill -f bmad_server
   ```

2. **Import errors:**
   ```bash
   # Make sure you're in the right directory
   cd /workspaces/Astrology-Synthesis
   
   # Activate virtual environment if needed
   source .venv/bin/activate
   ```

3. **API connection errors:**
   - Verify server is running: `http://localhost:5001/api/health`
   - Check firewall settings
   - Ensure correct port (5001)

## 📚 Advanced Usage

### Custom Analysis Pipeline
```python
# Direct access to BMAD components
import sys
sys.path.append('backend')

from bmad.services.personality_analyzer import PersonalityAnalyzer
from bmad.services.behavior_predictor import BehaviorPredictor

# Create analyzers
personality_analyzer = PersonalityAnalyzer()
behavior_predictor = BehaviorPredictor()

# Run custom analysis
personality_profile = personality_analyzer.analyze_personality(chart_data, birth_data)
behavior_profile = behavior_predictor.create_behavior_profile(chart_data, birth_data)

# Generate predictions
future_predictions = behavior_predictor.predict_future_behavior(
    behavior_profile, 
    months_ahead=6
)
```

---

## 🎊 You're Ready!

Your BMAD method is fully operational! Choose the integration approach that best fits your needs:

- **🌐 API Server** - Best for web applications and microservices
- **🐍 Direct Python** - Best for desktop applications and scripts  
- **🔗 Integration** - Best for extending existing astrology applications

Happy analyzing! 🌟✨