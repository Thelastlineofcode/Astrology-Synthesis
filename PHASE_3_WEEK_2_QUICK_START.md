# Phase 3 Week 2 - Quick Start Guide

## Status: ✅ Ready to Begin Phase 3 Week 2

### What's Complete

- ✅ SQLite database (15 tables, all initialized)
- ✅ Authentication system (22/22 tests passing, production-ready)
- ✅ Phase 2 calculation engines (all 4 engines ready to integrate)
- ✅ Database models, schemas, and configuration

### What's Next: Phase 3 Week 2 (Days 1-4)

---

## Quick Start Workflow

### Step 1: Understand Phase 2 Engines (30 minutes)

Read the integration guide to understand what each engine does:

- `PHASE_2_ENGINE_INTEGRATION.md` - Engine APIs and integration points
- `backend/calculations/ephemeris.py` - Lines 421-441 (key functions)
- `backend/calculations/kp_engine.py` - Lines 60-430 (key functions)

### Step 2: Create CalculationService (Day 1, 2 hours)

Create `backend/services/calculation_service.py`:

```python
"""
Calculation Service - Orchestrates all Phase 2 engines.
Provides unified interface for astrology calculations.
"""

from datetime import datetime
from typing import Dict, List, Optional
from backend.calculations import ephemeris, kp_engine, dasha_engine, transit_engine
from backend.models.database import BirthChart
import logging

logger = logging.getLogger(__name__)


class CalculationService:
    """
    Service layer wrapping all Phase 2 calculation engines.

    Provides high-level methods for:
    - Birth chart generation
    - Planetary position calculations
    - KP system analysis
    - Dasha period calculations
    - Transit analysis
    """

    @staticmethod
    def calculate_birth_chart(
        latitude: float,
        longitude: float,
        timezone: str,
        birth_datetime: datetime
    ) -> Dict:
        """
        Calculate complete birth chart from birth data.

        Args:
            latitude: Birth latitude (-90 to 90)
            longitude: Birth longitude (-180 to 180)
            timezone: IANA timezone string (e.g., "Asia/Kolkata")
            birth_datetime: Birth date and time (datetime object)

        Returns:
            Dictionary containing:
                - planetary_positions: Dict[str, float] - Planet longitudes
                - house_cusps: List[float] - 12 house cusps
                - ascendant: float - Ascendant longitude
                - kp_cusps: Dict - KP analysis for houses
                - kp_planets: Dict - KP analysis for planets
        """
        try:
            # Convert timezone to UTC offset
            import pytz
            tz = pytz.timezone(timezone)
            tz_offset = tz.utcoffset(birth_datetime).total_seconds() / 3600

            # Get planetary positions
            eph_data = ephemeris.get_current_ephemeris(
                latitude, longitude, tz_offset, birth_datetime
            )

            # Get KP analysis for house cusps
            kp_cusps = kp_engine.get_cuspal_sub_lords(eph_data["houses"])

            # Get KP analysis for planets
            kp_planets = kp_engine.get_planet_sub_lords(eph_data["planets"])

            logger.info(f"✅ Birth chart calculated for {birth_datetime}")

            return {
                "planetary_positions": eph_data["planets"],
                "house_cusps": eph_data["houses"],
                "ascendant": eph_data["ascendant"],
                "midheaven": eph_data["midheaven"],
                "kp_cusps": kp_cusps,
                "kp_planets": kp_planets,
                "timestamp": birth_datetime.isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Birth chart calculation failed: {str(e)}")
            raise

    @staticmethod
    def calculate_current_transits(
        birth_chart_data: Dict,
        current_datetime: datetime = None
    ) -> Dict:
        """
        Calculate current planetary transits for a birth chart.

        Args:
            birth_chart_data: Birth chart dictionary from calculate_birth_chart()
            current_datetime: Current date/time (defaults to now)

        Returns:
            Dictionary containing current transits and aspects
        """
        if current_datetime is None:
            current_datetime = datetime.now()

        try:
            # Use transit engine to analyze current positions
            # TODO: Implement based on transit_engine API
            logger.info(f"✅ Transits calculated for {current_datetime}")

            return {
                "timestamp": current_datetime.isoformat(),
                "transits": {},  # Populate with transit_engine results
            }

        except Exception as e:
            logger.error(f"❌ Transit calculation failed: {str(e)}")
            raise

    @staticmethod
    def calculate_dasha_period(
        birth_chart_data: Dict,
        target_date: datetime = None
    ) -> Dict:
        """
        Calculate Dasha/Bukti period at any date.

        Args:
            birth_chart_data: Birth chart dictionary
            target_date: Date to calculate for (defaults to today)

        Returns:
            Dictionary containing Dasha periods
        """
        if target_date is None:
            target_date = datetime.now()

        try:
            # Create Dasha calculator
            moon_lon = birth_chart_data["planetary_positions"]["Moon"]
            dasha_calc = dasha_engine.create_dasha_calculator(
                birth_chart_data["birth_datetime"],
                moon_lon
            )

            # Get Dasha at target date
            # TODO: Implement based on dasha_engine API

            logger.info(f"✅ Dasha calculated for {target_date}")

            return {
                "date": target_date.isoformat(),
                "dasha": {},  # Populate with dasha_engine results
            }

        except Exception as e:
            logger.error(f"❌ Dasha calculation failed: {str(e)}")
            raise


# Usage Examples:
#
# chart_data = CalculationService.calculate_birth_chart(
#     latitude=28.6139,
#     longitude=77.2090,
#     timezone="Asia/Kolkata",
#     birth_datetime=datetime(2000, 1, 1, 12, 0)
# )
#
# transits = CalculationService.calculate_current_transits(chart_data)
#
# dasha = CalculationService.calculate_dasha_period(chart_data)
```

