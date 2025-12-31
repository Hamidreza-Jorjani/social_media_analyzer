from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user, get_current_analyst, PaginationParams
from app.crud import trend as trend_crud
from app.models.user import User
from app.services.trend_service import trend_service
from app.services.tasks import detect_trends
from app.schemas.trend import (
    TrendCreate,
    TrendUpdate,
    TrendResponse,
    TrendWithDetails,
    TrendingItem
)
from app.schemas.base import MessageResponse

router = APIRouter()


@router.get("", response_model=List[TrendResponse])
async def get_trends(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    active_only: bool = True,
    current_user: User = Depends(get_current_user)
):
    """
    Get trends.
    """
    if active_only:
        trends = await trend_crud.get_active(
            db,
            skip=pagination.skip,
            limit=pagination.limit
        )
    else:
        trends = await trend_crud.get_multi(
            db,
            skip=pagination.skip,
            limit=pagination.limit
        )
    
    return [TrendResponse.model_validate(t) for t in trends]


@router.get("/summary")
async def get_trend_summary(
    db: AsyncSession = Depends(get_db),
    hours: int = Query(default=24, ge=1, le=168),
    current_user: User = Depends(get_current_user)
):
    """
    Get trend summary including hashtags, keywords, and active trends.
    """
    summary = await trend_service.get_trend_summary(db, hours=hours)
    return summary


@router.get("/hashtags", response_model=List[TrendingItem])
async def get_trending_hashtags(
    db: AsyncSession = Depends(get_db),
    hours: int = Query(default=24, ge=1, le=168),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get trending hashtags.
    """
    hashtags = await trend_service.get_trending_hashtags(
        db,
        hours=hours,
        limit=limit
    )
    return [TrendingItem(item=h["hashtag"], count=h["count"]) for h in hashtags]


@router.get("/keywords", response_model=List[TrendingItem])
async def get_trending_keywords(
    db: AsyncSession = Depends(get_db),
    hours: int = Query(default=24, ge=1, le=168),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get trending keywords from analysis results.
    """
    keywords = await trend_service.get_trending_keywords(
        db,
        hours=hours,
        limit=limit
    )
    return [TrendingItem(item=k["keyword"], count=k["count"]) for k in keywords]


@router.get("/sentiment")
async def get_sentiment_trends(
    db: AsyncSession = Depends(get_db),
    hours: int = Query(default=24, ge=1, le=168),
    interval: str = Query(default="1h", regex="^(1h|6h|1d)$"),
    current_user: User = Depends(get_current_user)
):
    """
    Get sentiment trends over time.
    """
    trends = await trend_service.get_sentiment_trends(
        db,
        hours=hours,
        interval=interval
    )
    return trends


@router.get("/volume")
async def get_volume_trends(
    db: AsyncSession = Depends(get_db),
    hours: int = Query(default=24, ge=1, le=168),
    interval: str = Query(default="1h", regex="^(1h|6h|1d)$"),
    platform: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get post volume trends over time.
    """
    trends = await trend_service.get_volume_trends(
        db,
        hours=hours,
        interval=interval,
        platform=platform
    )
    return trends


@router.get("/top/volume", response_model=List[TrendResponse])
async def get_top_trends_by_volume(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(default=10, ge=1, le=50),
    current_user: User = Depends(get_current_user)
):
    """
    Get top trends by volume.
    """
    trends = await trend_crud.get_top_by_volume(db, limit=limit)
    return [TrendResponse.model_validate(t) for t in trends]


@router.get("/top/growth", response_model=List[TrendResponse])
async def get_top_trends_by_growth(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(default=10, ge=1, le=50),
    current_user: User = Depends(get_current_user)
):
    """
    Get top trends by growth rate.
    """
    trends = await trend_crud.get_top_by_growth(db, limit=limit)
    return [TrendResponse.model_validate(t) for t in trends]


@router.get("/stats")
async def get_trend_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get trend statistics.
    """
    stats = await trend_crud.get_stats(db)
    return stats


@router.get("/{trend_id}", response_model=TrendWithDetails)
async def get_trend(
    trend_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get trend by ID with details.
    """
    trend = await trend_crud.get(db, trend_id)
    if not trend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trend not found"
        )
    
    return TrendWithDetails.model_validate(trend)


@router.post("/detect", response_model=MessageResponse)
async def trigger_trend_detection(
    hours: int = Query(default=24, ge=1, le=168),
    min_count: int = Query(default=10, ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Trigger trend detection (analyst only).
    """
    detect_trends.delay(hours=hours, min_count=min_count)
    return MessageResponse(message="Trend detection queued")


@router.post("", response_model=TrendResponse)
async def create_trend(
    trend_in: TrendCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Create new trend manually (analyst only).
    """
    trend = await trend_crud.create(db, obj_in=trend_in)
    return TrendResponse.model_validate(trend)


@router.put("/{trend_id}", response_model=TrendResponse)
async def update_trend(
    trend_id: int,
    trend_in: TrendUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Update trend.
    """
    trend = await trend_crud.get(db, trend_id)
    if not trend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trend not found"
        )
    
    updated = await trend_crud.update(db, db_obj=trend, obj_in=trend_in)
    return TrendResponse.model_validate(updated)


@router.delete("/{trend_id}", response_model=MessageResponse)
async def delete_trend(
    trend_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Delete trend.
    """
    trend = await trend_crud.delete(db, id=trend_id)
    if not trend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trend not found"
        )
    
    return MessageResponse(message="Trend deleted successfully")
