from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import Field
from app.schemas.base import BaseSchema, TimestampSchema
from app.schemas.author import AuthorBrief
from app.schemas.data_source import DataSourceBrief


class PostBase(BaseSchema):
    """Base post schema."""
    
    platform_id: str = Field(..., max_length=255)
    platform: str = Field(..., max_length=50)
    content: Optional[str] = None
    language: str = Field(default="fa", max_length=10)


class PostCreate(PostBase):
    """Schema for creating a post."""
    
    url: Optional[str] = None
    media_urls: Optional[List[str]] = None
    likes_count: int = 0
    comments_count: int = 0
    shares_count: int = 0
    views_count: int = 0
    posted_at: Optional[datetime] = None
    hashtags: Optional[List[str]] = None
    mentions: Optional[List[str]] = None
    data_source_id: Optional[int] = None
    author_id: Optional[int] = None


class PostUpdate(BaseSchema):
    """Schema for updating a post."""
    
    content: Optional[str] = None
    content_normalized: Optional[str] = None
    url: Optional[str] = None
    media_urls: Optional[List[str]] = None
    likes_count: Optional[int] = None
    comments_count: Optional[int] = None
    shares_count: Optional[int] = None
    views_count: Optional[int] = None
    hashtags: Optional[List[str]] = None
    mentions: Optional[List[str]] = None
    is_processed: Optional[bool] = None
    processing_error: Optional[str] = None


class PostResponse(PostBase, TimestampSchema):
    """Post response schema."""
    
    id: int
    url: Optional[str] = None
    media_urls: Optional[List[str]] = None
    likes_count: int = 0
    comments_count: int = 0
    shares_count: int = 0
    views_count: int = 0
    posted_at: Optional[datetime] = None
    hashtags: Optional[List[str]] = None
    mentions: Optional[List[str]] = None
    is_processed: bool = False
    data_source_id: Optional[int] = None
    author_id: Optional[int] = None


class PostWithRelations(PostResponse):
    """Post with related objects."""
    
    author: Optional[AuthorBrief] = None
    data_source: Optional[DataSourceBrief] = None


class PostBrief(BaseSchema):
    """Brief post info for embedding."""
    
    id: int
    platform: str
    content_preview: Optional[str] = None
    posted_at: Optional[datetime] = None
    
    @classmethod
    def from_post(cls, post) -> "PostBrief":
        content_preview = None
        if post.content:
            content_preview = post.content[:100] + "..." if len(post.content) > 100 else post.content
        return cls(
            id=post.id,
            platform=post.platform,
            content_preview=content_preview,
            posted_at=post.posted_at
        )


class PostBulkCreate(BaseSchema):
    """Schema for bulk creating posts."""
    
    posts: List[PostCreate]


class PostFilter(BaseSchema):
    """Post filter parameters."""
    
    platform: Optional[str] = None
    language: Optional[str] = None
    data_source_id: Optional[int] = None
    author_id: Optional[int] = None
    is_processed: Optional[bool] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search: Optional[str] = None
    hashtags: Optional[List[str]] = None
