# KP (Krishnamurti Paddhati) System Architecture

**Date**: November 1, 2025  
**Purpose**: Technical specification for building KP prediction engine  
**Status**: Design Phase

---

## 🎯 What is KP Astrology?

**Krishnamurti Paddhati** (KP) is a predictive astrology system developed by Prof. K.S. Krishnamurti in the 1960s-70s. It eliminates ambiguity in predictions by using:

1. **Sub-lord System**: Each zodiac degree divided into 249 sub-divisions
2. **Cuspal Sub-lords**: House cusp positions determine event timing
3. **Significator Theory**: Specific planets "signify" specific events
4. **Ruling Planets**: Moment of query reveals timing activators
5. **Stellar Astrology**: Nakshatra (star) positions more important than signs

### Why KP is Superior for Predictions

| Traditional Astrology                   | KP Astrology                                                                                              |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| "Mars in 7th = marriage delays" (vague) | "7th cusp sub-lord is Saturn in Venus star = marriage at age 28-30 when Venus dasha activates" (specific) |
| Multiple contradictory yogas            | Significator hierarchy resolves conflicts                                                                 |
| Wide orbs (8-10°)                       | Precise sub-lord positions (fractions of degree)                                                          |
| Guesswork on timing                     | Mathematical precision for dates                                                                          |

---

## 🧮 Core KP Calculations

### 1. Sub-lord Calculation (Vimshottari Proportions)

The zodiac is divided into **27 nakshatras** (lunar mansions), each 13°20' long.  
Each nakshatra is further divided into **9 sub-divisions** based on Vimshottari dasha proportions:

| Planet    | Dasha Years | Degrees | Arc Length                                |
| --------- | ----------- | ------- | ----------------------------------------- |
| Ketu      | 7           | 7       | 2° 46' 40"                                |
| Venus     | 20          | 20      | 7° 46' 40"                                |
| Sun       | 6           | 6       | 2° 20' 00"                                |
| Moon      | 10          | 10      | 3° 53' 20"                                |
| Mars      | 7           | 7       | 2° 46' 40"                                |
| Rahu      | 18          | 18      | 7° 00' 00"                                |
| Jupiter   | 16          | 16      | 6° 13' 20"                                |
| Saturn    | 19          | 19      | 7° 23' 20"                                |
| Mercury   | 17          | 17      | 6° 36' 40"                                |
| **Total** | **120**     | **120** | **46° 40' 00"** (repeats every nakshatra) |

**Calculation Formula**:

```python
def get_sub_lord(longitude_degrees):
    """
    Calculate sub-lord for any zodiac position.

    Args:
        longitude_degrees: 0-360 (absolute longitude)

    Returns:
        (nakshatra_num, nakshatra_lord, sub_lord, star_position)
    """
    # Nakshatra calculation
    nakshatra_length = 13 + (20/60)  # 13°20'
    nakshatra_num = int(longitude_degrees / nakshatra_length) + 1  # 1-27
    position_in_nakshatra = longitude_degrees % nakshatra_length

    # Nakshatra lords cycle (Ketu, Venus, Sun, Moon, Mars, Rahu, Jupiter, Saturn, Mercury)
    nakshatra_lords = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
    nakshatra_lord = nakshatra_lords[(nakshatra_num - 1) % 9]

    # Sub-lord calculation (Vimshottari proportions within nakshatra)
    sub_lord_divisions = [
        ('Ketu', 2 + 46/60 + 40/3600),     # 2°46'40"
        ('Venus', 7 + 46/60 + 40/3600),
        ('Sun', 2 + 20/60),
        ('Moon', 3 + 53/60 + 20/3600),
        ('Mars', 2 + 46/60 + 40/3600),
        ('Rahu', 7 + 0/60),
        ('Jupiter', 6 + 13/60 + 20/3600),
        ('Saturn', 7 + 23/60 + 20/3600),
        ('Mercury', 6 + 36/60 + 40/3600),
    ]

    cumulative = 0
    sub_lord = None
    for planet, arc in sub_lord_divisions:
        cumulative += arc
        if position_in_nakshatra < cumulative:
            sub_lord = planet
            break

    return {
        'nakshatra_num': nakshatra_num,
        'nakshatra_lord': nakshatra_lord,
        'sub_lord': sub_lord,
        'position_in_nakshatra': position_in_nakshatra,
        'longitude': longitude_degrees
    }
```

**Example**:

