from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Reading, AdvisorType
from app.schemas import ReadingCreate, ReadingResponse
from app.routers.auth import get_current_user

router = APIRouter()

@router.post("/ask", response_model=ReadingResponse)
async def ask_advisor(
    data: ReadingCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reading = Reading(
        user_id=current_user.id,
        advisor=data.advisor,
        question=data.question,
        response="[Placeholder - AI integration pending]",
        tokens_used=0,
        cost="0.00"
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading

@router.get("/{reading_id}", response_model=ReadingResponse)
async def get_reading(reading_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    reading = db.query(Reading).filter(Reading.id == reading_id, Reading.user_id == current_user.id).first()
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    return reading
