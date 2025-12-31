from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import Field
from app.schemas.base import BaseSchema, TimestampSchema


class TrendBase(BaseSchema):
    """Base trend schema."""
    
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class TrendCreate(TrendBase):
    """Schema for creating a trend."""
    
    volume: int = 0
    growth_rate: Optional[float] = None
    velocity: Optional[float] = None
    peak_time: Optional[datetime] = None
    keywords: Optional[List[str]] = None
    hashtags: Optional[List[str]] = None
    sentiment_distribution: Optional[Dict[str, float]] = None
    time_series: Optional[List[Dict[str, Any]]] = None
    geo_distribution: Optional[Dict[str, Any]] = None
    top_authors: Optional[List[Dict[str, Any]]] = None
    top_posts: Optional[List[int]] = None
    analysis_id: Optional[int] = None


class TrendUpdate(BaseSchema):
    """Schema for updating a trend."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    volume: Optional[int] = None
    growth_rate: Optional[float] = None
    is_active: Optional[str] = None


class TrendResponse(TrendBase, TimestampSchema):
    """Trend response schema."""
    
    id: int
    volume: int = 0
    growth_rate: Optional[float] = None
    velocity: Optional[float] = None
    peak_time: Optional[datetime] = None
    keywords: Optional[List[str]] = None
    hashtags: Optional[List[str]] = None
    sentiment_distribution: Optional[Dict[str, float]] = None
    is_active: str = "active"
    analysis_id: Optional[int] = None


class TrendWithDetails(TrendResponse):
    """Trend with full details."""
    
    time_series: Optional[List[Dict[str, Any]]] = None
    geo_distribution: Optional[Dict[str, Any]] = None
    top_authors: Optional[List[Dict[str, Any]]] = None
    top_posts: Optional[List[int]] = None


class TrendBrief(BaseSchema):
    """Brief trend info."""
    
    id: int
    name: str
    volume: int
    growth_rate: Optional[float] = None
    is_active: str


class TrendingItem(BaseSchema):
    """Single trending item (keyword, hashtag, etc.)."""
    
    item: str
    count: int
    growth: Optional[float] = None
    sentiment: Optional[str] = None
