"""
Birth chart endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.database import User, BirthChart, DashaPeriod
from app.schemas.models import ChartCreate, ChartResponse

router = APIRouter()


@router.post("/create", response_model=ChartResponse)
async def create_chart(
    chart_data: ChartCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a birth chart with calculations.
    
    - Calculates planetary positions
    - Generates Vimshottari Dasha timeline
    - Stores in database
    - Returns chart with current dasha info
    
    Note: Vedic calculation engine integration needed
    """
    # TODO: Integrate with Vedic calculation engine
    # This would typically call your existing Mula dasha engine
    # For now, creating placeholder chart_data
    
    calculated_chart_data = {
        "planets": {
            "Sun": {"longitude": 120.5, "sign": "Cancer", "nakshatra": "Pushya"},
            "Moon": {"longitude": 245.3, "sign": "Sagittarius", "nakshatra": "Mula"},
            # ... other planets
        },
        "houses": {
            "1": {"cusp": 80.2, "sign": "Gemini"},
            # ... other houses
        },
        "ascendant": {"longitude": 80.2, "sign": "Gemini"}
    }
    
    # Calculate current dasha (placeholder)
    current_mahadasha = "Venus"
    current_antardasha = "Mercury"
    current_period_start = datetime.utcnow()
    current_period_end = datetime(2027, 5, 15)
    
    # Create birth chart
    new_chart = BirthChart(
        user_id=current_user.id,
        birth_date=chart_data.birth_date,
        birth_time=chart_data.birth_time,
        birth_latitude=chart_data.birth_latitude,
        birth_longitude=chart_data.birth_longitude,
        birth_location=chart_data.birth_location,
        timezone=chart_data.timezone,
        chart_data=calculated_chart_data,
        current_mahadasha=current_mahadasha,
        current_antardasha=current_antardasha,
        current_period_start=current_period_start,
        current_period_end=current_period_end
    )
    
    db.add(new_chart)
    db.commit()
    db.refresh(new_chart)
    
    # TODO: Generate and store full dasha timeline in DashaPeriod table
    # This would create multiple DashaPeriod records for the full 120-year cycle
    
    return new_chart


@router.get("/{chart_id}", response_model=ChartResponse)
async def get_chart(
    chart_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get birth chart by ID.
    
    - Returns chart data
    - Includes current dasha information
    - User can only access their own charts
    """
    chart = db.query(BirthChart).filter(
        BirthChart.id == chart_id,
        BirthChart.user_id == current_user.id
    ).first()
    
    if not chart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chart not found"
        )
    
    return chart


@router.get("/", response_model=list[ChartResponse])
async def list_charts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all birth charts for current user.
    """
    charts = db.query(BirthChart).filter(
        BirthChart.user_id == current_user.id
    ).order_by(BirthChart.created_at.desc()).all()
    
    return charts