- Sun at 15° Leo (135° absolute)
- Nakshatra: 135 / 13.333 = 10.125 → Nakshatra #11 (Purva Phalguni, Venus ruled)
- Position in nakshatra: 135 % 13.333 = 1.67° into nakshatra
- Sub-lord: 1.67° falls in Ketu sub (0-2.777°)
- **Result**: Sun in Purva Phalguni (Venus star), Ketu sub-lord

### 2. Cuspal Sub-lord Calculation

The **12 house cusps** are the most important positions in KP. The sub-lord of each cusp determines events related to that house.

**Formula**:

```python
def get_cuspal_sub_lords(house_cusps):
    """
    Calculate sub-lords for all 12 house cusps.

    Args:
        house_cusps: List of 12 house cusp longitudes (degrees)

    Returns:
        Dict of house number → sub-lord data
    """
    cuspal_sub_lords = {}

    for house_num in range(1, 13):
        cusp_longitude = house_cusps[house_num - 1]
        sub_lord_data = get_sub_lord(cusp_longitude)
        cuspal_sub_lords[house_num] = sub_lord_data

    return cuspal_sub_lords
```

**Predictive Significance**:

- **7th cusp sub-lord = Venus**: Marriage likely in Venus dasha/antara
- **7th cusp sub-lord = Saturn**: Delays in marriage, practical partnerships
- **10th cusp sub-lord = Jupiter**: Career success through wisdom/teaching
- **10th cusp sub-lord = Mars**: Career through action/competition/military

### 3. Significator Analysis

**Significators** are planets that "signify" (control) specific houses/events. KP uses a hierarchy:

**Rules of Significators** (in priority order):

1. **Planets occupying a house** (strongest)
2. **Planets in the star of occupants**
3. **Planets occupying the star of house lord**
4. **House lord itself**
5. **Planets in the star of planets in house lord's constellation**
6. **Planets aspecting house or house lord**

**Example**: Finding significators for marriage (7th house):

```
Chart Data:
- 7th house cusp: 15° Aquarius
- 7th lord: Saturn (Aquarius ruled by Saturn)
- Planets in 7th house: Venus at 22° Aquarius
- Venus is in Purva Bhadrapada nakshatra (Jupiter ruled)
- Saturn aspects 7th house

Significator Hierarchy:
1. Venus (occupying 7th house) - PRIMARY
2. Planets in Jupiter star (Venus occupant's star lord) - SECONDARY
3. Planets in Saturn's stars (7th lord) - TERTIARY
4. Saturn (7th lord) - WEAK
5. Planets aspecting 7th - MINOR

Marriage timing: When Venus OR any Jupiter-star planet transits through favorable sub-lords
```

**Implementation**:

```python
def get_significators(house_num, chart_data):
    """
    Get significators for a specific house.

    Args:
        house_num: 1-12
        chart_data: Full chart with planets, houses, aspects

    Returns:
        List of significators with priority levels
    """
    significators = []

    # 1. Planets occupying the house
    occupants = [p for p in chart_data['planets']
                 if p['house'] == house_num]
    for planet in occupants:
        significators.append({
            'planet': planet['name'],
            'priority': 'PRIMARY',
            'reason': f"Occupying house {house_num}"
        })

        # Planets in star of occupants
        occupant_star_lord = get_nakshatra_lord(planet['longitude'])
        star_planets = [p for p in chart_data['planets']
                       if get_nakshatra_lord(p['longitude']) == occupant_star_lord]
        for sp in star_planets:
            significators.append({
                'planet': sp['name'],
                'priority': 'SECONDARY',
                'reason': f"In star of {planet['name']} (house occupant)"
            })

    # 2. House lord and planets in house lord's star
    house_lord = get_house_lord(house_num, chart_data)
    house_lord_star = get_nakshatra_lord(house_lord['longitude'])

    star_of_lord_planets = [p for p in chart_data['planets']
                           if get_nakshatra_lord(p['longitude']) == house_lord_star]
    for sp in star_of_lord_planets:
        significators.append({
            'planet': sp['name'],
            'priority': 'TERTIARY',
            'reason': f"In star of {house_lord['name']} (house lord)"
        })

    significators.append({
        'planet': house_lord['name'],
        'priority': 'WEAK',
        'reason': f"Lord of house {house_num}"
    })

    # 3. Aspecting planets (minor)
    aspects = get_aspects_to_house(house_num, chart_data)
    for asp in aspects:
        significators.append({
            'planet': asp['planet'],
            'priority': 'MINOR',
            'reason': f"Aspects house {house_num}"
        })

    return significators
```

### 4. Ruling Planets (Prashna/Query Analysis)

