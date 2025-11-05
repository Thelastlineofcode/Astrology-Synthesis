"""
Dasha period endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.database import User, BirthChart, DashaPeriod
from app.schemas.models import CurrentDashaResponse, DashaPeriodResponse

router = APIRouter()


@router.get("/current", response_model=CurrentDashaResponse)
async def get_current_dasha(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current dasha period for user.
    
    - Returns current Mahadasha, Antardasha, Pratyantardasha
    - Includes interpretation and themes
    - Calculates days remaining
    """
    # Get user's birth chart
    chart = db.query(BirthChart).filter(
        BirthChart.user_id == current_user.id
    ).first()
    
    if not chart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No birth chart found. Please create one first."
        )
    
    # Calculate days remaining
    if chart.current_period_end:
        days_remaining = (chart.current_period_end - datetime.utcnow()).days
    else:
        days_remaining = 0
    
    # Get interpretation (placeholder - would come from knowledge base)
    interpretation = f"{chart.current_mahadasha} mahadasha with {chart.current_antardasha} antardasha brings transformation and growth."
    
    themes = ["transformation", "communication", "relationships", "career advancement"]
    
    return CurrentDashaResponse(
        mahadasha=chart.current_mahadasha or "Unknown",
        antardasha=chart.current_antardasha or "Unknown",
        pratyantardasha=chart.current_pratyantardasha,
        period_start=chart.current_period_start or datetime.utcnow(),
        period_end=chart.current_period_end or datetime.utcnow(),
        days_remaining=days_remaining,
        interpretation=interpretation,
        themes=themes
    )


@router.get("/timeline", response_model=list[DashaPeriodResponse])
async def get_dasha_timeline(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get full dasha timeline (past, present, future).
    
    - Returns all Mahadasha periods
    - Optionally includes Antardasha and Pratyantardasha levels
    - Sorted by period_start
    """
    # Get user's birth chart
    chart = db.query(BirthChart).filter(
        BirthChart.user_id == current_user.id
    ).first()
    
    if not chart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No birth chart found. Please create one first."
        )
    
    # Get all dasha periods for this chart
    periods = db.query(DashaPeriod).filter(
        DashaPeriod.chart_id == chart.id
    ).order_by(DashaPeriod.period_start).all()
    
    if not periods:
        # TODO: Generate dasha timeline if not exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dasha timeline not yet calculated. This will be auto-generated soon."
        )
    
    return periods


@router.get("/meanings/{planet}")
async def get_dasha_meanings(
    planet: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get meanings and interpretations for a specific dasha lord.
    
    - Returns general themes for the planet
    - House-specific interpretations
    - Remedies and recommendations
    
    Note: This would integrate with your astrology knowledge base
    """
    # Placeholder meanings - would come from knowledge base
    meanings = {
        "Sun": {
            "themes": ["leadership", "authority", "father", "government", "health"],
            "general": "Sun dasha brings focus on career, authority, and personal power. Time for leadership roles.",
            "positive": ["career advancement", "recognition", "confidence boost"],
            "negative": ["ego conflicts", "health issues", "government troubles"],
            "remedies": ["Surya Namaskar", "Ruby gemstone", "Sunday fasting"]
        },
        "Moon": {
            "themes": ["emotions", "mother", "mind", "public", "travel"],
            "general": "Moon dasha emphasizes emotional life, family matters, and mental peace.",
            "positive": ["emotional fulfillment", "family harmony", "public recognition"],
            "negative": ["mood swings", "anxiety", "sleep issues"],
            "remedies": ["Moon mantra", "Pearl gemstone", "Monday fasting"]
        },
        "Venus": {
            "themes": ["love", "marriage", "luxury", "arts", "vehicles"],
            "general": "Venus dasha brings romance, luxury, and artistic pursuits to the forefront.",
            "positive": ["romantic relationships", "financial gains", "artistic success"],
            "negative": ["relationship troubles", "overspending", "health issues related to reproductive organs"],
            "remedies": ["Venus mantra", "Diamond/White Sapphire", "Friday fasting"]
        },
        "Mercury": {
            "themes": ["communication", "business", "education", "siblings", "short travels"],
            "general": "Mercury dasha enhances communication, learning, and business opportunities.",
            "positive": ["educational success", "business growth", "improved communication"],
            "negative": ["nervous disorders", "speech problems", "financial losses in speculation"],
            "remedies": ["Mercury mantra", "Emerald gemstone", "Wednesday fasting"]
        }
    }
    
    planet_capitalized = planet.capitalize()
    if planet_capitalized not in meanings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meanings for {planet} not found. Available: Sun, Moon, Venus, Mercury"
        )
    
    return {
        "planet": planet_capitalized,
        "meanings": meanings[planet_capitalized]
    }
