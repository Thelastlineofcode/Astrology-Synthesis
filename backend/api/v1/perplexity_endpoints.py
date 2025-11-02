"""
Perplexity Phase 5 API Endpoints
Provides LLM-powered interpretation endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import logging

from backend.services.cached_perplexity_service import create_cached_perplexity_service
from backend.services.faiss_vector_store import create_faiss_vector_store
from backend.services.hybrid_interpretation_service import HybridInterpretationService
from backend.services.knowledge_service import KnowledgeService
from backend.services.interpretation_service import InterpretationService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["perplexity"])

# Pydantic models
class ChartData(BaseModel):
    """Chart data for interpretation"""
    sun: str = Field(..., description="Sun sign")
    moon: Optional[str] = Field(None, description="Moon sign")
    ascendant: Optional[str] = Field(None, description="Ascendant sign")
    time_of_birth: Optional[str] = Field(None, description="Time of birth")
    location: Optional[str] = Field(None, description="Birth location")


class InterpretationRequest(BaseModel):
    """Request for interpretation"""
    chart_data: ChartData
    type: str = Field(..., description="Type of interpretation (sun, moon, etc.)")
    strategy: Optional[str] = Field("auto", description="Strategy: auto, llm, kb, or template")
    context: Optional[str] = Field(None, description="Additional context")


class InterpretationResponse(BaseModel):
    """Response with interpretation"""
    interpretation: str
    type: str
    strategy: str
    quality: float
    source: str
    cost: float
    execution_time: float


# Global services
_llm_service = None
_vector_store = None
_hybrid_service = None
_kb_service = None
_interp_service = None


def _init_services():
    """Initialize all Phase 5 services"""
    global _llm_service, _vector_store, _hybrid_service, _kb_service, _interp_service
    
    if _llm_service is None:
        try:
            _llm_service = create_cached_perplexity_service()
            _vector_store = create_faiss_vector_store()
            _kb_service = KnowledgeService()
            _interp_service = InterpretationService()
            _hybrid_service = HybridInterpretationService(
                llm_service=_llm_service,
                vector_store=_vector_store,
                kb_service=_kb_service,
                interpretation_service=_interp_service,
            )
            logger.info("All Phase 5 services initialized")
        except Exception as e:
            logger.error(f"Service initialization error: {str(e)}")
            raise


@router.post("/interpretations/hybrid", response_model=InterpretationResponse)
async def hybrid_interpretation(request: InterpretationRequest):
    """
    Generate interpretation with hybrid strategy
    
    Automatically selects between LLM, vector store, or templates
    based on availability and budget.
    """
    try:
        _init_services()
        
        result = _hybrid_service.interpret(
            chart_data=request.chart_data.dict(),
            interpretation_type=request.type,
            strategy=request.strategy,
            context=request.context,
        )
        
        if result.get("error"):
            raise HTTPException(status_code=400, detail=result["error"])
        
        return InterpretationResponse(**result)
        
    except Exception as e:
        logger.error(f"Error in hybrid_interpretation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/interpretations/llm", response_model=InterpretationResponse)
async def llm_interpretation(request: InterpretationRequest):
    """
    Generate interpretation with LLM only
    
    Uses Perplexity sonar-small for best quality.
    Cost: ~$0.0001 per interpretation
    """
    try:
        _init_services()
        
        result = _hybrid_service.interpret(
            chart_data=request.chart_data.dict(),
            interpretation_type=request.type,
            strategy="llm",
            context=request.context,
        )
        
        if result.get("error"):
            raise HTTPException(status_code=400, detail=result["error"])
        
        return InterpretationResponse(**result)
        
    except Exception as e:
        logger.error(f"Error in llm_interpretation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/interpretations/kb")
async def kb_interpretation(request: InterpretationRequest):
    """
    Generate interpretation with knowledge base only
    
    Uses FAISS semantic search over 82 knowledge base texts.
    Cost: $0
    Speed: <100ms
    """
    try:
        _init_services()
        
        result = _hybrid_service.interpret(
            chart_data=request.chart_data.dict(),
            interpretation_type=request.type,
            strategy="kb",
        )
        
        if result.get("error"):
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error in kb_interpretation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/interpretations/template")
async def template_interpretation(request: InterpretationRequest):
    """
    Generate interpretation with templates only
    
    Uses Phase 4 template-based interpretations.
    Cost: $0
    Speed: <10ms
    """
    try:
        _init_services()
        
        result = _hybrid_service.interpret(
            chart_data=request.chart_data.dict(),
            interpretation_type=request.type,
            strategy="template",
        )
        
        if result.get("error"):
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Error in template_interpretation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/budget")
async def get_budget():
    """
    Get remaining budget information
    
    Shows:
    - Total monthly budget
    - Used so far
    - Remaining
    - Alert status
    """
    try:
        _init_services()
        
        if not _llm_service:
            return {"error": "LLM service not available"}
        
        budget = _llm_service.get_budget_remaining()
        cache_stats = _llm_service.get_cache_stats()
        
        return {
            "budget": budget,
            "cache_stats": cache_stats,
            "model": "sonar-small",
        }
        
    except Exception as e:
        logger.error(f"Error getting budget: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """
    System health check
    
    Returns status of all Phase 5 components
    """
    try:
        _init_services()
        
        llm_ok = _llm_service is not None and _llm_service.is_available()
        vs_ok = _vector_store is not None and _vector_store.text_count > 0
        hybrid_ok = _hybrid_service is not None
        
        status = "healthy" if (llm_ok or vs_ok or hybrid_ok) else "degraded"
        
        return {
            "status": status,
            "components": {
                "llm": {
                    "available": llm_ok,
                    "budget_remaining": _llm_service.get_budget_remaining()["cost_remaining"] if _llm_service else 0,
                },
                "vector_store": {
                    "available": vs_ok,
                    "text_count": _vector_store.text_count if _vector_store else 0,
                },
                "hybrid": {
                    "available": hybrid_ok,
                    "stats": _hybrid_service.get_stats() if _hybrid_service else {},
                },
            },
        }
        
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats():
    """Get detailed service statistics"""
    try:
        _init_services()
        
        return {
            "hybrid_stats": _hybrid_service.get_stats() if _hybrid_service else {},
            "llm_stats": _llm_service.get_budget_remaining() if _llm_service else {},
            "cache_stats": _llm_service.get_cache_stats() if _llm_service else {},
            "vector_stats": _vector_store.get_stats() if _vector_store else {},
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
