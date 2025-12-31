from typing import Optional, Dict, Any, List
from pydantic import Field
from app.schemas.base import BaseSchema, TimestampSchema
from app.schemas.post import PostBrief


class SentimentResult(BaseSchema):
    """Sentiment analysis result."""
    
    label: str  # positive, negative, neutral
    score: float = Field(..., ge=-1.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)


class EmotionResult(BaseSchema):
    """Emotion analysis result."""
    
    emotions: Dict[str, float]
    dominant_emotion: str


class EntityResult(BaseSchema):
    """Named entity result."""
    
    text: str
    entity_type: str
    start: int
    end: int
    confidence: Optional[float] = None


class TopicResult(BaseSchema):
    """Topic result."""
    
    topic: str
    score: float
    keywords: Optional[List[str]] = None


class AnalysisResultBase(BaseSchema):
    """Base analysis result schema."""
    
    sentiment_label: Optional[str] = None
    sentiment_score: Optional[float] = None
    sentiment_confidence: Optional[float] = None
    dominant_emotion: Optional[str] = None


class AnalysisResultCreate(AnalysisResultBase):
    """Schema for creating analysis result."""
    
    post_id: int
    analysis_id: int
    emotions: Optional[Dict[str, float]] = None
    summary: Optional[str] = None
    keywords: Optional[List[str]] = None
    topics: Optional[List[Dict[str, Any]]] = None
    entities: Optional[List[Dict[str, Any]]] = None
    node_degree: Optional[int] = None
    centrality_score: Optional[float] = None
    community_id: Optional[int] = None
    raw_results: Optional[Dict[str, Any]] = None


class AnalysisResultResponse(AnalysisResultBase, TimestampSchema):
    """Analysis result response schema."""
    
    id: int
    post_id: int
    analysis_id: int
    emotions: Optional[Dict[str, float]] = None
    summary: Optional[str] = None
    keywords: Optional[List[str]] = None
    topics: Optional[List[Dict[str, Any]]] = None
    entities: Optional[List[Dict[str, Any]]] = None
    node_degree: Optional[int] = None
    centrality_score: Optional[float] = None
    community_id: Optional[int] = None


class AnalysisResultWithPost(AnalysisResultResponse):
    """Analysis result with post info."""
    
    post: Optional[PostBrief] = None


class AnalysisSummary(BaseSchema):
    """Aggregated analysis summary."""
    
    total_posts: int
    processed_posts: int
    
    # Sentiment distribution
    sentiment_distribution: Dict[str, int]
    average_sentiment_score: Optional[float] = None
    
    # Emotion distribution
    emotion_distribution: Dict[str, int]
    
    # Top items
    top_keywords: List[Dict[str, Any]]
    top_topics: List[Dict[str, Any]]
    top_entities: List[Dict[str, Any]]
    top_hashtags: List[Dict[str, Any]]
    
    # Time series
    sentiment_over_time: Optional[List[Dict[str, Any]]] = None
    volume_over_time: Optional[List[Dict[str, Any]]] = None


class BulkResultCreate(BaseSchema):
    """Bulk create analysis results."""
    
    results: List[AnalysisResultCreate]
