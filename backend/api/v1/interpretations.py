"""Interpretation API endpoints."""

from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Optional
import logging

from backend.services.interpretation_service import create_interpretation_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/interpretations", tags=["interpretations"])

# Initialize interpretation service
interpretation_service = create_interpretation_service()


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Interpretation service operational",
    }


@router.get("/templates")
def list_templates():
    """List available interpretation templates."""
    templates = interpretation_service.list_templates()
    return {
        "template_count": len(templates),
        "templates": templates,
    }


@router.post("/sun-sign")
def interpret_sun_sign(chart_data: Dict = Body(...)):
    """Generate Sun sign interpretation."""
    sun_sign = chart_data.get('sun_sign', 'Unknown')
    try:
        result = interpretation_service.generate_sun_sign_interpretation(sun_sign, chart_data)
        return result
    except Exception as e:
        logger.error(f"Sun sign interpretation error: {e}")
        raise HTTPException(status_code=500, detail="Interpretation failed")


@router.post("/moon-sign")
def interpret_moon_sign(chart_data: Dict = Body(...)):
    """Generate Moon sign interpretation."""
    moon_sign = chart_data.get('moon_sign', 'Unknown')
    try:
        result = interpretation_service.generate_moon_sign_interpretation(moon_sign, chart_data)
        return result
    except Exception as e:
        logger.error(f"Moon sign interpretation error: {e}")
        raise HTTPException(status_code=500, detail="Interpretation failed")


@router.post("/ascendant")
def interpret_ascendant(chart_data: Dict = Body(...)):
    """Generate Ascendant interpretation."""
    ascendant = chart_data.get('ascendant', 'Unknown')
    try:
        result = interpretation_service.generate_ascendant_interpretation(ascendant, chart_data)
        return result
    except Exception as e:
        logger.error(f"Ascendant interpretation error: {e}")
        raise HTTPException(status_code=500, detail="Interpretation failed")


@router.post("/vedic")
def interpret_vedic(chart_data: Dict = Body(...)):
    """Generate Vedic astrology interpretation."""
    try:
        result = interpretation_service.generate_vedic_interpretation(chart_data)
        return result
    except Exception as e:
        logger.error(f"Vedic interpretation error: {e}")
        raise HTTPException(status_code=500, detail="Interpretation failed")


@router.post("/health")
def interpret_health(chart_data: Dict = Body(...)):
    """Generate health interpretation using Ayurveda."""
    try:
        result = interpretation_service.generate_health_interpretation(chart_data)
        return result
    except Exception as e:
        logger.error(f"Health interpretation error: {e}")
        raise HTTPException(status_code=500, detail="Interpretation failed")


@router.post("/full-chart")
def interpret_full_chart(chart_data: Dict = Body(...)):
    """Generate comprehensive chart interpretation."""
    try:
        result = interpretation_service.generate_full_interpretation(chart_data)
        return result
    except Exception as e:
        logger.error(f"Full chart interpretation error: {e}")
        raise HTTPException(status_code=500, detail="Interpretation failed")
