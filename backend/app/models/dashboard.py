from sqlalchemy import (
    Column, String, Integer, Text, JSON,
    ForeignKey, Boolean
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Dashboard(BaseModel):
    """User dashboard configuration."""
    
    __tablename__ = "dashboards"
    
    # Dashboard identification
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Configuration
    layout = Column(JSON, nullable=True)
    # Example: {"widgets": [...], "grid": {...}}
    
    widgets = Column(JSON, nullable=True)
    # Example: [
    #     {"type": "sentiment_chart", "position": {"x": 0, "y": 0}, "config": {...}},
    #     {"type": "trend_list", "position": {"x": 1, "y": 0}, "config": {...}}
    # ]
    
    filters = Column(JSON, nullable=True)
    # Default filters for dashboard
    
    refresh_interval = Column(Integer, default=300)  # Seconds
    
    # Status
    is_default = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="dashboards")
    
    def __repr__(self):
        return f"<Dashboard(id={self.id}, name='{self.name}', user_id={self.user_id})>"