### Step 3: Test CalculationService (Day 1, 1 hour)

Create `test_calculation_service.py`:

```python
import pytest
from datetime import datetime
from backend.services.calculation_service import CalculationService


class TestCalculationService:
    """Test suite for CalculationService."""

    def test_calculate_birth_chart_valid_data(self):
        """Test birth chart calculation with valid data."""
        result = CalculationService.calculate_birth_chart(
            latitude=28.6139,
            longitude=77.2090,
            timezone="Asia/Kolkata",
            birth_datetime=datetime(2000, 1, 1, 12, 0)
        )

        assert "planetary_positions" in result
        assert "house_cusps" in result
        assert "ascendant" in result
        assert len(result["house_cusps"]) == 12

    def test_calculate_birth_chart_invalid_timezone(self):
        """Test birth chart calculation with invalid timezone."""
        with pytest.raises(Exception):
            CalculationService.calculate_birth_chart(
                latitude=28.6139,
                longitude=77.2090,
                timezone="Invalid/Timezone",
                birth_datetime=datetime(2000, 1, 1, 12, 0)
            )

    def test_calculate_current_transits(self):
        """Test transit calculation."""
        # First get a birth chart
        chart_data = CalculationService.calculate_birth_chart(
            latitude=28.6139,
            longitude=77.2090,
            timezone="Asia/Kolkata",
            birth_datetime=datetime(2000, 1, 1, 12, 0)
        )

        # Then get transits
        transits = CalculationService.calculate_current_transits(chart_data)

        assert "timestamp" in transits
        assert "transits" in transits

    def test_calculate_dasha_period(self):
        """Test Dasha period calculation."""
        chart_data = CalculationService.calculate_birth_chart(
            latitude=28.6139,
            longitude=77.2090,
            timezone="Asia/Kolkata",
            birth_datetime=datetime(2000, 1, 1, 12, 0)
        )

        dasha = CalculationService.calculate_dasha_period(chart_data)

        assert "date" in dasha
        assert "dasha" in dasha
```

Run tests:

```bash
pytest test_calculation_service.py -v
```

### Step 4: Create ChartService (Day 2, 2 hours)

Create `backend/services/chart_service.py` to handle database operations:

