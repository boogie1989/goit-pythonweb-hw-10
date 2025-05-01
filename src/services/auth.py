"""Authentication service and utilities.

This module provides authentication-related functionality including password hashing,
JWT token generation and validation, and user authentication.
"""

from datetime import datetime, timedelta, UTC
from typing import Optional, Dict, Any, Union

from fastapi import Depends, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from src.database.db import get_db
from src.conf.config import settings
from src.services.users import UserService
from src.utils import (
    HTTPUnprocessableEntityException,
    HTTPUnauthorizedException
)


class Hash:
    """Password hashing utility class using bcrypt.
    
    This class provides methods for hashing passwords and verifying password matches.
    """
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify if a plain password matches a hashed password.
        
        Args:
            plain_password: The plaintext password to verify
            hashed_password: The hashed password to compare against
            
        Returns:
            bool: True if the password matches, False otherwise
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Generate a bcrypt password hash.
        
        Args:
            password: The plaintext password to hash
            
        Returns:
            str: The hashed password
        """
        return self.pwd_context.hash(password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def create_access_token(payload: Dict[str, Any], expires_delta: Optional[int] = None) -> str:
    """Generate a JWT access token.
    
    Args:
        payload: The data to encode in the token
        expires_delta: Optional custom expiration time in seconds
        
    Returns:
        str: The encoded JWT token
    """
    payload_data = payload.copy()
    if expires_delta:
        expire = datetime.now(UTC) + timedelta(seconds=expires_delta)
    else:
        expire = datetime.now(UTC) + timedelta(
            seconds=int(settings.JWT_EXPIRATION_SECONDS)
        )
    payload_data.update({"exp": expire})
    encoded = jwt.encode(
        payload_data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded


def create_email_verification_token(payload: Dict[str, Any]) -> str:
    """Generate a JWT token for email verification.
    
    Args:
        payload: The data to encode in the token, typically contains the user's email
        
    Returns:
        str: The encoded JWT token with a 7-day expiration period
    """
    to_encode = payload.copy()
    expire = datetime.now(UTC) + timedelta(days=7)
    to_encode.update({"iat": datetime.now(UTC), "exp": expire})
    token = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    """Get and validate the current authenticated user.
    
    Args:
        token: JWT token from the Authorization header
        db: Database session
        
    Returns:
        User: The authenticated user object
        
    Raises:
        HTTPUnauthorizedException: If the token is invalid or the user doesn't exist
    """
    try:
        # Decode JWT
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise HTTPUnauthorizedException("Invalid token payload")
            
        # Get expiration and check if token is expired
        exp = payload.get("exp")
        if exp is None or datetime.fromtimestamp(exp, UTC) < datetime.now(UTC):
            raise HTTPUnauthorizedException("Token has expired")
            
    except JWTError:
        raise HTTPUnauthorizedException("Invalid authentication token")
    
    # Get user from database
    user_service = UserService(db)
    user = await user_service.get_user_by_username(username)
    
    if user is None:
        raise HTTPUnauthorizedException("User not found")
        
    if not user.is_active:
        raise HTTPUnauthorizedException("User is inactive")

    return user


async def get_email_from_token(token: str) -> str:
    """Extract email from verification token.
    
    Args:
        token: JWT token containing the user's email
        
    Returns:
        str: The user's email address
        
    Raises:
        HTTPUnprocessableEntityException: If the token is invalid
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise HTTPUnprocessableEntityException("Invalid token payload")
        return email
    except JWTError:
        raise HTTPUnprocessableEntityException("Invalid verification token")
