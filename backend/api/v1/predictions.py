"""Prediction endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from uuid import UUID
from backend.config.database import get_db
from backend.services.calculation_service import CalculationService
from backend.models.database import Prediction, PredictionEvent, User
from backend.schemas import (
    PredictionRequest, PredictionResponse, PredictionEventData,
    PredictionWithRemedies
)
from backend.api.v1.auth import get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/predict", tags=["Predictions"])
calc_service = CalculationService()


@router.post("", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
async def create_prediction(
    prediction_request: PredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generate comprehensive astrological prediction.
    
    Takes birth data and a prediction query, returns syncretic analysis
    combining KP Astrology, Vimshottari Dasha, and Transit analysis.
    
    **Confidence Score Calculation:**
    - confidence = (KP_score × 0.6) + (Dasha_score × 0.4)
    - Range: 0.0 to 1.0
    """
    try:
        # Generate syncretic prediction
        result = calc_service.get_syncretic_prediction(
            birth_data=prediction_request.birth_data,
            query=prediction_request.query,
            prediction_window_days=prediction_request.prediction_window_days,
        )
        
        # Calculate prediction window
        prediction_start = datetime.utcnow()
        prediction_end = prediction_start + timedelta(days=prediction_request.prediction_window_days)
        
        # Store prediction in database
        db_prediction = Prediction(
            user_id=current_user.user_id,
            chart_id=None,  # Will be populated if chart is saved
            query_text=prediction_request.query,
            query_date=datetime.utcnow(),
            prediction_start_date=prediction_start,
            prediction_end_date=prediction_end,
            prediction_data={
                "events": [e.dict() for e in result.events],
                "query": prediction_request.query,
            },
            confidence_score=result.confidence_score,
            kp_contribution=result.kp_contribution,
            dasha_contribution=result.dasha_contribution,
            transit_contribution=result.transit_contribution,
            model_version="1.0.0",
            calculation_time_ms=int(result.calculation_time_ms),
        )
        
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        
        logger.info(f"✅ Prediction created: {db_prediction.prediction_id}")
        
        return PredictionResponse(
            prediction_id=db_prediction.prediction_id,
            user_id=current_user.user_id,
            query=prediction_request.query,
            prediction_window_start=prediction_start,
            prediction_window_end=prediction_end,
            confidence_score=result.confidence_score,
            events=result.events,
            kp_contribution=result.kp_contribution,
            dasha_contribution=result.dasha_contribution,
            transit_contribution=result.transit_contribution,
            model_version="1.0.0",
            calculation_time_ms=int(result.calculation_time_ms),
            created_at=db_prediction.created_at,
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Prediction generation failed",
        )


@router.get("/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(
    prediction_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve a stored prediction by ID.
    """
    try:
        prediction = db.query(Prediction).filter(
            Prediction.prediction_id == prediction_id,
            Prediction.user_id == current_user.user_id,
        ).first()
        
        if not prediction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prediction not found",
            )
        
        # Reconstruct events from stored data
        events = prediction.prediction_data.get("events", [])
        
        return PredictionResponse(
            prediction_id=prediction.prediction_id,
            user_id=prediction.user_id,
            query=prediction.query_text,
            prediction_window_start=prediction.prediction_start_date,
            prediction_window_end=prediction.prediction_end_date,
            confidence_score=prediction.confidence_score,
            events=[PredictionEventData(**e) for e in events],
            kp_contribution=prediction.kp_contribution,
            dasha_contribution=prediction.dasha_contribution,
            transit_contribution=prediction.transit_contribution,
            model_version=prediction.model_version,
            calculation_time_ms=prediction.calculation_time_ms,
            created_at=prediction.created_at,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve prediction",
        )


@router.get("", response_model=list[PredictionResponse])
async def list_predictions(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    List user's predictions with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Number of records to return (default: 10, max: 100)
    """
    try:
        if limit > 100:
            limit = 100
        
        predictions = db.query(Prediction).filter(
            Prediction.user_id == current_user.user_id,
        ).order_by(
            Prediction.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        result = []
        for prediction in predictions:
            events = prediction.prediction_data.get("events", [])
            result.append(PredictionResponse(
                prediction_id=prediction.prediction_id,
                user_id=prediction.user_id,
                query=prediction.query_text,
                prediction_window_start=prediction.prediction_start_date,
                prediction_window_end=prediction.prediction_end_date,
                confidence_score=prediction.confidence_score,
                events=[PredictionEventData(**e) for e in events],
                kp_contribution=prediction.kp_contribution,
                dasha_contribution=prediction.dasha_contribution,
                transit_contribution=prediction.transit_contribution,
                model_version=prediction.model_version,
                calculation_time_ms=prediction.calculation_time_ms,
                created_at=prediction.created_at,
            ))
        
        return result
        
    except Exception as e:
        logger.error(f"List predictions error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list predictions",
        )
