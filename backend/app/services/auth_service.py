from typing import Optional, Tuple
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base import BaseService
from app.crud import user as user_crud
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password
)
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.auth import TokenResponse


class AuthService(BaseService):
    """Service for authentication operations."""
    
    def __init__(self):
        super().__init__("AuthService")
    
    async def authenticate(
        self,
        db: AsyncSession,
        *,
        identifier: str,
        password: str
    ) -> Optional[User]:
        """Authenticate user by email/username and password."""
        user = await user_crud.authenticate(
            db,
            identifier=identifier,
            password=password
        )
        
        if user:
            self.log_info(f"User {user.username} authenticated successfully")
        else:
            self.log_warning(f"Failed authentication attempt for {identifier}")
        
        return user
    
    async def create_tokens(
        self,
        user: User
    ) -> TokenResponse:
        """Create access and refresh tokens for user."""
        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    async def refresh_tokens(
        self,
        db: AsyncSession,
        *,
        refresh_token: str
    ) -> Optional[TokenResponse]:
        """Refresh access token using refresh token."""
        payload = decode_token(refresh_token)
        
        if not payload:
            self.log_warning("Invalid refresh token")
            return None
        
        if payload.get("type") != "refresh":
            self.log_warning("Token is not a refresh token")
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        user = await user_crud.get(db, int(user_id))
        if not user or not user.is_active:
            self.log_warning(f"User {user_id} not found or inactive")
            return None
        
        return await self.create_tokens(user)
    
    async def validate_token(
        self,
        db: AsyncSession,
        *,
        token: str
    ) -> Optional[User]:
        """Validate access token and return user."""
        payload = decode_token(token)
        
        if not payload:
            return None
        
        if payload.get("type") != "access":
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        user = await user_crud.get(db, int(user_id))
        if not user or not user.is_active:
            return None
        
        return user
    
    async def register(
        self,
        db: AsyncSession,
        *,
        user_in: UserCreate
    ) -> Tuple[Optional[User], Optional[str]]:
        """Register a new user. Returns (user, error_message)."""
        # Check if email exists
        existing_email = await user_crud.get_by_email(db, email=user_in.email)
        if existing_email:
            return None, "Email already registered"
        
        # Check if username exists
        existing_username = await user_crud.get_by_username(
            db, username=user_in.username
        )
        if existing_username:
            return None, "Username already taken"
        
        # Create user
        user = await user_crud.create(db, obj_in=user_in)
        
        self.log_info(f"New user registered: {user.username}")
        return user, None
    
    async def change_password(
        self,
        db: AsyncSession,
        *,
        user: User,
        current_password: str,
        new_password: str
    ) -> Tuple[bool, Optional[str]]:
        """Change user password. Returns (success, error_message)."""
        if not verify_password(current_password, user.hashed_password):
            return False, "Current password is incorrect"
        
        await user_crud.update_password(db, user=user, new_password=new_password)
        
        self.log_info(f"Password changed for user {user.username}")
        return True, None


# Create singleton instance
auth_service = AuthService()
