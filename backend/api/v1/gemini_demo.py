"""
Gemini Agent Demo API endpoints.

Provides endpoints to test the Gemini-powered LangChain agent.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import logging
import os

from backend.agents.factory import create_gemini_agent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/gemini-demo", tags=["gemini-demo"])


# Request/Response Models
class GeminiQueryRequest(BaseModel):
    """Request model for Gemini agent query."""
    query: str = Field(..., description="The astrological query")
    chart_data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional chart data context"
    )


class GeminiQueryResponse(BaseModel):
    """Response model for Gemini agent query."""
    interpretation: str
    model: str
    cost: float
    tokens: int
    quality: float
    strategy: str
    agent_name: str


class AgentInfoResponse(BaseModel):
    """Agent information response."""
    agent_name: str
    description: str
    model: str
    status: str
    metrics: Dict[str, Any]


# Global agent instance (initialized on first request)
_gemini_agent = None


def get_gemini_agent():
    """Get or create Gemini agent instance."""
    global _gemini_agent

    if _gemini_agent is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="GOOGLE_API_KEY not configured. Please set your API key."
            )

        try:
            _gemini_agent = create_gemini_agent(
                api_key=api_key,
                model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
                verbose=os.getenv("ENVIRONMENT", "development") == "development"
            )
            logger.info("Gemini agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini agent: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to initialize Gemini agent: {str(e)}"
            )

    return _gemini_agent


@router.post("/query", response_model=GeminiQueryResponse)
async def query_gemini_agent(request: GeminiQueryRequest):
    """
    Query the Gemini agent for astrological interpretation.

    This endpoint demonstrates the Gemini-powered LangChain agent
    with tool calling and reasoning capabilities.

    **Free tier available** - No cost for basic usage with generous limits.
    """
    try:
        agent = get_gemini_agent()

        # Prepare input
        input_data = {
            "query": request.query,
            "chart_data": request.chart_data or {}
        }

        # Invoke agent
        result = agent.invoke(input_data)

        # Check for errors
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Agent error: {result['error']}"
            )

        return GeminiQueryResponse(**result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in query_gemini_agent: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process query: {str(e)}"
        )


@router.get("/info", response_model=AgentInfoResponse)
async def get_agent_info():
    """
    Get information about the Gemini agent.

    Returns agent status, configuration, and performance metrics.
    """
    try:
        agent = get_gemini_agent()

        return AgentInfoResponse(
            agent_name=agent.agent_name,
            description=agent.description,
            model=agent.model,
            status="active",
            metrics=agent.get_metrics()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_agent_info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get agent info: {str(e)}"
        )


@router.post("/reset")
async def reset_agent():
    """
    Reset the Gemini agent (clear memory and metrics).

    Useful for testing and starting fresh conversations.
    """
    try:
        agent = get_gemini_agent()
        agent.clear_history()
        agent.reset_metrics()

        return {
            "status": "success",
            "message": "Agent reset successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in reset_agent: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset agent: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint for Gemini agent.

    Returns agent availability and configuration status.
    """
    try:
        # Check if API key is configured
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return {
                "status": "unavailable",
                "message": "GOOGLE_API_KEY not configured",
                "agent_initialized": _gemini_agent is not None
            }

        # Try to get/create agent
        agent = get_gemini_agent()

        return {
            "status": "healthy",
            "message": "Gemini agent is ready",
            "agent_name": agent.agent_name,
            "model": agent.model,
            "invocations": agent.invocation_count
        }

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "message": f"Agent initialization failed: {str(e)}",
            "agent_initialized": _gemini_agent is not None
        }
