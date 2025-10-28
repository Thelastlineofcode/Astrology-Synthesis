# BMAD - Behavioral Model and Data

## Overview

BMAD (Behavioral Model and Data) is a comprehensive astrological personality and behavioral analysis framework integrated into the Astrology Synthesis project. It provides sophisticated tools for analyzing personality traits and predicting behavioral patterns based on astrological chart data.

## Features

### 🧠 Personality Analysis
- **Trait Extraction**: Identifies personality traits from planetary positions, signs, houses, and aspects
- **Personality Profiling**: Creates comprehensive personality profiles with intensity levels
- **Compatibility Analysis**: Analyzes compatibility between two personality profiles
- **Dimensional Analysis**: Evaluates traits across multiple personality dimensions

### 🎯 Behavioral Prediction
- **Behavioral Indicators**: Identifies current behavioral patterns and tendencies
- **Future Predictions**: Predicts behavioral changes based on astrological transits
- **Trigger Analysis**: Identifies astrological conditions that activate specific behaviors
- **Evolution Tracking**: Tracks how behaviors evolve over time

### ⚙️ Configuration & Customization
- **Flexible Configuration**: Comprehensive configuration system for analysis parameters
- **Rule-based Analysis**: Customizable rules for trait and behavior identification
- **Intensity Scaling**: Configurable intensity calculation methods
- **API Customization**: Flexible API options for different use cases

## Architecture

### Models (`bmad/models/`)
- **`personality.py`**: Personality traits, profiles, and compatibility models
- **`behavior.py`**: Behavioral indicators, predictions, and evolution models

### Services (`bmad/services/`)
- **`personality_analyzer.py`**: Core personality analysis engine
- **`behavior_predictor.py`**: Behavioral prediction and analysis engine

### API (`bmad/api/`)
- **`routes.py`**: REST API endpoints for BMAD functionality

### Configuration (`bmad/config.py`)
- **`BMADConfig`**: Main configuration class with validation

## API Endpoints

### Personality Analysis
- **POST** `/api/bmad/personality/analyze` - Analyze personality from chart data
- **POST** `/api/bmad/personality/compatibility` - Analyze compatibility between profiles

### Behavioral Analysis
- **POST** `/api/bmad/behavior/profile` - Create behavioral profile
- **POST** `/api/bmad/behavior/predict` - Predict behavior for specific dates
- **POST** `/api/bmad/behavior/evolution` - Analyze behavioral evolution
- **POST** `/api/bmad/behavior/triggers/active` - Get active behavioral triggers

### Combined Analysis
- **POST** `/api/bmad/combined/full-analysis` - Complete BMAD analysis

### Information Endpoints
- **GET** `/api/bmad/info/dimensions` - Get personality dimensions
- **GET** `/api/bmad/info/behavior-categories` - Get behavior categories
- **GET** `/api/bmad/info/endpoints` - Get API endpoint information

### Enhanced Chart Analysis
- **POST** `/api/chart/enhanced` - Chart calculation with optional BMAD analysis

## Usage Examples

### Basic Personality Analysis

```python
from bmad.services.personality_analyzer import PersonalityAnalyzer

# Create analyzer
analyzer = PersonalityAnalyzer()

# Chart data from your astrology calculation
chart_data = {
    'planets': {
        'Sun': {'sign': 'Leo', 'degree': 15.5, 'house': 5},
        'Moon': {'sign': 'Cancer', 'degree': 22.3, 'house': 4}
        # ... more planets
    },
    'houses': {
        'house_1': {'sign': 'Aries', 'degree': 12.0}
        # ... more houses
    },
    'aspects': [
        {'planet1': 'Sun', 'planet2': 'Moon', 'aspect': 'sextile', 'orb': 3.2}
        # ... more aspects
    ]
}

birth_data = {
    'year': 1990, 'month': 8, 'day': 15,
    'hour': 14, 'minute': 30,
    'latitude': 40.7128, 'longitude': -74.0060
}

# Analyze personality
personality_profile = analyzer.analyze_personality(
    chart_data, birth_data, "John Doe"
)

print(f"Traits found: {len(personality_profile.traits)}")
print(f"Dominant dimensions: {personality_profile.dominant_dimensions}")
print(f"Summary: {personality_profile.summary}")
```

### Behavioral Prediction

```python
from bmad.services.behavior_predictor import BehaviorPredictor

# Create predictor
predictor = BehaviorPredictor()

# Create behavioral profile
behavior_profile = predictor.create_behavior_profile(
    chart_data, birth_data, "John Doe"
)

# Predict behavior for a specific date
predictions = predictor.predict_behavior_for_date(
    behavior_profile, "2024-06-15"
)

for prediction in predictions:
    print(f"Category: {prediction.category.value}")
    print(f"Behaviors: {prediction.predicted_behaviors}")
    print(f"Confidence: {prediction.confidence.value}")
```

### API Usage

