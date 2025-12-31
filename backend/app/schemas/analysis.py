from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import Field
from app.schemas.base import BaseSchema, TimestampSchema
from app.schemas.user import UserBrief
from app.models.analysis import AnalysisType, AnalysisStatus


class AnalysisBase(BaseSchema):
    """Base analysis schema."""
    
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    analysis_type: AnalysisType = AnalysisType.FULL


class AnalysisCreate(AnalysisBase):
    """Schema for creating an analysis."""
    
    config: Optional[Dict[str, Any]] = None
    query_filters: Optional[Dict[str, Any]] = None
    post_count: Optional[int] = None


class AnalysisUpdate(BaseSchema):
    """Schema for updating an analysis."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[AnalysisStatus] = None


class AnalysisResponse(AnalysisBase, TimestampSchema):
    """Analysis response schema."""
    
    id: int
    config: Optional[Dict[str, Any]] = None
    query_filters: Optional[Dict[str, Any]] = None
    post_count: int = 0
    status: AnalysisStatus
    progress: float = 0.0
    summary: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    user_id: int


class AnalysisWithUser(AnalysisResponse):
    """Analysis with user info."""
    
    user: Optional[UserBrief] = None


class AnalysisBrief(BaseSchema):
    """Brief analysis info."""
    
    id: int
    name: str
    analysis_type: AnalysisType
    status: AnalysisStatus
    progress: float = 0.0


class AnalysisConfig(BaseSchema):
    """Analysis configuration options."""
    
    # Sentiment analysis
    sentiment_enabled: bool = True
    sentiment_model: str = "default"
    
    # Emotion analysis
    emotion_enabled: bool = True
    emotion_categories: List[str] = ["joy", "sadness", "anger", "fear", "surprise"]
    
    # Summarization
    summarization_enabled: bool = True
    summary_max_length: int = 200
    
    # Topic modeling
    topic_modeling_enabled: bool = True
    num_topics: int = 10
    
    # Keyword extraction
    keyword_extraction_enabled: bool = True
    max_keywords: int = 20
    
    # Entity recognition
    ner_enabled: bool = True
    entity_types: List[str] = ["person", "location", "organization"]
    
    # Graph analysis
    graph_analysis_enabled: bool = True
    calculate_pagerank: bool = True
    detect_communities: bool = True


class AnalysisProgress(BaseSchema):
    """Analysis progress update."""
    
    analysis_id: int
    status: AnalysisStatus
    progress: float
    current_step: Optional[str] = None
    message: Optional[str] = None


class AnalysisSubmit(BaseSchema):
    """Schema for submitting analysis to BRAIN."""
    
    analysis_id: int
    posts: List[Dict[str, Any]]
    config: AnalysisConfig
