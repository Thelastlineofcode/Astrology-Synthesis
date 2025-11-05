"""
Notification endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()


@router.post("/register")
async def register_fcm_token(db: Session = Depends(get_db)):
    """Register FCM token for push notifications."""
    return {"message": "Register FCM token - to be implemented"}


@router.put("/preferences")
async def update_preferences(db: Session = Depends(get_db)):
    """Update notification preferences."""
    return {"message": "Update preferences - to be implemented"}


@router.get("/preferences")
async def get_preferences(db: Session = Depends(get_db)):
    """Get notification preferences."""
    return {"message": "Get preferences - to be implemented"}
