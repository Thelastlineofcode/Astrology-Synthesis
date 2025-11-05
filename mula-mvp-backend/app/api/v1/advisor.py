"""
Advisor (AI personality) endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()


@router.get("/list")
async def list_advisors(db: Session = Depends(get_db)):
    """List all available advisors."""
    return {"message": "List advisors - to be implemented"}


@router.post("/query")
async def query_advisor(db: Session = Depends(get_db)):
    """Ask a question to an advisor."""
    return {"message": "Query advisor - to be implemented"}


@router.get("/history")
async def get_conversation_history(db: Session = Depends(get_db)):
    """Get conversation history with advisors."""
    return {"message": "Conversation history - to be implemented"}
