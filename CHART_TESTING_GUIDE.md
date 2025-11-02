# Chart Calculator Testing Guide

## Quick Start

This guide shows you how to test the birth chart generation functionality at different layers of the application.

## Prerequisites

```bash
# Install testing dependencies
pip install pytest pytest-asyncio httpx

# Verify the backend is properly set up
cd backend
pip install -e .
```

## Test Files

### 1. **test_calculation_service.py** - Service Layer Tests

Tests the `CalculationService.generate_birth_chart()` method directly.

**Scope:**

- ✅ Birth chart generation logic
- ✅ Ephemeris calculations
- ✅ Timezone handling
- ✅ Data validation
- ✅ Historical charts (Einstein, Gandhi)

**Run:**

```bash
pytest test_calculation_service.py -v
```

**Key Tests:**

- `test_generate_birth_chart_basic` - Verify basic chart generation
- `test_chart_has_12_planets` - Check planetary data
- `test_chart_has_12_houses` - Check house cusp calculations
- `test_planet_coordinates_are_valid` - Validate coordinate ranges
- `test_chart_consistency` - Verify reproducibility
- `test_chart_with_southern_hemisphere` - Test different locations

### 2. **test_chart_calculator.py** - API Endpoint Tests

Tests the FastAPI `/api/v1/chart` endpoints with real HTTP requests.

**Scope:**

- ✅ API request/response handling
- ✅ Authentication & authorization
- ✅ Database storage
- ✅ Pagination
- ✅ Error responses
- ✅ Data validation
- ✅ User isolation

**Run:**

```bash
pytest test_chart_calculator.py -v
```

**Key Tests:**

- `test_create_birth_chart_success` - Create chart via API
- `test_get_birth_chart_success` - Retrieve chart
- `test_list_birth_charts_pagination` - Pagination testing
- `test_chart_has_all_planets` - Verify data accuracy
- `test_get_birth_chart_wrong_user` - Test access control
- `test_chart_has_all_houses` - Verify complete house data

## Testing Workflow

### Step 1: Test Service Layer First

```bash
cd /Users/houseofobi/Documents/GitHub/Astrology-Synthesis
pytest test_calculation_service.py -v -s
```

**Expected Output:**

```
CALCULATION SERVICE TEST SUITE
================================================================================

test_calculation_service.py::TestGenerateBirthChart::test_generate_birth_chart_basic PASSED
✅ Birth chart generation returns dict

test_calculation_service.py::TestGenerateBirthChart::test_chart_contains_required_fields PASSED
✅ Chart contains all required fields

test_calculation_service.py::TestGenerateBirthChart::test_chart_has_12_planets PASSED
✅ Chart includes 12 celestial bodies

test_calculation_service.py::TestGenerateBirthChart::test_chart_has_12_houses PASSED
✅ Chart includes 12 house cusps
```

### Step 2: Run API Integration Tests

```bash
pytest test_chart_calculator.py -v -s
```

**Expected Output:**

```
CHART CALCULATOR TEST SUITE
================================================================================

test_chart_calculator.py::TestBirthChartGeneration::test_create_birth_chart_success PASSED
✅ Birth chart created: 550e8400-e29b-41d4-a716-446655440000

test_chart_calculator.py::TestBirthChartGeneration::test_create_birth_chart_invalid_date PASSED
✅ Invalid date format rejected
```

### Step 3: Run All Tests with Coverage

```bash
pytest --cov=backend --cov-report=html -v
```

This generates an HTML coverage report in `htmlcov/index.html`.

## Test Examples

### Example 1: Generate A Birth Chart (Service)

```python
from backend.services.calculation_service import CalculationService
from backend.schemas import BirthDataInput

service = CalculationService()

birth_data = BirthDataInput(
    date="1995-06-15",
    time="14:30:00",
    timezone="America/New_York",
    latitude=40.7128,
    longitude=-74.0060,
    location_name="New York"
)

chart = service.generate_birth_chart(birth_data)

print(f"Chart Ascendant: {chart['ascendant']['zodiac_sign']}")
print(f"Number of Planets: {len(chart['planet_positions'])}")
print(f"Number of Aspects: {len(chart['aspects'])}")
```

