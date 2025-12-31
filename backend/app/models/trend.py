from sqlalchemy import (
    Column, String, Integer, Text, JSON,
    ForeignKey, Float, DateTime
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Trend(BaseModel):
    """Detected trends from analysis."""
    
    __tablename__ = "trends"
    
    # Trend identification
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Trend metrics
    volume = Column(Integer, default=0)  # Number of posts
    growth_rate = Column(Float, nullable=True)  # Percentage growth
    velocity = Column(Float, nullable=True)  # Speed of trend
    peak_time = Column(DateTime, nullable=True)
    
    # Trend details
    keywords = Column(JSON, nullable=True)  # Related keywords
    hashtags = Column(JSON, nullable=True)  # Related hashtags
    sentiment_distribution = Column(JSON, nullable=True)
    # Example: {"positive": 0.6, "negative": 0.2, "neutral": 0.2}
    
    # Time series data
    time_series = Column(JSON, nullable=True)
    # Example: [{"time": "2024-01-01T00:00:00", "count": 100}, ...]
    
    # Geographic distribution
    geo_distribution = Column(JSON, nullable=True)
    
    # Related entities
    top_authors = Column(JSON, nullable=True)
    top_posts = Column(JSON, nullable=True)
    
    # Status
    is_active = Column(String(10), default="active")  # active, declining, ended
    
    # Foreign keys
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=True)
    
    # Relationships
    analysis = relationship("Analysis", back_populates="trends")
    
    def __repr__(self):
        return f"<Trend(id={self.id}, name='{self.name}', volume={self.volume})>"