```bash
# Analyze personality via API
curl -X POST http://localhost:5000/api/bmad/personality/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "chart_data": {...},
    "birth_data": {...},
    "profile_name": "John Doe"
  }'

# Enhanced chart with BMAD analysis
curl -X POST http://localhost:5000/api/chart/enhanced \
  -H "Content-Type: application/json" \
  -d '{
    "birthData": {...},
    "options": {...},
    "bmadOptions": {
      "includeBMAD": true,
      "includePersonality": true,
      "includeBehavior": true,
      "includePredictions": true,
      "predictionMonths": 6,
      "personName": "John Doe"
    }
  }'
```

## Personality Dimensions

BMAD analyzes personality across multiple dimensions:

- **Extraversion**: Social engagement and energy direction
- **Agreeableness**: Cooperation and social harmony
- **Conscientiousness**: Organization and goal-directed behavior
- **Neuroticism**: Emotional stability and stress response
- **Openness**: Creativity and openness to experience
- **Assertiveness**: Direct communication and leadership
- **Emotional Stability**: Emotional regulation and resilience
- **Creativity**: Innovative thinking and artistic expression
- **Leadership**: Ability to guide and influence others
- **Communication**: Interpersonal communication skills

## Behavior Categories

Behavioral analysis covers these life areas:

- **Social**: Interpersonal relationships and social interactions
- **Professional**: Work, career, and achievement behaviors
- **Romantic**: Intimate relationships and partnership patterns
- **Family**: Family dynamics and domestic behaviors
- **Creative**: Artistic expression and creative pursuits
- **Spiritual**: Spiritual practices and philosophical beliefs
- **Financial**: Money management and financial behaviors
- **Health**: Health habits and wellness behaviors
- **Communication**: Communication styles and patterns
- **Decision Making**: Decision-making processes and styles

## Configuration

BMAD is highly configurable through the `BMADConfig` class:

```python
from bmad.config import get_config, update_config

# Get current configuration
config = get_config()

# Update configuration
update_config(
    personality={
        'default_intensity_threshold': 0.6,
        'max_traits_per_dimension': 15
    },
    behavior={
        'prediction_confidence_threshold': 0.4,
        'default_prediction_days': 45
    }
)
```

### Environment Variables

Configure BMAD through environment variables:

```bash
# Personality configuration
export BMAD_PERSONALITY_INTENSITY_THRESHOLD=0.6
export BMAD_PERSONALITY_PRECISION=4

# Behavior configuration
export BMAD_BEHAVIOR_CONFIDENCE_THRESHOLD=0.4
export BMAD_BEHAVIOR_DEFAULT_DAYS=45

# Analysis configuration
export BMAD_ANALYSIS_ORB_PRECISION=0.05

# API configuration
export BMAD_API_DEBUG_MODE=true
export BMAD_API_RATE_LIMIT=120
```

## Testing

Run the comprehensive BMAD test suite:

```bash
cd backend
python test_bmad_system.py
```

This will run:
- Basic functionality tests
- Sample analysis demonstration
- Full unit test suite
- Integration tests

## Development

### Adding New Personality Traits

1. Define trait rules in `personality_analyzer.py`
2. Add trait to the appropriate rule category (sun_signs, moon_signs, etc.)
3. Specify dimension, intensity, and keywords

```python
'Leo': [
    {
        'name': 'Creative Expression',
        'dimension': 'creativity',
        'description': 'Strong drive for creative self-expression',
        'intensity_base': 4,
        'keywords': ['creative', 'expressive', 'artistic', 'dramatic']
    }
]
```

### Adding New Behavioral Indicators

1. Define behavior rules in `behavior_predictor.py`
2. Add to planetary_positions or aspect_patterns
3. Specify category, intensity, and life phases

```python
'Venus_Libra_7': [{
    'name': 'Partnership Focus',
    'category': 'romantic',
    'description': 'Strong emphasis on romantic partnerships',
    'intensity': 0.8,
    'life_phases': ['young_adult', 'adult']
}]
```

### Extending the API

Add new endpoints to `bmad/api/routes.py`:

```python
@bmad_bp.route('/custom/analysis', methods=['POST'])
def custom_analysis():
    # Your custom analysis logic
    pass
```

## Integration

BMAD integrates seamlessly with the existing Astrology Synthesis project:

1. **Chart Calculation**: Uses existing chart calculation results
2. **API Extension**: Adds new endpoints alongside existing ones
3. **Configuration**: Separate configuration system that doesn't interfere
4. **Testing**: Independent test suite with integration tests

## Future Enhancements

- **Machine Learning Integration**: Train models on historical behavioral data
- **Transit Calculations**: Real-time transit analysis for trigger identification
- **Comparative Analysis**: Multi-person group dynamics analysis
- **Visualization**: Charts and graphs for personality and behavior patterns
- **External APIs**: Integration with psychological assessment tools
- **Database Storage**: Persistent storage for profiles and analysis history

## Contributing

When contributing to BMAD:

1. Follow the existing code structure and patterns
2. Add comprehensive tests for new functionality
3. Update documentation for new features
4. Validate configurations and handle errors gracefully
5. Consider performance implications for large datasets

## License

BMAD is part of the Astrology Synthesis project and follows the same licensing terms.