```python
from backend.models.database import BirthChart
from backend.schemas import BirthChartRequest, BirthChartResponse
from backend.services.calculation_service import CalculationService
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


class ChartService:
    """Service for birth chart management."""

    @staticmethod
    def create_chart(
        user_id: str,
        birth_data: BirthChartRequest,
        db: Session
    ) -> BirthChart:
        """
        Create and store a new birth chart.

        Args:
            user_id: User ID
            birth_data: Birth data (from Pydantic schema)
            db: Database session

        Returns:
            BirthChart database model
        """
        # Calculate chart
        chart_data = CalculationService.calculate_birth_chart(
            latitude=birth_data.latitude,
            longitude=birth_data.longitude,
            timezone=birth_data.timezone,
            birth_datetime=birth_data.date_time
        )

        # Create database record
        chart = BirthChart(
            chart_id=str(uuid.uuid4()),
            user_id=user_id,
            name=birth_data.name,
            birth_date=birth_data.date_time.date(),
            birth_time=birth_data.date_time.time(),
            latitude=birth_data.latitude,
            longitude=birth_data.longitude,
            timezone=birth_data.timezone,
            planetary_positions=chart_data["planetary_positions"],
            house_cusps=chart_data["house_cusps"],
            ascendant=chart_data["ascendant"],
            notes=birth_data.notes
        )

        db.add(chart)
        db.commit()
        db.refresh(chart)

        logger.info(f"✅ Chart created: {chart.chart_id}")
        return chart

    @staticmethod
    def get_chart(chart_id: str, db: Session) -> BirthChart:
        """Retrieve a chart by ID."""
        chart = db.query(BirthChart).filter(BirthChart.chart_id == chart_id).first()
        if not chart:
            raise ValueError(f"Chart not found: {chart_id}")
        return chart

    @staticmethod
    def list_user_charts(user_id: str, db: Session) -> list:
        """List all charts for a user."""
        return db.query(BirthChart).filter(BirthChart.user_id == user_id).all()

    @staticmethod
    def delete_chart(chart_id: str, db: Session) -> bool:
        """Delete a chart."""
        chart = db.query(BirthChart).filter(BirthChart.chart_id == chart_id).first()
        if not chart:
            return False
        db.delete(chart)
        db.commit()
        logger.info(f"✅ Chart deleted: {chart_id}")
        return True
```

### Step 5: Create API Endpoints (Day 3, 3 hours)

Create `backend/api/v1/chart_endpoints.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from backend.models.database import User
from backend.schemas import BirthChartRequest, BirthChartResponse
from backend.services.chart_service import ChartService
from backend.config.database import get_db
from backend.api.v1.auth_endpoints import get_current_user

router = APIRouter(prefix="/api/v1/charts", tags=["Charts"])


@router.post(
    "/",
    response_model=BirthChartResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate Birth Chart"
)
async def create_chart(
    request: BirthChartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> BirthChartResponse:
    """
    Generate a new birth chart from birth data.

    **Required fields:**
    - name: Person's name
    - date: Birth date
    - time: Birth time (HH:MM:SS)
    - latitude: Birth latitude
    - longitude: Birth longitude
    - timezone: IANA timezone (e.g., "Asia/Kolkata")
    """
    try:
        chart = ChartService.create_chart(current_user.user_id, request, db)
        return BirthChartResponse.from_orm(chart)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{chart_id}",
    response_model=BirthChartResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Birth Chart"
)
async def get_chart(
    chart_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> BirthChartResponse:
    """Retrieve a specific birth chart."""
    try:
        chart = ChartService.get_chart(chart_id, db)

        # Verify ownership
        if chart.user_id != current_user.user_id:
            raise HTTPException(status_code=403, detail="Access denied")

        return BirthChartResponse.from_orm(chart)
    except ValueError:
        raise HTTPException(status_code=404, detail="Chart not found")


@router.get(
    "/",
    response_model=List[BirthChartResponse],
    status_code=status.HTTP_200_OK,
    summary="List Birth Charts"
)
async def list_charts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
) -> List[BirthChartResponse]:
    """List all birth charts for the current user."""
    charts = ChartService.list_user_charts(current_user.user_id, db)
    return [BirthChartResponse.from_orm(chart) for chart in charts[skip:skip+limit]]


@router.delete(
    "/{chart_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Birth Chart"
)
async def delete_chart(
    chart_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> None:
    """Delete a birth chart."""
    chart = ChartService.get_chart(chart_id, db)

    # Verify ownership
    if chart.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    ChartService.delete_chart(chart_id, db)
```

