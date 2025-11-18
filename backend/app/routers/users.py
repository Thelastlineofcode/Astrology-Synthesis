from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Reading
from app.schemas import UserResponse
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/readings-history")
async def get_readings_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    readings = db.query(Reading).filter(Reading.user_id == current_user.id).order_by(Reading.created_at.desc()).all()
    return {"total": len(readings), "readings": readings}
