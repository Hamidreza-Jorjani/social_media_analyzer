from typing import Optional, Dict, Any
from pydantic import Field
from app.schemas.base import BaseSchema, TimestampSchema


class AuthorBase(BaseSchema):
    """Base author schema."""
    
    platform_id: str = Field(..., max_length=255)
    platform: str = Field(..., max_length=50)
    username: Optional[str] = Field(None, max_length=255)
    display_name: Optional[str] = Field(None, max_length=255)


class AuthorCreate(AuthorBase):
    """Schema for creating an author."""
    
    bio: Optional[str] = None
    profile_url: Optional[str] = None
    avatar_url: Optional[str] = None
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    extra_data: Optional[Dict[str, Any]] = None


class AuthorUpdate(BaseSchema):
    """Schema for updating an author."""
    
    username: Optional[str] = Field(None, max_length=255)
    display_name: Optional[str] = Field(None, max_length=255)
    bio: Optional[str] = None
    profile_url: Optional[str] = None
    avatar_url: Optional[str] = None
    followers_count: Optional[int] = None
    following_count: Optional[int] = None
    posts_count: Optional[int] = None
    influence_score: Optional[float] = None
    pagerank_score: Optional[float] = None
    extra_data: Optional[Dict[str, Any]] = None


class AuthorResponse(AuthorBase, TimestampSchema):
    """Author response schema."""
    
    id: int
    bio: Optional[str] = None
    profile_url: Optional[str] = None
    avatar_url: Optional[str] = None
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    influence_score: Optional[float] = None
    pagerank_score: Optional[float] = None


class AuthorBrief(BaseSchema):
    """Brief author info for embedding."""
    
    id: int
    username: Optional[str] = None
    display_name: Optional[str] = None
    platform: str


class AuthorWithMetrics(AuthorResponse):
    """Author with analysis metrics."""
    
    total_posts_analyzed: int = 0
    average_sentiment: Optional[float] = None
    top_topics: Optional[list] = None
    engagement_rate: Optional[float] = None
