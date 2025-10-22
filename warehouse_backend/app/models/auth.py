"""
Authentication models
"""
from pydantic import BaseModel, Field
from typing import Optional


class LoginRequest(BaseModel):
    """Login request model"""
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=100)


class LoginResponse(BaseModel):
    """Login response model"""
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    name: str


class VerifyPinRequest(BaseModel):
    """Verify PIN request model"""
    pin: str = Field(..., min_length=4, max_length=4, pattern="^[0-9]{4}$")


class VerifyPinResponse(BaseModel):
    """Verify PIN response model"""
    success: bool
    message: Optional[str] = None


class UserInfo(BaseModel):
    """User information model"""
    id: int
    username: str
    name: str
    email: Optional[str] = None


class TokenData(BaseModel):
    """Token payload data"""
    user_id: int
    username: str
    odoo_uid: int
