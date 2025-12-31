from datetime import datetime
from typing import Optional
from pydantic import EmailStr, Field, field_validator
from app.schemas.base import BaseSchema, TimestampSchema
from app.models.user import UserRole
import re


class UserBase(BaseSchema):
    """Base user schema."""
    
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError(
                "Username can only contain letters, numbers, underscores, and hyphens"
            )
        return v.lower()


class UserCreate(UserBase):
    """Schema for creating a new user."""
    
    password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseSchema):
    """Schema for updating a user."""
    
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None


class UserUpdatePassword(BaseSchema):
    """Schema for updating user password."""
    
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)


class UserInDB(UserBase, TimestampSchema):
    """User schema as stored in database."""
    
    id: int
    is_active: bool
    is_superuser: bool
    role: UserRole


class UserResponse(UserBase, TimestampSchema):
    """User response schema (public)."""
    
    id: int
    is_active: bool
    role: UserRole


class UserBrief(BaseSchema):
    """Brief user info for embedding."""
    
    id: int
    username: str
    full_name: Optional[str] = None
