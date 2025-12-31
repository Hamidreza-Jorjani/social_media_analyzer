from sqlalchemy import (
    Column, String, Integer, Text, JSON, 
    ForeignKey, DateTime, Float, Boolean
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Post(BaseModel):
    """Social media post/content model."""
    
    __tablename__ = "posts"
    
    # Platform identification
    platform_id = Column(String(255), unique=True, index=True, nullable=False)
    platform = Column(String(50), index=True, nullable=False)
    
    # Content
    content = Column(Text, nullable=True)
    content_normalized = Column(Text, nullable=True)  # Normalized Persian text
    language = Column(String(10), default="fa", index=True)
    
    # URLs and media
    url = Column(String(500), nullable=True)
    media_urls = Column(JSON, nullable=True)
    
    # Engagement metrics
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    
    # Metadata
    posted_at = Column(DateTime, index=True, nullable=True)
    hashtags = Column(JSON, nullable=True)
    mentions = Column(JSON, nullable=True)
    
    # Processing status
    is_processed = Column(Boolean, default=False, index=True)
    processing_error = Column(Text, nullable=True)
    
    # Foreign keys
    data_source_id = Column(Integer, ForeignKey("data_sources.id"), nullable=True)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=True)
    
    # Relationships
    data_source = relationship("DataSource", back_populates="posts")
    author = relationship("Author", back_populates="posts")
    analysis_results = relationship(
        "AnalysisResult",
        back_populates="post",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        content_preview = self.content[:50] if self.content else "No content"
        return f"<Post(id={self.id}, platform='{self.platform}', content='{content_preview}...')>"
