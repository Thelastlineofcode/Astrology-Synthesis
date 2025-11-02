# Phase 2 Calculation Engines - Integration Guide

## Overview

This document maps the Phase 2 calculation engine APIs to the Phase 3 service layer integration points.

---

## 1. KP Engine (`backend/calculations/kp_engine.py`)

### Key Data Structures

```python
@dataclass
class SubLordPosition:
    """Represents a planet's position with nakshatra and sub-lord."""
    longitude: float  # 0-360 degrees
    nakshatra_num: int  # 1-27
    nakshatra_name: str
    nakshatra_lord: str
    sub_lord: str
    position_in_nakshatra: float  # Degrees within nakshatra (0-13.333)
    sub_lord_start: float  # Sub-lord arc start position
    sub_lord_end: float  # Sub-lord arc end position
```

### Public API Functions

#### `get_sub_lord(longitude_degrees: float) -> SubLordPosition`

Calculates sub-lord for any zodiac position using KP system.

**Integration Point:** `CalculationService.calculate_planet_sublord()`

```python
def calculate_planet_sublord(planet_longitude: float) -> Dict:
    from backend.calculations.kp_engine import get_sub_lord
    result = get_sub_lord(planet_longitude)
    return {
        "nakshatra": result.nakshatra_name,
        "nakshatra_lord": result.nakshatra_lord,
        "sub_lord": result.sub_lord,
        "position": result.position_in_nakshatra
    }
```

#### `get_cuspal_sub_lords(house_cusps: List[float]) -> Dict[int, SubLordPosition]`

Calculates KP sub-lords for all 12 house cusps.

**Integration Point:** `CalculationService.calculate_cuspal_analysis()`

```python
def calculate_cuspal_analysis(house_cusps: List[float]) -> Dict:
    from backend.calculations.kp_engine import get_cuspal_sub_lords
    results = get_cuspal_sub_lords(house_cusps)
    return {
        str(house_num): {
            "lord": analysis.nakshatra_lord,
            "sub_lord": analysis.sub_lord,
            "longitude": analysis.longitude
        }
        for house_num, analysis in results.items()
    }
```

#### `get_planet_sub_lords(planets: Dict[str, float]) -> Dict[str, SubLordPosition]`

Calculates sub-lords for all planets in a chart.

**Integration Point:** `CalculationService.analyze_planetary_positions()`

```python
def analyze_planetary_positions(planets: Dict[str, float]) -> Dict:
    from backend.calculations.kp_engine import get_planet_sub_lords
    results = get_planet_sub_lords(planets)
    return {
        planet: {
            "nakshatra": analysis.nakshatra_name,
            "lord": analysis.nakshatra_lord,
            "sub_lord": analysis.sub_lord
        }
        for planet, analysis in results.items()
    }
```

#### `get_significators_for_house(house_num: int, birth_chart: 'BirthChart', query_planet: Optional[str] = None) -> Dict`

Gets significators for a house (KP method).

**Integration Point:** `PredictionService.analyze_house_significance()`

#### `get_ruling_planets(query_datetime: datetime, asc_longitude: float, moon_longitude: float) -> List[str]`

Calculates ruling planets at any given moment.

**Integration Point:** `TransitService.get_current_ruling_planets()`

---

## 2. Ephemeris Engine (`backend/calculations/ephemeris.py`)

### Key Data Structures

```python
class PlanetaryData:
    """Represents planetary positions for a specific moment."""
    timestamp: datetime
    planets: Dict[str, float]  # Planet name -> longitude
    houses: List[float]  # 12 house cusps
    ascendant: float
    midheaven: float
    moon_node_rahu: float
    moon_node_ketu: float
```

### Public API Functions

#### `get_current_ephemeris(lat: float, lon: float, tz_offset: float, date_time: datetime) -> Dict`

Calculates current planetary positions for a location and time.

**Integration Point:** `CalculationService.calculate_planetary_positions()`

```python
def calculate_planetary_positions(
    latitude: float,
    longitude: float,
    timezone: str,
    date_time: datetime
) -> Dict:
    from backend.calculations.ephemeris import get_current_ephemeris
    from pytz import timezone as pytz_tz

    tz = pytz_tz(timezone)
    tz_offset = tz.utcoffset(date_time).total_seconds() / 3600

    result = get_current_ephemeris(latitude, longitude, tz_offset, date_time)
    return {
        "timestamp": date_time.isoformat(),
        "planets": result["planets"],
        "houses": result["houses"],
        "ascendant": result["ascendant"],
        "midheaven": result["midheaven"]
    }
```

#### `get_birth_chart(birth_data: Dict) -> BirthChart`

Generates complete birth chart from birth data.

**Integration Point:** `ChartService.generate_birth_chart()`

---

## 3. Dasha Engine (`backend/calculations/dasha_engine.py`)

### Key Data Structures

```python
@dataclass
class DashaCalculator:
    """Calculator for Vimshottari Dasha periods."""
    birth_chart_datetime: datetime
    birth_moon_longitude: float

    def get_dasha_at_date(self, target_date: datetime) -> DashaPeriod
    def get_next_dasha_change(self) -> Tuple[str, str, datetime]
    def get_dasha_timeline(days: int) -> List[DashaPeriod]
```

