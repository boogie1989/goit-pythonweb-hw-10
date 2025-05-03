from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword",
            }
        }


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    
    class Config:
        schema_extra = {
            "example": {
                "email": "new.email@example.com"
            }
        }


class UserInDB(UserBase):
    id: int
    avatar_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class UserResponse(UserInDB):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class TokenData(BaseModel):
    sub: int
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword"
            }
        }
