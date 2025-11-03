from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ReadingCreate(BaseModel):
    advisor: str = Field(..., pattern="^(legba|oshun|shango|yemaya)$")
    question: str = Field(..., min_length=5, max_length=500)

class ReadingResponse(BaseModel):
    id: int
    advisor: str
    question: str
    response: Optional[str]
    tokens_used: int
    cost: str
    created_at: datetime
    
    class Config:
        from_attributes = True
