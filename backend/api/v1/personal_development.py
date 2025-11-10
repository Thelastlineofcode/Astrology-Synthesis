"""
Personal Development API Endpoints

FastAPI endpoints for personal development, coaching, and team building.

CRITICAL LEGAL NOTICE:
This API provides personal development insights ONLY. It is NOT intended for
and must NOT be used for hiring, promotion, performance evaluation, or any
employment decisions. Misuse may violate employment discrimination laws.

Intended Use:
- Personal development coaching
- Team building activities
- Wellness program integration
- Self-awareness exercises
- Communication style mapping

Prohibited Use:
- Hiring decisions
- Promotion decisions
- Performance reviews
- Employee assessment
- Compensation decisions
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import date
import logging
import os

from backend.calculations.personal_development_engine import (
    FlexibleBirthData,
    FlexibleInsightsEngine,
    DataCompleteness,
)
from backend.calculations.team_dynamics_engine import TeamDynamicsEngine
from backend.calculations.numerology_engine import NumerologyCalculator
from backend.agents.personal_development_agent import PersonalDevelopmentAgent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/personal-development", tags=["personal-development"])

# Initialize services
insights_engine = FlexibleInsightsEngine()
team_engine = TeamDynamicsEngine()
numerology_calc = NumerologyCalculator()


# Request/Response Models
class FlexiblePersonalReadingRequest(BaseModel):
    """
    Flexible personal reading request.

    Works with ANY level of birth data completeness.
    """
    # Required: Just birth date
    birth_date: str = Field(..., description="Birth date (YYYY-MM-DD)")

    # Optional: Adds name-based numerology
    full_name: Optional[str] = Field(None, description="Full birth name (optional)")

    # Optional: Adds basic astrology
    birth_time: Optional[str] = Field(None, description="Birth time HH:MM:SS (optional)")

    # Optional: Enables full astrology
    birth_location: Optional[str] = Field(None, description="Birth location name (optional)")
    latitude: Optional[float] = Field(None, description="Birth latitude (optional)")
    longitude: Optional[float] = Field(None, description="Birth longitude (optional)")
    timezone: Optional[str] = Field(None, description="Timezone (optional)")

    # Options
    include_coaching_prompts: bool = Field(
        default=True,
        description="Include coaching conversation prompts"
    )


class QuickNumerologyRequest(BaseModel):
    """Quick numerology calculation (date only)."""
    birth_date: str = Field(..., description="Birth date (YYYY-MM-DD)")
    full_name: Optional[str] = Field(None, description="Full name (optional)")


class TeamAnalysisRequest(BaseModel):
    """Team dynamics analysis request."""
    team_name: str = Field(..., description="Team name")
    team_members: List[Dict[str, Any]] = Field(
        ...,
        description="List of team member data (each with birth_date, optional full_name, etc.)"
    )
    include_pairwise_analysis: bool = Field(
        default=True,
        description="Include pairwise synergy analysis"
    )


class AgentCoachingRequest(BaseModel):
    """AI agent coaching session request."""
    birth_date: str = Field(..., description="Birth date (YYYY-MM-DD)")
    full_name: Optional[str] = Field(None, description="Full name (optional)")
    coaching_query: str = Field(
        ...,
        description="Specific coaching question or topic"
    )


class PersonalReadingResponse(BaseModel):
    """Personal development reading response."""
    status: str
    data_completeness: str
    available_analyses: List[str]

    # Numerology (always present)
    life_path_number: int
    life_path_interpretation: str
    day_of_week: str
    day_of_week_insights: str

    # Name numerology (if provided)
    destiny_number: Optional[int] = None
    soul_urge_number: Optional[int] = None
    personality_number: Optional[int] = None

    # Astrology (if data available)
    sun_sign: Optional[str] = None
    moon_sign: Optional[str] = None
    rising_sign: Optional[str] = None

    # Synthesis
    strengths_themes: List[str]
    growth_opportunities: List[str]
    communication_style: Optional[str] = None

    # Coaching
    reflection_prompts: Optional[List[str]] = None

    # Legal compliance
    disclaimer: str


class TeamAnalysisResponse(BaseModel):
    """Team dynamics analysis response."""
    status: str
    team_name: str
    member_count: int

    # Compatibility scores
    overall_synergy: float
    communication_compatibility: float
    strengths_diversity: float

    # Insights
    team_strengths: List[str]
    growth_areas: List[str]
    communication_tips: List[str]

    # Distributions
    life_path_distribution: Dict[int, int]
    element_balance: Optional[Dict[str, int]] = None

    # Pairwise (top synergies)
    top_synergies: Optional[List[Dict[str, Any]]] = None

    # Coaching
    team_coaching_prompts: List[str]

    # Legal compliance
    disclaimer: str


# Endpoints
@router.post("/reading", response_model=PersonalReadingResponse)
async def get_personal_reading(request: FlexiblePersonalReadingRequest):
    """
    Generate personal development reading from flexible birth data.

    This endpoint accepts ANY level of birth data completeness:
    - Minimum: Just birth date (provides numerology)
    - With name: Adds name-based numerology
    - With time: Adds basic astrology (sun sign)
    - With location: Adds full astrology (moon, rising, houses)

    More data = more comprehensive insights, but ALL requests get a reading.

    COMPLIANCE: This is a personal development tool, NOT for employment decisions.
    """
    try:
        logger.info(
            f"Personal reading request: date={request.birth_date}, "
            f"has_name={bool(request.full_name)}, has_time={bool(request.birth_time)}, "
            f"has_location={bool(request.latitude)}"
        )

        # Parse birth date
        from datetime import datetime
        birth_date = datetime.strptime(request.birth_date, "%Y-%m-%d").date()

        # Create flexible birth data
        birth_data = FlexibleBirthData(
            birth_date=birth_date,
            full_name=request.full_name,
            birth_time=request.birth_time,
            birth_location=request.birth_location,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone=request.timezone,
        )

        # Generate reading
        reading = insights_engine.generate_reading(
            birth_data,
            include_coaching_prompts=request.include_coaching_prompts,
        )

        # Format response
        return PersonalReadingResponse(
            status="success",
            data_completeness=reading.data_completeness.value,
            available_analyses=reading.available_analyses,
            life_path_number=reading.life_path_number,
            life_path_interpretation=reading.life_path_interpretation,
            day_of_week=reading.day_of_week,
            day_of_week_insights=reading.day_of_week_insights,
            destiny_number=reading.destiny_number,
            soul_urge_number=reading.soul_urge_number,
            personality_number=reading.personality_number,
            sun_sign=reading.sun_sign,
            moon_sign=reading.moon_sign,
            rising_sign=reading.rising_sign,
            strengths_themes=reading.strengths_themes,
            growth_opportunities=reading.growth_opportunities,
            communication_style=reading.communication_style,
            reflection_prompts=reading.reflection_prompts,
            disclaimer=reading.disclaimer,
        )

    except Exception as e:
        logger.error(f"Error generating personal reading: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/numerology")
async def calculate_numerology(request: QuickNumerologyRequest):
    """
    Quick numerology calculation (works with date only).

    Calculates life path number and optionally name-based numbers.
    Fastest endpoint, no astrology calculations needed.

    COMPLIANCE: Personal development tool only.
    """
    try:
        from datetime import datetime

        birth_date = datetime.strptime(request.birth_date, "%Y-%m-%d").date()

        numbers = numerology_calc.get_all_numbers(birth_date, request.full_name)
        interpretations = numerology_calc.get_all_interpretations(
            birth_date, request.full_name
        )

        return {
            "status": "success",
            "numbers": numbers,
            "interpretations": interpretations,
            "disclaimer": (
                "This numerology reading is for personal development and "
                "self-reflection only. Not for employment decisions."
            ),
        }

    except Exception as e:
        logger.error(f"Error calculating numerology: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/team/analyze", response_model=TeamAnalysisResponse)
async def analyze_team(request: TeamAnalysisRequest):
    """
    Analyze team dynamics and compatibility.

    Provides team-wide insights including:
    - Overall synergy score
    - Communication compatibility
    - Strengths diversity
    - Life path distribution
    - Top pairwise synergies
    - Team coaching prompts

    COMPLIANCE: For team building and coaching ONLY.
    NOT for hiring, promotion, or performance evaluation.
    """
    try:
        logger.info(
            f"Team analysis request: {request.team_name} "
            f"with {len(request.team_members)} members"
        )

        # Analyze team
        analysis = team_engine.analyze_team(
            request.team_members,
            request.team_name,
            request.include_pairwise_analysis,
        )

        # Format top synergies
        top_synergies = None
        if analysis.strongest_synergies:
            top_synergies = [
                {
                    "person1": syn[0],
                    "person2": syn[1],
                    "synergy_score": syn[2],
                }
                for syn in analysis.strongest_synergies
            ]

        return TeamAnalysisResponse(
            status="success",
            team_name=analysis.team_name,
            member_count=analysis.member_count,
            overall_synergy=analysis.compatibility_score.overall_synergy,
            communication_compatibility=analysis.compatibility_score.communication_compatibility,
            strengths_diversity=analysis.compatibility_score.strengths_diversity,
            team_strengths=analysis.compatibility_score.team_strengths,
            growth_areas=analysis.compatibility_score.growth_areas,
            communication_tips=analysis.compatibility_score.communication_tips,
            life_path_distribution=analysis.life_path_distribution,
            element_balance=analysis.element_balance,
            top_synergies=top_synergies,
            team_coaching_prompts=analysis.team_coaching_prompts,
            disclaimer=analysis.disclaimer,
        )

    except Exception as e:
        logger.error(f"Error analyzing team: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agent/coaching")
async def agent_coaching_session(request: AgentCoachingRequest):
    """
    AI-powered coaching session.

    Uses LangChain agent for sophisticated, conversational coaching insights.
    Requires PERPLEXITY_API_KEY environment variable.

    COMPLIANCE: Coaching tool only, not for employment decisions.
    """
    try:
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=503,
                detail="AI coaching unavailable: API key not configured"
            )

        # Create agent
        agent = PersonalDevelopmentAgent(api_key=api_key, verbose=True)

        # Get insights
        result = agent.get_personal_insights(
            birth_date=request.birth_date,
            full_name=request.full_name,
            focus_area=request.coaching_query,
        )

        # Add compliance reminder
        result = agent.add_compliance_reminder(result)

        return {
            "status": "success",
            "coaching_insights": result.get("analysis", ""),
            "cost": result.get("cost", 0),
            "model": result.get("model", ""),
            "disclaimer": result.get("disclaimer", ""),
            "compliance_notice": result.get("compliance_notice", ""),
        }

    except Exception as e:
        logger.error(f"Error in agent coaching: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_service_info():
    """
    Get personal development service information.

    Includes compliance notice and intended use cases.
    """
    return {
        "service": "Personal Development Insights",
        "version": "1.0.0",
        "description": "Flexible personal development tool using numerology and astrology",
        "positioning": "Coaching and Wellness Tool",
        "intended_use": [
            "Personal development coaching",
            "Team building activities",
            "Wellness program integration",
            "Communication style mapping",
            "Self-awareness exercises",
            "Trust-building conversations",
        ],
        "prohibited_use": [
            "Hiring decisions",
            "Promotion decisions",
            "Performance evaluation",
            "Employee assessment",
            "Compensation decisions",
            "Any employment-related decisions",
        ],
        "features": [
            "Flexible input (works with any level of birth data)",
            "Numerology insights (always available)",
            "Astrological insights (when data available)",
            "Team dynamics analysis",
            "AI-powered coaching (optional)",
            "Privacy-first design",
        ],
        "data_levels": {
            "date_only": "Numerology insights (life path, day of week)",
            "date_and_name": "Full numerology (destiny, soul urge, personality)",
            "date_and_time": "Numerology + basic astrology (sun sign)",
            "full_data": "Numerology + complete astrology (moon, rising, houses)",
        },
        "endpoints": {
            "/reading": "Flexible personal development reading",
            "/numerology": "Quick numerology calculation",
            "/team/analyze": "Team dynamics analysis",
            "/agent/coaching": "AI-powered coaching session",
        },
        "legal_compliance": {
            "purpose": "Personal development and coaching ONLY",
            "not_for": "Employment decisions of any kind",
            "privacy": "User consent required, data encrypted",
            "disclaimer": "Not scientifically validated, for reflection only",
        },
    }


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "personal-development",
        "version": "1.0.0",
        "compliance": "Coaching tool - NOT for employment decisions",
    }


@router.get("/examples")
async def get_usage_examples():
    """
    Get API usage examples for different data completeness levels.
    """
    return {
        "minimal_data_example": {
            "description": "Works with just birth date",
            "request": {
                "birth_date": "1990-06-15"
            },
            "provides": [
                "Life path number and interpretation",
                "Day of week insights",
                "Basic strengths and growth areas",
            ],
        },
        "with_name_example": {
            "description": "Add name for full numerology",
            "request": {
                "birth_date": "1990-06-15",
                "full_name": "Jane Doe"
            },
            "provides": [
                "Life path number",
                "Destiny number (life mission)",
                "Soul urge number (inner motivation)",
                "Personality number (outer expression)",
            ],
        },
        "with_time_example": {
            "description": "Add time for basic astrology",
            "request": {
                "birth_date": "1990-06-15",
                "birth_time": "14:30:00",
                "full_name": "Jane Doe"
            },
            "provides": [
                "Full numerology",
                "Sun sign and interpretation",
                "Moon phase insights",
            ],
        },
        "complete_data_example": {
            "description": "Full data for complete analysis",
            "request": {
                "birth_date": "1990-06-15",
                "birth_time": "14:30:00",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "timezone": "America/New_York",
                "full_name": "Jane Doe"
            },
            "provides": [
                "Complete numerology",
                "Sun, Moon, and Rising signs",
                "Planetary positions",
                "House positions",
                "Comprehensive synthesis",
            ],
        },
        "team_analysis_example": {
            "description": "Team dynamics analysis",
            "request": {
                "team_name": "Product Team",
                "team_members": [
                    {"birth_date": "1990-06-15", "full_name": "Alice"},
                    {"birth_date": "1988-03-22", "full_name": "Bob"},
                    {"birth_date": "1992-11-08", "full_name": "Charlie"},
                ]
            },
            "provides": [
                "Team synergy score",
                "Communication compatibility",
                "Strengths diversity",
                "Pairwise synergies",
                "Team coaching prompts",
            ],
        },
    }
