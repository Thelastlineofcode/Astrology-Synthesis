"""
Synastry API Endpoints

FastAPI endpoints for relationship compatibility analysis.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging

from backend.calculations.synastry_engine import SynastryCalculator, SynastryResult
from backend.agents.synastry_agent import SynastryAgent
from backend.services.calculation_service import CalculationService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/synastry", tags=["synastry"])

# Initialize services
synastry_calculator = SynastryCalculator()
calculation_service = CalculationService()


# Request/Response Models
class SynastryRequest(BaseModel):
    """Request model for synastry analysis."""
    person1_name: str = Field(..., description="First person's name")
    person1_date: str = Field(..., description="Date (YYYY-MM-DD)")
    person1_time: str = Field(..., description="Time (HH:MM:SS)")
    person1_latitude: float = Field(..., description="Latitude")
    person1_longitude: float = Field(..., description="Longitude")
    person1_timezone: str = Field(..., description="Timezone")

    person2_name: str = Field(..., description="Second person's name")
    person2_date: str = Field(..., description="Date (YYYY-MM-DD)")
    person2_time: str = Field(..., description="Time (HH:MM:SS)")
    person2_latitude: float = Field(..., description="Latitude")
    person2_longitude: float = Field(..., description="Longitude")
    person2_timezone: str = Field(..., description="Timezone")

    include_composite: bool = Field(default=True, description="Include composite chart")


class QuickCompatibilityRequest(BaseModel):
    """Quick compatibility check using existing chart IDs."""
    chart1_id: str = Field(..., description="First chart ID")
    chart2_id: str = Field(..., description="Second chart ID")
    person1_name: Optional[str] = Field(None, description="First person's name")
    person2_name: Optional[str] = Field(None, description="Second person's name")


class AspectInterpretationRequest(BaseModel):
    """Request for aspect interpretation."""
    planet1: str = Field(..., description="First planet")
    planet2: str = Field(..., description="Second planet")
    aspect_type: str = Field(..., description="Aspect type")


class SynastryResponse(BaseModel):
    """Response model for synastry analysis."""
    status: str
    person1_name: str
    person2_name: str
    compatibility_score: Dict[str, Any]
    aspects_count: Dict[str, int]
    house_overlays_count: int
    composite_chart: Optional[Dict[str, Any]]
    message: str


class AgentAnalysisRequest(BaseModel):
    """Request for AI agent analysis."""
    chart1_id: str
    chart2_id: str
    person1_name: str
    person2_name: str
    query: Optional[str] = Field(
        None,
        description="Specific question (optional)"
    )


# Endpoints
@router.post("/analyze", response_model=SynastryResponse)
async def analyze_synastry(request: SynastryRequest):
    """
    Analyze relationship compatibility between two people.

    This endpoint performs a complete synastry analysis including:
    - Inter-chart aspects
    - House overlays
    - Compatibility scoring
    - Optional composite chart

    Returns detailed compatibility metrics and insights.
    """
    try:
        logger.info(
            f"Synastry analysis request: {request.person1_name} + {request.person2_name}"
        )

        # Generate birth charts for both people
        from backend.schemas import BirthDataInput

        birth_data1 = BirthDataInput(
            date=request.person1_date,
            time=request.person1_time,
            latitude=request.person1_latitude,
            longitude=request.person1_longitude,
            timezone=request.person1_timezone,
            location_name="",
        )

        birth_data2 = BirthDataInput(
            date=request.person2_date,
            time=request.person2_time,
            latitude=request.person2_latitude,
            longitude=request.person2_longitude,
            timezone=request.person2_timezone,
            location_name="",
        )

        # Generate charts
        chart1 = calculation_service.generate_birth_chart(birth_data1)
        chart2 = calculation_service.generate_birth_chart(birth_data2)

        # Calculate synastry
        result = synastry_calculator.calculate_synastry(
            chart1,
            chart2,
            person1_name=request.person1_name,
            person2_name=request.person2_name,
            include_composite=request.include_composite,
        )

        # Format response
        return SynastryResponse(
            status="success",
            person1_name=result.person1_name,
            person2_name=result.person2_name,
            compatibility_score={
                "overall": result.compatibility_score.overall_score,
                "emotional": result.compatibility_score.emotional_compatibility,
                "romantic": result.compatibility_score.romantic_compatibility,
                "communication": result.compatibility_score.communication_compatibility,
                "long_term": result.compatibility_score.long_term_compatibility,
                "sexual": result.compatibility_score.sexual_compatibility,
                "strengths": result.compatibility_score.strengths,
                "challenges": result.compatibility_score.challenges,
                "advice": result.compatibility_score.advice,
            },
            aspects_count={
                "harmonious": result.compatibility_score.harmonious_aspects,
                "challenging": result.compatibility_score.challenging_aspects,
                "total": len(result.inter_aspects),
            },
            house_overlays_count=len(result.house_overlays),
            composite_chart=(
                {
                    "sun": result.composite_chart.composite_sun,
                    "moon": result.composite_chart.composite_moon,
                    "ascendant": result.composite_chart.composite_ascendant,
                }
                if result.composite_chart
                else None
            ),
            message=f"Synastry analysis complete. Overall compatibility: {result.compatibility_score.overall_score:.0f}/100",
        )

    except Exception as e:
        logger.error(f"Error in synastry analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compatibility/{chart1_id}/{chart2_id}")
async def quick_compatibility(
    chart1_id: str,
    chart2_id: str,
    person1_name: Optional[str] = None,
    person2_name: Optional[str] = None,
):
    """
    Quick compatibility check using existing chart IDs.

    Useful when charts are already calculated and stored.
    """
    try:
        # TODO: Retrieve charts from database
        # For now, return error
        raise HTTPException(
            status_code=501,
            detail="Chart retrieval not yet implemented. Use /analyze endpoint."
        )

    except Exception as e:
        logger.error(f"Error in quick compatibility: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/aspects/interpret")
async def interpret_aspect(request: AspectInterpretationRequest):
    """
    Get interpretation for a specific synastry aspect.

    Provides detailed meaning of how two planets interact in synastry.
    """
    try:
        # TODO: Implement aspect interpretation lookup
        # For now, return simple interpretation

        interpretations = {
            ("Sun", "Moon", "Trine"): "Harmonious emotional understanding",
            ("Venus", "Mars", "Conjunction"): "Strong romantic attraction",
            ("Moon", "Moon", "Square"): "Different emotional needs",
        }

        key = (request.planet1, request.planet2, request.aspect_type)
        interpretation = interpretations.get(
            key,
            f"{request.planet1}-{request.planet2} {request.aspect_type} aspect"
        )

        return {
            "status": "success",
            "aspect": {
                "planet1": request.planet1,
                "planet2": request.planet2,
                "type": request.aspect_type,
                "interpretation": interpretation,
            },
        }

    except Exception as e:
        logger.error(f"Error interpreting aspect: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agent/analyze")
async def agent_analysis(request: AgentAnalysisRequest):
    """
    Get AI agent analysis of the relationship.

    Uses LangChain agent for sophisticated, conversational analysis.
    Requires PERPLEXITY_API_KEY environment variable.
    """
    try:
        import os

        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=503,
                detail="Perplexity API key not configured"
            )

        # Create synastry agent
        agent = SynastryAgent(api_key=api_key, verbose=True)

        # Analyze
        query = request.query or "Analyze the relationship compatibility in detail."
        result = agent.invoke({
            "query": query,
            "chart1_id": request.chart1_id,
            "chart2_id": request.chart2_id,
            "person1_name": request.person1_name,
            "person2_name": request.person2_name,
        })

        return {
            "status": "success",
            "analysis": result.get("analysis", ""),
            "cost": result.get("cost", 0),
            "model": result.get("model", ""),
            "person1_name": request.person1_name,
            "person2_name": request.person2_name,
        }

    except Exception as e:
        logger.error(f"Error in agent analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "synastry",
        "version": "1.0.0",
    }


@router.get("/info")
async def get_info():
    """Get synastry service information."""
    return {
        "service": "Synastry Compatibility Analysis",
        "version": "1.0.0",
        "description": "Relationship compatibility using synastry techniques",
        "features": [
            "Inter-chart aspect analysis",
            "House overlay interpretation",
            "Composite chart calculation",
            "Compatibility scoring",
            "AI-powered relationship insights",
        ],
        "endpoints": {
            "/analyze": "Full synastry analysis",
            "/compatibility/{chart1_id}/{chart2_id}": "Quick compatibility check",
            "/aspects/interpret": "Aspect interpretation",
            "/agent/analyze": "AI agent analysis",
        },
    }