### Public API Functions

#### `get_dasha_at_date(moon_longitude: float, birth_datetime: datetime, target_date: datetime) -> Dict`

Gets current Dasha/Bukti period at any date.

**Integration Point:** `CalculationService.calculate_dasha_period()`

```python
def calculate_dasha_period(
    moon_longitude: float,
    birth_datetime: datetime,
    target_date: datetime
) -> Dict:
    from backend.calculations.dasha_engine import get_dasha_at_date

    result = get_dasha_at_date(moon_longitude, birth_datetime, target_date)
    return {
        "main_dasha": result["mahadasha"],
        "sub_dasha": result["antardasha"],
        "remaining_years": result["remaining_years"],
        "start_date": result["start_date"],
        "end_date": result["end_date"]
    }
```

#### `create_dasha_calculator(birth_datetime: datetime, moon_longitude: float) -> DashaCalculator`

Creates a reusable Dasha calculator for a birth chart.

**Integration Point:** `PredictionService.prepare_dasha_analysis()`

---

## 4. Transit Engine (`backend/calculations/transit_engine.py`)

### Key Data Structures

```python
@dataclass
class TransitAnalysis:
    """Results of transit analysis."""
    planet_transiting: str
    natal_planet: str
    aspect: str  # conjunction, opposition, trine, etc.
    aspect_degree: float
    strength: str  # strong, moderate, weak
    interpretation: str
```

### Public API Functions

#### `analyze_marriage_window(birth_chart: BirthChart) -> Dict`

Analyzes marriage timing windows using transits and dasha.

**Integration Point:** `PredictionService.predict_marriage_window()`

```python
def predict_marriage_window(birth_chart: BirthChart) -> Dict:
    from backend.calculations.transit_engine import analyze_marriage_window

    result = analyze_marriage_window(birth_chart)
    return {
        "probable_years": result["years"],
        "planetary_indicators": result["planets"],
        "dasha_indicators": result["dasha_periods"],
        "confidence": result["confidence"]
    }
```

#### `analyze_career_window(birth_chart: BirthChart) -> Dict`

Analyzes career progression windows.

**Integration Point:** `PredictionService.predict_career_window()`

---

## Integration Strategy

### Phase 3 Week 2 Days 1-2: Service Wrapper Implementation

```python
# backend/services/calculation_service.py

from backend.calculations import kp_engine, ephemeris, dasha_engine, transit_engine
from backend.models.database import BirthChart
from typing import Dict, List

class CalculationService:
    """Orchestrates all Phase 2 calculation engines."""

    @staticmethod
    def calculate_birth_chart(
        latitude: float,
        longitude: float,
        timezone: str,
        birth_datetime: datetime
    ) -> Dict:
        """Comprehensive birth chart calculation."""
        # Step 1: Get planetary positions
        planetary_data = ephemeris.get_current_ephemeris(
            latitude, longitude, tz_offset, birth_datetime
        )

        # Step 2: Calculate KP analysis
        kp_analysis = kp_engine.get_cuspal_sub_lords(planetary_data["houses"])
        kp_planets = kp_engine.get_planet_sub_lords(planetary_data["planets"])

        # Step 3: Prepare Dasha calculator
        moon_lon = planetary_data["planets"]["Moon"]
        dasha_calc = dasha_engine.create_dasha_calculator(birth_datetime, moon_lon)

        return {
            "planetary_positions": planetary_data["planets"],
            "house_cusps": planetary_data["houses"],
            "ascendant": planetary_data["ascendant"],
            "kp_cusps": kp_analysis,
            "kp_planets": kp_planets,
            "dasha_calculator": dasha_calc
        }

    @staticmethod
    def calculate_current_transits(
        birth_chart_data: Dict,
        current_datetime: datetime
    ) -> Dict:
        """Calculate current transits for a birth chart."""
        # Use transit engine
        current_positions = ephemeris.get_current_ephemeris(
            birth_chart_data["latitude"],
            birth_chart_data["longitude"],
            birth_chart_data["tz_offset"],
            current_datetime
        )

        transit_analysis = transit_engine.analyze_current_transits(
            birth_chart_data["planetary_positions"],
            current_positions["planets"]
        )

        return transit_analysis
```

---

## Testing Strategy for Integration

### Unit Tests (Mock Phase 2)

```python
# tests/services/test_calculation_service.py

def test_calculate_birth_chart_with_valid_data():
    """Test birth chart calculation."""
    service = CalculationService()
    result = service.calculate_birth_chart(
        latitude=28.6139,
        longitude=77.2090,
        timezone="Asia/Kolkata",
        birth_datetime=datetime(2000, 1, 1, 12, 0)
    )

    assert "planetary_positions" in result
    assert "house_cusps" in result
    assert "kp_analysis" in result

def test_calculate_transits():
    """Test transit calculation."""
    birth_chart = {...}
    service = CalculationService()
    transits = service.calculate_current_transits(birth_chart, datetime.now())

    assert "current_transits" in transits
    assert len(transits["significant_aspects"]) > 0
```

