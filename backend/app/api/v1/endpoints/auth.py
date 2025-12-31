from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.services.auth_service import auth_service
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    AuthResponse
)
from app.schemas.user import UserCreate, UserResponse
from app.schemas.base import MessageResponse

router = APIRouter()


@router.post("/login", response_model=AuthResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with username/email and password.
    Returns access and refresh tokens.
    """
    user = await auth_service.authenticate(
        db,
        identifier=login_data.username,
        password=login_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    tokens = await auth_service.create_tokens(user)
    
    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=tokens
    )


@router.post("/register", response_model=AuthResponse)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account.
    """
    user, error = await auth_service.register(db, user_in=user_in)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    tokens = await auth_service.create_tokens(user)
    
    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=tokens
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    """
    tokens = await auth_service.refresh_tokens(
        db,
        refresh_token=refresh_data.refresh_token
    )
    
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return tokens


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user = Depends(get_current_user)
):
    """
    Get current authenticated user information.
    """
    return UserResponse.model_validate(current_user)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user = Depends(get_current_user)
):
    """
    Logout current user.
    Note: JWT tokens are stateless, so this is mainly for client-side handling.
    For full logout, implement token blacklisting with Redis.
    """
    return MessageResponse(
        message="Successfully logged out",
        success=True
    )


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    current_password: str,
    new_password: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Change current user's password.
    """
    success, error = await auth_service.change_password(
        db,
        user=current_user,
        current_password=current_password,
        new_password=new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return MessageResponse(
        message="Password changed successfully",
        success=True
    )
