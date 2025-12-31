from typing import Optional
from pydantic import EmailStr
from app.schemas.base import BaseSchema
from app.schemas.user import UserResponse


class LoginRequest(BaseSchema):
    """Login request schema."""
    
    username: str  # Can be username or email
    password: str


class TokenResponse(BaseSchema):
    """Token response schema."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseSchema):
    """JWT token payload schema."""
    
    sub: str
    exp: int
    type: str


class RefreshTokenRequest(BaseSchema):
    """Refresh token request schema."""
    
    refresh_token: str


class AuthResponse(BaseSchema):
    """Full authentication response."""
    
    user: UserResponse
    tokens: TokenResponse


class PasswordResetRequest(BaseSchema):
    """Password reset request schema."""
    
    email: EmailStr


class PasswordResetConfirm(BaseSchema):
    """Password reset confirmation schema."""
    
    token: str
    new_password: str
