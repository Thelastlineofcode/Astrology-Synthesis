"""Birth chart endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from backend.config.database import get_db
from backend.services.calculation_service import CalculationService
from backend.models.database import BirthChart, User
from backend.schemas import (
    CreateBirthChartRequest, BirthChartResponse, BirthChartData
)
from backend.api.v1.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chart", tags=["Charts"])
calc_service = CalculationService()


@router.post("", response_model=BirthChartResponse, status_code=status.HTTP_201_CREATED)
async def create_birth_chart(
    chart_request: CreateBirthChartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generate and store a birth chart.
    
    Computes planetary positions, house cusps, aspects, and other
    astrological data for the given birth time and location.
    """
    try:
        # Generate birth chart
        chart_data = calc_service.generate_birth_chart(chart_request.birth_data)
        
        # Store in database
        db_chart = BirthChart(
            user_id=current_user.user_id,
            birth_date=chart_request.birth_data.date,
            birth_time=chart_request.birth_data.time,
            birth_latitude=chart_request.birth_data.latitude,
            birth_longitude=chart_request.birth_data.longitude,
            timezone=chart_request.birth_data.timezone,
            birth_location=chart_request.birth_data.location_name,
            chart_data=chart_data,
            ayanamsa=chart_request.ayanamsa,
            house_system=chart_request.house_system or "PLACIDUS",
        )
        
        db.add(db_chart)
        db.commit()
        db.refresh(db_chart)
        
        logger.info(f"✅ Birth chart created: {db_chart.chart_id}")
        
        return BirthChartResponse(
            chart_id=db_chart.chart_id,
            user_id=current_user.user_id,
            birth_date=db_chart.birth_date,
            birth_time=db_chart.birth_time,
            birth_latitude=db_chart.birth_latitude,
            birth_longitude=db_chart.birth_longitude,
            timezone=db_chart.timezone,
            birth_location=db_chart.birth_location,
            chart_data=chart_data,
            ayanamsa=db_chart.ayanamsa,
            house_system=db_chart.house_system,
            created_at=db_chart.created_at,
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Birth chart generation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Birth chart generation failed",
        )


@router.get("/{chart_id}", response_model=BirthChartResponse)
async def get_birth_chart(
    chart_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve a stored birth chart."""
    try:
        chart = db.query(BirthChart).filter(
            BirthChart.chart_id == chart_id,
            BirthChart.user_id == current_user.user_id,
        ).first()
        
        if not chart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Birth chart not found",
            )
        
        return BirthChartResponse(
            chart_id=chart.chart_id,
            user_id=chart.user_id,
            birth_date=chart.birth_date,
            birth_latitude=chart.birth_latitude,
            birth_longitude=chart.birth_longitude,
            birth_timezone=chart.birth_timezone,
            birth_location_name=chart.birth_location_name,
            chart_data=BirthChartData(**chart.chart_data),
            ayanamsa=chart.ayanamsa,
            name=chart.name,
            created_at=chart.created_at,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get chart error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve chart",
        )


@router.get("", response_model=list[BirthChartResponse])
async def list_charts(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List user's birth charts."""
    try:
        if limit > 100:
            limit = 100
        
        charts = db.query(BirthChart).filter(
            BirthChart.user_id == current_user.user_id,
        ).order_by(
            BirthChart.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        return [
            BirthChartResponse(
                chart_id=chart.chart_id,
                user_id=chart.user_id,
                birth_date=chart.birth_date,
                birth_latitude=chart.birth_latitude,
                birth_longitude=chart.birth_longitude,
                birth_timezone=chart.birth_timezone,
                birth_location_name=chart.birth_location_name,
                chart_data=BirthChartData(**chart.chart_data),
                ayanamsa=chart.ayanamsa,
                name=chart.name,
                created_at=chart.created_at,
            )
            for chart in charts
        ]
        
    except Exception as e:
        logger.error(f"List charts error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list charts",
        )