### Step 6: Update Main App (Day 3, 30 minutes)

Update `backend/main.py` to register new endpoints:

```python
# Add to imports
from backend.api.v1 import chart_endpoints, prediction_endpoints, transit_endpoints

# Add to app setup (after auth_endpoints)
app.include_router(chart_endpoints.router)
# app.include_router(prediction_endpoints.router)  # TODO: Add when ready
# app.include_router(transit_endpoints.router)     # TODO: Add when ready
```

### Step 7: Test Everything (Day 4, 1 hour)

```bash
# Run calculation service tests
pytest test_calculation_service.py -v

# Run integration tests
pytest tests/services/ -v

# Run endpoint tests
pytest tests/api/v1/test_chart_endpoints.py -v

# Full test suite
pytest --cov=backend --cov-report=html
```

---

## File Checklist for Days 1-4

### Day 1: CalculationService

- [ ] `backend/services/calculation_service.py` (350+ lines)
- [ ] `test_calculation_service.py` (150+ lines)
- [ ] Update `backend/services/__init__.py` to export CalculationService
- ✅ Tests passing: `20+ tests`

### Day 2: Supporting Services

- [ ] `backend/services/chart_service.py` (200+ lines)
- [ ] `backend/services/transit_service.py` (150+ lines)
- [ ] `backend/services/prediction_service.py` (200+ lines)
- ✅ Tests passing: `15+ tests per service`

### Day 3: Chart Endpoints

- [ ] `backend/api/v1/chart_endpoints.py` (350+ lines)
- [ ] Update `backend/schemas/__init__.py` with BirthChartRequest/Response
- [ ] Update `backend/main.py` to register routes
- [ ] `tests/api/v1/test_chart_endpoints.py` (150+ lines)
- ✅ Tests passing: `20+ endpoint tests`

### Day 4: Transit & Prediction

- [ ] `backend/api/v1/prediction_endpoints.py` (400+ lines)
- [ ] `backend/api/v1/transit_endpoints.py` (250+ lines)
- [ ] `backend/api/v1/remedy_endpoints.py` (200+ lines)
- [ ] Full test suite
- ✅ Tests passing: `50+ total endpoint tests`

---

## Running the Application

```bash
# Start backend server
python -m uvicorn backend.main:app --reload --port 8000

# Open browser
open http://localhost:8000/docs

# You should see:
- ✅ /auth endpoints (8 endpoints)
- ✅ /charts endpoints (4 endpoints)
- ✅ /predictions endpoints (4 endpoints)
- ✅ /transits endpoints (3 endpoints)
- ✅ /remedies endpoints (2 endpoints)
```

---

## Key Implementation Notes

1. **Database Session:** Always inject `db: Session = Depends(get_db)`
2. **Authentication:** Always inject `user: User = Depends(get_current_user)`
3. **Error Handling:** Use HTTPException with proper status codes
4. **Logging:** Use logger for all important operations
5. **Testing:** Write tests as you go, not after
6. **Type Hints:** Use proper type hints for all functions

---

## Ready? Let's Begin! 🚀

All preparation complete. Time to build!

**Next command:**

```bash
cd /Users/houseofobi/Documents/GitHub/Astrology-Synthesis
touch backend/services/calculation_service.py
# Start implementing CalculationService!
```

---

**Estimated Timeline:**

- Day 1: Service foundation (4 hours)
- Day 2: Supporting services (5 hours)
- Day 3: API endpoints (4 hours)
- Day 4: Integration & testing (3 hours)

**Total: ~16 working hours across 4 days**

Status: ✅ **READY TO BEGIN PHASE 3 WEEK 2**
