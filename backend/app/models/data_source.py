from sqlalchemy import Column, String, Boolean, Enum as SQLEnum, Text, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import enum


class SourcePlatform(str, enum.Enum):
    """Supported social media platforms."""
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    TELEGRAM = "telegram"
    LINKEDIN = "linkedin"
    YOUTUBE = "youtube"
    NEWS = "news"
    FORUM = "forum"
    CUSTOM = "custom"


class DataSource(BaseModel):
    """Data source configuration for social media platforms."""
    
    __tablename__ = "data_sources"
    
    # Source identification
    name = Column(String(255), nullable=False)
    platform = Column(
        SQLEnum(SourcePlatform),
        default=SourcePlatform.CUSTOM,
        nullable=False,
        index=True
    )
    
    # Connection details
    api_endpoint = Column(String(500), nullable=True)
    credentials = Column(JSON, nullable=True)  # Encrypted in production
    
    # Configuration
    collection_config = Column(JSON, nullable=True)
    description = Column(Text, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    last_sync_at = Column(String(50), nullable=True)
    
    # Relationships
    posts = relationship("Post", back_populates="data_source", lazy="dynamic")
    
    def __repr__(self):
        return f"<DataSource(id={self.id}, name='{self.name}', platform='{self.platform}')>"