When a question is asked, the **ruling planets** at that moment reveal timing:

**Three Ruling Planets**:

1. **Ascendant lord & sub-lord** at query time
2. **Moon nakshatra lord & sub-lord** at query time
3. **Day lord** (weekday ruler)

**Calculation**:

```python
def get_ruling_planets(query_datetime, query_location):
    """
    Calculate ruling planets for a prashna (horary) query.

    Args:
        query_datetime: datetime object of question
        query_location: (lat, lon) tuple

    Returns:
        Dict with 3 ruling planets
    """
    # Calculate chart for query moment
    query_chart = calculate_chart(query_datetime, query_location)

    # 1. Ascendant lord and sub-lord
    asc_longitude = query_chart['houses'][0]  # 1st house cusp
    asc_sign = get_sign(asc_longitude)
    asc_lord = get_sign_lord(asc_sign)
    asc_sub_lord_data = get_sub_lord(asc_longitude)

    # 2. Moon star lord and sub-lord
    moon_longitude = query_chart['planets']['Moon']['longitude']
    moon_nakshatra_lord = get_nakshatra_lord(moon_longitude)
    moon_sub_lord_data = get_sub_lord(moon_longitude)

    # 3. Day lord (weekday ruler)
    weekday = query_datetime.weekday()
    day_lords = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
    day_lord = day_lords[weekday]  # 0=Sunday

    return {
        'ascendant': {
            'sign_lord': asc_lord,
            'sub_lord': asc_sub_lord_data['sub_lord']
        },
        'moon': {
            'star_lord': moon_nakshatra_lord,
            'sub_lord': moon_sub_lord_data['sub_lord']
        },
        'day_lord': day_lord,
        'query_time': query_datetime.isoformat()
    }
```

**Predictive Use**:

- If ruling planets = significators → Event will happen
- If ruling planets oppose significators → Event blocked
- Timing: When ruling planets transit through favorable sub-lords

---

## 🔮 KP Prediction Logic

### Question Type Classification

```python
QUESTION_TYPES = {
    'career': {
        'keywords': ['job', 'promotion', 'career', 'work', 'business'],
        'houses': [10, 6, 2],  # Career, service, wealth
        'significators_needed': [10, 2, 11]  # Profession, income, gains
    },
    'marriage': {
        'keywords': ['marriage', 'wedding', 'spouse', 'partner'],
        'houses': [7, 2, 11],  # Partnership, family, fulfillment
        'significators_needed': [7, 2, 11]
    },
    'childbirth': {
        'keywords': ['child', 'pregnancy', 'baby', 'conceive'],
        'houses': [5, 2, 11],  # Children, family, gains
        'significators_needed': [5, 2, 11]
    },
    'health': {
        'keywords': ['health', 'illness', 'disease', 'recovery'],
        'houses': [6, 8, 12, 1],  # Disease, surgery, hospitalization, body
        'significators_needed': [1, 11]  # Recovery significators
    },
    'education': {
        'keywords': ['exam', 'study', 'degree', 'admission'],
        'houses': [4, 9, 11],  # Learning, higher ed, success
        'significators_needed': [4, 9, 11]
    },
    'travel': {
        'keywords': ['travel', 'foreign', 'abroad', 'relocation'],
        'houses': [3, 9, 12],  # Short journey, long journey, foreign
        'significators_needed': [3, 9, 12]
    }
}
```

### Prediction Algorithm

```python
def predict(birth_data, question, current_datetime):
    """
    Generate KP prediction for a specific question.

    Args:
        birth_data: Birth date, time, location
        question: Natural language question string
        current_datetime: Query moment

    Returns:
        Prediction object with timing, confidence, reasoning
    """
    # 1. Calculate natal chart
    natal_chart = calculate_chart(birth_data)
    cuspal_sub_lords = get_cuspal_sub_lords(natal_chart['houses'])

    # 2. Classify question type
    question_type = classify_question(question)
    relevant_houses = QUESTION_TYPES[question_type]['houses']
    significator_houses = QUESTION_TYPES[question_type]['significators_needed']

    # 3. Get significators for relevant houses
    all_significators = []
    for house in significator_houses:
        sigs = get_significators(house, natal_chart)
        all_significators.extend(sigs)

    # 4. Get ruling planets at query time
    ruling_planets = get_ruling_planets(current_datetime, birth_data['location'])

    # 5. Check cuspal sub-lord promise
    primary_house = relevant_houses[0]
    cusp_sub_lord = cuspal_sub_lords[primary_house]['sub_lord']

    # Check if cuspal sub-lord is favorable
    favorable_significators = [s['planet'] for s in all_significators
                              if s['priority'] in ['PRIMARY', 'SECONDARY']]

    if cusp_sub_lord in favorable_significators:
        promise = "YES"
        confidence_base = 0.8
    else:
        promise = "DOUBTFUL"
        confidence_base = 0.4

    # 6. Calculate timing windows
    timing_windows = calculate_transit_timing(
        natal_chart,
        all_significators,
        ruling_planets,
        current_datetime
    )

    # 7. Build prediction
    prediction = {
        'answer': promise,
        'confidence': calculate_confidence(promise, ruling_planets, all_significators),
        'timing_windows': timing_windows,
        'cuspal_sub_lord': {
            'house': primary_house,
            'sub_lord': cusp_sub_lord,
            'favorable': promise == "YES"
        },
        'significators': all_significators[:5],  # Top 5
        'ruling_planets': ruling_planets,
        'reasoning': generate_kp_reasoning(
            promise, cusp_sub_lord, all_significators, ruling_planets
        )
    }

    return prediction
```

