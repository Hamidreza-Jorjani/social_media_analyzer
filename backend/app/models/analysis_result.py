from sqlalchemy import (
    Column, String, Integer, Text, JSON,
    ForeignKey, Float
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class AnalysisResult(BaseModel):
    """Individual analysis result for a post."""
    
    __tablename__ = "analysis_results"
    
    # Sentiment Analysis
    sentiment_label = Column(String(20), nullable=True)  # positive, negative, neutral
    sentiment_score = Column(Float, nullable=True)  # -1.0 to 1.0
    sentiment_confidence = Column(Float, nullable=True)  # 0.0 to 1.0
    
    # Emotion Analysis
    emotions = Column(JSON, nullable=True)
    # Example: {"joy": 0.8, "sadness": 0.1, "anger": 0.05, "fear": 0.05}
    dominant_emotion = Column(String(50), nullable=True)
    
    # Text Analysis
    summary = Column(Text, nullable=True)
    keywords = Column(JSON, nullable=True)  # ["keyword1", "keyword2", ...]
    topics = Column(JSON, nullable=True)  # [{"topic": "politics", "score": 0.85}, ...]
    
    # Entity Recognition
    entities = Column(JSON, nullable=True)
    # Example: [{"text": "تهران", "type": "location", "start": 10, "end": 15}]
    
    # Graph metrics (from BRAIN)
    node_degree = Column(Integer, nullable=True)
    centrality_score = Column(Float, nullable=True)
    community_id = Column(Integer, nullable=True)
    
    # Full raw results from BRAIN
    raw_results = Column(JSON, nullable=True)
    
    # Foreign keys
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False, index=True)
    
    # Relationships
    post = relationship("Post", back_populates="analysis_results")
    analysis = relationship("Analysis", back_populates="results")
    
    def __repr__(self):
        return f"<AnalysisResult(id={self.id}, post_id={self.post_id}, sentiment='{self.sentiment_label}')>"
