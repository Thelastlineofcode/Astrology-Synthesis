"""
Notification endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.database import User, NotificationToken
from app.schemas.models import (
    NotificationTokenRegister,
    NotificationPreferences,
    NotificationPreferencesResponse
)

router = APIRouter()


@router.post("/register")
async def register_fcm_token(
    token_data: NotificationTokenRegister,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Register FCM token for push notifications.
    
    - Stores device FCM token
    - Updates if token already exists
    - Enables notifications by default
    """
    # Check if token already exists
    existing_token = db.query(NotificationToken).filter(
        NotificationToken.fcm_token == token_data.fcm_token
    ).first()
    
    if existing_token:
        # Update existing token
        existing_token.user_id = current_user.id
        existing_token.device_type = token_data.device_type
        existing_token.is_active = True
        existing_token.last_used_at = datetime.utcnow()
    else:
        # Create new token
        new_token = NotificationToken(
            user_id=current_user.id,
            fcm_token=token_data.fcm_token,
            device_type=token_data.device_type,
            daily_dasha_enabled=True,
            period_change_enabled=True,
            advisor_messages_enabled=True,
            is_active=True
        )
        db.add(new_token)
    
    db.commit()
    
    return {"message": "FCM token registered successfully"}


@router.put("/preferences", response_model=NotificationPreferencesResponse)
async def update_preferences(
    preferences: NotificationPreferences,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update notification preferences.
    
    - Enable/disable daily dasha notifications
    - Enable/disable period change alerts
    - Enable/disable advisor message notifications
    """
    # Get user's notification token(s)
    tokens = db.query(NotificationToken).filter(
        NotificationToken.user_id == current_user.id,
        NotificationToken.is_active == True
    ).all()
    
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No notification tokens found. Please register a device first."
        )
    
    # Update all active tokens with new preferences
    for token in tokens:
        token.daily_dasha_enabled = preferences.daily_dasha_enabled
        token.period_change_enabled = preferences.period_change_enabled
        token.advisor_messages_enabled = preferences.advisor_messages_enabled
    
    db.commit()
    
    return NotificationPreferencesResponse(
        daily_dasha_enabled=preferences.daily_dasha_enabled,
        period_change_enabled=preferences.period_change_enabled,
        advisor_messages_enabled=preferences.advisor_messages_enabled
    )


@router.get("/preferences", response_model=NotificationPreferencesResponse)
async def get_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get notification preferences.
    
    - Returns current notification settings
    - Uses first active token if multiple devices
    """
    token = db.query(NotificationToken).filter(
        NotificationToken.user_id == current_user.id,
        NotificationToken.is_active == True
    ).first()
    
    if not token:
        # Return default preferences if no token exists
        return NotificationPreferencesResponse(
            daily_dasha_enabled=True,
            period_change_enabled=True,
            advisor_messages_enabled=True
        )
    
    return NotificationPreferencesResponse(
        daily_dasha_enabled=token.daily_dasha_enabled,
        period_change_enabled=token.period_change_enabled,
        advisor_messages_enabled=token.advisor_messages_enabled
    )
