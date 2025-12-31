from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import Field, HttpUrl
from app.schemas.base import BaseSchema, TimestampSchema
from app.models.data_source import SourcePlatform


class DataSourceBase(BaseSchema):
    """Base data source schema."""
    
    name: str = Field(..., min_length=1, max_length=255)
    platform: SourcePlatform = SourcePlatform.CUSTOM
    description: Optional[str] = None


class DataSourceCreate(DataSourceBase):
    """Schema for creating a data source."""
    
    api_endpoint: Optional[str] = None
    credentials: Optional[Dict[str, Any]] = None
    collection_config: Optional[Dict[str, Any]] = None


class DataSourceUpdate(BaseSchema):
    """Schema for updating a data source."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    platform: Optional[SourcePlatform] = None
    api_endpoint: Optional[str] = None
    credentials: Optional[Dict[str, Any]] = None
    collection_config: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class DataSourceResponse(DataSourceBase, TimestampSchema):
    """Data source response schema."""
    
    id: int
    api_endpoint: Optional[str] = None
    collection_config: Optional[Dict[str, Any]] = None
    is_active: bool
    last_sync_at: Optional[str] = None


class DataSourceBrief(BaseSchema):
    """Brief data source info."""
    
    id: int
    name: str
    platform: SourcePlatform
    is_active: bool


class DataSourceStats(BaseSchema):
    """Data source statistics."""
    
    id: int
    name: str
    platform: SourcePlatform
    total_posts: int = 0
    total_authors: int = 0
    last_sync_at: Optional[str] = None