### Example 2: Create Birth Chart via API

```bash
curl -X POST http://localhost:8000/api/v1/chart \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "date": "1995-06-15",
      "time": "14:30:00",
      "timezone": "America/New_York",
      "latitude": 40.7128,
      "longitude": -74.0060
    },
    "name": "My Chart",
    "notes": "Test chart"
  }'
```

### Example 3: Retrieve Birth Chart

```bash
curl -X GET http://localhost:8000/api/v1/chart/{chart_id} \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Example 4: List User's Charts

```bash
curl -X GET "http://localhost:8000/api/v1/chart?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Test Data

All tests use well-known birth charts as reference data:

| Name        | Date       | Time  | Location         | Zodiac |
| ----------- | ---------- | ----- | ---------------- | ------ |
| Modern Test | 1995-06-15 | 14:30 | New York, USA    | Gemini |
| Einstein    | 1879-03-14 | 11:30 | Ulm, Germany     | Pisces |
| Gandhi      | 1869-10-02 | 07:07 | Porbandar, India | Libra  |

## Troubleshooting

### Test fails: "ModuleNotFoundError: No module named 'backend'"

**Solution:** Install backend in editable mode

```bash
cd backend
pip install -e .
cd ..
```

### Test fails: "Database is locked"

**Solution:** Delete test database and retry

```bash
rm test.db
pytest test_chart_calculator.py -v
```

### Test fails: "Invalid timezone"

**Solution:** Ensure pytz is installed

```bash
pip install pytz
```

### Tests pass but service returns empty data

**Solution:** Verify ephemeris module is properly imported

```bash
python -c "from backend.calculations.ephemeris import EphemerisCalculator; print('OK')"
```

## Continuous Integration

To run all tests before committing:

```bash
# Run service tests
pytest test_calculation_service.py -v

# Run API tests
pytest test_chart_calculator.py -v

# Run with coverage
pytest --cov=backend --cov-report=term-missing

# Run all tests
pytest -v
```

## Performance Benchmarks

Expected performance on modern hardware:

| Operation                     | Latency | P95    | P99    |
| ----------------------------- | ------- | ------ | ------ |
| generate_birth_chart()        | ~50ms   | ~100ms | ~150ms |
| POST /api/v1/chart            | ~150ms  | ~250ms | ~350ms |
| GET /api/v1/chart             | ~10ms   | ~20ms  | ~50ms  |
| POST /api/v1/chart (DB write) | ~100ms  | ~200ms | ~300ms |

**Note:** Times include ephemeris calculation, database operations, and serialization.

## What Gets Tested

### Service Layer Tests

- ✅ Birth chart generation algorithm
- ✅ Planetary position calculations
- ✅ House cusp calculations
- ✅ Aspect calculations
- ✅ Timezone conversions
- ✅ Coordinate validation
- ✅ Error handling
- ✅ Consistency (same input = same output)

### API Layer Tests

- ✅ Request validation (Pydantic schemas)
- ✅ Response format
- ✅ HTTP status codes
- ✅ Authentication (JWT)
- ✅ Authorization (user isolation)
- ✅ Database storage
- ✅ Pagination
- ✅ Error responses
- ✅ CORS (if enabled)

### Data Accuracy Tests

- ✅ All 12 planets present
- ✅ All 12 house cusps present
- ✅ Coordinates within valid ranges
- ✅ Zodiac signs correctly assigned
- ✅ Aspects correctly calculated
- ✅ Ascendant correctly identified

## Next Steps

1. **Run service layer tests:** `pytest test_calculation_service.py -v`
2. **Run API tests:** `pytest test_chart_calculator.py -v`
3. **Check coverage:** `pytest --cov=backend --cov-report=html`
4. **Review results:** Open `htmlcov/index.html` in browser

## Success Criteria

✅ All tests pass (both service and API)
✅ Code coverage > 85%
✅ Performance: API response < 500ms P95
✅ No errors in logs
✅ Database operations working
✅ Authentication/authorization working
✅ Historical charts verified against known data

---

**Questions?** Check the test files themselves - they have detailed comments explaining each test.
