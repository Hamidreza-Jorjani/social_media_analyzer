from sqlalchemy import (
    Column, String, Integer, Text, JSON,
    ForeignKey, Enum as SQLEnum, Float
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import enum


class AnalysisType(str, enum.Enum):
    """Types of analysis that can be performed."""
    SENTIMENT = "sentiment"
    EMOTION = "emotion"
    SUMMARIZATION = "summarization"
    TOPIC_MODELING = "topic_modeling"
    KEYWORD_EXTRACTION = "keyword_extraction"
    ENTITY_RECOGNITION = "entity_recognition"
    TREND_DETECTION = "trend_detection"
    GRAPH_ANALYSIS = "graph_analysis"
    FULL = "full"


class AnalysisStatus(str, enum.Enum):
    """Status of an analysis job."""
    PENDING = "pending"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Analysis(BaseModel):
    """Analysis job model."""
    
    __tablename__ = "analyses"
    
    # Job identification
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Analysis configuration
    analysis_type = Column(
        SQLEnum(AnalysisType),
        default=AnalysisType.FULL,
        nullable=False,
        index=True
    )
    config = Column(JSON, nullable=True)  # Analysis parameters
    
    # Data selection
    query_filters = Column(JSON, nullable=True)  # Filters for selecting posts
    post_count = Column(Integer, default=0)  # Number of posts to analyze
    
    # Status
    status = Column(
        SQLEnum(AnalysisStatus),
        default=AnalysisStatus.PENDING,
        nullable=False,
        index=True
    )
    progress = Column(Float, default=0.0)  # 0.0 to 100.0
    
    # Results
    summary = Column(JSON, nullable=True)  # Summary of results
    error_message = Column(Text, nullable=True)
    
    # Timing
    started_at = Column(String(50), nullable=True)
    completed_at = Column(String(50), nullable=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="analyses")
    results = relationship(
        "AnalysisResult",
        back_populates="analysis",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )
    trends = relationship(
        "Trend",
        back_populates="analysis",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Analysis(id={self.id}, name='{self.name}', type='{self.analysis_type}', status='{self.status}')>"
