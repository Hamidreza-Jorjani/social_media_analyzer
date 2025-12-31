from sqlalchemy import Column, String, Integer, Text, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Author(BaseModel):
    """Social media author/account model."""
    
    __tablename__ = "authors"
    
    # Platform identification
    platform_id = Column(String(255), index=True, nullable=False)
    platform = Column(String(50), index=True, nullable=False)
    
    # Profile information
    username = Column(String(255), index=True, nullable=True)
    display_name = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    profile_url = Column(String(500), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Metrics
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    posts_count = Column(Integer, default=0)
    
    # Calculated scores (from BRAIN)
    influence_score = Column(Float, nullable=True)
    pagerank_score = Column(Float, nullable=True)
    
    # Additional data - RENAMED from 'metadata' to 'extra_data'
    extra_data = Column(JSON, nullable=True)
    
    # Relationships
    posts = relationship("Post", back_populates="author", lazy="dynamic")
    
    def __repr__(self):
        return f"<Author(id={self.id}, username='{self.username}', platform='{self.platform}')>"
