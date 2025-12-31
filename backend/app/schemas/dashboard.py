from typing import Optional, Dict, Any, List
from pydantic import Field
from app.schemas.base import BaseSchema, TimestampSchema


class WidgetConfig(BaseSchema):
    """Dashboard widget configuration."""
    
    widget_id: str
    widget_type: str  # chart, table, metric, map, wordcloud
    title: str
    position: Dict[str, int]  # {"x": 0, "y": 0, "w": 2, "h": 2}
    config: Optional[Dict[str, Any]] = None
    data_source: Optional[str] = None  # API endpoint or query


class DashboardBase(BaseSchema):
    """Base dashboard schema."""
    
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class DashboardCreate(DashboardBase):
    """Schema for creating a dashboard."""
    
    layout: Optional[Dict[str, Any]] = None
    widgets: Optional[List[WidgetConfig]] = None
    filters: Optional[Dict[str, Any]] = None
    refresh_interval: int = 300
    is_default: bool = False
    is_public: bool = False


class DashboardUpdate(BaseSchema):
    """Schema for updating a dashboard."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    layout: Optional[Dict[str, Any]] = None
    widgets: Optional[List[WidgetConfig]] = None
    filters: Optional[Dict[str, Any]] = None
    refresh_interval: Optional[int] = None
    is_default: Optional[bool] = None
    is_public: Optional[bool] = None


class DashboardResponse(DashboardBase, TimestampSchema):
    """Dashboard response schema."""
    
    id: int
    layout: Optional[Dict[str, Any]] = None
    widgets: Optional[List[Dict[str, Any]]] = None
    filters: Optional[Dict[str, Any]] = None
    refresh_interval: int = 300
    is_default: bool
    is_public: bool
    user_id: int


class DashboardBrief(BaseSchema):
    """Brief dashboard info."""
    
    id: int
    name: str
    is_default: bool
    is_public: bool


class WidgetData(BaseSchema):
    """Data response for a widget."""
    
    widget_id: str
    data: Any
    updated_at: str
