from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user, PaginationParams
from app.crud import dashboard as dashboard_crud
from app.models.user import User
from app.services.dashboard_service import dashboard_service
from app.schemas.dashboard import (
    DashboardCreate,
    DashboardUpdate,
    DashboardResponse,
    WidgetData
)
from app.schemas.base import MessageResponse

router = APIRouter()


@router.get("/overview")
async def get_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get dashboard overview statistics.
    """
    return await dashboard_service.get_overview_stats(db)


@router.get("/sentiment")
async def get_sentiment_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get sentiment analysis overview.
    """
    return await dashboard_service.get_sentiment_overview(db)


@router.get("/emotions")
async def get_emotion_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get emotion analysis overview.
    """
    return await dashboard_service.get_emotion_overview(db)


@router.get("/platforms")
async def get_platform_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get statistics by platform.
    """
    return await dashboard_service.get_platform_stats(db)


@router.get("/widget/{widget_type}")
async def get_widget_data(
    widget_type: str,
    db: AsyncSession = Depends(get_db),
    hours: int = 24,
    limit: int = 10,
    interval: str = "1h",
    current_user: User = Depends(get_current_user)
):
    """
    Get data for a specific widget type.
    """
    config = {
        "hours": hours,
        "limit": limit,
        "interval": interval
    }
    
    data = await dashboard_service.get_widget_data(
        db,
        widget_type=widget_type,
        config=config
    )
    
    return data


@router.get("", response_model=List[DashboardResponse])
async def get_dashboards(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's dashboards.
    """
    dashboards = await dashboard_crud.get_by_user(
        db,
        user_id=current_user.id,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return [DashboardResponse.model_validate(d) for d in dashboards]


@router.get("/public", response_model=List[DashboardResponse])
async def get_public_dashboards(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_user)
):
    """
    Get public dashboards.
    """
    dashboards = await dashboard_crud.get_public(
        db,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return [DashboardResponse.model_validate(d) for d in dashboards]


@router.get("/default", response_model=DashboardResponse)
async def get_default_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's default dashboard.
    """
    dashboard = await dashboard_crud.get_default(db, user_id=current_user.id)
    
    if not dashboard:
        # Create default dashboard if none exists
        dashboard = await dashboard_service.create_default_dashboard(
            db,
            user_id=current_user.id
        )
    
    return DashboardResponse.model_validate(dashboard)


@router.get("/{dashboard_id}", response_model=DashboardResponse)
async def get_dashboard(
    dashboard_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get dashboard by ID.
    """
    dashboard = await dashboard_crud.get(db, dashboard_id)
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    
    # Check access
    if dashboard.user_id != current_user.id and not dashboard.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return DashboardResponse.model_validate(dashboard)


@router.post("", response_model=DashboardResponse)
async def create_dashboard(
    dashboard_in: DashboardCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create new dashboard.
    """
    dashboard = await dashboard_crud.create_with_user(
        db,
        obj_in=dashboard_in,
        user_id=current_user.id
    )
    return DashboardResponse.model_validate(dashboard)


@router.put("/{dashboard_id}", response_model=DashboardResponse)
async def update_dashboard(
    dashboard_id: int,
    dashboard_in: DashboardUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update dashboard.
    """
    dashboard = await dashboard_crud.get(db, dashboard_id)
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    
    if dashboard.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not your dashboard"
        )
    
    updated = await dashboard_crud.update(db, db_obj=dashboard, obj_in=dashboard_in)
    return DashboardResponse.model_validate(updated)


@router.post("/{dashboard_id}/set-default", response_model=DashboardResponse)
async def set_default_dashboard(
    dashboard_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Set dashboard as default.
    """
    dashboard = await dashboard_crud.set_default(
        db,
        dashboard_id=dashboard_id,
        user_id=current_user.id
    )
    
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found or not yours"
        )
    
    return DashboardResponse.model_validate(dashboard)


@router.post("/{dashboard_id}/duplicate", response_model=DashboardResponse)
async def duplicate_dashboard(
    dashboard_id: int,
    new_name: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Duplicate a dashboard.
    """
    dashboard = await dashboard_crud.duplicate(
        db,
        dashboard_id=dashboard_id,
        user_id=current_user.id,
        new_name=new_name
    )
    
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    
    return DashboardResponse.model_validate(dashboard)


@router.delete("/{dashboard_id}", response_model=MessageResponse)
async def delete_dashboard(
    dashboard_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete dashboard.
    """
    dashboard = await dashboard_crud.get(db, dashboard_id)
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    
    if dashboard.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not your dashboard"
        )
    
    await dashboard_crud.delete(db, id=dashboard_id)
    return MessageResponse(message="Dashboard deleted successfully")
