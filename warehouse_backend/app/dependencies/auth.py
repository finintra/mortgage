"""
Authentication dependencies
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

from app.config import settings
from app.models.auth import TokenData
from app.services.odoo_client import get_odoo_client

logger = logging.getLogger(__name__)

security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """Verify JWT token and return token data"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("user_id")
        username: str = payload.get("username")
        odoo_uid: int = payload.get("odoo_uid")

        if user_id is None or username is None or odoo_uid is None:
            raise credentials_exception

        token_data = TokenData(user_id=user_id, username=username, odoo_uid=odoo_uid)
        return token_data

    except JWTError as e:
        logger.error(f"JWT Error: {e}")
        raise credentials_exception


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    """
    Dependency to get current authenticated user from JWT token
    Use this in route parameters to require authentication
    """
    token = credentials.credentials
    return verify_token(token)


async def get_current_active_user(
    current_user: TokenData = Depends(get_current_user)
) -> TokenData:
    """
    Dependency to get current active user
    Can add additional checks here (e.g., user is active, not banned, etc.)
    """
    # Optional: Check if user still exists and is active in Odoo
    odoo = get_odoo_client()
    try:
        user_info = odoo.get_user_info(current_user.odoo_uid)
        if not user_info:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error(f"Error checking user status: {e}")
        raise HTTPException(status_code=500, detail="Could not verify user status")

    return current_user
