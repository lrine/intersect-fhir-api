"""
Authentication Router
Handles user registration, login, and profile endpoints
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
from typing import Optional

from app.models.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.models.enums import UserRole
from app.services.password_service import hash_password, verify_password
from app.services.jwt_service import create_access_token, get_token_data
from app.database import get_database

router = APIRouter()
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependency to get current authenticated user from JWT token

    Args:
        credentials: HTTP Bearer token credentials

    Returns:
        User data dictionary

    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    token_data = get_token_data(token)

    db = get_database()
    user = await db.users.find_one({"_id": token_data["user_id"]})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """
    Register a new user

    Creates a new user account with hashed password.
    Email must be unique.
    """
    db = get_database()

    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    password_hash = hash_password(user_data.password)

    # Create user document
    user_doc = {
        "_id": user_data.email,  # Use email as _id for easy lookup
        "email": user_data.email,
        "password_hash": password_hash,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "role": user_data.role.value,
        "created_at": datetime.utcnow(),
        "is_active": True
    }

    await db.users.insert_one(user_doc)

    # Remove password hash from response
    user_doc.pop("password_hash")

    return user_doc


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """
    Authenticate user and return JWT token

    Verifies credentials and returns access token with user role in payload.
    """
    db = get_database()

    # Find user by email
    user = await db.users.find_one({"email": credentials.email})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Check if user is active
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Create access token with user data
    token_data = {
        "user_id": user["_id"],
        "email": user["email"],
        "role": user["role"]
    }
    access_token = create_access_token(token_data)

    # Prepare user response (without password hash)
    user_response = {
        "_id": user["_id"],
        "email": user["email"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "role": user["role"],
        "created_at": user["created_at"],
        "is_active": user.get("is_active", True)
    }

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: dict = Depends(get_current_user)
):
    """
    Get current authenticated user's profile

    Returns user information from JWT token.
    """
    # Remove password hash and MongoDB _id if present
    user_data = {k: v for k, v in current_user.items() if k not in ["password_hash"]}

    return user_data