### Transit Timing Calculation

```python
def calculate_transit_timing(natal_chart, significators, ruling_planets, start_date):
    """
    Calculate when significators transit through favorable sub-lords.

    Returns:
        List of date ranges when event is likely
    """
    timing_windows = []

    # Get primary significators (planets to watch)
    primary_sigs = [s['planet'] for s in significators
                   if s['priority'] in ['PRIMARY', 'SECONDARY']]

    # Check transits for next 2 years
    current_date = start_date
    end_date = start_date + timedelta(days=730)

    while current_date < end_date:
        # Calculate transit positions
        transit_chart = calculate_chart_for_date(current_date, natal_chart['location'])

        # Check each significator planet's transit
        for planet_name in primary_sigs:
            transit_planet = transit_chart['planets'][planet_name]
            transit_sub_lord = get_sub_lord(transit_planet['longitude'])['sub_lord']

            # Check if transit sub-lord is a ruling planet or significator
            if transit_sub_lord in ruling_planets.values() or \
               transit_sub_lord in primary_sigs:

                # Calculate how long planet stays in this sub-lord
                sub_lord_duration = calculate_sub_lord_duration(
                    planet_name,
                    transit_planet['longitude']
                )

                timing_windows.append({
                    'start_date': current_date.date().isoformat(),
                    'end_date': (current_date + sub_lord_duration).date().isoformat(),
                    'planet': planet_name,
                    'transit_sub_lord': transit_sub_lord,
                    'reason': f"{planet_name} transits through {transit_sub_lord} sub-lord"
                })

        current_date += timedelta(days=7)  # Check weekly

    # Merge overlapping windows
    timing_windows = merge_timing_windows(timing_windows)

    return timing_windows[:3]  # Return top 3 windows
```

---

## 📊 Database Schema (KP Additions)

```sql
-- KP Sub-lord reference table
CREATE TABLE kp_sub_lords (
    id SERIAL PRIMARY KEY,
    longitude_start DECIMAL(10, 6) NOT NULL,
    longitude_end DECIMAL(10, 6) NOT NULL,
    nakshatra_num INT NOT NULL,  -- 1-27
    nakshatra_name VARCHAR(50) NOT NULL,
    nakshatra_lord VARCHAR(20) NOT NULL,
    sub_lord VARCHAR(20) NOT NULL,
    INDEX idx_longitude (longitude_start, longitude_end)
);

-- KP Chart calculations (cached)
CREATE TABLE kp_charts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    birth_datetime TIMESTAMP NOT NULL,
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL(10, 6) NOT NULL,
    cuspal_sub_lords JSONB NOT NULL,  -- {1: 'Venus', 2: 'Mars', ...}
    planet_sub_lords JSONB NOT NULL,  -- {'Sun': 'Ketu', 'Moon': 'Jupiter', ...}
    calculated_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_user (user_id)
);

-- KP Predictions (logged)
CREATE TABLE kp_predictions (
    id SERIAL PRIMARY KEY,
    kp_chart_id INT REFERENCES kp_charts(id),
    question TEXT NOT QUESTION,
    question_type VARCHAR(50),  -- 'career', 'marriage', etc.
    query_datetime TIMESTAMP NOT NULL,
    prediction_result JSONB NOT NULL,  -- Full prediction object
    confidence_score DECIMAL(3, 2),
    timing_windows JSONB,
    ruling_planets JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- KP Validation (for accuracy tracking)
CREATE TABLE kp_validations (
    id SERIAL PRIMARY KEY,
    prediction_id INT REFERENCES kp_predictions(id),
    outcome VARCHAR(20),  -- 'correct', 'incorrect', 'partial', 'pending'
    actual_date DATE,
    user_feedback TEXT,
    validated_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🧪 Testing Strategy

### Unit Tests

```python
def test_sub_lord_calculation():
    """Test sub-lord calculation for known positions."""
    # Sun at 0° Aries = Ashwini nakshatra (Ketu ruled)
    result = get_sub_lord(0.0)
    assert result['nakshatra_lord'] == 'Ketu'
    assert result['sub_lord'] == 'Ketu'  # First sub-division

    # Sun at 15° Leo (known KP position)
    result = get_sub_lord(135.0)
    assert result['nakshatra_num'] == 11  # Purva Phalguni
    assert result['nakshatra_lord'] == 'Venus'

