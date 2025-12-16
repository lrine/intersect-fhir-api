"""
User models and schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.enums import UserRole


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: UserRole


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schema for user responses (excludes password)"""
    id: str = Field(alias="_id")
    created_at: datetime
    is_active: bool = True

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "email": "john.doe@hospital.com",
                "first_name": "John",
                "last_name": "Doe",
                "role": "practitioner",
                "created_at": "2024-01-01T00:00:00",
                "is_active": True
            }
        }


class User(UserBase):
    """User model stored in MongoDB"""
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
