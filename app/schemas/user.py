"""
AegisCare Enterprise Patient Management System - User & Auth Schemas
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.core.constants import UserRole


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=64)
    last_name: str = Field(..., min_length=1, max_length=64)
    phone_number: Optional[str] = None
    role: UserRole = UserRole.PATIENT


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    username_or_email: str = Field(...)
    password: str = Field(...)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6)
