# Phase 3 Week 2 - Service Layer Integration & Core API Endpoints

## Overview

**Duration:** Days 1-4 (8 working days)  
**Objective:** Integrate Phase 2 calculation engines with FastAPI, create core prediction endpoints  
**Status:** Ready to begin

---

## Architecture Design

### Service Layer Structure

```
backend/services/
├── auth_service.py          ✅ COMPLETE
├── calculation_service.py   (NEW) - Orchestrate all 4 engines
├── chart_service.py         (NEW) - Birth chart generation
├── prediction_service.py    (NEW) - Astrological predictions
├── transit_service.py       (NEW) - Current transits
└── remedy_service.py        (NEW) - Remedial measures
```

### Phase 2 Calculation Engines Integration

| Engine             | Location                                     | Status | Integration Point   |
| ------------------ | -------------------------------------------- | ------ | ------------------- |
| KP Calculator      | `backend/calculations/kp_calculator.py`      | Ready  | calculation_service |
| Dasha Calculator   | `backend/calculations/dasha_calculator.py`   | Ready  | calculation_service |
| Transit Calculator | `backend/calculations/transit_calculator.py` | Ready  | transit_service     |
| Ephemeris Manager  | `backend/calculations/ephemeris_manager.py`  | Ready  | calculation_service |

### API Endpoint Architecture

```
/api/v1/
├── /auth/                   ✅ COMPLETE (8 endpoints)
├── /predictions/            (NEW) Core prediction endpoints
│   ├── POST /               Create prediction
│   ├── GET /{id}            Retrieve prediction
│   ├── GET                  List user's predictions
│   └── DELETE /{id}         Delete prediction
├── /charts/                 (NEW) Birth chart endpoints
│   ├── POST /               Generate chart
│   ├── GET /{id}            Retrieve chart
│   └── GET                  List user's charts
├── /transits/               (NEW) Transit endpoints
│   ├── GET /current         Current transits
│   ├── GET /upcoming        Upcoming transits
│   └── GET /for-date        Transits for specific date
├── /remedies/               (NEW) Remedy endpoints
│   ├── GET /{id}            Get remedy details
│   └── GET /for-planet      Get remedies for planet
└── /health                  ✅ COMPLETE (1 endpoint)
```

---

## Phase 3 Week 2 Days 1-2: Service Layer Integration

### Day 1: Calculation Service Foundation

**Objective:** Create wrapper service for all calculation engines

**Files to Create:**

1. `backend/services/calculation_service.py` (350+ lines)

**Key Methods:**

```python
class CalculationService:
    # Birth chart calculations
    @staticmethod
    def calculate_birth_chart(birth_data: BirthChartRequest) -> BirthChartData

    # Planetary positions
    @staticmethod
    def get_planetary_positions(chart_date: datetime) -> Dict[str, Position]

    # KP system calculations
    @staticmethod
    def calculate_kp_houses(chart_data: BirthChartData) -> Dict[str, House]

    # Dasha system
    @staticmethod
    def calculate_dasha_period(birth_chart: BirthChartData) -> DashaPeriod

    # Transit calculations
    @staticmethod
    def calculate_transits(current_date: datetime, birth_chart: BirthChartData) -> TransitData
```

**Implementation Checklist:**

- [ ] Import all Phase 2 calculation classes
- [ ] Create orchestration methods combining engines
- [ ] Add error handling (try-catch with logging)
- [ ] Add input validation for birth data
- [ ] Add caching for ephemeris data
- [ ] Write 20+ unit tests

**Testing Strategy:**

- Unit tests for each wrapper method
- Mock Phase 2 engines for speed
- Validate output formats against schemas
- Test error conditions (invalid dates, missing data)

---

### Day 2: Supporting Services

**Objective:** Create domain-specific service layers

**Files to Create:**

1. `backend/services/chart_service.py` (250+ lines)

```python
class ChartService:
    @staticmethod
    def create_chart(user_id: str, birth_data: BirthChartRequest, db: Session) -> BirthChart

    @staticmethod
    def get_chart(chart_id: str, db: Session) -> BirthChart

    @staticmethod
    def list_user_charts(user_id: str, db: Session) -> List[BirthChart]

    @staticmethod
    def delete_chart(chart_id: str, db: Session) -> bool

    @staticmethod
    def update_chart_interpretation(chart_id: str, interpretation: str, db: Session) -> BirthChart
```

2. `backend/services/prediction_service.py` (300+ lines)

```python
class PredictionService:
    @staticmethod
    def create_prediction(
        user_id: str,
        chart_id: str,
        request: PredictionRequest,
        db: Session
    ) -> Prediction

    @staticmethod
    def get_prediction(prediction_id: str, db: Session) -> Prediction

    @staticmethod
    def list_user_predictions(user_id: str, filters: Dict, db: Session) -> List[Prediction]

    @staticmethod
    def calculate_prediction_accuracy(
        prediction: Prediction,
        actual_outcome: str
    ) -> float
```

3. `backend/services/transit_service.py` (200+ lines)