### Integration Tests (Real Phase 2)

```python
def test_full_prediction_workflow():
    """Test complete prediction workflow."""
    # 1. Generate birth chart
    chart = ChartService.create_chart(user_id, birth_data, db)

    # 2. Calculate current transits
    transits = TransitService.get_current_transits(chart, db)

    # 3. Make prediction
    prediction = PredictionService.create_prediction(
        user_id, chart.chart_id, prediction_request, db
    )

    assert prediction.predicted_events is not None
    assert len(prediction.predicted_events) > 0
```

---

## Performance Considerations

### Caching Strategy

```python
# backend/services/cache_manager.py

from functools import lru_cache
from datetime import datetime, timedelta

class EphemerisCache:
    """Cache ephemeris calculations for 24 hours."""

    def __init__(self, ttl_hours=24):
        self.cache = {}
        self.ttl = timedelta(hours=ttl_hours)

    def get_cached_ephemeris(self, date_key: str) -> Optional[Dict]:
        """Get cached ephemeris for a specific date."""
        if date_key in self.cache:
            timestamp, data = self.cache[date_key]
            if datetime.now() - timestamp < self.ttl:
                return data
        return None

    def cache_ephemeris(self, date_key: str, data: Dict):
        """Cache ephemeris data."""
        self.cache[date_key] = (datetime.now(), data)
```

### Async Operations

```python
# Use async for long-running calculations
async def calculate_birth_chart_async(birth_data: BirthChartRequest) -> Dict:
    """Non-blocking birth chart calculation."""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        CalculationService.calculate_birth_chart,
        birth_data.latitude,
        birth_data.longitude,
        birth_data.timezone,
        birth_data.datetime
    )
    return result
```

---

## Error Handling

```python
class CalculationError(Exception):
    """Base error for calculation failures."""
    pass

class InvalidBirthData(CalculationError):
    """Raised when birth data is invalid."""
    pass

class EphemerisDataMissing(CalculationError):
    """Raised when ephemeris data is unavailable."""
    pass

# In service layer:
try:
    chart = CalculationService.calculate_birth_chart(...)
except InvalidBirthData as e:
    logger.error(f"Invalid birth data: {e}")
    raise HTTPException(status_code=400, detail=str(e))
except EphemerisDataMissing as e:
    logger.error(f"Ephemeris data missing: {e}")
    raise HTTPException(status_code=503, detail="Service temporarily unavailable")
```

---

## Data Flow Diagram

```
User Request (Birth Data)
        ↓
ChartService.create_chart()
        ↓
CalculationService.calculate_birth_chart()
        ├─→ ephemeris.get_current_ephemeris() [planetary positions]
        ├─→ kp_engine.get_cuspal_sub_lords() [KP analysis]
        ├─→ kp_engine.get_planet_sub_lords() [planet analysis]
        ├─→ dasha_engine.create_dasha_calculator() [Dasha setup]
        └─→ Store in BirthChart table
        ↓
Return BirthChart to User
        ↓
[Later] TransitService.get_current_transits()
        ├─→ CalculationService.calculate_current_transits()
        └─→ transit_engine.analyze_current_transits()
        ↓
PredictionService.create_prediction()
        ├─→ Combine multiple analyses
        ├─→ Generate interpretation
        └─→ Store in Prediction table
        ↓
Return Prediction to User
```

---

## Implementation Checklist for Phase 3 Week 2

### Day 1: Service Layer Foundation

- [ ] Create `backend/services/calculation_service.py`
  - [ ] Wrap ephemeris functions
  - [ ] Wrap KP engine functions
  - [ ] Wrap Dasha engine functions
  - [ ] Add error handling
  - [ ] Write 20+ unit tests

### Day 2: Supporting Services

- [ ] Create `backend/services/chart_service.py`
  - [ ] Database CRUD for charts
  - [ ] Call calculation_service
  - [ ] Audit logging
- [ ] Create `backend/services/transit_service.py`
  - [ ] Transit calculations
  - [ ] Transit interpretation
- [ ] Create `backend/services/prediction_service.py`
  - [ ] Combine multiple calculations
  - [ ] Generate predictions

### Day 3: API Endpoints

- [ ] Create `backend/api/v1/prediction_endpoints.py`
- [ ] Create `backend/api/v1/chart_endpoints.py`
- [ ] 20+ endpoint tests

### Day 4: Transit & Remedy Endpoints

- [ ] Create `backend/api/v1/transit_endpoints.py`
- [ ] Create `backend/api/v1/remedy_endpoints.py`
- [ ] 15+ endpoint tests

---

## Ready to Begin?

All Phase 2 calculation engines are available and tested. The integration points are clear. Begin with:

1. **First:** Deep dive into ephemeris.py to understand data structure
2. **Second:** Create CalculationService wrapper class
3. **Third:** Write unit tests with mocked Phase 2 engines
4. **Fourth:** Integrate real Phase 2 calls
5. **Fifth:** Build service layer on top

---

**Status:** ✅ Ready for Phase 3 Week 2 Days 1-2 Implementation
