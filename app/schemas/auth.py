"""
Authentication Schemas
Request/Response models for authentication
"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    """JWT Token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data stored in JWT token"""
    username: Optional[str] = None
    email: Optional[str] = None
    roles: Optional[list] = []


class UserLogin(BaseModel):
    """Login request"""
    username: str
    password: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "john.smith@intersect.health",
                "password": "SecurePassword123!"
            }
        }
    }


class UserCreate(BaseModel):
    """User registration"""
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    roles: list = ["user"]
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "john.smith",
                "email": "john.smith@intersect.health",
                "password": "SecurePassword123!",
                "full_name": "John Smith",
                "roles": ["clinician"]
            }
        }
    }


class User(BaseModel):
    """User response model (no password)"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: bool = False
    roles: list = []
