"""Knowledge Base API endpoints."""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging

from backend.services.knowledge_service import create_knowledge_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/knowledge", tags=["knowledge"])

# Initialize knowledge service
knowledge_service = create_knowledge_service()


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Knowledge service operational",
    }


@router.get("/categories")
def list_categories():
    """List all knowledge base categories."""
    categories = knowledge_service.list_categories()
    return {
        "total_categories": len(categories),
        "categories": categories,
    }


@router.get("/category/{category_name}")
def get_category_info(category_name: str):
    """Get information about a specific category."""
    info = knowledge_service.get_category_info(category_name)
    if not info.get('name'):
        raise HTTPException(status_code=404, detail=f"Category not found: {category_name}")
    return info


@router.post("/search")
def search_knowledge_base(query: str = Query(..., min_length=3), category: Optional[str] = None, limit: int = Query(5, le=20)):
    """Search knowledge base for relevant content."""
    try:
        results = knowledge_service.search_local(query, category=category, limit=limit)
        return {
            "query": query,
            "category_filter": category,
            "result_count": len(results),
            "results": results,
        }
    except Exception as e:
        logger.error(f"Knowledge search error: {e}")
        raise HTTPException(status_code=500, detail="Search failed")


@router.get("/books/{category_name}")
def list_books_in_category(category_name: str):
    """List all books in a category."""
    categories = knowledge_service.list_categories()
    cat_info = next((c for c in categories if c['name'] == category_name), None)
    
    if not cat_info:
        raise HTTPException(status_code=404, detail=f"Category not found: {category_name}")
    
    return cat_info


@router.get("/apex")
def get_apex_section():
    """Get the apex section (Voodoo/Spirituality)."""
    categories = knowledge_service.list_categories()
    apex = next((c for c in categories if c['name'] == "01_voodoo_spiritual_apex"), None)
    
    if not apex:
        raise HTTPException(status_code=404, detail="Apex section not found")
    
    return {
        "name": "Voodoo & Spiritual Traditions (APEX)",
        "importance": "primary_pillar",
        **apex
    }


@router.get("/pillars")
def get_primary_pillars():
    """Get all primary interpretation pillars."""
    categories = knowledge_service.list_categories()
    primary = [
        c for c in categories if c['name'] in [
            "01_voodoo_spiritual_apex",
            "02_vedic_core",
            "03_vedic_advanced",
            "04_dasha_timing",
            "15_ayurveda_medicine",
        ]
    ]
    
    return {
        "pillar_count": len(primary),
        "pillars": primary,
    }