```python
class TransitService:
    @staticmethod
    def get_current_transits(birth_chart: BirthChartData) -> TransitData

    @staticmethod
    def get_upcoming_transits(
        birth_chart: BirthChartData,
        days_ahead: int = 90
    ) -> List[TransitEvent]

    @staticmethod
    def get_transits_for_date(
        birth_chart: BirthChartData,
        target_date: datetime
    ) -> TransitData

    @staticmethod
    def identify_significant_transits(
        birth_chart: BirthChartData,
        transit_data: TransitData
    ) -> List[SignificantTransit]
```

4. `backend/services/remedy_service.py` (150+ lines)

```python
class RemedyService:
    @staticmethod
    def get_remedies_for_issue(
        chart: BirthChartData,
        issue_type: str,
        db: Session
    ) -> List[Remedy]

    @staticmethod
    def recommend_remedies(
        prediction: Prediction,
        db: Session
    ) -> List[RecommendedRemedy]
```

**Implementation Checklist:**

- [ ] Database CRUD operations for each entity
- [ ] Call calculation_service for computations
- [ ] Audit logging for all operations
- [ ] Error handling and validation
- [ ] Rate limiting preparation (add user_id tracking)
- [ ] Write 15+ unit tests per service

---

## Phase 3 Week 2 Days 3-4: Core API Endpoints

### Day 3: Prediction & Chart Endpoints

**Files to Create:**
`backend/api/v1/prediction_endpoints.py` (400+ lines)
`backend/api/v1/chart_endpoints.py` (350+ lines)

#### Prediction Endpoints

```python
@router.post(
    "/",
    response_model=PredictionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create New Prediction",
    tags=["Predictions"]
)
async def create_prediction(
    request: PredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> PredictionResponse:
    """Create a new astrological prediction based on birth chart."""
    # Validate chart exists and belongs to user
    # Call PredictionService.create_prediction()
    # Log to audit trail
    # Return formatted response

@router.get(
    "/{prediction_id}",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Prediction",
    tags=["Predictions"]
)
async def get_prediction(
    prediction_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> PredictionResponse:
    """Retrieve a specific prediction."""

@router.get(
    "/",
    response_model=List[PredictionResponse],
    status_code=status.HTTP_200_OK,
    summary="List Predictions",
    tags=["Predictions"]
)
async def list_predictions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    chart_id: Optional[str] = None,
    status_filter: Optional[str] = None
) -> List[PredictionResponse]:
    """List user's predictions with filtering."""

@router.delete(
    "/{prediction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Prediction",
    tags=["Predictions"]
)
async def delete_prediction(
    prediction_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> None:
    """Delete a prediction."""
```

#### Chart Endpoints

```python
@router.post(
    "/",
    response_model=BirthChartResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate Birth Chart",
    tags=["Charts"]
)
async def create_chart(
    request: BirthChartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> BirthChartResponse:
    """Generate a new birth chart from birth data."""

@router.get(
    "/{chart_id}",
    response_model=BirthChartResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Birth Chart",
    tags=["Charts"]
)
async def get_chart(
    chart_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> BirthChartResponse:
    """Retrieve a birth chart."""

@router.get(
    "/",
    response_model=List[BirthChartResponse],
    status_code=status.HTTP_200_OK,
    summary="List Birth Charts",
    tags=["Charts"]
)
async def list_charts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
) -> List[BirthChartResponse]:
    """List user's birth charts."""
```

**Implementation Checklist:**

- [ ] Input validation using Pydantic schemas
- [ ] Call appropriate service methods
- [ ] Format responses using response_model
- [ ] Add proper HTTP status codes
- [ ] Add OpenAPI documentation
- [ ] Error handling (400, 404, 500 responses)
- [ ] Audit logging for all operations
- [ ] Write 20+ integration tests

---

### Day 4: Transit & Remedy Endpoints

**Files to Create:**
`backend/api/v1/transit_endpoints.py` (250+ lines)
`backend/api/v1/remedy_endpoints.py` (200+ lines)

#### Transit Endpoints

```python
@router.get(
    "/current",
    response_model=TransitDataResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Current Transits",
    tags=["Transits"]
)
async def get_current_transits(
    chart_id: str = Query(..., description="Birth chart ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TransitDataResponse:
    """Get current planetary transits for a birth chart."""

@router.get(
    "/upcoming",
    response_model=List[TransitEventResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Upcoming Transits",
    tags=["Transits"]
)
async def get_upcoming_transits(
    chart_id: str = Query(..., description="Birth chart ID"),
    days_ahead: int = Query(90, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[TransitEventResponse]:
    """Get upcoming significant transits."""

@router.get(
    "/for-date",
    response_model=TransitDataResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Transits for Date",
    tags=["Transits"]
)
async def get_transits_for_date(
    chart_id: str = Query(...),
    date: datetime = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TransitDataResponse:
    """Get planetary positions for a specific date."""
```

#### Remedy Endpoints

