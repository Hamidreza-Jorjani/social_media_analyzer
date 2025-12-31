from typing import Optional, Dict, Any, List
from pydantic import Field
from app.schemas.base import BaseSchema


class BrainHealthResponse(BaseSchema):
    """BRAIN service health response."""
    
    status: str
    gpu_available: bool
    gpu_memory_used: Optional[float] = None
    gpu_memory_total: Optional[float] = None


class TextAnalysisRequest(BaseSchema):
    """Request for text analysis to BRAIN."""
    
    texts: List[str]
    text_ids: List[str]
    analysis_types: List[str] = ["sentiment", "emotion", "keywords"]
    language: str = "fa"
    config: Optional[Dict[str, Any]] = None


class TextAnalysisResponse(BaseSchema):
    """Response from BRAIN text analysis."""
    
    text_id: str
    sentiment: Optional[Dict[str, Any]] = None
    emotions: Optional[Dict[str, float]] = None
    keywords: Optional[List[str]] = None
    entities: Optional[List[Dict[str, Any]]] = None
    summary: Optional[str] = None
    topics: Optional[List[Dict[str, Any]]] = None


class BatchAnalysisRequest(BaseSchema):
    """Batch analysis request to BRAIN."""
    
    analysis_id: int
    posts: List[Dict[str, Any]]
    config: Dict[str, Any]
    callback_url: Optional[str] = None


class BatchAnalysisResponse(BaseSchema):
    """Batch analysis response from BRAIN."""
    
    analysis_id: int
    status: str
    task_id: Optional[str] = None
    message: Optional[str] = None


class GraphAnalysisRequest(BaseSchema):
    """Request for graph analysis to BRAIN."""
    
    analysis_id: int
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    algorithms: List[str] = ["pagerank", "community_detection"]
    config: Optional[Dict[str, Any]] = None


class GraphAnalysisResponse(BaseSchema):
    """Response from BRAIN graph analysis."""
    
    analysis_id: int
    nodes: List[Dict[str, Any]]  # With computed metrics
    communities: Optional[List[Dict[str, Any]]] = None
    stats: Optional[Dict[str, Any]] = None


class SummarizationRequest(BaseSchema):
    """Request for text summarization to BRAIN."""
    
    texts: List[str]
    max_length: int = 150
    min_length: int = 30
    language: str = "fa"


class TrendDetectionRequest(BaseSchema):
    """Request for trend detection to BRAIN."""
    
    posts: List[Dict[str, Any]]
    time_field: str = "posted_at"
    content_field: str = "content"
    min_trend_size: int = 10
    time_window: str = "1h"
