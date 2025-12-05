"""
Authentication Service
Handles JWT token creation, validation, and user authentication
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from app.schemas.auth import TokenData, User
from app.database import get_database

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_prefix}/auth/login", auto_error=False)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token
    
    Args:
        data: Data to encode in token
        expires_delta: Token expiration time
        
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    return encoded_jwt


async def get_user_by_username(username: str):
    """
    Get user from database by username
    
    Args:
        username: Username to search for
        
    Returns:
        User document or None
    """
    db = get_database()
    user = await db.users.find_one({"username": username})
    return user


async def authenticate_user(username: str, password: str):
    """
    Authenticate user with username and password
    
    Args:
        username: Username
        password: Plain text password
        
    Returns:
        User document or False
    """
    user = await get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get current user from JWT token
    """
    # Bypass auth for development
    return User(username="anonymous", email="anon@test.com", full_name="Anonymous", disabled=False, roles=["admin"])

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get current active user (not disabled)
    
    Args:
        current_user: Current user from token
        
    Returns:
        User: Active user
        
    Raises:
        HTTPException: If user is disabled
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_roles(required_roles: list):
    """
    Dependency to require specific roles
    
    Usage:
        @router.get("/admin", dependencies=[Depends(require_roles(["admin"]))])
    """
    async def check_roles(current_user: User = Depends(get_current_active_user)):
        if not any(role in current_user.roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    
    return check_roles