```python
@router.get(
    "/{remedy_id}",
    response_model=RemedyResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Remedy Details",
    tags=["Remedies"]
)
async def get_remedy(
    remedy_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> RemedyResponse:
    """Get detailed information about a remedy."""

@router.get(
    "/for-planet/{planet_name}",
    response_model=List[RemedyResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Remedies for Planet",
    tags=["Remedies"]
)
async def get_remedies_for_planet(
    planet_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[RemedyResponse]:
    """Get recommended remedies for a specific planet."""
```

**Implementation Checklist:**

- [ ] Input validation and query parameters
- [ ] Service layer calls
- [ ] Response formatting
- [ ] Error handling
- [ ] Write 15+ endpoint tests

---

## Response Schema Definitions

### Key Schemas Needed

```python
class BirthChartRequest(BaseModel):
    name: str
    date: datetime
    time: str  # HH:MM:SS
    latitude: float
    longitude: float
    timezone: str

class BirthChartResponse(BaseModel):
    chart_id: str
    user_id: str
    name: str
    date: datetime
    time: str
    latitude: float
    longitude: float
    planetary_positions: Dict[str, Position]
    kp_houses: Dict[str, House]
    created_at: datetime
    updated_at: datetime

class PredictionRequest(BaseModel):
    chart_id: str
    prediction_type: str  # "general", "career", "health", etc.
    target_date: Optional[datetime] = None
    duration_days: int = 30

class PredictionResponse(BaseModel):
    prediction_id: str
    user_id: str
    chart_id: str
    prediction_type: str
    description: str
    confidence_score: float
    predicted_events: List[str]
    created_at: datetime
    updated_at: datetime

class TransitEventResponse(BaseModel):
    planet: str
    house: int
    date: datetime
    significance: str  # "major", "minor"
    interpretation: str

class RemedyResponse(BaseModel):
    remedy_id: str
    planet: str
    remedy_type: str
    description: str
    effectiveness: float
    implementation_difficulty: int  # 1-5
```

---

## Integration Testing Strategy

### Test Coverage Goals

- **Unit Tests:** 40+ tests for service layer
- **Integration Tests:** 30+ tests for endpoints
- **End-to-End Tests:** 15+ tests for full workflows
- **Target Coverage:** 85%+

### Example Test Cases

```python
# Service Layer Tests
def test_calculate_birth_chart_valid_data()
def test_calculate_birth_chart_invalid_timezone()
def test_calculate_transits_for_date()
def test_dasha_period_calculation()

# Endpoint Tests
def test_create_prediction_success()
def test_create_prediction_invalid_chart_id()
def test_list_predictions_with_filtering()
def test_get_current_transits()
def test_delete_prediction_removes_from_db()

# End-to-End Tests
def test_full_prediction_workflow()
def test_chart_generation_and_analysis()
```

---

## Dependencies & Configuration

### Required Packages (Already Installed)

- FastAPI ✅
- SQLAlchemy ✅
- Pydantic v2 ✅
- PyJWT ✅
- Passlib + Bcrypt ✅

### Python Calculation Libraries (Phase 2)

- `calculations/kp_calculator.py` ✅
- `calculations/dasha_calculator.py` ✅
- `calculations/transit_calculator.py` ✅
- `calculations/ephemeris_manager.py` ✅

### Environment Configuration

```bash
# .env
DB_DRIVER=sqlite
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
EPHEMERIS_DATA_PATH=./ephemeris_data/
CACHE_ENABLED=true
LOG_LEVEL=INFO
```

---

## Deployment Readiness Checklist

- [ ] All service classes implemented
- [ ] All API endpoints created
- [ ] 85%+ test coverage achieved
- [ ] Error handling comprehensive
- [ ] Audit logging on all operations
- [ ] API documentation (OpenAPI/Swagger)
- [ ] Database migrations ready
- [ ] Performance validated
- [ ] Security reviewed

---

## Success Criteria

✅ **By End of Days 3-4:**

1. All 5 service classes implemented
2. All core endpoints working (4+ endpoints)
3. 70+ endpoint tests passing
4. Swagger documentation generated
5. Full integration test suite created
6. Performance benchmarks show <500ms P95 latency

---

## Risk Mitigation

| Risk                                  | Mitigation                                    |
| ------------------------------------- | --------------------------------------------- |
| Integration bugs with Phase 2 engines | Early integration testing, mock first         |
| Performance issues with calculations  | Caching, query optimization, async operations |
| Schema mismatches                     | Strong typing with Pydantic, early validation |
| Database constraints                  | Schema review, constraint testing             |
| Rate limiting issues                  | Add tracking, implement later if needed       |

---

## Next Steps (After Week 2)

- Phase 3 Week 3: Performance testing, Docker containerization, CI/CD
- Phase 4: Frontend integration, user dashboard, advanced analytics

---

**Ready to begin Phase 3 Week 2? Proceed with:**

1. Analysis of Phase 2 calculation engine APIs
2. Service layer interface design
3. Database schema finalization
4. Test fixture preparation