def test_cuspal_sub_lord():
    """Test cuspal sub-lord extraction."""
    house_cusps = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
    cuspal = get_cuspal_sub_lords(house_cusps)
    assert len(cuspal) == 12
    assert 'sub_lord' in cuspal[1]

def test_significator_analysis():
    """Test significator hierarchy."""
    # Mock chart with Venus in 7th house
    chart = {
        'planets': [
            {'name': 'Venus', 'longitude': 315.0, 'house': 7}
        ],
        'houses': [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
    }
    sigs = get_significators(7, chart)
    assert sigs[0]['planet'] == 'Venus'
    assert sigs[0]['priority'] == 'PRIMARY'
```

### Integration Tests

```python
def test_full_prediction_flow():
    """Test complete prediction from birth data to result."""
    birth_data = {
        'date': '1990-08-15',
        'time': '14:30',
        'location': (29.7604, -95.3698)  # Houston
    }
    question = "When will I get married?"
    result = predict(birth_data, question, datetime.now())

    assert 'answer' in result
    assert 'confidence' in result
    assert 'timing_windows' in result
    assert len(result['timing_windows']) > 0
```

### Accuracy Validation Tests

```python
def test_historical_predictions():
    """Test against known outcomes."""
    known_cases = [
        {
            'birth': {...},
            'question': "When will I get married?",
            'asked_date': '2020-01-15',
            'actual_marriage_date': '2021-06-10',
            'predicted_window': ('2021-05-01', '2021-07-30')
        }
    ]

    for case in known_cases:
        prediction = predict(case['birth'], case['question'], case['asked_date'])
        actual = datetime.fromisoformat(case['actual_marriage_date'])

        # Check if actual date falls in predicted window
        in_window = any(
            datetime.fromisoformat(w['start_date']) <= actual <=
            datetime.fromisoformat(w['end_date'])
            for w in prediction['timing_windows']
        )

        assert in_window, f"Prediction missed for case: {case['question']}"
```

---

## 📈 Performance Targets

| Operation                  | Target Time | Notes                              |
| -------------------------- | ----------- | ---------------------------------- |
| Sub-lord calculation       | < 1ms       | Pure math, should be instant       |
| Cuspal sub-lord (12 cusps) | < 10ms      | 12 sub-lord calculations           |
| Significator analysis      | < 100ms     | Depends on chart complexity        |
| Full prediction query      | < 3s        | Includes chart calc + AI synthesis |
| Transit timing (2 years)   | < 5s        | Daily granularity check            |

---

## 🔧 Implementation Priority

1. ✅ Swiss Ephemeris integration (already working)
2. **Sub-lord calculator** (core KP calculation)
3. **Cuspal sub-lord extractor**
4. **Significator analyzer**
5. **Ruling planets calculator**
6. **Question classifier** (NLP)
7. **Transit timing engine**
8. **Prediction confidence scorer**
9. **Full prediction API**

---

## 📚 Reference Materials Needed

### Must Acquire

- **KP Reader 1-6** by Prof. K.S. Krishnamurti (original source)
- **Krishnamurti Paddhati: A Practical Guide** by M.P. Shanmugham
- **KP System of House Division** by K. Subramaniam

### Supplementary

- **Stellar Astrology** (various KP authors)
- **Ruling Planets** by K.S. Krishnamurti
- **Cuspal Interlinks** by K. Hariharan

---

**Next Steps**:

1. Implement `get_sub_lord()` function
2. Validate against known KP positions
3. Build cuspal sub-lord calculator
4. Test with sample questions

**Author**: Technical Architecture Team  
**Last Updated**: November 1, 2025
