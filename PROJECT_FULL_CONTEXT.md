# Persian Social Media Analyzer - Full Context

## Quick Info
- **Architecture:** Frontend:3000 -> Backend:8000 -> BRAIN:8001
- **Database:** PostgreSQL:5432, Redis:6379
- **Credentials:** admin / Admin123!
- **Docs:** http://localhost:8000/docs

## Project Structure
```
/home/great/projects/social_media_analyzer
├── ai_document
│   ├── API.md
│   ├── OPENAPI.JSON
│   ├── PERSIAN_ANALYZER_FULL_CODE_FOR_AI.txt
│   └── TECHNICAL_FOR_MACHINE.md
├── app
│   ├── dashboard
│   │   └── page.tsx
│   ├── globals.css
│   └── layout.tsx
├── backend
│   ├── alembic
│   │   ├── versions
│   │   │   └── 20240101_0001_initial_migration.py
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── app
│   │   ├── api
│   │   │   ├── v1
│   │   │   │   ├── endpoints
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── analysis.py
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── authors.py
│   │   │   │   │   ├── brain.py
│   │   │   │   │   ├── dashboard.py
│   │   │   │   │   ├── data_sources.py
│   │   │   │   │   ├── graph.py
│   │   │   │   │   ├── graph.py.backup
│   │   │   │   │   ├── posts.py
│   │   │   │   │   ├── trends.py
│   │   │   │   │   └── users.py
│   │   │   │   ├── __init__.py
│   │   │   │   └── router.py
│   │   │   ├── __init__.py
│   │   │   └── deps.py
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── init_data.py
│   │   │   └── security.py
│   │   ├── crud
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── crud_analysis.py
│   │   │   ├── crud_analysis_result.py
│   │   │   ├── crud_author.py
│   │   │   ├── crud_dashboard.py
│   │   │   ├── crud_data_source.py
│   │   │   ├── crud_graph.py
│   │   │   ├── crud_post.py
│   │   │   ├── crud_trend.py
│   │   │   └── crud_user.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── analysis.py
│   │   │   ├── analysis_result.py
│   │   │   ├── author.py
│   │   │   ├── base.py
│   │   │   ├── dashboard.py
│   │   │   ├── data_source.py
│   │   │   ├── graph.py
│   │   │   ├── post.py
│   │   │   ├── trend.py
│   │   │   └── user.py
│   │   ├── schemas
│   │   │   ├── __init__.py
│   │   │   ├── analysis.py
│   │   │   ├── analysis_result.py
│   │   │   ├── auth.py
│   │   │   ├── author.py
│   │   │   ├── base.py
│   │   │   ├── brain.py
│   │   │   ├── dashboard.py
│   │   │   ├── data_source.py
│   │   │   ├── graph.py
│   │   │   ├── post.py
│   │   │   ├── trend.py
│   │   │   └── user.py
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   ├── analysis_service.py
│   │   │   ├── auth_service.py
│   │   │   ├── base.py
│   │   │   ├── brain_service.py
│   │   │   ├── celery_app.py
│   │   │   ├── dashboard_service.py
│   │   │   ├── graph_service.py
│   │   │   ├── redis_service.py
│   │   │   ├── tasks.py
│   │   │   └── trend_service.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   ├── datetime.py
│   │   │   ├── json.py
│   │   │   ├── pagination.py
│   │   │   ├── security.py
│   │   │   ├── text.py
│   │   │   └── validators.py
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── main.py
│   ├── scripts
│   │   ├── init_db.py
│   │   ├── migrate.sh
│   │   ├── run_celery.sh
│   │   ├── run_celery_beat.sh
│   │   ├── run_dev.sh
│   │   ├── run_tests.sh
│   │   ├── seed_data.py
│   │   ├── start.sh
│   │   ├── stop.sh
│   │   └── verify_project.sh
│   ├── tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_api.py
│   │   ├── test_crud.py
│   │   ├── test_models.py
│   │   ├── test_schemas.py
│   │   └── test_utils.py
│   ├── Dockerfile
│   ├── README.md
│   ├── alembic.ini
│   ├── docker-compose.dev.yml
│   ├── docker-compose.yml
│   ├── docker-compose.yml.backup
│   ├── pytest.ini
│   ├── requirements.txt
│   └── technical_for_machine.md
├── brain
│   ├── app
│   │   ├── routers
│   │   │   ├── __init__.py
│   │   │   ├── analysis.py
│   │   │   ├── batch.py
│   │   │   └── graph.py
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── main.py
│   │   └── mock_data.py
│   ├── models
│   ├── tests
│   ├── Dockerfile
│   ├── README.md
│   ├── docker-compose.yml
│   └── requirements.txt
├── data
│   ├── postgres  [error opening dir]
│   └── redis
│       ├── appendonlydir  [error opening dir]
│       └── dump.rdb
├── scripts
│   ├── collect_docker_debug.sh
│   ├── generate_docs.sh
│   ├── get_context.sh
│   ├── help.sh
│   ├── test_full_flow.sh
│   └── test_integration.sh
├── tests
│   ├── lib
│   │   └── common.sh
│   ├── results
│   ├── test_auth.sh
│   ├── test_brain.sh
│   ├── test_health.sh
│   └── test_posts.sh
├── Dockerfile.legacy
├── PROJECT_CONTEXT.md
├── PROJECT_FULL_CONTEXT.md
├── README.md
├── cleanup.sh
├── docker-compose.yml.legacy
├── full_test.sh
├── rebuild.sh
├── sma_diagnose.sh
├── start.sh
├── stop.sh
└── update.sh

32 directories, 148 files
```

## Database Models
### analysis.py
```python
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
```

### analysis_result.py
```python
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
```

### author.py
```python
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
```

### dashboard.py
```python
from sqlalchemy import (
    Column, String, Integer, Text, JSON,
    ForeignKey, Boolean
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Dashboard(BaseModel):
    """User dashboard configuration."""
    
    __tablename__ = "dashboards"
    
    # Dashboard identification
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Configuration
    layout = Column(JSON, nullable=True)
    # Example: {"widgets": [...], "grid": {...}}
    
    widgets = Column(JSON, nullable=True)
    # Example: [
    #     {"type": "sentiment_chart", "position": {"x": 0, "y": 0}, "config": {...}},
    #     {"type": "trend_list", "position": {"x": 1, "y": 0}, "config": {...}}
    # ]
    
    filters = Column(JSON, nullable=True)
    # Default filters for dashboard
    
    refresh_interval = Column(Integer, default=300)  # Seconds
    
    # Status
    is_default = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="dashboards")
    
    def __repr__(self):
        return f"<Dashboard(id={self.id}, name='{self.name}', user_id={self.user_id})>"

```

### data_source.py
```python
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
```

### graph.py
```python
from sqlalchemy import (
    Column, String, Integer, Text, JSON,
    ForeignKey, Float
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class GraphNode(BaseModel):
    """Graph node for network analysis."""
    
    __tablename__ = "graph_nodes"
    
    # Node identification
    node_id = Column(String(255), unique=True, index=True, nullable=False)
    node_type = Column(String(50), index=True, nullable=False)
    # Types: author, hashtag, topic, keyword, post
    
    # Node attributes
    label = Column(String(255), nullable=True)
    attributes = Column(JSON, nullable=True)
    
    # Centrality metrics
    degree = Column(Integer, default=0)
    in_degree = Column(Integer, default=0)
    out_degree = Column(Integer, default=0)
    pagerank = Column(Float, nullable=True)
    betweenness_centrality = Column(Float, nullable=True)
    closeness_centrality = Column(Float, nullable=True)
    eigenvector_centrality = Column(Float, nullable=True)
    
    # Community detection
    community_id = Column(Integer, nullable=True, index=True)
    
    # Relationships
    edges_from = relationship(
        "GraphEdge",
        foreign_keys="GraphEdge.source_id",
        back_populates="source_node",
        lazy="dynamic"
    )
    edges_to = relationship(
        "GraphEdge",
        foreign_keys="GraphEdge.target_id",
        back_populates="target_node",
        lazy="dynamic"
    )
    
    def __repr__(self):
        return f"<GraphNode(id={self.id}, node_id='{self.node_id}', type='{self.node_type}')>"


class GraphEdge(BaseModel):
    """Graph edge for network analysis."""
    
    __tablename__ = "graph_edges"
    
    # Edge identification
    edge_type = Column(String(50), index=True, nullable=False)
    # Types: mentions, replies_to, retweets, follows, co_occurrence
    
    # Edge attributes
    weight = Column(Float, default=1.0)
    attributes = Column(JSON, nullable=True)
    
    # Timestamps
    first_seen = Column(String(50), nullable=True)
    last_seen = Column(String(50), nullable=True)
    occurrence_count = Column(Integer, default=1)
    
    # Foreign keys
    source_id = Column(Integer, ForeignKey("graph_nodes.id"), nullable=False, index=True)
    target_id = Column(Integer, ForeignKey("graph_nodes.id"), nullable=False, index=True)
    
    # Relationships
    source_node = relationship(
        "GraphNode",
        foreign_keys=[source_id],
        back_populates="edges_from"
    )
    target_node = relationship(
        "GraphNode",
        foreign_keys=[target_id],
        back_populates="edges_to"
    )
    
    def __repr__(self):
        return f"<GraphEdge(id={self.id}, type='{self.edge_type}', source={self.source_id}, target={self.target_id})>"
```

### post.py
```python
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
```

### trend.py
```python
from sqlalchemy import (
    Column, String, Integer, Text, JSON,
    ForeignKey, Float, DateTime
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Trend(BaseModel):
    """Detected trends from analysis."""
    
    __tablename__ = "trends"
    
    # Trend identification
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Trend metrics
    volume = Column(Integer, default=0)  # Number of posts
    growth_rate = Column(Float, nullable=True)  # Percentage growth
    velocity = Column(Float, nullable=True)  # Speed of trend
    peak_time = Column(DateTime, nullable=True)
    
    # Trend details
    keywords = Column(JSON, nullable=True)  # Related keywords
    hashtags = Column(JSON, nullable=True)  # Related hashtags
    sentiment_distribution = Column(JSON, nullable=True)
    # Example: {"positive": 0.6, "negative": 0.2, "neutral": 0.2}
    
    # Time series data
    time_series = Column(JSON, nullable=True)
    # Example: [{"time": "2024-01-01T00:00:00", "count": 100}, ...]
    
    # Geographic distribution
    geo_distribution = Column(JSON, nullable=True)
    
    # Related entities
    top_authors = Column(JSON, nullable=True)
    top_posts = Column(JSON, nullable=True)
    
    # Status
    is_active = Column(String(10), default="active")  # active, declining, ended
    
    # Foreign keys
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=True)
    
    # Relationships
    analysis = relationship("Analysis", back_populates="trends")
    
    def __repr__(self):
        return f"<Trend(id={self.id}, name='{self.name}', volume={self.volume})>"
```

### user.py
```python
from sqlalchemy import Column, String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import enum


class UserRole(str, enum.Enum):
    """User roles for authorization."""
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


class User(BaseModel):
    """User model for system authentication."""
    
    __tablename__ = "users"
    
    # Authentication fields
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile fields
    full_name = Column(String(255), nullable=True)
    
    # Status fields
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    role = Column(
        SQLEnum(UserRole),
        default=UserRole.VIEWER,
        nullable=False
    )
    
    # Relationships
    analyses = relationship("Analysis", back_populates="user", lazy="dynamic")
    dashboards = relationship("Dashboard", back_populates="user", lazy="dynamic")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
```

## Schemas
### analysis.py
```python
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
```

### analysis_result.py
```python
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
```

### auth.py
```python
from typing import Optional
from pydantic import EmailStr
from app.schemas.base import BaseSchema
from app.schemas.user import UserResponse


class LoginRequest(BaseSchema):
    """Login request schema."""
    
    username: str  # Can be username or email
    password: str


class TokenResponse(BaseSchema):
    """Token response schema."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseSchema):
    """JWT token payload schema."""
    
    sub: str
    exp: int
    type: str


class RefreshTokenRequest(BaseSchema):
    """Refresh token request schema."""
    
    refresh_token: str


class AuthResponse(BaseSchema):
    """Full authentication response."""
    
    user: UserResponse
    tokens: TokenResponse


class PasswordResetRequest(BaseSchema):
    """Password reset request schema."""
    
    email: EmailStr


class PasswordResetConfirm(BaseSchema):
    """Password reset confirmation schema."""
    
    token: str
    new_password: str
```

### author.py
```python
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
```

### brain.py
```python
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
```

### dashboard.py
```python
from typing import Optional, Dict, Any, List
from pydantic import Field
from app.schemas.base import BaseSchema, TimestampSchema


class WidgetConfig(BaseSchema):
    """Dashboard widget configuration."""
    
    widget_id: str
    widget_type: str  # chart, table, metric, map, wordcloud
    title: str
    position: Dict[str, int]  # {"x": 0, "y": 0, "w": 2, "h": 2}
    config: Optional[Dict[str, Any]] = None
    data_source: Optional[str] = None  # API endpoint or query


class DashboardBase(BaseSchema):
    """Base dashboard schema."""
    
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class DashboardCreate(DashboardBase):
    """Schema for creating a dashboard."""
    
    layout: Optional[Dict[str, Any]] = None
    widgets: Optional[List[WidgetConfig]] = None
    filters: Optional[Dict[str, Any]] = None
    refresh_interval: int = 300
    is_default: bool = False
    is_public: bool = False


class DashboardUpdate(BaseSchema):
    """Schema for updating a dashboard."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    layout: Optional[Dict[str, Any]] = None
    widgets: Optional[List[WidgetConfig]] = None
    filters: Optional[Dict[str, Any]] = None
    refresh_interval: Optional[int] = None
    is_default: Optional[bool] = None
    is_public: Optional[bool] = None


class DashboardResponse(DashboardBase, TimestampSchema):
    """Dashboard response schema."""
    
    id: int
    layout: Optional[Dict[str, Any]] = None
    widgets: Optional[List[Dict[str, Any]]] = None
    filters: Optional[Dict[str, Any]] = None
    refresh_interval: int = 300
    is_default: bool
    is_public: bool
    user_id: int


class DashboardBrief(BaseSchema):
    """Brief dashboard info."""
    
    id: int
    name: str
    is_default: bool
    is_public: bool


class WidgetData(BaseSchema):
    """Data response for a widget."""
    
    widget_id: str
    data: Any
    updated_at: str
```

### data_source.py
```python
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import Field, HttpUrl
from app.schemas.base import BaseSchema, TimestampSchema
from app.models.data_source import SourcePlatform


class DataSourceBase(BaseSchema):
    """Base data source schema."""
    
    name: str = Field(..., min_length=1, max_length=255)
    platform: SourcePlatform = SourcePlatform.CUSTOM
    description: Optional[str] = None


class DataSourceCreate(DataSourceBase):
    """Schema for creating a data source."""
    
    api_endpoint: Optional[str] = None
    credentials: Optional[Dict[str, Any]] = None
    collection_config: Optional[Dict[str, Any]] = None


class DataSourceUpdate(BaseSchema):
    """Schema for updating a data source."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    platform: Optional[SourcePlatform] = None
    api_endpoint: Optional[str] = None
    credentials: Optional[Dict[str, Any]] = None
    collection_config: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class DataSourceResponse(DataSourceBase, TimestampSchema):
    """Data source response schema."""
    
    id: int
    api_endpoint: Optional[str] = None
    collection_config: Optional[Dict[str, Any]] = None
    is_active: bool
    last_sync_at: Optional[str] = None


class DataSourceBrief(BaseSchema):
    """Brief data source info."""
    
    id: int
    name: str
    platform: SourcePlatform
    is_active: bool


class DataSourceStats(BaseSchema):
    """Data source statistics."""
    
    id: int
    name: str
    platform: SourcePlatform
    total_posts: int = 0
    total_authors: int = 0
    last_sync_at: Optional[str] = None
```

### graph.py
```python
from typing import Optional, Dict, Any, List
from pydantic import Field
from app.schemas.base import BaseSchema, TimestampSchema


class GraphNodeBase(BaseSchema):
    """Base graph node schema."""
    
    node_id: str = Field(..., max_length=255)
    node_type: str = Field(..., max_length=50)
    label: Optional[str] = None


class GraphNodeCreate(GraphNodeBase):
    """Schema for creating a graph node."""
    
    attributes: Optional[Dict[str, Any]] = None
    degree: int = 0
    in_degree: int = 0
    out_degree: int = 0
    pagerank: Optional[float] = None
    betweenness_centrality: Optional[float] = None
    closeness_centrality: Optional[float] = None
    eigenvector_centrality: Optional[float] = None
    community_id: Optional[int] = None


class GraphNodeUpdate(BaseSchema):
    """Schema for updating a graph node."""
    
    label: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    degree: Optional[int] = None
    pagerank: Optional[float] = None
    community_id: Optional[int] = None


class GraphNodeResponse(GraphNodeBase, TimestampSchema):
    """Graph node response schema."""
    
    id: int
    attributes: Optional[Dict[str, Any]] = None
    degree: int = 0
    in_degree: int = 0
    out_degree: int = 0
    pagerank: Optional[float] = None
    betweenness_centrality: Optional[float] = None
    closeness_centrality: Optional[float] = None
    eigenvector_centrality: Optional[float] = None
    community_id: Optional[int] = None


class GraphEdgeBase(BaseSchema):
    """Base graph edge schema."""
    
    edge_type: str = Field(..., max_length=50)
    source_id: int
    target_id: int


class GraphEdgeCreate(GraphEdgeBase):
    """Schema for creating a graph edge."""
    
    weight: float = 1.0
    attributes: Optional[Dict[str, Any]] = None


class GraphEdgeResponse(GraphEdgeBase, TimestampSchema):
    """Graph edge response schema."""
    
    id: int
    weight: float = 1.0
    attributes: Optional[Dict[str, Any]] = None
    occurrence_count: int = 1


class GraphData(BaseSchema):
    """Full graph data for visualization."""
    
    nodes: List[GraphNodeResponse]
    edges: List[GraphEdgeResponse]
    metadata: Optional[Dict[str, Any]] = None


class GraphStats(BaseSchema):
    """Graph statistics."""
    
    total_nodes: int
    total_edges: int
    node_types: Dict[str, int]
    edge_types: Dict[str, int]
    communities_count: int
    avg_degree: float
    density: float


class CommunityInfo(BaseSchema):
    """Community detection result."""
    
    community_id: int
    size: int
    top_nodes: List[Dict[str, Any]]
    keywords: Optional[List[str]] = None


class PageRankResult(BaseSchema):
    """PageRank results."""
    
    node_id: str
    label: Optional[str] = None
    pagerank_score: float
    node_type: str


class GraphAnalysisRequest(BaseSchema):
    """Request for graph analysis to BRAIN."""
    
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    algorithms: List[str] = ["pagerank", "community_detection", "centrality"]
```

### post.py
```python
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
```

### trend.py
```python
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import Field
from app.schemas.base import BaseSchema, TimestampSchema


class TrendBase(BaseSchema):
    """Base trend schema."""
    
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class TrendCreate(TrendBase):
    """Schema for creating a trend."""
    
    volume: int = 0
    growth_rate: Optional[float] = None
    velocity: Optional[float] = None
    peak_time: Optional[datetime] = None
    keywords: Optional[List[str]] = None
    hashtags: Optional[List[str]] = None
    sentiment_distribution: Optional[Dict[str, float]] = None
    time_series: Optional[List[Dict[str, Any]]] = None
    geo_distribution: Optional[Dict[str, Any]] = None
    top_authors: Optional[List[Dict[str, Any]]] = None
    top_posts: Optional[List[int]] = None
    analysis_id: Optional[int] = None


class TrendUpdate(BaseSchema):
    """Schema for updating a trend."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    volume: Optional[int] = None
    growth_rate: Optional[float] = None
    is_active: Optional[str] = None


class TrendResponse(TrendBase, TimestampSchema):
    """Trend response schema."""
    
    id: int
    volume: int = 0
    growth_rate: Optional[float] = None
    velocity: Optional[float] = None
    peak_time: Optional[datetime] = None
    keywords: Optional[List[str]] = None
    hashtags: Optional[List[str]] = None
    sentiment_distribution: Optional[Dict[str, float]] = None
    is_active: str = "active"
    analysis_id: Optional[int] = None


class TrendWithDetails(TrendResponse):
    """Trend with full details."""
    
    time_series: Optional[List[Dict[str, Any]]] = None
    geo_distribution: Optional[Dict[str, Any]] = None
    top_authors: Optional[List[Dict[str, Any]]] = None
    top_posts: Optional[List[int]] = None


class TrendBrief(BaseSchema):
    """Brief trend info."""
    
    id: int
    name: str
    volume: int
    growth_rate: Optional[float] = None
    is_active: str


class TrendingItem(BaseSchema):
    """Single trending item (keyword, hashtag, etc.)."""
    
    item: str
    count: int
    growth: Optional[float] = None
    sentiment: Optional[str] = None
```

### user.py
```python
from datetime import datetime
from typing import Optional
from pydantic import EmailStr, Field, field_validator
from app.schemas.base import BaseSchema, TimestampSchema
from app.models.user import UserRole
import re


class UserBase(BaseSchema):
    """Base user schema."""
    
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError(
                "Username can only contain letters, numbers, underscores, and hyphens"
            )
        return v.lower()


class UserCreate(UserBase):
    """Schema for creating a new user."""
    
    password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseSchema):
    """Schema for updating a user."""
    
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None


class UserUpdatePassword(BaseSchema):
    """Schema for updating user password."""
    
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)


class UserInDB(UserBase, TimestampSchema):
    """User schema as stored in database."""
    
    id: int
    is_active: bool
    is_superuser: bool
    role: UserRole


class UserResponse(UserBase, TimestampSchema):
    """User response schema (public)."""
    
    id: int
    is_active: bool
    role: UserRole


class UserBrief(BaseSchema):
    """Brief user info for embedding."""
    
    id: int
    username: str
    full_name: Optional[str] = None
```

## API Endpoints
### analysis.py
```python
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user, get_current_analyst, PaginationParams
from app.crud import analysis as analysis_crud
from app.crud import analysis_result as result_crud
from app.models.user import User
from app.models.analysis import AnalysisType, AnalysisStatus
from app.services.analysis_service import analysis_service
from app.services.tasks import process_analysis
from app.schemas.analysis import (
    AnalysisCreate,
    AnalysisUpdate,
    AnalysisResponse,
    AnalysisWithUser,
    AnalysisConfig,
    AnalysisProgress
)
from app.schemas.analysis_result import (
    AnalysisResultResponse,
    AnalysisSummary
)
from app.schemas.base import MessageResponse

router = APIRouter()


@router.get("", response_model=List[AnalysisResponse])
async def get_analyses(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    status_filter: Optional[AnalysisStatus] = None,
    type_filter: Optional[AnalysisType] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get all analyses for current user.
    """
    if status_filter:
        analyses = await analysis_crud.get_by_status(
            db,
            status=status_filter,
            skip=pagination.skip,
            limit=pagination.limit
        )
    elif type_filter:
        analyses = await analysis_crud.get_by_type(
            db,
            analysis_type=type_filter,
            skip=pagination.skip,
            limit=pagination.limit
        )
    else:
        analyses = await analysis_crud.get_by_user(
            db,
            user_id=current_user.id,
            skip=pagination.skip,
            limit=pagination.limit
        )
    
    return [AnalysisResponse.model_validate(a) for a in analyses]


@router.get("/stats")
async def get_analysis_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get analysis statistics.
    """
    stats = await analysis_crud.get_stats(db, user_id=current_user.id)
    return stats


@router.get("/pending", response_model=List[AnalysisResponse])
async def get_pending_analyses(
    db: AsyncSession = Depends(get_db),
    limit: int = 10,
    current_user: User = Depends(get_current_analyst)
):
    """
    Get pending analyses (analyst only).
    """
    analyses = await analysis_crud.get_pending(db, limit=limit)
    return [AnalysisResponse.model_validate(a) for a in analyses]


@router.get("/{analysis_id}", response_model=AnalysisWithUser)
async def get_analysis(
    analysis_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get analysis by ID.
    """
    analysis = await analysis_crud.get_with_user(db, id=analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    return AnalysisWithUser.model_validate(analysis)


@router.get("/{analysis_id}/progress")
async def get_analysis_progress(
    analysis_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get analysis progress.
    """
    analysis = await analysis_crud.get(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    # Try to get from cache first
    cached = await analysis_service.get_progress(analysis_id)
    if cached:
        return cached
    
    return {
        "analysis_id": analysis_id,
        "status": analysis.status.value,
        "progress": analysis.progress
    }


@router.get("/{analysis_id}/results", response_model=List[AnalysisResultResponse])
async def get_analysis_results(
    analysis_id: int,
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_user)
):
    """
    Get results for an analysis.
    """
    analysis = await analysis_crud.get(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    results = await result_crud.get_by_analysis(
        db,
        analysis_id=analysis_id,
        skip=pagination.skip,
        limit=pagination.limit
    )
    
    return [AnalysisResultResponse.model_validate(r) for r in results]


@router.get("/{analysis_id}/summary")
async def get_analysis_summary(
    analysis_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get analysis summary.
    """
    analysis = await analysis_crud.get(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    if analysis.summary:
        return analysis.summary
    
    # Generate summary if not exists
    summary = await analysis_service.generate_summary(db, analysis_id=analysis_id)
    return summary


@router.post("", response_model=AnalysisResponse)
async def create_analysis(
    analysis_in: AnalysisCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Create new analysis.
    """
    analysis = await analysis_service.create_analysis(
        db,
        analysis_in=analysis_in,
        user_id=current_user.id
    )
    
    return AnalysisResponse.model_validate(analysis)


@router.post("/{analysis_id}/start", response_model=MessageResponse)
async def start_analysis(
    analysis_id: int,
    config: Optional[AnalysisConfig] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Start processing an analysis.
    """
    analysis = await analysis_crud.get(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    if analysis.status != AnalysisStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Analysis is already {analysis.status.value}"
        )
    
    # Queue task for processing
    config_dict = config.model_dump() if config else None
    process_analysis.delay(analysis_id, config_dict)
    
    # Update status to queued
    await analysis_crud.update_status(
        db,
        analysis_id=analysis_id,
        status=AnalysisStatus.QUEUED
    )
    
    return MessageResponse(message="Analysis queued for processing")


@router.post("/{analysis_id}/cancel", response_model=MessageResponse)
async def cancel_analysis(
    analysis_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Cancel an analysis.
    """
    success = await analysis_service.cancel_analysis(db, analysis_id=analysis_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel this analysis"
        )
    
    return MessageResponse(message="Analysis cancelled")


@router.put("/{analysis_id}", response_model=AnalysisResponse)
async def update_analysis(
    analysis_id: int,
    analysis_in: AnalysisUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Update analysis.
    """
    analysis = await analysis_crud.get(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    updated = await analysis_crud.update(db, db_obj=analysis, obj_in=analysis_in)
    return AnalysisResponse.model_validate(updated)


@router.delete("/{analysis_id}", response_model=MessageResponse)
async def delete_analysis(
    analysis_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Delete analysis and its results.
    """
    analysis = await analysis_crud.get(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    # Delete results first
    await result_crud.delete_by_analysis(db, analysis_id=analysis_id)
    
    # Delete analysis
    await analysis_crud.delete(db, id=analysis_id)
    
    return MessageResponse(message="Analysis deleted successfully")
```

### auth.py
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.services.auth_service import auth_service
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    AuthResponse
)
from app.schemas.user import UserCreate, UserResponse
from app.schemas.base import MessageResponse

router = APIRouter()


@router.post("/login", response_model=AuthResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with username/email and password.
    Returns access and refresh tokens.
    """
    user = await auth_service.authenticate(
        db,
        identifier=login_data.username,
        password=login_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    tokens = await auth_service.create_tokens(user)
    
    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=tokens
    )


@router.post("/register", response_model=AuthResponse)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account.
    """
    user, error = await auth_service.register(db, user_in=user_in)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    tokens = await auth_service.create_tokens(user)
    
    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=tokens
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    """
    tokens = await auth_service.refresh_tokens(
        db,
        refresh_token=refresh_data.refresh_token
    )
    
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return tokens


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user = Depends(get_current_user)
):
    """
    Get current authenticated user information.
    """
    return UserResponse.model_validate(current_user)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user = Depends(get_current_user)
):
    """
    Logout current user.
    Note: JWT tokens are stateless, so this is mainly for client-side handling.
    For full logout, implement token blacklisting with Redis.
    """
    return MessageResponse(
        message="Successfully logged out",
        success=True
    )


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    current_password: str,
    new_password: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Change current user's password.
    """
    success, error = await auth_service.change_password(
        db,
        user=current_user,
        current_password=current_password,
        new_password=new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return MessageResponse(
        message="Password changed successfully",
        success=True
    )
```

### authors.py
```python
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user, PaginationParams
from app.crud import author as author_crud
from app.models.user import User
from app.schemas.author import (
    AuthorCreate,
    AuthorUpdate,
    AuthorResponse,
    AuthorWithMetrics
)
from app.schemas.base import MessageResponse

router = APIRouter()


@router.get("", response_model=List[AuthorResponse])
async def get_authors(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    platform: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get all authors with optional filtering.
    """
    if search:
        authors = await author_crud.search(
            db,
            query_str=search,
            platform=platform,
            skip=pagination.skip,
            limit=pagination.limit
        )
    else:
        authors = await author_crud.get_multi(
            db,
            skip=pagination.skip,
            limit=pagination.limit
        )
    
    return [AuthorResponse.model_validate(a) for a in authors]


@router.get("/top/followers", response_model=List[AuthorResponse])
async def get_top_authors_by_followers(
    db: AsyncSession = Depends(get_db),
    platform: Optional[str] = None,
    limit: int = Query(default=10, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get top authors by follower count.
    """
    authors = await author_crud.get_top_by_followers(
        db,
        platform=platform,
        limit=limit
    )
    return [AuthorResponse.model_validate(a) for a in authors]


@router.get("/top/pagerank", response_model=List[AuthorResponse])
async def get_top_authors_by_pagerank(
    db: AsyncSession = Depends(get_db),
    platform: Optional[str] = None,
    limit: int = Query(default=10, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get top authors by PageRank score.
    """
    authors = await author_crud.get_top_by_pagerank(
        db,
        platform=platform,
        limit=limit
    )
    return [AuthorResponse.model_validate(a) for a in authors]


@router.get("/top/influence", response_model=List[AuthorResponse])
async def get_top_authors_by_influence(
    db: AsyncSession = Depends(get_db),
    platform: Optional[str] = None,
    limit: int = Query(default=10, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get top authors by influence score.
    """
    authors = await author_crud.get_top_by_influence(
        db,
        platform=platform,
        limit=limit
    )
    return [AuthorResponse.model_validate(a) for a in authors]


@router.get("/stats")
async def get_author_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get author statistics by platform.
    """
    stats = await author_crud.count_by_platform(db)
    total = sum(stats.values())
    
    return {
        "total": total,
        "by_platform": stats
    }


@router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(
    author_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get author by ID.
    """
    author = await author_crud.get(db, author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    
    return AuthorResponse.model_validate(author)


@router.post("", response_model=AuthorResponse)
async def create_author(
    author_in: AuthorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create new author.
    """
    # Check if exists
    existing = await author_crud.get_by_platform_id(
        db,
        platform_id=author_in.platform_id,
        platform=author_in.platform
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author already exists for this platform"
        )
    
    author = await author_crud.create(db, obj_in=author_in)
    return AuthorResponse.model_validate(author)


@router.put("/{author_id}", response_model=AuthorResponse)
async def update_author(
    author_id: int,
    author_in: AuthorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update author.
    """
    author = await author_crud.get(db, author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    
    updated = await author_crud.update(db, db_obj=author, obj_in=author_in)
    return AuthorResponse.model_validate(updated)


@router.delete("/{author_id}", response_model=MessageResponse)
async def delete_author(
    author_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete author.
    """
    author = await author_crud.delete(db, id=author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    
    return MessageResponse(message="Author deleted successfully")
```

### brain.py
```python
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user, get_current_analyst
from app.models.user import User
from app.services.brain_service import brain_service, BrainServiceError
from app.schemas.brain import (
    BrainHealthResponse,
    TextAnalysisRequest,
    TextAnalysisResponse,
    SummarizationRequest
)

router = APIRouter()


@router.get("/health", response_model=BrainHealthResponse)
async def check_brain_health(
    current_user: User = Depends(get_current_user)
):
    """
    Check BRAIN service health status.
    """
    health = await brain_service.health_check()
    return health


@router.get("/available")
async def check_brain_available(
    current_user: User = Depends(get_current_user)
):
    """
    Check if BRAIN service is available.
    """
    available = await brain_service.is_available()
    return {"available": available}


@router.post("/analyze/sentiment")
async def analyze_sentiment(
    texts: List[str],
    current_user: User = Depends(get_current_analyst)
):
    """
    Analyze sentiment of texts.
    """
    try:
        results = await brain_service.analyze_sentiment(texts)
        return {"results": results}
    except BrainServiceError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=e.message
        )


@router.post("/analyze/emotions")
async def analyze_emotions(
    texts: List[str],
    current_user: User = Depends(get_current_analyst)
):
    """
    Analyze emotions in texts.
    """
    try:
        results = await brain_service.analyze_emotions(texts)
        return {"results": results}
    except BrainServiceError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=e.message
        )


@router.post("/analyze/text", response_model=List[TextAnalysisResponse])
async def analyze_text(
    request: TextAnalysisRequest,
    current_user: User = Depends(get_current_analyst)
):
    """
    Full text analysis including sentiment, emotion, keywords.
    """
    try:
        results = await brain_service.analyze_text(
            texts=request.texts,
            text_ids=request.text_ids,
            analysis_types=request.analysis_types,
            config=request.config
        )
        return results
    except BrainServiceError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=e.message
        )


@router.post("/summarize")
async def summarize_texts(
    request: SummarizationRequest,
    current_user: User = Depends(get_current_analyst)
):
    """
    Summarize texts.
    """
    try:
        summaries = await brain_service.summarize_texts(
            texts=request.texts,
            max_length=request.max_length,
            min_length=request.min_length
        )
        return {"summaries": summaries}
    except BrainServiceError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=e.message
        )


@router.post("/extract/keywords")
async def extract_keywords(
    texts: List[str],
    max_keywords: int = 10,
    current_user: User = Depends(get_current_analyst)
):
    """
    Extract keywords from texts.
    """
    try:
        keywords = await brain_service.extract_keywords(
            texts=texts,
            max_keywords=max_keywords
        )
        return {"keywords": keywords}
    except BrainServiceError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=e.message
        )


@router.post("/extract/entities")
async def extract_entities(
    texts: List[str],
    current_user: User = Depends(get_current_analyst)
):
    """
    Extract named entities from texts.
    """
    try:
        entities = await brain_service.extract_entities(texts)
        return {"entities": entities}
    except BrainServiceError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=e.message
        )


@router.post("/detect/topics")
async def detect_topics(
    texts: List[str],
    num_topics: int = 10,
    current_user: User = Depends(get_current_analyst)
):
    """
    Detect topics in texts.
    """
    try:
        result = await brain_service.detect_topics(
            texts=texts,
            num_topics=num_topics
        )
        return result
    except BrainServiceError as e:
        raise HTTPException(
            status_code=e.status_code or 500,
            detail=e.message
        )
```

### dashboard.py
```python
from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user, PaginationParams
from app.crud import dashboard as dashboard_crud
from app.models.user import User
from app.services.dashboard_service import dashboard_service
from app.schemas.dashboard import (
    DashboardCreate,
    DashboardUpdate,
    DashboardResponse,
    WidgetData
)
from app.schemas.base import MessageResponse

router = APIRouter()


@router.get("/overview")
async def get_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get dashboard overview statistics.
    """
    return await dashboard_service.get_overview_stats(db)


@router.get("/sentiment")
async def get_sentiment_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get sentiment analysis overview.
    """
    return await dashboard_service.get_sentiment_overview(db)


@router.get("/emotions")
async def get_emotion_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get emotion analysis overview.
    """
    return await dashboard_service.get_emotion_overview(db)


@router.get("/platforms")
async def get_platform_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get statistics by platform.
    """
    return await dashboard_service.get_platform_stats(db)


@router.get("/widget/{widget_type}")
async def get_widget_data(
    widget_type: str,
    db: AsyncSession = Depends(get_db),
    hours: int = 24,
    limit: int = 10,
    interval: str = "1h",
    current_user: User = Depends(get_current_user)
):
    """
    Get data for a specific widget type.
    """
    config = {
        "hours": hours,
        "limit": limit,
        "interval": interval
    }
    
    data = await dashboard_service.get_widget_data(
        db,
        widget_type=widget_type,
        config=config
    )
    
    return data


@router.get("", response_model=List[DashboardResponse])
async def get_dashboards(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's dashboards.
    """
    dashboards = await dashboard_crud.get_by_user(
        db,
        user_id=current_user.id,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return [DashboardResponse.model_validate(d) for d in dashboards]


@router.get("/public", response_model=List[DashboardResponse])
async def get_public_dashboards(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_user)
):
    """
    Get public dashboards.
    """
    dashboards = await dashboard_crud.get_public(
        db,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return [DashboardResponse.model_validate(d) for d in dashboards]


@router.get("/default", response_model=DashboardResponse)
async def get_default_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's default dashboard.
    """
    dashboard = await dashboard_crud.get_default(db, user_id=current_user.id)
    
    if not dashboard:
        # Create default dashboard if none exists
        dashboard = await dashboard_service.create_default_dashboard(
            db,
            user_id=current_user.id
        )
    
    return DashboardResponse.model_validate(dashboard)


@router.get("/{dashboard_id}", response_model=DashboardResponse)
async def get_dashboard(
    dashboard_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get dashboard by ID.
    """
    dashboard = await dashboard_crud.get(db, dashboard_id)
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    
    # Check access
    if dashboard.user_id != current_user.id and not dashboard.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return DashboardResponse.model_validate(dashboard)


@router.post("", response_model=DashboardResponse)
async def create_dashboard(
    dashboard_in: DashboardCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create new dashboard.
    """
    dashboard = await dashboard_crud.create_with_user(
        db,
        obj_in=dashboard_in,
        user_id=current_user.id
    )
    return DashboardResponse.model_validate(dashboard)


@router.put("/{dashboard_id}", response_model=DashboardResponse)
async def update_dashboard(
    dashboard_id: int,
    dashboard_in: DashboardUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update dashboard.
    """
    dashboard = await dashboard_crud.get(db, dashboard_id)
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    
    if dashboard.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not your dashboard"
        )
    
    updated = await dashboard_crud.update(db, db_obj=dashboard, obj_in=dashboard_in)
    return DashboardResponse.model_validate(updated)


@router.post("/{dashboard_id}/set-default", response_model=DashboardResponse)
async def set_default_dashboard(
    dashboard_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Set dashboard as default.
    """
    dashboard = await dashboard_crud.set_default(
        db,
        dashboard_id=dashboard_id,
        user_id=current_user.id
    )
    
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found or not yours"
        )
    
    return DashboardResponse.model_validate(dashboard)


@router.post("/{dashboard_id}/duplicate", response_model=DashboardResponse)
async def duplicate_dashboard(
    dashboard_id: int,
    new_name: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Duplicate a dashboard.
    """
    dashboard = await dashboard_crud.duplicate(
        db,
        dashboard_id=dashboard_id,
        user_id=current_user.id,
        new_name=new_name
    )
    
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    
    return DashboardResponse.model_validate(dashboard)


@router.delete("/{dashboard_id}", response_model=MessageResponse)
async def delete_dashboard(
    dashboard_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete dashboard.
    """
    dashboard = await dashboard_crud.get(db, dashboard_id)
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )
    
    if dashboard.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not your dashboard"
        )
    
    await dashboard_crud.delete(db, id=dashboard_id)
    return MessageResponse(message="Dashboard deleted successfully")
```

### data_sources.py
```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_db,
    get_current_user,
    get_current_analyst,
    PaginationParams
)
from app.crud import data_source as data_source_crud
from app.models.user import User
from app.models.data_source import SourcePlatform
from app.schemas.data_source import (
    DataSourceCreate,
    DataSourceUpdate,
    DataSourceResponse,
    DataSourceStats
)
from app.schemas.base import MessageResponse

router = APIRouter()


@router.get("", response_model=List[DataSourceResponse])
async def get_data_sources(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    platform: SourcePlatform = None,
    active_only: bool = False,
    current_user: User = Depends(get_current_user)
):
    """
    Get all data sources.
    """
    if active_only:
        sources = await data_source_crud.get_active(
            db,
            skip=pagination.skip,
            limit=pagination.limit
        )
    elif platform:
        sources = await data_source_crud.get_by_platform(
            db,
            platform=platform,
            skip=pagination.skip,
            limit=pagination.limit
        )
    else:
        sources = await data_source_crud.get_multi(
            db,
            skip=pagination.skip,
            limit=pagination.limit
        )
    
    return [DataSourceResponse.model_validate(s) for s in sources]


@router.get("/{source_id}", response_model=DataSourceResponse)
async def get_data_source(
    source_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get data source by ID.
    """
    source = await data_source_crud.get(db, source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data source not found"
        )
    
    return DataSourceResponse.model_validate(source)


@router.get("/{source_id}/stats", response_model=DataSourceStats)
async def get_data_source_stats(
    source_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get statistics for a data source.
    """
    source = await data_source_crud.get(db, source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data source not found"
        )
    
    stats = await data_source_crud.get_stats(db, data_source_id=source_id)
    
    return DataSourceStats(
        id=source.id,
        name=source.name,
        platform=source.platform,
        total_posts=stats["total_posts"],
        total_authors=stats["total_authors"],
        last_sync_at=source.last_sync_at
    )


@router.post("", response_model=DataSourceResponse)
async def create_data_source(
    source_in: DataSourceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Create new data source (analyst or admin).
    """
    # Check if name exists
    existing = await data_source_crud.get_by_name(db, name=source_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data source with this name already exists"
        )
    
    source = await data_source_crud.create(db, obj_in=source_in)
    return DataSourceResponse.model_validate(source)


@router.put("/{source_id}", response_model=DataSourceResponse)
async def update_data_source(
    source_id: int,
    source_in: DataSourceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Update data source (analyst or admin).
    """
    source = await data_source_crud.get(db, source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data source not found"
        )
    
    updated = await data_source_crud.update(db, db_obj=source, obj_in=source_in)
    return DataSourceResponse.model_validate(updated)


@router.delete("/{source_id}", response_model=MessageResponse)
async def delete_data_source(
    source_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Delete data source (analyst or admin).
    """
    source = await data_source_crud.delete(db, id=source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data source not found"
        )
    
    return MessageResponse(message="Data source deleted successfully")


@router.post("/{source_id}/activate", response_model=DataSourceResponse)
async def activate_data_source(
    source_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Activate data source.
    """
    source = await data_source_crud.get(db, source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data source not found"
        )
    
    source = await data_source_crud.activate(db, db_obj=source)
    return DataSourceResponse.model_validate(source)


@router.post("/{source_id}/deactivate", response_model=DataSourceResponse)
async def deactivate_data_source(
    source_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Deactivate data source.
    """
    source = await data_source_crud.get(db, source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data source not found"
        )
    
    source = await data_source_crud.deactivate(db, db_obj=source)
    return DataSourceResponse.model_validate(source)
```

### graph.py
```python
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user, get_current_analyst, PaginationParams
from app.crud import graph_node as node_crud
from app.crud import graph_edge as edge_crud
from app.models.user import User
from app.services.graph_service import graph_service
from app.services.tasks import build_graph, calculate_pagerank
from app.schemas.graph import (
    GraphNodeCreate,
    GraphNodeResponse,
    GraphEdgeCreate,
    GraphEdgeResponse,
    GraphData,
    GraphStats,
    PageRankResult
)
from app.schemas.base import MessageResponse

router = APIRouter()


@router.get("/data", response_model=GraphData)
async def get_graph_data(
    db: AsyncSession = Depends(get_db),
    node_type: Optional[str] = None,
    limit: int = Query(default=500, ge=1, le=5000),
    current_user: User = Depends(get_current_user)
):
    """
    Get graph data for visualization.
    """
    data = await graph_service.get_graph_data(
        db,
        node_type=node_type,
        limit=limit
    )
    return data


@router.get("/stats", response_model=GraphStats)
async def get_graph_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get graph statistics.
    """
    stats = await graph_service.get_stats(db)
    return stats


@router.get("/nodes", response_model=List[GraphNodeResponse])
async def get_nodes(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    node_type: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get graph nodes.
    """
    if node_type:
        nodes = await node_crud.get_by_type(
            db,
            node_type=node_type,
            skip=pagination.skip,
            limit=pagination.limit
        )
    else:
        nodes = await node_crud.get_multi(
            db,
            skip=pagination.skip,
            limit=pagination.limit
        )
    
    return [GraphNodeResponse.model_validate(n) for n in nodes]


@router.get("/nodes/top/pagerank", response_model=List[GraphNodeResponse])
async def get_top_nodes_by_pagerank(
    db: AsyncSession = Depends(get_db),
    node_type: Optional[str] = None,
    limit: int = Query(default=10, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get top nodes by PageRank score.
    """
    nodes = await node_crud.get_top_by_pagerank(
        db,
        node_type=node_type,
        limit=limit
    )
    return [GraphNodeResponse.model_validate(n) for n in nodes]


@router.get("/nodes/top/degree", response_model=List[GraphNodeResponse])
async def get_top_nodes_by_degree(
    db: AsyncSession = Depends(get_db),
    node_type: Optional[str] = None,
    limit: int = Query(default=10, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get top nodes by degree.
    """
    nodes = await node_crud.get_top_by_degree(
        db,
        node_type=node_type,
        limit=limit
    )
    return [GraphNodeResponse.model_validate(n) for n in nodes]


@router.get("/nodes/top/betweenness", response_model=List[GraphNodeResponse])
async def get_top_nodes_by_betweenness(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(default=10, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get top nodes by betweenness centrality.
    """
    nodes = await node_crud.get_top_by_betweenness(db, limit=limit)
    return [GraphNodeResponse.model_validate(n) for n in nodes]


@router.get("/nodes/community/{community_id}", response_model=List[GraphNodeResponse])
async def get_nodes_by_community(
    community_id: int,
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_user)
):
    """
    Get nodes in a community.
    """
    nodes = await node_crud.get_by_community(
        db,
        community_id=community_id,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return [GraphNodeResponse.model_validate(n) for n in nodes]


@router.get("/nodes/{node_id}", response_model=GraphNodeResponse)
async def get_node(
    node_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get node by ID.
    """
    node = await node_crud.get(db, node_id)
    if not node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found"
        )
    
    return GraphNodeResponse.model_validate(node)


@router.get("/edges", response_model=List[GraphEdgeResponse])
async def get_edges(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    edge_type: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get graph edges.
    """
    if edge_type:
        edges = await edge_crud.get_by_type(
            db,
            edge_type=edge_type,
            skip=pagination.skip,
            limit=pagination.limit
        )
    else:
        edges = await edge_crud.get_multi(
            db,
            skip=pagination.skip,
            limit=pagination.limit
        )
    
    return [GraphEdgeResponse.model_validate(e) for e in edges]


@router.post("/build/hashtag-network", response_model=MessageResponse)
async def build_hashtag_network(
    platform: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Build hashtag co-occurrence network (analyst only).
    """
    result = await graph_service.build_hashtag_network(
        db,
        platform=platform
    )
    return MessageResponse(
        message=f"Hashtag network built: {result.get('nodes_created', 0)} nodes, {result.get('edges_created', 0)} edges"
    )


@router.post("/calculate/pagerank", response_model=MessageResponse)
async def trigger_pagerank_calculation(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Calculate PageRank for all nodes (analyst only).
    """
    calculate_pagerank.delay()
    return MessageResponse(message="PageRank calculation queued")


@router.post("/detect/communities", response_model=MessageResponse)
async def trigger_community_detection(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Detect communities in the graph (analyst only).
    """
    result = await graph_service.detect_communities(db)
    return MessageResponse(
        message=f"Community detection completed: {result.get('communities', 0)} communities found"
    )


@router.delete("/clear", response_model=MessageResponse)
async def clear_graph(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Clear all graph data (analyst only).
    """
    await edge_crud.delete_all(db)
    await node_crud.delete_all(db)
    return MessageResponse(message="Graph data cleared")
```

### posts.py
```python
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user, get_current_analyst, PaginationParams
from app.crud import post as post_crud
from app.models.user import User
from app.schemas.post import (
    PostCreate,
    PostUpdate,
    PostResponse,
    PostWithRelations,
    PostBulkCreate,
    PostFilter
)
from app.schemas.base import MessageResponse

router = APIRouter()


@router.get("", response_model=List[PostResponse])
async def get_posts(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    platform: Optional[str] = None,
    language: Optional[str] = None,
    data_source_id: Optional[int] = None,
    author_id: Optional[int] = None,
    is_processed: Optional[bool] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get posts with filtering options.
    """
    filters = PostFilter(
        platform=platform,
        language=language,
        data_source_id=data_source_id,
        author_id=author_id,
        is_processed=is_processed,
        date_from=date_from,
        date_to=date_to,
        search=search
    )
    
    posts = await post_crud.get_filtered(
        db,
        filters=filters,
        skip=pagination.skip,
        limit=pagination.limit
    )
    
    return [PostResponse.model_validate(p) for p in posts]


@router.get("/stats")
async def get_post_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get post statistics.
    """
    stats = await post_crud.get_stats(db)
    return stats


@router.get("/unprocessed", response_model=List[PostResponse])
async def get_unprocessed_posts(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_user)
):
    """
    Get unprocessed posts.
    """
    posts = await post_crud.get_unprocessed(
        db,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return [PostResponse.model_validate(p) for p in posts]


@router.get("/search", response_model=List[PostResponse])
async def search_posts(
    q: str = Query(..., min_length=2),
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    platform: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Search posts by content.
    """
    posts = await post_crud.search(
        db,
        query_str=q,
        platform=platform,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return [PostResponse.model_validate(p) for p in posts]


@router.get("/by-hashtag/{hashtag}", response_model=List[PostResponse])
async def get_posts_by_hashtag(
    hashtag: str,
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_user)
):
    """
    Get posts containing a specific hashtag.
    """
    posts = await post_crud.get_by_hashtag(
        db,
        hashtag=hashtag,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return [PostResponse.model_validate(p) for p in posts]


@router.get("/{post_id}", response_model=PostWithRelations)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get post by ID with relations.
    """
    post = await post_crud.get_with_relations(db, id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    return PostWithRelations.model_validate(post)


@router.post("", response_model=PostResponse)
async def create_post(
    post_in: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Create new post.
    """
    # Check if exists
    existing = await post_crud.get_by_platform_id(
        db,
        platform_id=post_in.platform_id
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post already exists"
        )
    
    post = await post_crud.create(db, obj_in=post_in)
    return PostResponse.model_validate(post)


@router.post("/bulk", response_model=dict)
async def bulk_create_posts(
    bulk_in: PostBulkCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Bulk create posts.
    """
    posts, created, existing = await post_crud.bulk_create(
        db,
        posts_in=bulk_in.posts
    )
    
    return {
        "total": len(posts),
        "created": created,
        "existing": existing
    }


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_in: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Update post.
    """
    post = await post_crud.get(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    updated = await post_crud.update(db, db_obj=post, obj_in=post_in)
    return PostResponse.model_validate(updated)


@router.delete("/{post_id}", response_model=MessageResponse)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Delete post.
    """
    post = await post_crud.delete(db, id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    return MessageResponse(message="Post deleted successfully")
```

### trends.py
```python
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user, get_current_analyst, PaginationParams
from app.crud import trend as trend_crud
from app.models.user import User
from app.services.trend_service import trend_service
from app.services.tasks import detect_trends
from app.schemas.trend import (
    TrendCreate,
    TrendUpdate,
    TrendResponse,
    TrendWithDetails,
    TrendingItem
)
from app.schemas.base import MessageResponse

router = APIRouter()


@router.get("", response_model=List[TrendResponse])
async def get_trends(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    active_only: bool = True,
    current_user: User = Depends(get_current_user)
):
    """
    Get trends.
    """
    if active_only:
        trends = await trend_crud.get_active(
            db,
            skip=pagination.skip,
            limit=pagination.limit
        )
    else:
        trends = await trend_crud.get_multi(
            db,
            skip=pagination.skip,
            limit=pagination.limit
        )
    
    return [TrendResponse.model_validate(t) for t in trends]


@router.get("/summary")
async def get_trend_summary(
    db: AsyncSession = Depends(get_db),
    hours: int = Query(default=24, ge=1, le=168),
    current_user: User = Depends(get_current_user)
):
    """
    Get trend summary including hashtags, keywords, and active trends.
    """
    summary = await trend_service.get_trend_summary(db, hours=hours)
    return summary


@router.get("/hashtags", response_model=List[TrendingItem])
async def get_trending_hashtags(
    db: AsyncSession = Depends(get_db),
    hours: int = Query(default=24, ge=1, le=168),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get trending hashtags.
    """
    hashtags = await trend_service.get_trending_hashtags(
        db,
        hours=hours,
        limit=limit
    )
    return [TrendingItem(item=h["hashtag"], count=h["count"]) for h in hashtags]


@router.get("/keywords", response_model=List[TrendingItem])
async def get_trending_keywords(
    db: AsyncSession = Depends(get_db),
    hours: int = Query(default=24, ge=1, le=168),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get trending keywords from analysis results.
    """
    keywords = await trend_service.get_trending_keywords(
        db,
        hours=hours,
        limit=limit
    )
    return [TrendingItem(item=k["keyword"], count=k["count"]) for k in keywords]


@router.get("/sentiment")
async def get_sentiment_trends(
    db: AsyncSession = Depends(get_db),
    hours: int = Query(default=24, ge=1, le=168),
    interval: str = Query(default="1h", regex="^(1h|6h|1d)$"),
    current_user: User = Depends(get_current_user)
):
    """
    Get sentiment trends over time.
    """
    trends = await trend_service.get_sentiment_trends(
        db,
        hours=hours,
        interval=interval
    )
    return trends


@router.get("/volume")
async def get_volume_trends(
    db: AsyncSession = Depends(get_db),
    hours: int = Query(default=24, ge=1, le=168),
    interval: str = Query(default="1h", regex="^(1h|6h|1d)$"),
    platform: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get post volume trends over time.
    """
    trends = await trend_service.get_volume_trends(
        db,
        hours=hours,
        interval=interval,
        platform=platform
    )
    return trends


@router.get("/top/volume", response_model=List[TrendResponse])
async def get_top_trends_by_volume(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(default=10, ge=1, le=50),
    current_user: User = Depends(get_current_user)
):
    """
    Get top trends by volume.
    """
    trends = await trend_crud.get_top_by_volume(db, limit=limit)
    return [TrendResponse.model_validate(t) for t in trends]


@router.get("/top/growth", response_model=List[TrendResponse])
async def get_top_trends_by_growth(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(default=10, ge=1, le=50),
    current_user: User = Depends(get_current_user)
):
    """
    Get top trends by growth rate.
    """
    trends = await trend_crud.get_top_by_growth(db, limit=limit)
    return [TrendResponse.model_validate(t) for t in trends]


@router.get("/stats")
async def get_trend_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get trend statistics.
    """
    stats = await trend_crud.get_stats(db)
    return stats


@router.get("/{trend_id}", response_model=TrendWithDetails)
async def get_trend(
    trend_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get trend by ID with details.
    """
    trend = await trend_crud.get(db, trend_id)
    if not trend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trend not found"
        )
    
    return TrendWithDetails.model_validate(trend)


@router.post("/detect", response_model=MessageResponse)
async def trigger_trend_detection(
    hours: int = Query(default=24, ge=1, le=168),
    min_count: int = Query(default=10, ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Trigger trend detection (analyst only).
    """
    detect_trends.delay(hours=hours, min_count=min_count)
    return MessageResponse(message="Trend detection queued")


@router.post("", response_model=TrendResponse)
async def create_trend(
    trend_in: TrendCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Create new trend manually (analyst only).
    """
    trend = await trend_crud.create(db, obj_in=trend_in)
    return TrendResponse.model_validate(trend)


@router.put("/{trend_id}", response_model=TrendResponse)
async def update_trend(
    trend_id: int,
    trend_in: TrendUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Update trend.
    """
    trend = await trend_crud.get(db, trend_id)
    if not trend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trend not found"
        )
    
    updated = await trend_crud.update(db, db_obj=trend, obj_in=trend_in)
    return TrendResponse.model_validate(updated)


@router.delete("/{trend_id}", response_model=MessageResponse)
async def delete_trend(
    trend_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Delete trend.
    """
    trend = await trend_crud.delete(db, id=trend_id)
    if not trend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trend not found"
        )
    
    return MessageResponse(message="Trend deleted successfully")
```

### users.py
```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_db,
    get_current_user,
    get_current_admin,
    PaginationParams
)
from app.crud import user as user_crud
from app.models.user import User, UserRole
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserInDB
)
from app.schemas.base import MessageResponse, PaginatedResponse

router = APIRouter()


@router.get("", response_model=List[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_admin)
):
    """
    Get all users (admin only).
    """
    users = await user_crud.get_multi(
        db,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return [UserResponse.model_validate(u) for u in users]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user by ID.
    """
    # Users can only view their own profile unless admin
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = await user_crud.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.model_validate(user)


@router.post("", response_model=UserResponse)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Create new user (admin only).
    """
    # Check if email exists
    existing = await user_crud.get_by_email(db, email=user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username exists
    existing = await user_crud.get_by_username(db, username=user_in.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    user = await user_crud.create(db, obj_in=user_in)
    return UserResponse.model_validate(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update user.
    """
    # Users can only update their own profile unless admin
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = await user_crud.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Only admin can change roles
    if user_in.role is not None and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can change user roles"
        )
    
    updated_user = await user_crud.update(db, db_obj=user, obj_in=user_in)
    return UserResponse.model_validate(updated_user)


@router.delete("/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Delete user (admin only).
    """
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself"
        )
    
    user = await user_crud.delete(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return MessageResponse(message="User deleted successfully")


@router.post("/{user_id}/activate", response_model=UserResponse)
async def activate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Activate user account (admin only).
    """
    user = await user_crud.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user = await user_crud.activate(db, user=user)
    return UserResponse.model_validate(user)


@router.post("/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Deactivate user account (admin only).
    """
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate yourself"
        )
    
    user = await user_crud.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user = await user_crud.deactivate(db, user=user)
    return UserResponse.model_validate(user)
```

## Services
### analysis_service.py
```python
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base import BaseService
from app.services.brain_service import brain_service, BrainServiceError
from app.services.redis_service import redis_service
from app.crud import analysis as analysis_crud
from app.crud import analysis_result as result_crud
from app.crud import post as post_crud
from app.crud import trend as trend_crud
from app.models.analysis import AnalysisStatus, AnalysisType
from app.schemas.analysis import AnalysisCreate, AnalysisConfig
from app.schemas.analysis_result import AnalysisResultCreate
from app.schemas.trend import TrendCreate


class AnalysisService(BaseService):
    """Service for managing analysis jobs."""
    
    def __init__(self):
        super().__init__("AnalysisService")
    
    async def create_analysis(
        self,
        db: AsyncSession,
        *,
        analysis_in: AnalysisCreate,
        user_id: int
    ):
        """Create a new analysis job."""
        analysis = await analysis_crud.create_with_user(
            db,
            obj_in=analysis_in,
            user_id=user_id
        )
        self.log_info(f"Created analysis {analysis.id} for user {user_id}")
        return analysis
    
    async def start_analysis(
        self,
        db: AsyncSession,
        *,
        analysis_id: int
    ) -> bool:
        """Start an analysis job."""
        analysis = await analysis_crud.get(db, analysis_id)
        if not analysis:
            self.log_error(f"Analysis {analysis_id} not found")
            return False
        
        if analysis.status != AnalysisStatus.PENDING:
            self.log_warning(f"Analysis {analysis_id} is not pending")
            return False
        
        # Update status to processing
        await analysis_crud.update_status(
            db,
            analysis_id=analysis_id,
            status=AnalysisStatus.PROCESSING,
            progress=0.0
        )
        
        # Update Redis progress
        await redis_service.set_analysis_progress(
            analysis_id,
            progress=0.0,
            status="processing"
        )
        
        self.log_info(f"Started analysis {analysis_id}")
        return True
    
    async def process_analysis(
        self,
        db: AsyncSession,
        *,
        analysis_id: int,
        config: Optional[AnalysisConfig] = None
    ) -> bool:
        """Process an analysis job."""
        analysis = await analysis_crud.get(db, analysis_id)
        if not analysis:
            return False
        
        # Get posts based on filters
        filters = analysis.query_filters or {}
        posts = await self._get_posts_for_analysis(db, filters, analysis.post_count)
        
        if not posts:
            await analysis_crud.update_status(
                db,
                analysis_id=analysis_id,
                status=AnalysisStatus.FAILED,
                error_message="No posts found matching filters"
            )
            return False
        
        # Prepare posts data
        posts_data = [
            {
                "id": p.id,
                "content": p.content,
                "platform": p.platform,
                "posted_at": p.posted_at.isoformat() if p.posted_at else None
            }
            for p in posts
        ]
        
        # Get config
        if config is None:
            config = AnalysisConfig()
        
        try:
            # Check BRAIN availability
            if not await brain_service.is_available():
                raise BrainServiceError("BRAIN service unavailable")
            
            # Submit batch analysis
            batch_response = await brain_service.submit_batch_analysis(
                analysis_id=analysis_id,
                posts=posts_data,
                config=config.model_dump()
            )
            
            self.log_info(
                f"Submitted analysis {analysis_id} to BRAIN, "
                f"task_id: {batch_response.task_id}"
            )
            
            return True
            
        except BrainServiceError as e:
            self.log_error(f"BRAIN service error: {e.message}")
            await analysis_crud.update_status(
                db,
                analysis_id=analysis_id,
                status=AnalysisStatus.FAILED,
                error_message=f"BRAIN service error: {e.message}"
            )
            return False
    
    async def _get_posts_for_analysis(
        self,
        db: AsyncSession,
        filters: Dict[str, Any],
        limit: Optional[int] = None
    ) -> List:
        """Get posts for analysis based on filters."""
        from app.schemas.post import PostFilter
        
        post_filter = PostFilter(**filters) if filters else PostFilter()
        
        posts = await post_crud.get_filtered(
            db,
            filters=post_filter,
            skip=0,
            limit=limit or 1000
        )
        
        return posts
    
    async def process_analysis_results(
        self,
        db: AsyncSession,
        *,
        analysis_id: int,
        results: List[Dict[str, Any]]
    ) -> int:
        """Process and store analysis results from BRAIN."""
        stored_count = 0
        
        for result_data in results:
            try:
                result_in = AnalysisResultCreate(
                    post_id=result_data.get("post_id") or result_data.get("text_id"),
                    analysis_id=analysis_id,
                    sentiment_label=result_data.get("sentiment", {}).get("label"),
                    sentiment_score=result_data.get("sentiment", {}).get("score"),
                    sentiment_confidence=result_data.get("sentiment", {}).get("confidence"),
                    emotions=result_data.get("emotions"),
                    dominant_emotion=result_data.get("dominant_emotion"),
                    summary=result_data.get("summary"),
                    keywords=result_data.get("keywords"),
                    topics=result_data.get("topics"),
                    entities=result_data.get("entities"),
                    raw_results=result_data
                )
                
                await result_crud.create(db, obj_in=result_in)
                stored_count += 1
                
                # Mark post as processed
                await post_crud.mark_processed(
                    db,
                    post_id=result_in.post_id
                )
                
            except Exception as e:
                self.log_error(f"Error storing result: {e}")
                continue
        
        # Update progress
        progress = (stored_count / len(results)) * 100 if results else 100
        await redis_service.set_analysis_progress(
            analysis_id,
            progress=progress,
            status="storing_results"
        )
        
        return stored_count
    
    async def complete_analysis(
        self,
        db: AsyncSession,
        *,
        analysis_id: int,
        summary: Optional[Dict[str, Any]] = None
    ):
        """Complete an analysis job."""
        # Generate summary if not provided
        if summary is None:
            summary = await self.generate_summary(db, analysis_id=analysis_id)
        
        # Update analysis
        await analysis_crud.update_status(
            db,
            analysis_id=analysis_id,
            status=AnalysisStatus.COMPLETED,
            progress=100.0
        )
        
        await analysis_crud.set_summary(
            db,
            analysis_id=analysis_id,
            summary=summary
        )
        
        # Update Redis
        await redis_service.set_analysis_progress(
            analysis_id,
            progress=100.0,
            status="completed"
        )
        
        # Cache summary
        await redis_service.cache_analysis_result(
            analysis_id,
            summary
        )
        
        self.log_info(f"Completed analysis {analysis_id}")
    
    async def generate_summary(
        self,
        db: AsyncSession,
        *,
        analysis_id: int
    ) -> Dict[str, Any]:
        """Generate summary for completed analysis."""
        # Get counts
        total_results = await result_crud.count_by_analysis(db, analysis_id=analysis_id)
        
        # Get distributions
        sentiment_dist = await result_crud.get_sentiment_distribution(
            db, analysis_id=analysis_id
        )
        emotion_dist = await result_crud.get_emotion_distribution(
            db, analysis_id=analysis_id
        )
        
        # Get average sentiment
        avg_sentiment = await result_crud.get_average_sentiment(
            db, analysis_id=analysis_id
        )
        
        # Get top keywords
        top_keywords = await result_crud.aggregate_keywords(
            db, analysis_id=analysis_id, limit=20
        )
        
        summary = {
            "total_posts": total_results,
            "processed_posts": total_results,
            "sentiment_distribution": sentiment_dist,
            "emotion_distribution": emotion_dist,
            "average_sentiment_score": avg_sentiment,
            "top_keywords": top_keywords,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return summary
    
    async def fail_analysis(
        self,
        db: AsyncSession,
        *,
        analysis_id: int,
        error_message: str
    ):
        """Mark analysis as failed."""
        await analysis_crud.update_status(
            db,
            analysis_id=analysis_id,
            status=AnalysisStatus.FAILED,
            error_message=error_message
        )
        
        await redis_service.set_analysis_progress(
            analysis_id,
            progress=0.0,
            status="failed"
        )
        
        self.log_error(f"Analysis {analysis_id} failed: {error_message}")
    
    async def get_progress(
        self,
        analysis_id: int
    ) -> Optional[Dict[str, Any]]:
        """Get analysis progress from cache."""
        return await redis_service.get_analysis_progress(analysis_id)
    
    async def cancel_analysis(
        self,
        db: AsyncSession,
        *,
        analysis_id: int
    ) -> bool:
        """Cancel an analysis job."""
        analysis = await analysis_crud.get(db, analysis_id)
        if not analysis:
            return False
        
        if analysis.status in [AnalysisStatus.COMPLETED, AnalysisStatus.FAILED]:
            return False
        
        await analysis_crud.update_status(
            db,
            analysis_id=analysis_id,
            status=AnalysisStatus.CANCELLED
        )
        
        await redis_service.set_analysis_progress(
            analysis_id,
            progress=0.0,
            status="cancelled"
        )
        
        self.log_info(f"Cancelled analysis {analysis_id}")
        return True


# Create singleton instance
analysis_service = AnalysisService()
```

### auth_service.py
```python
from typing import Optional, Tuple
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base import BaseService
from app.crud import user as user_crud
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password
)
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.auth import TokenResponse


class AuthService(BaseService):
    """Service for authentication operations."""
    
    def __init__(self):
        super().__init__("AuthService")
    
    async def authenticate(
        self,
        db: AsyncSession,
        *,
        identifier: str,
        password: str
    ) -> Optional[User]:
        """Authenticate user by email/username and password."""
        user = await user_crud.authenticate(
            db,
            identifier=identifier,
            password=password
        )
        
        if user:
            self.log_info(f"User {user.username} authenticated successfully")
        else:
            self.log_warning(f"Failed authentication attempt for {identifier}")
        
        return user
    
    async def create_tokens(
        self,
        user: User
    ) -> TokenResponse:
        """Create access and refresh tokens for user."""
        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    async def refresh_tokens(
        self,
        db: AsyncSession,
        *,
        refresh_token: str
    ) -> Optional[TokenResponse]:
        """Refresh access token using refresh token."""
        payload = decode_token(refresh_token)
        
        if not payload:
            self.log_warning("Invalid refresh token")
            return None
        
        if payload.get("type") != "refresh":
            self.log_warning("Token is not a refresh token")
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        user = await user_crud.get(db, int(user_id))
        if not user or not user.is_active:
            self.log_warning(f"User {user_id} not found or inactive")
            return None
        
        return await self.create_tokens(user)
    
    async def validate_token(
        self,
        db: AsyncSession,
        *,
        token: str
    ) -> Optional[User]:
        """Validate access token and return user."""
        payload = decode_token(token)
        
        if not payload:
            return None
        
        if payload.get("type") != "access":
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        user = await user_crud.get(db, int(user_id))
        if not user or not user.is_active:
            return None
        
        return user
    
    async def register(
        self,
        db: AsyncSession,
        *,
        user_in: UserCreate
    ) -> Tuple[Optional[User], Optional[str]]:
        """Register a new user. Returns (user, error_message)."""
        # Check if email exists
        existing_email = await user_crud.get_by_email(db, email=user_in.email)
        if existing_email:
            return None, "Email already registered"
        
        # Check if username exists
        existing_username = await user_crud.get_by_username(
            db, username=user_in.username
        )
        if existing_username:
            return None, "Username already taken"
        
        # Create user
        user = await user_crud.create(db, obj_in=user_in)
        
        self.log_info(f"New user registered: {user.username}")
        return user, None
    
    async def change_password(
        self,
        db: AsyncSession,
        *,
        user: User,
        current_password: str,
        new_password: str
    ) -> Tuple[bool, Optional[str]]:
        """Change user password. Returns (success, error_message)."""
        if not verify_password(current_password, user.hashed_password):
            return False, "Current password is incorrect"
        
        await user_crud.update_password(db, user=user, new_password=new_password)
        
        self.log_info(f"Password changed for user {user.username}")
        return True, None


# Create singleton instance
auth_service = AuthService()
```

### brain_service.py
```python
from typing import Optional, Any, Dict, List
import httpx
from app.core.config import settings
from app.services.base import BaseService
from app.schemas.brain import (
    BrainHealthResponse,
    TextAnalysisRequest,
    TextAnalysisResponse,
    BatchAnalysisRequest,
    BatchAnalysisResponse,
    SummarizationRequest,
    TrendDetectionRequest,
)


class BrainServiceError(Exception):
    """Exception for BRAIN service errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class BrainService(BaseService):
    """
    Service for communicating with the BRAIN (RAPIDS Docker) container.
    Handles all AI/ML analysis requests.
    """
    
    def __init__(self):
        super().__init__("BrainService")
        self.base_url = settings.BRAIN_SERVICE_URL
        self.timeout = settings.BRAIN_SERVICE_TIMEOUT
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=httpx.Timeout(self.timeout),
                headers={"Content-Type": "application/json"}
            )
        return self._client
    
    async def close(self) -> None:
        """Close HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to BRAIN service."""
        client = await self._get_client()
        
        try:
            response = await client.request(
                method=method,
                url=endpoint,
                json=data,
                params=params
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            self.log_error(f"BRAIN service timeout: {endpoint}")
            raise BrainServiceError("BRAIN service timeout", status_code=504)
        except httpx.HTTPStatusError as e:
            self.log_error(f"BRAIN service HTTP error: {e.response.status_code}")
            raise BrainServiceError(
                f"BRAIN service error: {e.response.text}",
                status_code=e.response.status_code
            )
        except httpx.RequestError as e:
            self.log_error(f"BRAIN service connection error: {e}")
            raise BrainServiceError("BRAIN service unavailable", status_code=503)
        except Exception as e:
            self.log_error(f"BRAIN service unexpected error: {e}")
            raise BrainServiceError(str(e))
    
    async def health_check(self) -> BrainHealthResponse:
        """Check BRAIN service health."""
        try:
            result = await self._request("GET", "/health")
            return BrainHealthResponse(**result)
        except BrainServiceError:
            return BrainHealthResponse(
                status="unhealthy",
                gpu_available=False
            )
    
    async def is_available(self) -> bool:
        """Check if BRAIN service is available."""
        try:
            health = await self.health_check()
            return health.status == "healthy"
        except Exception:
            return False
    
    # ==========================================
    # Sentiment Analysis
    # ==========================================
    
    async def analyze_sentiment(
        self,
        texts: List[str],
        text_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Analyze sentiment of texts."""
        if text_ids is None:
            text_ids = [str(i) for i in range(len(texts))]
        
        request_data = {
            "texts": texts,
            "text_ids": text_ids,
            "analysis_types": ["sentiment"],
            "language": "fa"
        }
        
        result = await self._request("POST", "/analyze/sentiment", data=request_data)
        return result.get("results", [])
    
    async def analyze_sentiment_batch(
        self,
        posts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Batch sentiment analysis for posts."""
        texts = [p.get("content", "") for p in posts]
        text_ids = [str(p.get("id", i)) for i, p in enumerate(posts)]
        
        return await self.analyze_sentiment(texts, text_ids)
    
    # ==========================================
    # Emotion Analysis
    # ==========================================
    
    async def analyze_emotions(
        self,
        texts: List[str],
        text_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Analyze emotions in texts."""
        if text_ids is None:
            text_ids = [str(i) for i in range(len(texts))]
        
        request_data = {
            "texts": texts,
            "text_ids": text_ids,
            "analysis_types": ["emotion"],
            "language": "fa"
        }
        
        result = await self._request("POST", "/analyze/emotion", data=request_data)
        return result.get("results", [])
    
    # ==========================================
    # Full Text Analysis
    # ==========================================
    
    async def analyze_text(
        self,
        texts: List[str],
        text_ids: Optional[List[str]] = None,
        analysis_types: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> List[TextAnalysisResponse]:
        """Full text analysis including sentiment, emotion, keywords, etc."""
        if text_ids is None:
            text_ids = [str(i) for i in range(len(texts))]
        
        if analysis_types is None:
            analysis_types = ["sentiment", "emotion", "keywords", "entities"]
        
        request_data = TextAnalysisRequest(
            texts=texts,
            text_ids=text_ids,
            analysis_types=analysis_types,
            language="fa",
            config=config
        ).model_dump()
        
        result = await self._request("POST", "/analyze/text", data=request_data)
        
        return [TextAnalysisResponse(**r) for r in result.get("results", [])]
    
    # ==========================================
    # Summarization
    # ==========================================
    
    async def summarize_texts(
        self,
        texts: List[str],
        max_length: int = 150,
        min_length: int = 30
    ) -> List[str]:
        """Summarize texts."""
        request_data = SummarizationRequest(
            texts=texts,
            max_length=max_length,
            min_length=min_length,
            language="fa"
        ).model_dump()
        
        result = await self._request("POST", "/analyze/summarize", data=request_data)
        return result.get("summaries", [])
    
    async def summarize_single(
        self,
        text: str,
        max_length: int = 150
    ) -> str:
        """Summarize a single text."""
        summaries = await self.summarize_texts([text], max_length)
        return summaries[0] if summaries else ""
    
    # ==========================================
    # Keyword Extraction
    # ==========================================
    
    async def extract_keywords(
        self,
        texts: List[str],
        max_keywords: int = 10
    ) -> List[List[str]]:
        """Extract keywords from texts."""
        request_data = {
            "texts": texts,
            "max_keywords": max_keywords,
            "language": "fa"
        }
        
        result = await self._request("POST", "/analyze/keywords", data=request_data)
        return result.get("keywords", [])
    
    # ==========================================
    # Named Entity Recognition
    # ==========================================
    
    async def extract_entities(
        self,
        texts: List[str]
    ) -> List[List[Dict[str, Any]]]:
        """Extract named entities from texts."""
        request_data = {
            "texts": texts,
            "language": "fa"
        }
        
        result = await self._request("POST", "/analyze/entities", data=request_data)
        return result.get("entities", [])
    
    # ==========================================
    # Topic Modeling
    # ==========================================
    
    async def detect_topics(
        self,
        texts: List[str],
        num_topics: int = 10
    ) -> Dict[str, Any]:
        """Detect topics in texts."""
        request_data = {
            "texts": texts,
            "num_topics": num_topics,
            "language": "fa"
        }
        
        result = await self._request("POST", "/analyze/topics", data=request_data)
        return result
    
    # ==========================================
    # Trend Detection
    # ==========================================
    
    async def detect_trends(
        self,
        posts: List[Dict[str, Any]],
        time_window: str = "1h",
        min_trend_size: int = 10
    ) -> List[Dict[str, Any]]:
        """Detect trends in posts."""
        request_data = TrendDetectionRequest(
            posts=posts,
            time_field="posted_at",
            content_field="content",
            min_trend_size=min_trend_size,
            time_window=time_window
        ).model_dump()
        
        result = await self._request("POST", "/analyze/trends", data=request_data)
        return result.get("trends", [])
    
    # ==========================================
    # Graph Analysis
    # ==========================================
    
    async def analyze_graph(
        self,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]],
        algorithms: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Analyze graph structure."""
        if algorithms is None:
            algorithms = ["pagerank", "community_detection", "centrality"]
        
        request_data = {
            "nodes": nodes,
            "edges": edges,
            "algorithms": algorithms
        }
        
        result = await self._request("POST", "/analyze/graph", data=request_data)
        return result
    
    async def calculate_pagerank(
        self,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]],
        damping: float = 0.85
    ) -> List[Dict[str, Any]]:
        """Calculate PageRank for nodes."""
        request_data = {
            "nodes": nodes,
            "edges": edges,
            "algorithm": "pagerank",
            "damping": damping
        }
        
        result = await self._request("POST", "/analyze/graph/pagerank", data=request_data)
        return result.get("nodes", [])
    
    async def detect_communities(
        self,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Detect communities in graph."""
        request_data = {
            "nodes": nodes,
            "edges": edges,
            "algorithm": "community_detection"
        }
        
        result = await self._request("POST", "/analyze/graph/communities", data=request_data)
        return result
    
    # ==========================================
    # Batch Analysis
    # ==========================================
    
    async def submit_batch_analysis(
        self,
        analysis_id: int,
        posts: List[Dict[str, Any]],
        config: Dict[str, Any],
        callback_url: Optional[str] = None
    ) -> BatchAnalysisResponse:
        """Submit batch analysis job to BRAIN."""
        request_data = BatchAnalysisRequest(
            analysis_id=analysis_id,
            posts=posts,
            config=config,
            callback_url=callback_url
        ).model_dump()
        
        result = await self._request("POST", "/batch/analyze", data=request_data)
        return BatchAnalysisResponse(**result)
    
    async def get_batch_status(
        self,
        task_id: str
    ) -> Dict[str, Any]:
        """Get batch analysis status."""
        result = await self._request("GET", f"/batch/status/{task_id}")
        return result
    
    async def get_batch_result(
        self,
        task_id: str
    ) -> Dict[str, Any]:
        """Get batch analysis result."""
        result = await self._request("GET", f"/batch/result/{task_id}")
        return result


# Create singleton instance
brain_service = BrainService()
```

### celery_app.py
```python
from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "persian_analytics",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.services.tasks"
    ]
)

# Celery configuration
celery_app.conf.update(
    # Task settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Task execution settings
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max
    task_soft_time_limit=3300,  # 55 minutes soft limit
    
    # Result settings
    result_expires=86400,  # Results expire after 24 hours
    
    # Worker settings
    worker_prefetch_multiplier=1,
    worker_concurrency=4,
    
    # Task routing
    task_routes={
        "app.services.tasks.process_analysis": {"queue": "analysis"},
        "app.services.tasks.detect_trends": {"queue": "trends"},
        "app.services.tasks.build_graph": {"queue": "graph"},
    },
    
    # Beat schedule for periodic tasks
    beat_schedule={
        "detect-trends-hourly": {
            "task": "app.services.tasks.detect_trends_periodic",
            "schedule": 3600.0,  # Every hour
        },
        "update-trend-status": {
            "task": "app.services.tasks.update_trend_status_periodic",
            "schedule": 1800.0,  # Every 30 minutes
        },
        "cleanup-old-results": {
            "task": "app.services.tasks.cleanup_old_results",
            "schedule": 86400.0,  # Every 24 hours
        },
    },
)


# Optional: Configure task queues
celery_app.conf.task_queues = {
    "default": {
        "exchange": "default",
        "routing_key": "default",
    },
    "analysis": {
        "exchange": "analysis",
        "routing_key": "analysis",
    },
    "trends": {
        "exchange": "trends",
        "routing_key": "trends",
    },
    "graph": {
        "exchange": "graph",
        "routing_key": "graph",
    },
}
```

### dashboard_service.py
```python
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base import BaseService
from app.services.redis_service import redis_service
from app.crud import dashboard as dashboard_crud
from app.crud import analysis as analysis_crud
from app.crud import post as post_crud
from app.crud import trend as trend_crud
from app.crud import graph_node as node_crud
from app.schemas.dashboard import DashboardCreate


class DashboardService(BaseService):
    """Service for dashboard operations."""
    
    def __init__(self):
        super().__init__("DashboardService")
    
    async def get_overview_stats(
        self,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Get overview statistics for dashboard."""
        # Try to get from cache
        cached = await redis_service.get_json("dashboard:overview")
        if cached:
            return cached
        
        # Get stats from database
        post_stats = await post_crud.get_stats(db)
        
        # Count active trends
        active_trends = await trend_crud.get_active(db, limit=1)
        trend_stats = await trend_crud.get_stats(db)
        
        # Get graph stats
        graph_stats = await node_crud.get_stats(db)
        
        # Get analysis stats
        analysis_stats = await analysis_crud.get_stats(db)
        
        overview = {
            "posts": {
                "total": post_stats["total"],
                "processed": post_stats["processed"],
                "by_platform": post_stats["by_platform"],
                "by_language": post_stats["by_language"]
            },
            "trends": {
                "active": trend_stats["active"],
                "total": trend_stats["total"]
            },
            "graph": {
                "nodes": graph_stats["total_nodes"],
                "communities": graph_stats["communities_count"]
            },
            "analyses": {
                "total": analysis_stats["total"],
                "by_status": analysis_stats["by_status"]
            }
        }
        
        # Cache for 5 minutes
        await redis_service.set_json("dashboard:overview", overview, expire=300)
        
        return overview
    
    async def get_sentiment_overview(
        self,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Get sentiment analysis overview."""
        from app.models.analysis_result import AnalysisResult
        from sqlalchemy import select, func
        
        # Get sentiment distribution
        query = (
            select(
                AnalysisResult.sentiment_label,
                func.count(AnalysisResult.id)
            )
            .where(AnalysisResult.sentiment_label.isnot(None))
            .group_by(AnalysisResult.sentiment_label)
        )
        result = await db.execute(query)
        
        distribution = {row[0]: row[1] for row in result.all()}
        
        # Calculate percentages
        total = sum(distribution.values())
        percentages = {}
        if total > 0:
            percentages = {
                k: round((v / total) * 100, 2)
                for k, v in distribution.items()
            }
        
        # Get average score
        avg_query = select(func.avg(AnalysisResult.sentiment_score))
        avg_result = await db.execute(avg_query)
        avg_score = avg_result.scalar()
        
        return {
            "distribution": distribution,
            "percentages": percentages,
            "average_score": float(avg_score) if avg_score else 0,
            "total_analyzed": total
        }
    
    async def get_emotion_overview(
        self,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Get emotion analysis overview."""
        from app.models.analysis_result import AnalysisResult
        from sqlalchemy import select, func
        
        query = (
            select(
                AnalysisResult.dominant_emotion,
                func.count(AnalysisResult.id)
            )
            .where(AnalysisResult.dominant_emotion.isnot(None))
            .group_by(AnalysisResult.dominant_emotion)
        )
        result = await db.execute(query)
        
        distribution = {row[0]: row[1] for row in result.all()}
        
        total = sum(distribution.values())
        percentages = {}
        if total > 0:
            percentages = {
                k: round((v / total) * 100, 2)
                for k, v in distribution.items()
            }
        
        return {
            "distribution": distribution,
            "percentages": percentages,
            "total_analyzed": total
        }
    
    async def get_platform_stats(
        self,
        db: AsyncSession
    ) -> List[Dict[str, Any]]:
        """Get statistics by platform."""
        post_stats = await post_crud.get_stats(db)
        
        platforms = []
        for platform, count in post_stats["by_platform"].items():
            platforms.append({
                "platform": platform,
                "post_count": count,
                "percentage": round(
                    (count / post_stats["total"]) * 100, 2
                ) if post_stats["total"] > 0 else 0
            })
        
        return sorted(platforms, key=lambda x: x["post_count"], reverse=True)
    
    async def get_widget_data(
        self,
        db: AsyncSession,
        *,
        widget_type: str,
        config: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Get data for a specific widget type."""
        config = config or {}
        
        if widget_type == "sentiment_chart":
            return await self.get_sentiment_overview(db)
        
        elif widget_type == "emotion_chart":
            return await self.get_emotion_overview(db)
        
        elif widget_type == "trending_hashtags":
            from app.services.trend_service import trend_service
            return await trend_service.get_trending_hashtags(
                db,
                hours=config.get("hours", 24),
                limit=config.get("limit", 10)
            )
        
        elif widget_type == "trending_keywords":
            from app.services.trend_service import trend_service
            return await trend_service.get_trending_keywords(
                db,
                hours=config.get("hours", 24),
                limit=config.get("limit", 10)
            )
        
        elif widget_type == "volume_chart":
            from app.services.trend_service import trend_service
            return await trend_service.get_volume_trends(
                db,
                hours=config.get("hours", 24),
                interval=config.get("interval", "1h")
            )
        
        elif widget_type == "platform_stats":
            return await self.get_platform_stats(db)
        
        elif widget_type == "overview":
            return await self.get_overview_stats(db)
        
        elif widget_type == "top_authors":
            from app.crud import author as author_crud
            authors = await author_crud.get_top_by_influence(
                db,
                limit=config.get("limit", 10)
            )
            return [
                {
                    "id": a.id,
                    "username": a.username,
                    "display_name": a.display_name,
                    "influence_score": a.influence_score,
                    "followers_count": a.followers_count
                }
                for a in authors
            ]
        
        elif widget_type == "recent_analyses":
            analyses = await analysis_crud.get_multi(db, limit=config.get("limit", 5))
            return [
                {
                    "id": a.id,
                    "name": a.name,
                    "status": a.status.value,
                    "progress": a.progress,
                    "created_at": a.created_at.isoformat() if a.created_at else None
                }
                for a in analyses
            ]
        
        else:
            return {"error": f"Unknown widget type: {widget_type}"}
    
    async def create_default_dashboard(
        self,
        db: AsyncSession,
        *,
        user_id: int
    ):
        """Create default dashboard for a user."""
        default_widgets = [
            {
                "widget_id": "overview-1",
                "widget_type": "overview",
                "title": "Overview",
                "position": {"x": 0, "y": 0, "w": 4, "h": 2}
            },
            {
                "widget_id": "sentiment-1",
                "widget_type": "sentiment_chart",
                "title": "Sentiment Distribution",
                "position": {"x": 4, "y": 0, "w": 4, "h": 2}
            },
            {
                "widget_id": "emotions-1",
                "widget_type": "emotion_chart",
                "title": "Emotion Distribution",
                "position": {"x": 8, "y": 0, "w": 4, "h": 2}
            },
            {
                "widget_id": "hashtags-1",
                "widget_type": "trending_hashtags",
                "title": "Trending Hashtags",
                "position": {"x": 0, "y": 2, "w": 6, "h": 3}
            },
            {
                "widget_id": "volume-1",
                "widget_type": "volume_chart",
                "title": "Post Volume",
                "position": {"x": 6, "y": 2, "w": 6, "h": 3}
            }
        ]
        
        dashboard_in = DashboardCreate(
            name="Default Dashboard",
            description="Auto-generated default dashboard",
            widgets=default_widgets,
            is_default=True
        )
        
        dashboard = await dashboard_crud.create_with_user(
            db,
            obj_in=dashboard_in,
            user_id=user_id
        )
        
        self.log_info(f"Created default dashboard for user {user_id}")
        return dashboard


# Create singleton instance
dashboard_service = DashboardService()
```

### graph_service.py
```python
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base import BaseService
from app.services.brain_service import brain_service, BrainServiceError
from app.crud import graph_node as node_crud
from app.crud import graph_edge as edge_crud
from app.crud import author as author_crud
from app.crud import post as post_crud
from app.schemas.graph import GraphNodeCreate, GraphEdgeCreate


class GraphService(BaseService):
    """Service for graph analysis operations."""
    
    def __init__(self):
        super().__init__("GraphService")
    
    async def build_author_network(
        self,
        db: AsyncSession,
        *,
        platform: Optional[str] = None
    ) -> Dict[str, Any]:
        """Build author interaction network from posts."""
        # Get all posts with mentions
        from app.schemas.post import PostFilter
        
        filters = PostFilter(platform=platform) if platform else PostFilter()
        posts = await post_crud.get_filtered(db, filters=filters, limit=10000)
        
        nodes_created = 0
        edges_created = 0
        
        for post in posts:
            if not post.author_id:
                continue
            
            # Create author node
            author_node = GraphNodeCreate(
                node_id=f"author_{post.author_id}",
                node_type="author",
                label=str(post.author_id)
            )
            await node_crud.get_or_create(db, obj_in=author_node)
            nodes_created += 1
            
            # Process mentions
            if post.mentions:
                for mention in post.mentions:
                    # Create mention node
                    mention_node = GraphNodeCreate(
                        node_id=f"mention_{mention}",
                        node_type="mention",
                        label=mention
                    )
                    target, _ = await node_crud.get_or_create(db, obj_in=mention_node)
                    
                    # Get source node
                    source = await node_crud.get_by_node_id(
                        db, node_id=f"author_{post.author_id}"
                    )
                    
                    if source and target:
                        # Create edge
                        edge = GraphEdgeCreate(
                            edge_type="mentions",
                            source_id=source.id,
                            target_id=target.id,
                            weight=1.0
                        )
                        await edge_crud.get_or_create(db, obj_in=edge)
                        edges_created += 1
        
        return {
            "nodes_created": nodes_created,
            "edges_created": edges_created
        }
    
    async def build_hashtag_network(
        self,
        db: AsyncSession,
        *,
        platform: Optional[str] = None
    ) -> Dict[str, Any]:
        """Build hashtag co-occurrence network."""
        from app.schemas.post import PostFilter
        
        filters = PostFilter(platform=platform) if platform else PostFilter()
        posts = await post_crud.get_filtered(db, filters=filters, limit=10000)
        
        nodes_created = 0
        edges_created = 0
        
        for post in posts:
            if not post.hashtags or len(post.hashtags) < 2:
                continue
            
            # Create nodes for hashtags
            hashtag_nodes = []
            for hashtag in post.hashtags:
                node = GraphNodeCreate(
                    node_id=f"hashtag_{hashtag}",
                    node_type="hashtag",
                    label=hashtag
                )
                db_node, created = await node_crud.get_or_create(db, obj_in=node)
                hashtag_nodes.append(db_node)
                if created:
                    nodes_created += 1
            
            # Create edges between co-occurring hashtags
            for i, source in enumerate(hashtag_nodes):
                for target in hashtag_nodes[i+1:]:
                    edge = GraphEdgeCreate(
                        edge_type="co_occurrence",
                        source_id=source.id,
                        target_id=target.id,
                        weight=1.0
                    )
                    _, created = await edge_crud.get_or_create(db, obj_in=edge)
                    if created:
                        edges_created += 1
        
        return {
            "nodes_created": nodes_created,
            "edges_created": edges_created
        }
    
    async def calculate_pagerank(
        self,
        db: AsyncSession
    ) -> int:
        """Calculate PageRank for all nodes using BRAIN service."""
        # Get all nodes and edges
        nodes = await node_crud.get_all(db)
        edges = await edge_crud.get_all(db)
        
        if not nodes or not edges:
            return 0
        
        # Prepare data for BRAIN
        nodes_data = [
            {"id": n.node_id, "type": n.node_type}
            for n in nodes
        ]
        edges_data = [
            {
                "source": (await node_crud.get(db, e.source_id)).node_id,
                "target": (await node_crud.get(db, e.target_id)).node_id,
                "weight": e.weight
            }
            for e in edges
        ]
        
        try:
            # Call BRAIN service
            results = await brain_service.calculate_pagerank(
                nodes=nodes_data,
                edges=edges_data
            )
            
            # Update nodes with PageRank scores
            updated = 0
            for result in results:
                node = await node_crud.get_by_node_id(db, node_id=result["id"])
                if node:
                    await node_crud.update(
                        db,
                        db_obj=node,
                        obj_in={"pagerank": result.get("pagerank", 0)}
                    )
                    updated += 1
            
            return updated
            
        except BrainServiceError as e:
            self.log_error(f"PageRank calculation failed: {e.message}")
            return 0
    
    async def detect_communities(
        self,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Detect communities using BRAIN service."""
        nodes = await node_crud.get_all(db)
        edges = await edge_crud.get_all(db)
        
        if not nodes or not edges:
            return {"communities": 0}
        
        nodes_data = [
            {"id": n.node_id, "type": n.node_type}
            for n in nodes
        ]
        edges_data = [
            {
                "source": (await node_crud.get(db, e.source_id)).node_id,
                "target": (await node_crud.get(db, e.target_id)).node_id,
                "weight": e.weight
            }
            for e in edges
        ]
        
        try:
            result = await brain_service.detect_communities(
                nodes=nodes_data,
                edges=edges_data
            )
            
            # Update nodes with community IDs
            for node_result in result.get("nodes", []):
                node = await node_crud.get_by_node_id(
                    db, node_id=node_result["id"]
                )
                if node:
                    await node_crud.update(
                        db,
                        db_obj=node,
                        obj_in={"community_id": node_result.get("community_id")}
                    )
            
            return {
                "communities": len(result.get("communities", [])),
                "communities_data": result.get("communities", [])
            }
            
        except BrainServiceError as e:
            self.log_error(f"Community detection failed: {e.message}")
            return {"communities": 0, "error": e.message}
    
    async def get_graph_data(
        self,
        db: AsyncSession,
        *,
        node_type: Optional[str] = None,
        limit: int = 1000
    ) -> Dict[str, Any]:
        """Get graph data for visualization."""
        if node_type:
            nodes = await node_crud.get_by_type(db, node_type=node_type, limit=limit)
        else:
            nodes = await node_crud.get_multi(db, limit=limit)
        
        node_ids = [n.id for n in nodes]
        
        # Get edges for these nodes
        edges = []
        for node in nodes:
            node_edges = await edge_crud.get_by_source(db, source_id=node.id, limit=100)
            edges.extend([e for e in node_edges if e.target_id in node_ids])
        
        return {
            "nodes": [
                {
                    "id": n.node_id,
                    "label": n.label,
                    "type": n.node_type,
                    "pagerank": n.pagerank,
                    "degree": n.degree,
                    "community": n.community_id
                }
                for n in nodes
            ],
            "edges": [
                {
                    "source": (await node_crud.get(db, e.source_id)).node_id,
                    "target": (await node_crud.get(db, e.target_id)).node_id,
                    "type": e.edge_type,
                    "weight": e.weight
                }
                for e in edges
            ]
        }
    
    async def get_stats(
        self,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Get graph statistics."""
        node_stats = await node_crud.get_stats(db)
        edge_stats = await edge_crud.get_stats(db)
        
        total_nodes = node_stats["total_nodes"]
        total_edges = edge_stats["total_edges"]
        
        # Calculate density
        density = 0.0
        if total_nodes > 1:
            max_edges = total_nodes * (total_nodes - 1)
            density = (2 * total_edges) / max_edges if max_edges > 0 else 0
        
        return {
            **node_stats,
            **edge_stats,
            "density": density
        }


# Create singleton instance
graph_service = GraphService()
```

### redis_service.py
```python
from typing import Optional, Any, List
import json
import redis.asyncio as redis
from app.core.config import settings
from app.services.base import BaseService


class RedisService(BaseService):
    """Service for Redis cache operations."""
    
    def __init__(self):
        super().__init__("RedisService")
        self._client: Optional[redis.Redis] = None
    
    async def connect(self) -> None:
        """Connect to Redis."""
        if not self._client:
            self._client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            await self._client.ping()
            self.log_info("Connected to Redis")
    
    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self._client:
            await self._client.close()
            self._client = None
            self.log_info("Disconnected from Redis")
    
    @property
    def client(self) -> redis.Redis:
        """Get Redis client."""
        if not self._client:
            raise RuntimeError("Redis not connected. Call connect() first.")
        return self._client
    
    async def get(self, key: str) -> Optional[str]:
        """Get value by key."""
        try:
            return await self.client.get(key)
        except Exception as e:
            self.log_error(f"Redis GET error: {e}")
            return None
    
    async def set(
        self,
        key: str,
        value: str,
        expire: Optional[int] = None
    ) -> bool:
        """Set value with optional expiration (seconds)."""
        try:
            if expire:
                await self.client.setex(key, expire, value)
            else:
                await self.client.set(key, value)
            return True
        except Exception as e:
            self.log_error(f"Redis SET error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key."""
        try:
            await self.client.delete(key)
            return True
        except Exception as e:
            self.log_error(f"Redis DELETE error: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        try:
            return await self.client.exists(key) > 0
        except Exception as e:
            self.log_error(f"Redis EXISTS error: {e}")
            return False
    
    async def get_json(self, key: str) -> Optional[Any]:
        """Get JSON value by key."""
        value = await self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return None
        return None
    
    async def set_json(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None
    ) -> bool:
        """Set JSON value."""
        try:
            json_str = json.dumps(value, default=str)
            return await self.set(key, json_str, expire)
        except Exception as e:
            self.log_error(f"Redis SET JSON error: {e}")
            return False
    
    async def incr(self, key: str) -> int:
        """Increment integer value."""
        try:
            return await self.client.incr(key)
        except Exception as e:
            self.log_error(f"Redis INCR error: {e}")
            return 0
    
    async def lpush(self, key: str, *values: str) -> int:
        """Push values to list."""
        try:
            return await self.client.lpush(key, *values)
        except Exception as e:
            self.log_error(f"Redis LPUSH error: {e}")
            return 0
    
    async def lrange(
        self,
        key: str,
        start: int = 0,
        end: int = -1
    ) -> List[str]:
        """Get list range."""
        try:
            return await self.client.lrange(key, start, end)
        except Exception as e:
            self.log_error(f"Redis LRANGE error: {e}")
            return []
    
    async def publish(self, channel: str, message: str) -> int:
        """Publish message to channel."""
        try:
            return await self.client.publish(channel, message)
        except Exception as e:
            self.log_error(f"Redis PUBLISH error: {e}")
            return 0
    
    async def cache_analysis_result(
        self,
        analysis_id: int,
        result: dict,
        expire: int = 3600
    ) -> bool:
        """Cache analysis result."""
        key = f"analysis:{analysis_id}:result"
        return await self.set_json(key, result, expire)
    
    async def get_cached_analysis_result(
        self,
        analysis_id: int
    ) -> Optional[dict]:
        """Get cached analysis result."""
        key = f"analysis:{analysis_id}:result"
        return await self.get_json(key)
    
    async def set_analysis_progress(
        self,
        analysis_id: int,
        progress: float,
        status: str
    ) -> bool:
        """Set analysis progress in cache."""
        key = f"analysis:{analysis_id}:progress"
        data = {"progress": progress, "status": status}
        return await self.set_json(key, data, expire=3600)
    
    async def get_analysis_progress(
        self,
        analysis_id: int
    ) -> Optional[dict]:
        """Get analysis progress from cache."""
        key = f"analysis:{analysis_id}:progress"
        return await self.get_json(key)


# Create singleton instance
redis_service = RedisService()
```

### tasks.py
```python
from typing import Optional, Dict, Any, List
from celery import current_task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import asyncio
import httpx

from app.services.celery_app import celery_app
from app.core.config import settings
from loguru import logger

# Create sync engine for Celery tasks
sync_engine = create_engine(
    settings.DATABASE_SYNC_URL,
    pool_pre_ping=True
)
SyncSessionLocal = sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)


def get_sync_db() -> Session:
    """Get synchronous database session for Celery tasks."""
    db = SyncSessionLocal()
    return db


def run_async(coro):
    """Run async function in sync context - properly handles event loop."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    try:
        return loop.run_until_complete(coro)
    finally:
        # Don't close the loop, just clean up pending tasks
        try:
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
        except RuntimeError:
            pass


def call_brain_sync(endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Synchronous HTTP call to BRAIN service."""
    url = f"{settings.BRAIN_SERVICE_URL}{endpoint}"
    
    try:
        with httpx.Client(timeout=settings.BRAIN_SERVICE_TIMEOUT) as client:
            response = client.post(url, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        logger.error(f"BRAIN service timeout: {endpoint}")
        raise Exception("BRAIN service timeout")
    except httpx.HTTPStatusError as e:
        logger.error(f"BRAIN service HTTP error: {e.response.status_code}")
        raise Exception(f"BRAIN service error: {e.response.text}")
    except httpx.RequestError as e:
        logger.error(f"BRAIN service connection error: {e}")
        raise Exception("BRAIN service unavailable")


@celery_app.task(bind=True, name="app.services.tasks.process_analysis")
def process_analysis(
    self,
    analysis_id: int,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Process an analysis job.
    """
    logger.info(f"Starting analysis task for analysis_id={analysis_id}")
    
    db = get_sync_db()
    
    try:
        from app.models.analysis import Analysis, AnalysisStatus
        from app.models.post import Post
        from app.models.analysis_result import AnalysisResult
        from datetime import datetime
        
        # Get analysis
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            logger.error(f"Analysis {analysis_id} not found")
            return {"status": "error", "message": "Analysis not found"}
        
        # Update status to processing
        analysis.status = AnalysisStatus.PROCESSING
        analysis.started_at = datetime.utcnow()
        analysis.progress = 0.0
        db.commit()
        
        # Get posts based on filters
        query = db.query(Post)
        
        filters = analysis.query_filters or {}
        if filters.get("platform"):
            query = query.filter(Post.platform == filters["platform"])
        if filters.get("language"):
            query = query.filter(Post.language == filters["language"])
        if filters.get("data_source_id"):
            query = query.filter(Post.data_source_id == filters["data_source_id"])
        
        limit = analysis.post_count or 1000
        posts = query.limit(limit).all()
        
        if not posts:
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = "No posts found matching filters"
            db.commit()
            return {"status": "error", "message": "No posts found"}
        
        # Update progress
        self.update_state(state="PROGRESS", meta={"progress": 10})
        analysis.progress = 10.0
        db.commit()
        
        # Prepare posts data for BRAIN
        texts = [p.content or "" for p in posts]
        text_ids = [str(p.id) for p in posts]
        
        # Call BRAIN service synchronously
        try:
            analysis_config = config or {
                "sentiment_enabled": True,
                "emotion_enabled": True,
                "keyword_extraction_enabled": True,
            }
            
            request_data = {
                "texts": texts,
                "text_ids": text_ids,
                "analysis_types": ["sentiment", "emotion", "keywords"],
                "language": "fa",
                "config": analysis_config
            }
            
            result = call_brain_sync("/analyze/text", request_data)
            results = result.get("results", [])
            
            # Update progress
            self.update_state(state="PROGRESS", meta={"progress": 50})
            analysis.progress = 50.0
            db.commit()
            
            # Store results
            for i, res in enumerate(results):
                post_id = int(res.get("text_id", i))
                
                sentiment = res.get("sentiment", {})
                emotions = res.get("emotions", {})
                
                analysis_result = AnalysisResult(
                    post_id=post_id,
                    analysis_id=analysis_id,
                    sentiment_label=sentiment.get("label"),
                    sentiment_score=sentiment.get("score"),
                    sentiment_confidence=sentiment.get("confidence"),
                    emotions=emotions,
                    dominant_emotion=res.get("dominant_emotion") or (max(emotions, key=emotions.get) if emotions else None),
                    keywords=res.get("keywords"),
                    entities=res.get("entities"),
                    summary=res.get("summary"),
                    raw_results=res
                )
                db.add(analysis_result)
                
                # Mark post as processed
                post = db.query(Post).filter(Post.id == post_id).first()
                if post:
                    post.is_processed = True
                
                # Update progress periodically
                if i % 100 == 0:
                    progress = 50 + (i / len(results)) * 40
                    self.update_state(state="PROGRESS", meta={"progress": progress})
                    analysis.progress = progress
                    db.commit()
            
            db.commit()
            
            # Generate summary
            summary = generate_analysis_summary(db, analysis_id)
            
            # Complete analysis
            analysis.status = AnalysisStatus.COMPLETED
            analysis.progress = 100.0
            analysis.completed_at = datetime.utcnow()
            analysis.summary = summary
            db.commit()
            
            logger.info(f"Analysis {analysis_id} completed successfully")
            return {
                "status": "completed",
                "analysis_id": analysis_id,
                "results_count": len(results)
            }
            
        except Exception as e:
            logger.error(f"BRAIN service error: {str(e)}")
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = f"BRAIN service error: {str(e)}"
            db.commit()
            return {"status": "error", "message": str(e)}
        
    except Exception as e:
        logger.error(f"Analysis task error: {str(e)}")
        try:
            analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
            if analysis:
                analysis.status = AnalysisStatus.FAILED
                analysis.error_message = str(e)
                db.commit()
        except Exception:
            pass
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


def generate_analysis_summary(db: Session, analysis_id: int) -> Dict[str, Any]:
    """Generate summary for completed analysis."""
    from app.models.analysis_result import AnalysisResult
    from sqlalchemy import func
    
    # Count results
    total = db.query(func.count(AnalysisResult.id)).filter(
        AnalysisResult.analysis_id == analysis_id
    ).scalar() or 0
    
    # Sentiment distribution
    sentiment_query = db.query(
        AnalysisResult.sentiment_label,
        func.count(AnalysisResult.id)
    ).filter(
        AnalysisResult.analysis_id == analysis_id,
        AnalysisResult.sentiment_label.isnot(None)
    ).group_by(AnalysisResult.sentiment_label).all()
    
    sentiment_dist = {row[0]: row[1] for row in sentiment_query}
    
    # Emotion distribution
    emotion_query = db.query(
        AnalysisResult.dominant_emotion,
        func.count(AnalysisResult.id)
    ).filter(
        AnalysisResult.analysis_id == analysis_id,
        AnalysisResult.dominant_emotion.isnot(None)
    ).group_by(AnalysisResult.dominant_emotion).all()
    
    emotion_dist = {row[0]: row[1] for row in emotion_query}
    
    # Average sentiment
    avg_sentiment = db.query(func.avg(AnalysisResult.sentiment_score)).filter(
        AnalysisResult.analysis_id == analysis_id
    ).scalar()
    
    # Top keywords
    results = db.query(AnalysisResult.keywords).filter(
        AnalysisResult.analysis_id == analysis_id,
        AnalysisResult.keywords.isnot(None)
    ).all()
    
    keyword_counts = {}
    for row in results:
        for kw in (row[0] or []):
            keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
    
    top_keywords = sorted(
        keyword_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:20]
    
    return {
        "total_posts": total,
        "sentiment_distribution": sentiment_dist,
        "emotion_distribution": emotion_dist,
        "average_sentiment_score": float(avg_sentiment) if avg_sentiment else None,
        "top_keywords": [{"keyword": k, "count": v} for k, v in top_keywords]
    }


@celery_app.task(bind=True, name="app.services.tasks.detect_trends")
def detect_trends(
    self,
    hours: int = 24,
    min_count: int = 10
) -> Dict[str, Any]:
    """Detect trends from recent posts."""
    logger.info(f"Starting trend detection for last {hours} hours")
    
    db = get_sync_db()
    
    try:
        from app.models.post import Post
        from app.models.trend import Trend
        from datetime import datetime, timedelta
        
        since = datetime.utcnow() - timedelta(hours=hours)
        
        # Get recent posts
        posts = db.query(Post).filter(
            Post.posted_at >= since
        ).limit(10000).all()
        
        if not posts:
            return {"status": "no_posts", "trends": 0}
        
        # Count hashtags
        hashtag_counts = {}
        for post in posts:
            if post.hashtags:
                for tag in post.hashtags:
                    hashtag_counts[tag] = hashtag_counts.get(tag, 0) + 1
        
        # Filter trending
        trending = [
            (tag, count) for tag, count in hashtag_counts.items()
            if count >= min_count
        ]
        trending.sort(key=lambda x: x[1], reverse=True)
        
        # Create trends
        created = 0
        for tag, count in trending[:50]:
            existing = db.query(Trend).filter(
                Trend.name == f"#{tag}",
                Trend.is_active == "active"
            ).first()
            
            if existing:
                existing.volume = count
                existing.updated_at = datetime.utcnow()
            else:
                trend = Trend(
                    name=f"#{tag}",
                    description=f"Trending hashtag with {count} mentions",
                    volume=count,
                    hashtags=[tag],
                    is_active="active"
                )
                db.add(trend)
                created += 1
        
        db.commit()
        
        logger.info(f"Trend detection completed: {created} new trends")
        return {"status": "completed", "new_trends": created}
        
    except Exception as e:
        logger.error(f"Trend detection error: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


@celery_app.task(name="app.services.tasks.detect_trends_periodic")
def detect_trends_periodic():
    """Periodic task to detect trends."""
    return detect_trends.delay(hours=24, min_count=10)


@celery_app.task(name="app.services.tasks.update_trend_status_periodic")
def update_trend_status_periodic():
    """Periodic task to update trend status."""
    logger.info("Updating trend statuses")
    
    db = get_sync_db()
    
    try:
        from app.models.trend import Trend
        from app.models.post import Post
        from datetime import datetime, timedelta
        
        since = datetime.utcnow() - timedelta(hours=6)
        
        active_trends = db.query(Trend).filter(
            Trend.is_active == "active"
        ).all()
        
        updated = 0
        for trend in active_trends:
            if trend.hashtags:
                recent_count = 0
                for hashtag in trend.hashtags:
                    count = db.query(Post).filter(
                        Post.posted_at >= since,
                        Post.hashtags.contains([hashtag])
                    ).count()
                    recent_count += count
                
                if recent_count < trend.volume * 0.1:
                    trend.is_active = "ended"
                    updated += 1
                elif recent_count < trend.volume * 0.3:
                    trend.is_active = "declining"
                    updated += 1
        
        db.commit()
        logger.info(f"Updated {updated} trend statuses")
        return {"updated": updated}
        
    except Exception as e:
        logger.error(f"Trend status update error: {str(e)}")
        return {"error": str(e)}
    
    finally:
        db.close()


@celery_app.task(bind=True, name="app.services.tasks.build_graph")
def build_graph(
    self,
    graph_type: str = "author_network"
) -> Dict[str, Any]:
    """Build graph from posts."""
    logger.info(f"Building {graph_type} graph")
    
    db = get_sync_db()
    
    try:
        from app.models.post import Post
        from app.models.graph import GraphNode, GraphEdge
        
        nodes_created = 0
        edges_created = 0
        
        posts = db.query(Post).filter(
            Post.mentions.isnot(None)
        ).limit(10000).all()
        
        for post in posts:
            if not post.author_id or not post.mentions:
                continue
            
            # Create or get source node
            source_node_id = f"author_{post.author_id}"
            source = db.query(GraphNode).filter(
                GraphNode.node_id == source_node_id
            ).first()
            
            if not source:
                source = GraphNode(
                    node_id=source_node_id,
                    node_type="author",
                    label=str(post.author_id)
                )
                db.add(source)
                db.flush()
                nodes_created += 1
            
            # Process mentions
            for mention in post.mentions:
                target_node_id = f"mention_{mention}"
                target = db.query(GraphNode).filter(
                    GraphNode.node_id == target_node_id
                ).first()
                
                if not target:
                    target = GraphNode(
                        node_id=target_node_id,
                        node_type="mention",
                        label=mention
                    )
                    db.add(target)
                    db.flush()
                    nodes_created += 1
                
                # Create edge
                edge = db.query(GraphEdge).filter(
                    GraphEdge.source_id == source.id,
                    GraphEdge.target_id == target.id,
                    GraphEdge.edge_type == "mentions"
                ).first()
                
                if edge:
                    edge.occurrence_count += 1
                    edge.weight += 1.0
                else:
                    edge = GraphEdge(
                        edge_type="mentions",
                        source_id=source.id,
                        target_id=target.id,
                        weight=1.0,
                        occurrence_count=1
                    )
                    db.add(edge)
                    edges_created += 1
        
        db.commit()
        
        logger.info(f"Graph built: {nodes_created} nodes, {edges_created} edges")
        return {
            "status": "completed",
            "nodes_created": nodes_created,
            "edges_created": edges_created
        }
        
    except Exception as e:
        logger.error(f"Graph building error: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()


@celery_app.task(name="app.services.tasks.cleanup_old_results")
def cleanup_old_results():
    """Clean up old analysis results."""
    logger.info("Starting cleanup of old results")
    
    db = get_sync_db()
    
    try:
        from app.models.analysis_result import AnalysisResult
        from datetime import datetime, timedelta
        
        cutoff = datetime.utcnow() - timedelta(days=30)
        
        deleted = db.query(AnalysisResult).filter(
            AnalysisResult.created_at < cutoff
        ).delete()
        
        db.commit()
        
        logger.info(f"Cleaned up {deleted} old results")
        return {"deleted": deleted}
        
    except Exception as e:
        logger.error(f"Cleanup error: {str(e)}")
        return {"error": str(e)}
    
    finally:
        db.close()


@celery_app.task(bind=True, name="app.services.tasks.calculate_pagerank")
def calculate_pagerank(self) -> Dict[str, Any]:
    """Calculate PageRank for graph nodes."""
    logger.info("Calculating PageRank")
    
    db = get_sync_db()
    
    try:
        from app.models.graph import GraphNode, GraphEdge
        
        nodes = db.query(GraphNode).all()
        edges = db.query(GraphEdge).all()
        
        if not nodes or not edges:
            return {"status": "no_data"}
        
        # Prepare data for BRAIN
        nodes_data = [{"id": n.node_id, "type": n.node_type} for n in nodes]
        edges_data = []
        
        for e in edges:
            source = db.query(GraphNode).get(e.source_id)
            target = db.query(GraphNode).get(e.target_id)
            if source and target:
                edges_data.append({
                    "source": source.node_id,
                    "target": target.node_id,
                    "weight": e.weight
                })
        
        # Call BRAIN service synchronously
        request_data = {
            "nodes": nodes_data,
            "edges": edges_data,
            "damping": 0.85
        }
        
        result = call_brain_sync("/analyze/graph/pagerank", request_data)
        pagerank_results = result.get("nodes", [])
        
        # Update nodes
        updated = 0
        for pr in pagerank_results:
            node = db.query(GraphNode).filter(
                GraphNode.node_id == pr["id"]
            ).first()
            if node:
                node.pagerank = pr.get("pagerank", 0)
                updated += 1
        
        db.commit()
        
        logger.info(f"PageRank calculated for {updated} nodes")
        return {"status": "completed", "updated": updated}
        
    except Exception as e:
        logger.error(f"PageRank calculation error: {str(e)}")
        return {"status": "error", "message": str(e)}
    
    finally:
        db.close()
```

### trend_service.py
```python
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.services.base import BaseService
from app.services.brain_service import brain_service, BrainServiceError
from app.crud import trend as trend_crud
from app.crud import post as post_crud
from app.crud import analysis_result as result_crud
from app.models.post import Post
from app.schemas.trend import TrendCreate


class TrendService(BaseService):
    """Service for trend detection and management."""
    
    def __init__(self):
        super().__init__("TrendService")
    
    async def detect_trends(
        self,
        db: AsyncSession,
        *,
        hours: int = 24,
        min_count: int = 10,
        analysis_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Detect trends from recent posts."""
        # Get recent posts
        since = datetime.utcnow() - timedelta(hours=hours)
        
        query = (
            select(Post)
            .where(Post.posted_at >= since)
            .order_by(Post.posted_at.desc())
            .limit(10000)
        )
        result = await db.execute(query)
        posts = list(result.scalars().all())
        
        if not posts:
            return []
        
        posts_data = [
            {
                "id": p.id,
                "content": p.content,
                "posted_at": p.posted_at.isoformat() if p.posted_at else None,
                "hashtags": p.hashtags or [],
                "platform": p.platform
            }
            for p in posts
        ]
        
        try:
            # Use BRAIN service for trend detection
            trends = await brain_service.detect_trends(
                posts=posts_data,
                time_window="1h",
                min_trend_size=min_count
            )
            
            # Store detected trends
            stored_trends = []
            for trend_data in trends:
                trend_in = TrendCreate(
                    name=trend_data.get("name", "Unknown Trend"),
                    description=trend_data.get("description"),
                    volume=trend_data.get("volume", 0),
                    growth_rate=trend_data.get("growth_rate"),
                    velocity=trend_data.get("velocity"),
                    keywords=trend_data.get("keywords"),
                    hashtags=trend_data.get("hashtags"),
                    time_series=trend_data.get("time_series"),
                    analysis_id=analysis_id
                )
                
                stored_trend = await trend_crud.create(db, obj_in=trend_in)
                stored_trends.append(stored_trend)
            
            self.log_info(f"Detected and stored {len(stored_trends)} trends")
            return stored_trends
            
        except BrainServiceError as e:
            self.log_error(f"Trend detection failed: {e.message}")
            return await self._fallback_trend_detection(db, posts, min_count)
    
    async def _fallback_trend_detection(
        self,
        db: AsyncSession,
        posts: List[Post],
        min_count: int
    ) -> List[Dict[str, Any]]:
        """Fallback trend detection using hashtag counting."""
        hashtag_counts: Dict[str, int] = {}
        
        for post in posts:
            if post.hashtags:
                for hashtag in post.hashtags:
                    hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
        
        # Filter by min count
        trending = [
            (tag, count) for tag, count in hashtag_counts.items()
            if count >= min_count
        ]
        
        # Sort by count
        trending.sort(key=lambda x: x[1], reverse=True)
        
        # Create trend records
        trends = []
        for tag, count in trending[:20]:
            trend_in = TrendCreate(
                name=f"#{tag}",
                description=f"Trending hashtag with {count} mentions",
                volume=count,
                hashtags=[tag]
            )
            trend = await trend_crud.create(db, obj_in=trend_in)
            trends.append(trend)
        
        return trends
    
    async def get_trending_hashtags(
        self,
        db: AsyncSession,
        *,
        hours: int = 24,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get trending hashtags from recent posts."""
        since = datetime.utcnow() - timedelta(hours=hours)
        
        # Aggregate hashtags from posts
        query = (
            select(Post.hashtags)
            .where(
                Post.posted_at >= since,
                Post.hashtags.isnot(None)
            )
        )
        result = await db.execute(query)
        
        hashtag_counts: Dict[str, int] = {}
        for row in result.all():
            hashtags = row[0] or []
            for tag in hashtags:
                hashtag_counts[tag] = hashtag_counts.get(tag, 0) + 1
        
        # Sort and limit
        sorted_tags = sorted(
            hashtag_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        return [
            {"hashtag": tag, "count": count}
            for tag, count in sorted_tags
        ]
    
    async def get_trending_keywords(
        self,
        db: AsyncSession,
        *,
        hours: int = 24,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get trending keywords from analysis results."""
        since = datetime.utcnow() - timedelta(hours=hours)
        
        # Get recent analysis results
        from app.models.analysis_result import AnalysisResult
        
        query = (
            select(AnalysisResult.keywords)
            .where(
                AnalysisResult.created_at >= since,
                AnalysisResult.keywords.isnot(None)
            )
        )
        result = await db.execute(query)
        
        keyword_counts: Dict[str, int] = {}
        for row in result.all():
            keywords = row[0] or []
            for keyword in keywords:
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        sorted_keywords = sorted(
            keyword_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        return [
            {"keyword": keyword, "count": count}
            for keyword, count in sorted_keywords
        ]
    
    async def get_sentiment_trends(
        self,
        db: AsyncSession,
        *,
        hours: int = 24,
        interval: str = "1h"
    ) -> List[Dict[str, Any]]:
        """Get sentiment trends over time."""
        since = datetime.utcnow() - timedelta(hours=hours)
        
        from app.models.analysis_result import AnalysisResult
        
        query = (
            select(
                AnalysisResult.sentiment_label,
                AnalysisResult.created_at
            )
            .where(
                AnalysisResult.created_at >= since,
                AnalysisResult.sentiment_label.isnot(None)
            )
            .order_by(AnalysisResult.created_at.asc())
        )
        result = await db.execute(query)
        
        # Group by time intervals
        time_buckets: Dict[str, Dict[str, int]] = {}
        
        for row in result.all():
            sentiment = row[0]
            created_at = row[1]
            
            # Create bucket key based on interval
            if interval == "1h":
                bucket_key = created_at.strftime("%Y-%m-%d %H:00")
            elif interval == "1d":
                bucket_key = created_at.strftime("%Y-%m-%d")
            else:
                bucket_key = created_at.strftime("%Y-%m-%d %H:00")
            
            if bucket_key not in time_buckets:
                time_buckets[bucket_key] = {
                    "positive": 0,
                    "negative": 0,
                    "neutral": 0
                }
            
            if sentiment in time_buckets[bucket_key]:
                time_buckets[bucket_key][sentiment] += 1
        
        # Convert to list
        return [
            {
                "time": bucket_key,
                **counts
            }
            for bucket_key, counts in sorted(time_buckets.items())
        ]
    
    async def get_volume_trends(
        self,
        db: AsyncSession,
        *,
        hours: int = 24,
        interval: str = "1h",
        platform: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get post volume trends over time."""
        since = datetime.utcnow() - timedelta(hours=hours)
        
        query = (
            select(Post.posted_at, Post.platform)
            .where(
                Post.posted_at >= since,
                Post.posted_at.isnot(None)
            )
            .order_by(Post.posted_at.asc())
        )
        
        if platform:
            query = query.where(Post.platform == platform)
        
        result = await db.execute(query)
        
        time_buckets: Dict[str, int] = {}
        
        for row in result.all():
            posted_at = row[0]
            
            if interval == "1h":
                bucket_key = posted_at.strftime("%Y-%m-%d %H:00")
            elif interval == "1d":
                bucket_key = posted_at.strftime("%Y-%m-%d")
            else:
                bucket_key = posted_at.strftime("%Y-%m-%d %H:00")
            
            time_buckets[bucket_key] = time_buckets.get(bucket_key, 0) + 1
        
        return [
            {"time": bucket_key, "count": count}
            for bucket_key, count in sorted(time_buckets.items())
        ]
    
    async def update_trend_status(
        self,
        db: AsyncSession
    ) -> int:
        """Update status of existing trends based on recent activity."""
        active_trends = await trend_crud.get_active(db, limit=100)
        updated = 0
        
        for trend in active_trends:
            # Check if trend is still active
            if trend.hashtags:
                recent_count = 0
                for hashtag in trend.hashtags:
                    posts = await post_crud.get_by_hashtag(
                        db,
                        hashtag=hashtag,
                        limit=100
                    )
                    recent_count += len(posts)
                
                # If volume dropped significantly, mark as declining
                if recent_count < trend.volume * 0.3:
                    await trend_crud.update_status(
                        db,
                        trend_id=trend.id,
                        status="declining"
                    )
                    updated += 1
                elif recent_count < trend.volume * 0.1:
                    await trend_crud.update_status(
                        db,
                        trend_id=trend.id,
                        status="ended"
                    )
                    updated += 1
        
        return updated
    
    async def get_trend_summary(
        self,
        db: AsyncSession,
        *,
        hours: int = 24
    ) -> Dict[str, Any]:
        """Get summary of trending activity."""
        trending_hashtags = await self.get_trending_hashtags(
            db, hours=hours, limit=10
        )
        trending_keywords = await self.get_trending_keywords(
            db, hours=hours, limit=10
        )
        
        active_trends = await trend_crud.get_active(db, limit=10)
        top_growing = await trend_crud.get_top_by_growth(db, limit=5)
        
        stats = await trend_crud.get_stats(db)
        
        return {
            "trending_hashtags": trending_hashtags,
            "trending_keywords": trending_keywords,
            "active_trends": [
                {
                    "id": t.id,
                    "name": t.name,
                    "volume": t.volume,
                    "growth_rate": t.growth_rate
                }
                for t in active_trends
            ],
            "top_growing": [
                {
                    "id": t.id,
                    "name": t.name,
                    "growth_rate": t.growth_rate
                }
                for t in top_growing
            ],
            "stats": stats
        }


# Create singleton instance
trend_service = TrendService()
```

## Core
### config.py
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List
import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    APP_NAME: str = "Persian Social Analytics"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    API_V1_PREFIX: str = "/api/v1"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/persian_analytics"
    DATABASE_SYNC_URL: str = "postgresql://postgres:postgres@localhost:5432/persian_analytics"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # BRAIN Service
    BRAIN_SERVICE_URL: str = "http://localhost:8001"
    BRAIN_SERVICE_TIMEOUT: int = 300
    
    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Default Admin User (created on startup)
    DEFAULT_ADMIN_EMAIL: str = "admin@example.com"
    DEFAULT_ADMIN_USERNAME: str = "admin"
    DEFAULT_ADMIN_PASSWORD: str = "Admin123!"
    
    # Auto-initialization
    AUTO_INIT_DB: bool = True
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [origin.strip() for origin in v.split(",")]
        return v


# Create global settings instance
settings = Settings()
```

### init_data.py
```python
"""
Initial data setup - runs on application startup.
Creates default admin user, data sources, etc.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from app.core.config import settings
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.models.data_source import DataSource


async def init_default_admin(db: AsyncSession) -> None:
    """Create default admin user if not exists."""
    
    # Check if admin exists
    result = await db.execute(
        select(User).where(User.username == settings.DEFAULT_ADMIN_USERNAME)
    )
    existing_admin = result.scalar_one_or_none()
    
    if existing_admin:
        logger.info(f"Admin user '{settings.DEFAULT_ADMIN_USERNAME}' already exists")
        return
    
    # Create admin user
    admin_user = User(
        email=settings.DEFAULT_ADMIN_EMAIL,
        username=settings.DEFAULT_ADMIN_USERNAME,
        hashed_password=hash_password(settings.DEFAULT_ADMIN_PASSWORD),
        full_name="System Administrator",
        is_active=True,
        is_superuser=True,
        role=UserRole.ADMIN
    )
    
    db.add(admin_user)
    await db.commit()
    
    logger.info(f"✅ Created default admin user: {settings.DEFAULT_ADMIN_USERNAME}")


async def init_default_data_sources(db: AsyncSession) -> None:
    """Create default data sources if not exist."""
    
    default_sources = [
        {
            "name": "Twitter Persian",
            "platform": "twitter",
            "description": "Persian Twitter/X data collection",
            "is_active": True
        },
        {
            "name": "Instagram Persian",
            "platform": "instagram",
            "description": "Persian Instagram data collection",
            "is_active": True
        },
        {
            "name": "Telegram Persian",
            "platform": "telegram",
            "description": "Persian Telegram channels and groups",
            "is_active": True
        }
    ]
    
    for source_data in default_sources:
        result = await db.execute(
            select(DataSource).where(
                DataSource.name == source_data["name"]
            )
        )
        existing = result.scalar_one_or_none()
        
        if not existing:
            source = DataSource(**source_data)
            db.add(source)
            logger.info(f"✅ Created data source: {source_data['name']}")
    
    await db.commit()


async def init_db_data(db: AsyncSession) -> None:
    """Initialize all default data."""
    logger.info("🔧 Initializing default data...")
    
    try:
        await init_default_admin(db)
        await init_default_data_sources(db)
        logger.info("✅ Default data initialization complete!")
    except Exception as e:
        logger.error(f"❌ Error initializing default data: {e}")
        raise
```

### security.py
```python
from datetime import datetime, timedelta, timezone
from typing import Optional, Any
import bcrypt
from jose import jwt, JWTError
from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    try:
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def create_access_token(
    subject: str | Any,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT access token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access"
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    subject: str | Any,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create JWT refresh token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh"
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Decode and verify JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None
```

## Main Files
### main.py
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
import redis.asyncio as redis
from loguru import logger
import sys

from app.core.config import settings
from app.database import init_db, close_db, AsyncSessionLocal
from app.api.v1.router import api_router


# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG" if settings.DEBUG else "INFO"
)


# Redis client (global)
redis_client: redis.Redis = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global redis_client
    
    logger.info("🚀 Starting up Persian Social Analytics API...")
    
    # Initialize database tables
    try:
        await init_db()
        logger.info("✅ Database tables initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
    
    # Auto-initialize default data (admin user, data sources, etc.)
    if settings.AUTO_INIT_DB:
        try:
            from app.core.init_data import init_db_data
            async with AsyncSessionLocal() as session:
                await init_db_data(session)
        except Exception as e:
            logger.error(f"❌ Default data initialization failed: {e}")
    
    # Initialize Redis
    try:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
        await redis_client.ping()
        logger.info("✅ Redis connected successfully")
    except Exception as e:
        logger.error(f"❌ Redis connection failed: {e}")
        redis_client = None
    
    logger.info("✅ Application startup complete!")
    logger.info(f"   API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    logger.info(f"   Admin User: {settings.DEFAULT_ADMIN_USERNAME}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    
    if redis_client:
        await redis_client.close()
        logger.info("Redis connection closed")
    
    await close_db()
    logger.info("Database connection closed")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Persian Social Media Analysis System API",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for Docker and load balancers."""
    health_status = {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
    
    # Check Redis
    global redis_client
    if redis_client:
        try:
            await redis_client.ping()
            health_status["redis"] = "connected"
        except Exception:
            health_status["redis"] = "disconnected"
    else:
        health_status["redis"] = "not configured"
    
    return health_status


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Persian Social Analytics API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "api": settings.API_V1_PREFIX,
    }


# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    logger.debug(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.debug(f"Response: {response.status_code}")
    return response
```

### database.py
```python
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from app.core.config import settings

# Async engine for FastAPI
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Sync engine for Alembic migrations
sync_engine = create_engine(
    settings.DATABASE_SYNC_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

# Base class for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Dependency for getting async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database tables."""
    # Import models to ensure they are registered with Base
    from app.models import (
        User, DataSource, Author, Post,
        Analysis, AnalysisResult, Trend,
        GraphNode, GraphEdge, Dashboard
    )
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Close database connections."""
    await async_engine.dispose()
```

## BRAIN Service
### main.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
from loguru import logger
import sys

from app.config import settings
from app.routers import analysis_router, graph_router, batch_router


# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level="DEBUG" if settings.DEBUG else "INFO"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("🧠 BRAIN Mock Service starting...")
    logger.info(f"   Version: {settings.APP_VERSION}")
    logger.info(f"   Debug: {settings.DEBUG}")
    logger.info(f"   GPU Simulation: {settings.SIMULATE_GPU}")
    logger.info("🚀 BRAIN Mock Service ready!")
    
    yield
    
    logger.info("🧠 BRAIN Mock Service shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Mock BRAIN Service for Persian Social Media Analysis (Development)",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "gpu_available": settings.SIMULATE_GPU,
        "gpu_memory_used": 2048 if settings.SIMULATE_GPU else None,
        "gpu_memory_total": 8192 if settings.SIMULATE_GPU else None,
        "mode": "mock"
    }


# Root
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health",
        "mode": "mock",
        "message": "This is a MOCK service. Replace with real BRAIN for production."
    }


# Include routers
app.include_router(analysis_router)
app.include_router(graph_router)
app.include_router(batch_router)


# Trend detection endpoint (at root level to match backend expectations)
@app.post("/analyze/trends", tags=["Analysis"])
async def analyze_trends(posts: list, time_window: str = "1h", min_trend_size: int = 10):
    """Detect trends endpoint at root level."""
    from app.mock_data import generate_trend_detection
    trends = generate_trend_detection(posts)
    return {"trends": trends}
```

### config.py
```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """BRAIN Mock Service Settings"""
    
    APP_NAME: str = "BRAIN Mock Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    
    # Simulate processing delay (seconds)
    MOCK_DELAY_MIN: float = 0.1
    MOCK_DELAY_MAX: float = 0.5
    
    # GPU simulation
    SIMULATE_GPU: bool = True
    
    class Config:
        env_file = ".env"


settings = Settings()
```

### mock_data.py
```python
"""
Enhanced Persian Mock Data Generator
Generates realistic NLP analysis results for Persian text.
"""

import random
import re
from typing import List, Dict, Any, Optional


# ============================================
# Persian Word Lists
# ============================================

# Positive words for sentiment detection
POSITIVE_WORDS = [
    "عالی", "خوب", "زیبا", "قشنگ", "فوق‌العاده", "عشق", "دوست", "خوشحال",
    "موفق", "بهترین", "شگفت‌انگیز", "لذت", "سپاس", "ممنون", "مثبت",
    "امید", "پیروز", "برنده", "خوش", "مبارک", "تبریک", "افتخار",
    "عالیه", "خوبه", "دوستت", "عاشق", "محشر", "باحال", "توپ"
]

# Negative words for sentiment detection
NEGATIVE_WORDS = [
    "بد", "زشت", "افتضاح", "وحشتناک", "غم", "ناراحت", "شکست",
    "بدترین", "متنفر", "نفرت", "خسته", "گرانی", "مشکل", "سخت",
    "درد", "رنج", "ناامید", "بیچاره", "فقر", "جنگ", "مرگ",
    "بده", "گرون", "داغون", "خراب", "ضعیف", "بیکار", "ترافیک"
]

# Emotion-specific words
EMOTION_WORDS = {
    "joy": ["خوشحال", "شاد", "لذت", "خنده", "جشن", "مبارک", "عید", "خوش"],
    "sadness": ["غم", "ناراحت", "گریه", "اشک", "تنها", "دلتنگ", "افسرده", "غصه"],
    "anger": ["عصبانی", "خشم", "جنگ", "دعوا", "متنفر", "نفرت", "لعنت", "کثیف"],
    "fear": ["ترس", "وحشت", "نگران", "خطر", "تهدید", "فرار", "وحشتناک", "خوف"],
    "surprise": ["عجیب", "شگفت", "باورنکردنی", "ناگهان", "غیرمنتظره", "وای", "چه"],
    "disgust": ["چندش", "نفرت‌انگیز", "زشت", "کثیف", "بد", "متعفن", "حال‌بهم‌زن"]
}

# Common Persian keywords by category
KEYWORDS_BY_CATEGORY = {
    "سیاست": ["سیاست", "دولت", "مجلس", "رئیس‌جمهور", "انتخابات", "قانون", "وزیر"],
    "اقتصاد": ["اقتصاد", "قیمت", "گرانی", "دلار", "بورس", "تورم", "بازار", "کار"],
    "ورزش": ["فوتبال", "ورزش", "تیم", "بازی", "گل", "برد", "باخت", "قهرمان"],
    "تکنولوژی": ["تکنولوژی", "اینترنت", "موبایل", "کامپیوتر", "هوش مصنوعی", "اپلیکیشن"],
    "فرهنگ": ["فرهنگ", "هنر", "موسیقی", "فیلم", "کتاب", "شعر", "سینما", "تئاتر"],
    "اجتماعی": ["مردم", "جامعه", "خانواده", "دوست", "عشق", "زندگی", "روابط"],
    "گردشگری": ["سفر", "گردشگری", "هتل", "پرواز", "تعطیلات", "طبیعت", "دریا", "کوه"],
    "غذا": ["غذا", "رستوران", "آشپزی", "چلوکباب", "پیتزا", "قهوه", "چای"],
    "آموزش": ["دانشگاه", "مدرسه", "درس", "امتحان", "استاد", "دانشجو", "تحصیل"],
    "سلامت": ["سلامت", "بیماری", "دکتر", "بیمارستان", "دارو", "کرونا", "واکسن"]
}

# Persian named entities
ENTITIES_DB = {
    "location": [
        "تهران", "مشهد", "اصفهان", "شیراز", "تبریز", "کرج", "قم",
        "ایران", "ترکیه", "دبی", "آلمان", "کانادا", "آمریکا",
        "دربند", "درکه", "کیش", "قشم", "شمال", "جنوب"
    ],
    "person": [
        "علی", "محمد", "حسین", "رضا", "امیر", "فاطمه", "زهرا", "مریم",
        "شجریان", "فردوسی", "حافظ", "سعدی", "مولانا"
    ],
    "organization": [
        "دانشگاه تهران", "دانشگاه شریف", "صدا و سیما", "بانک ملی",
        "ایران خودرو", "سایپا", "دیجی‌کالا", "اسنپ", "تپسی"
    ],
    "event": [
        "نوروز", "عید", "یلدا", "چهارشنبه‌سوری", "سیزده‌بدر",
        "جام جهانی", "المپیک", "لیگ برتر"
    ],
    "product": [
        "آیفون", "سامسونگ", "پراید", "پژو", "تسلا"
    ]
}

# Persian topics
TOPICS_LIST = [
    {"name": "سیاست", "keywords": ["دولت", "مجلس", "انتخابات", "قانون"]},
    {"name": "اقتصاد", "keywords": ["قیمت", "دلار", "بورس", "تورم"]},
    {"name": "ورزش", "keywords": ["فوتبال", "تیم", "بازی", "قهرمان"]},
    {"name": "فرهنگ و هنر", "keywords": ["موسیقی", "فیلم", "کتاب", "سینما"]},
    {"name": "اجتماعی", "keywords": ["مردم", "جامعه", "خانواده", "زندگی"]},
    {"name": "تکنولوژی", "keywords": ["اینترنت", "موبایل", "هوش مصنوعی"]},
    {"name": "سلامت", "keywords": ["بیماری", "دکتر", "دارو", "سلامت"]},
    {"name": "آموزش", "keywords": ["دانشگاه", "مدرسه", "درس", "تحصیل"]},
    {"name": "گردشگری", "keywords": ["سفر", "هتل", "گردشگری", "طبیعت"]},
    {"name": "آشپزی", "keywords": ["غذا", "رستوران", "آشپزی", "دستور"]}
]

# Summary templates
SUMMARY_TEMPLATES = {
    "positive": [
        "این متن نگرش مثبتی نسبت به {topic} دارد.",
        "نویسنده رضایت خود را از {topic} ابراز کرده است.",
        "محتوا حاوی دیدگاه مثبت درباره {topic} است.",
        "در این پست، {topic} مورد تحسین قرار گرفته است."
    ],
    "negative": [
        "این متن انتقادی نسبت به {topic} است.",
        "نویسنده نارضایتی خود را از {topic} بیان کرده است.",
        "محتوا حاوی انتقاد از {topic} است.",
        "در این پست، نگرانی درباره {topic} مطرح شده است."
    ],
    "neutral": [
        "این متن اطلاعاتی درباره {topic} ارائه می‌دهد.",
        "محتوا به صورت خنثی درباره {topic} صحبت می‌کند.",
        "نویسنده بدون قضاوت درباره {topic} نوشته است.",
        "این پست شامل اطلاعات عمومی درباره {topic} است."
    ]
}


# ============================================
# Text Analysis Functions
# ============================================

def analyze_text_content(text: str) -> Dict[str, Any]:
    """Analyze Persian text to extract features."""
    text_lower = text.lower() if text else ""
    
    # Count positive/negative words
    positive_count = sum(1 for word in POSITIVE_WORDS if word in text)
    negative_count = sum(1 for word in NEGATIVE_WORDS if word in text)
    
    # Detect emotions
    emotion_scores = {}
    for emotion, words in EMOTION_WORDS.items():
        score = sum(1 for word in words if word in text)
        emotion_scores[emotion] = score
    
    # Detect category
    category_scores = {}
    for category, keywords in KEYWORDS_BY_CATEGORY.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            category_scores[category] = score
    
    # Find entities in text
    found_entities = []
    for entity_type, entities in ENTITIES_DB.items():
        for entity in entities:
            if entity in text:
                found_entities.append({"text": entity, "type": entity_type})
    
    # Extract hashtags
    hashtags = re.findall(r'#([\u0600-\u06FF\w]+)', text)
    
    return {
        "positive_count": positive_count,
        "negative_count": negative_count,
        "emotion_scores": emotion_scores,
        "category_scores": category_scores,
        "found_entities": found_entities,
        "hashtags": hashtags,
        "text_length": len(text)
    }


def generate_sentiment(text: str = "") -> Dict[str, Any]:
    """Generate sentiment based on text analysis."""
    analysis = analyze_text_content(text)
    
    positive = analysis["positive_count"]
    negative = analysis["negative_count"]
    
    # Determine sentiment
    if positive > negative:
        label = "positive"
        base_score = 0.3 + min(positive * 0.15, 0.6)
    elif negative > positive:
        label = "negative"
        base_score = -0.3 - min(negative * 0.15, 0.6)
    else:
        label = "neutral"
        base_score = random.uniform(-0.2, 0.2)
    
    # Add some randomness
    score = base_score + random.uniform(-0.1, 0.1)
    score = max(-1.0, min(1.0, score))
    
    confidence = 0.7 + min((positive + negative) * 0.05, 0.25)
    confidence += random.uniform(-0.05, 0.05)
    confidence = max(0.5, min(0.99, confidence))
    
    return {
        "label": label,
        "score": round(score, 4),
        "confidence": round(confidence, 4)
    }


def generate_emotions(text: str = "") -> Dict[str, float]:
    """Generate emotion scores based on text analysis."""
    analysis = analyze_text_content(text)
    emotion_hints = analysis["emotion_scores"]
    
    emotions = {}
    total_hints = sum(emotion_hints.values()) or 1
    remaining = 1.0
    
    # Base emotions on detected words
    emotion_names = ["joy", "sadness", "anger", "fear", "surprise", "disgust"]
    
    for i, emotion in enumerate(emotion_names):
        if i == len(emotion_names) - 1:
            emotions[emotion] = round(remaining, 4)
        else:
            hint_weight = emotion_hints.get(emotion, 0) / total_hints
            base = 0.1 + hint_weight * 0.4
            value = base + random.uniform(0, 0.15)
            value = min(value, remaining - 0.05 * (len(emotion_names) - i - 1))
            emotions[emotion] = round(value, 4)
            remaining -= value
    
    return emotions


def generate_keywords(text: str = "", count: int = 5) -> List[str]:
    """Extract keywords based on text content."""
    analysis = analyze_text_content(text)
    keywords = []
    
    # Add hashtags as keywords
    keywords.extend(analysis["hashtags"][:3])
    
    # Add keywords from detected categories
    for category, score in sorted(analysis["category_scores"].items(), key=lambda x: -x[1]):
        if len(keywords) >= count:
            break
        for kw in KEYWORDS_BY_CATEGORY[category]:
            if kw in text and kw not in keywords:
                keywords.append(kw)
                if len(keywords) >= count:
                    break
    
    # Fill with random keywords if needed
    if len(keywords) < count:
        all_keywords = [kw for kws in KEYWORDS_BY_CATEGORY.values() for kw in kws]
        remaining = count - len(keywords)
        keywords.extend(random.sample(all_keywords, min(remaining, len(all_keywords))))
    
    return keywords[:count]


def generate_entities(text: str = "") -> List[Dict[str, Any]]:
    """Extract named entities from text."""
    analysis = analyze_text_content(text)
    entities = []
    
    for entity_info in analysis["found_entities"]:
        entity_text = entity_info["text"]
        start_pos = text.find(entity_text) if text else 0
        
        entities.append({
            "text": entity_text,
            "type": entity_info["type"],
            "start": start_pos,
            "end": start_pos + len(entity_text),
            "confidence": round(random.uniform(0.85, 0.99), 4)
        })
    
    # Add some random entities if none found
    if not entities and random.random() > 0.3:
        entity_type = random.choice(list(ENTITIES_DB.keys()))
        entity_text = random.choice(ENTITIES_DB[entity_type])
        entities.append({
            "text": entity_text,
            "type": entity_type,
            "start": 0,
            "end": len(entity_text),
            "confidence": round(random.uniform(0.75, 0.95), 4)
        })
    
    return entities


def generate_topics(text: str = "", count: int = 3) -> List[Dict[str, Any]]:
    """Detect topics in text."""
    analysis = analyze_text_content(text)
    topics = []
    
    # Score topics based on keyword matches
    topic_scores = []
    for topic in TOPICS_LIST:
        score = sum(1 for kw in topic["keywords"] if kw in text)
        if score > 0:
            topic_scores.append((topic, score))
    
    # Sort by score
    topic_scores.sort(key=lambda x: -x[1])
    
    # Add matched topics
    for topic, score in topic_scores[:count]:
        topics.append({
            "topic": topic["name"],
            "score": round(0.5 + score * 0.15 + random.uniform(0, 0.2), 4),
            "keywords": topic["keywords"][:3]
        })
    
    # Fill with random topics if needed
    if len(topics) < count:
        remaining_topics = [t for t in TOPICS_LIST if t["name"] not in [x["topic"] for x in topics]]
        for topic in random.sample(remaining_topics, min(count - len(topics), len(remaining_topics))):
            topics.append({
                "topic": topic["name"],
                "score": round(random.uniform(0.3, 0.6), 4),
                "keywords": topic["keywords"][:3]
            })
    
    return sorted(topics, key=lambda x: -x["score"])


def generate_summary(text: str = "") -> str:
    """Generate a summary based on text content."""
    sentiment = generate_sentiment(text)
    analysis = analyze_text_content(text)
    
    # Find main topic
    topic = "این موضوع"
    if analysis["category_scores"]:
        main_category = max(analysis["category_scores"], key=analysis["category_scores"].get)
        topic = main_category
    elif analysis["hashtags"]:
        topic = analysis["hashtags"][0]
    
    # Select template based on sentiment
    templates = SUMMARY_TEMPLATES.get(sentiment["label"], SUMMARY_TEMPLATES["neutral"])
    template = random.choice(templates)
    
    return template.format(topic=topic)


def generate_full_analysis(text_id: str, text: str = "") -> Dict[str, Any]:
    """Generate complete analysis for a text."""
    emotions = generate_emotions(text)
    
    return {
        "text_id": text_id,
        "sentiment": generate_sentiment(text),
        "emotions": emotions,
        "dominant_emotion": max(emotions, key=emotions.get),
        "keywords": generate_keywords(text, random.randint(4, 8)),
        "entities": generate_entities(text),
        "topics": generate_topics(text, random.randint(1, 3)),
        "summary": generate_summary(text)
    }


# ============================================
# Graph Analysis Functions
# ============================================

def generate_pagerank_scores(nodes: List[Dict]) -> List[Dict[str, Any]]:
    """Generate PageRank scores for nodes."""
    results = []
    total_nodes = len(nodes)
    
    for i, node in enumerate(nodes):
        # Higher scores for earlier nodes (simulating importance)
        base_rank = 1.0 / total_nodes
        variance = random.uniform(0.5, 2.0)
        pagerank = base_rank * variance
        
        results.append({
            "id": node.get("id"),
            "type": node.get("type", "unknown"),
            "pagerank": round(pagerank, 6),
            "degree": random.randint(1, min(50, total_nodes)),
            "in_degree": random.randint(0, 30),
            "out_degree": random.randint(0, 30)
        })
    
    # Normalize PageRank
    total = sum(r["pagerank"] for r in results)
    for r in results:
        r["pagerank"] = round(r["pagerank"] / total, 6)
    
    # Sort by pagerank
    results.sort(key=lambda x: x["pagerank"], reverse=True)
    return results


def generate_communities(nodes: List[Dict]) -> Dict[str, Any]:
    """Generate community detection results."""
    num_nodes = len(nodes)
    num_communities = max(1, min(num_nodes // 5, 10))
    
    communities = []
    for i in range(num_communities):
        size = random.randint(max(1, num_nodes // num_communities - 2), 
                             num_nodes // num_communities + 3)
        communities.append({
            "community_id": i,
            "size": size,
            "density": round(random.uniform(0.2, 0.8), 4),
            "keywords": random.sample(
                [kw for kws in KEYWORDS_BY_CATEGORY.values() for kw in kws], 
                min(3, len([kw for kws in KEYWORDS_BY_CATEGORY.values() for kw in kws]))
            )
        })
    
    # Assign nodes to communities
    node_results = []
    for node in nodes:
        node_results.append({
            "id": node.get("id"),
            "community_id": random.randint(0, num_communities - 1)
        })
    
    return {
        "communities": communities,
        "nodes": node_results,
        "modularity": round(random.uniform(0.3, 0.8), 4),
        "num_communities": num_communities
    }


def generate_trend_detection(posts: List[Dict]) -> List[Dict[str, Any]]:
    """Generate trend detection results."""
    # Collect all hashtags from posts
    hashtag_counts = {}
    for post in posts:
        content = post.get("content", "")
        hashtags = re.findall(r'#([\u0600-\u06FF\w]+)', content)
        for tag in hashtags:
            hashtag_counts[tag] = hashtag_counts.get(tag, 0) + 1
    
    # Also add hashtags from hashtags field
    for post in posts:
        for tag in post.get("hashtags", []):
            hashtag_counts[tag] = hashtag_counts.get(tag, 0) + 1
    
    # Generate trends
    trends = []
    sorted_hashtags = sorted(hashtag_counts.items(), key=lambda x: -x[1])
    
    for tag, count in sorted_hashtags[:10]:
        trends.append({
            "name": f"#{tag}",
            "volume": count * random.randint(5, 20),
            "growth_rate": round(random.uniform(-0.3, 2.5), 4),
            "velocity": round(random.uniform(0.1, 1.0), 4),
            "sentiment": generate_sentiment(tag),
            "keywords": [tag] + random.sample(
                [kw for kws in KEYWORDS_BY_CATEGORY.values() for kw in kws],
                min(2, 5)
            )
        })
    
    # Add some predefined trends if none found
    if not trends:
        predefined = ["تهران", "ایران", "فوتبال", "سیاست", "اقتصاد"]
        for tag in random.sample(predefined, 3):
            trends.append({
                "name": f"#{tag}",
                "volume": random.randint(50, 500),
                "growth_rate": round(random.uniform(0.5, 2.0), 4),
                "velocity": round(random.uniform(0.3, 0.9), 4),
                "sentiment": generate_sentiment(tag),
                "keywords": [tag]
            })
    
    return sorted(trends, key=lambda x: x["volume"], reverse=True)
```

### routers/analysis.py
```python
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import random

from app.config import settings
from app.mock_data import (
    generate_sentiment,
    generate_emotions,
    generate_keywords,
    generate_entities,
    generate_topics,
    generate_summary,
    generate_full_analysis
)

router = APIRouter(prefix="/analyze", tags=["Analysis"])


class TextAnalysisRequest(BaseModel):
    texts: List[str]
    text_ids: Optional[List[str]] = None
    analysis_types: List[str] = ["sentiment", "emotion", "keywords"]
    language: str = "fa"
    config: Optional[Dict[str, Any]] = None


class SentimentRequest(BaseModel):
    texts: List[str]
    text_ids: Optional[List[str]] = None
    language: str = "fa"


class SummarizationRequest(BaseModel):
    texts: List[str]
    max_length: int = 150
    min_length: int = 30
    language: str = "fa"


class KeywordRequest(BaseModel):
    texts: List[str]
    max_keywords: int = 10
    language: str = "fa"


class EntityRequest(BaseModel):
    texts: List[str]
    language: str = "fa"


class TopicRequest(BaseModel):
    texts: List[str]
    num_topics: int = 10
    language: str = "fa"


async def simulate_delay():
    """Simulate processing time."""
    delay = random.uniform(settings.MOCK_DELAY_MIN, settings.MOCK_DELAY_MAX)
    await asyncio.sleep(delay)


@router.post("/sentiment")
async def analyze_sentiment(request: SentimentRequest):
    """Analyze sentiment of texts."""
    await simulate_delay()
    
    text_ids = request.text_ids or [str(i) for i in range(len(request.texts))]
    
    results = []
    for i, text in enumerate(request.texts):
        results.append({
            "text_id": text_ids[i],
            "sentiment": generate_sentiment(text)  # Pass text for analysis
        })
    
    return {"results": results}


@router.post("/emotion")
async def analyze_emotions(request: SentimentRequest):
    """Analyze emotions in texts."""
    await simulate_delay()
    
    text_ids = request.text_ids or [str(i) for i in range(len(request.texts))]
    
    results = []
    for i, text in enumerate(request.texts):
        emotions = generate_emotions(text)  # Pass text for analysis
        results.append({
            "text_id": text_ids[i],
            "emotions": emotions,
            "dominant_emotion": max(emotions, key=emotions.get)
        })
    
    return {"results": results}


@router.post("/text")
async def analyze_text(request: TextAnalysisRequest):
    """Full text analysis."""
    await simulate_delay()
    
    text_ids = request.text_ids or [str(i) for i in range(len(request.texts))]
    
    results = []
    for i, text in enumerate(request.texts):
        result = {"text_id": text_ids[i]}
        
        if "sentiment" in request.analysis_types:
            result["sentiment"] = generate_sentiment(text)
        
        if "emotion" in request.analysis_types:
            emotions = generate_emotions(text)
            result["emotions"] = emotions
            result["dominant_emotion"] = max(emotions, key=emotions.get)
        
        if "keywords" in request.analysis_types:
            result["keywords"] = generate_keywords(text)
        
        if "entities" in request.analysis_types:
            result["entities"] = generate_entities(text)
        
        if "topics" in request.analysis_types:
            result["topics"] = generate_topics(text)
        
        if "summary" in request.analysis_types:
            result["summary"] = generate_summary(text)
        
        results.append(result)
    
    return {"results": results}


@router.post("/summarize")
async def summarize_texts(request: SummarizationRequest):
    """Summarize texts."""
    await simulate_delay()
    
    summaries = [generate_summary(text) for text in request.texts]
    
    return {"summaries": summaries}


@router.post("/keywords")
async def extract_keywords(request: KeywordRequest):
    """Extract keywords from texts."""
    await simulate_delay()
    
    keywords = [
        generate_keywords(text, request.max_keywords) 
        for text in request.texts
    ]
    
    return {"keywords": keywords}


@router.post("/entities")
async def extract_entities(request: EntityRequest):
    """Extract named entities from texts."""
    await simulate_delay()
    
    entities = [generate_entities(text) for text in request.texts]
    
    return {"entities": entities}


@router.post("/topics")
async def detect_topics(request: TopicRequest):
    """Detect topics in texts."""
    await simulate_delay()
    
    # Global topics from all texts
    all_text = " ".join(request.texts)
    global_topics = generate_topics(all_text, request.num_topics)
    
    # Topic distribution per document
    doc_topics = [generate_topics(text, 3) for text in request.texts]
    
    return {
        "global_topics": global_topics,
        "document_topics": doc_topics
    }
```

### routers/batch.py
```python
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import uuid
import random

from app.config import settings
from app.mock_data import generate_full_analysis, generate_trend_detection

router = APIRouter(prefix="/batch", tags=["Batch Processing"])

# In-memory storage for batch jobs (use Redis in production)
batch_jobs: Dict[str, Dict[str, Any]] = {}


class BatchAnalysisRequest(BaseModel):
    analysis_id: int
    posts: List[Dict[str, Any]]
    config: Dict[str, Any]
    callback_url: Optional[str] = None


class TrendDetectionRequest(BaseModel):
    posts: List[Dict[str, Any]]
    time_field: str = "posted_at"
    content_field: str = "content"
    min_trend_size: int = 10
    time_window: str = "1h"


async def process_batch_job(task_id: str, request: BatchAnalysisRequest):
    """Background task to process batch analysis."""
    batch_jobs[task_id]["status"] = "processing"
    batch_jobs[task_id]["progress"] = 0
    
    results = []
    total = len(request.posts)
    
    for i, post in enumerate(request.posts):
        # Simulate processing delay
        await asyncio.sleep(random.uniform(0.01, 0.05))
        
        post_id = str(post.get("id", i))
        content = post.get("content", "")
        
        result = generate_full_analysis(post_id, content)
        results.append(result)
        
        # Update progress
        batch_jobs[task_id]["progress"] = int(((i + 1) / total) * 100)
    
    batch_jobs[task_id]["status"] = "completed"
    batch_jobs[task_id]["progress"] = 100
    batch_jobs[task_id]["results"] = results


@router.post("/analyze")
async def submit_batch_analysis(
    request: BatchAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """Submit batch analysis job."""
    task_id = str(uuid.uuid4())
    
    batch_jobs[task_id] = {
        "task_id": task_id,
        "analysis_id": request.analysis_id,
        "status": "queued",
        "progress": 0,
        "total_posts": len(request.posts),
        "results": None
    }
    
    # Start background processing
    background_tasks.add_task(process_batch_job, task_id, request)
    
    return {
        "analysis_id": request.analysis_id,
        "task_id": task_id,
        "status": "queued",
        "message": f"Batch job queued for {len(request.posts)} posts"
    }


@router.get("/status/{task_id}")
async def get_batch_status(task_id: str):
    """Get batch job status."""
    if task_id not in batch_jobs:
        return {"error": "Task not found", "task_id": task_id}
    
    job = batch_jobs[task_id]
    
    return {
        "task_id": task_id,
        "status": job["status"],
        "progress": job["progress"],
        "total_posts": job["total_posts"]
    }


@router.get("/result/{task_id}")
async def get_batch_result(task_id: str):
    """Get batch job results."""
    if task_id not in batch_jobs:
        return {"error": "Task not found", "task_id": task_id}
    
    job = batch_jobs[task_id]
    
    if job["status"] != "completed":
        return {
            "task_id": task_id,
            "status": job["status"],
            "message": "Job not completed yet"
        }
    
    return {
        "task_id": task_id,
        "status": "completed",
        "results": job["results"]
    }


@router.post("/trends")
async def detect_trends(request: TrendDetectionRequest):
    """Detect trends from posts."""
    await asyncio.sleep(random.uniform(0.1, 0.3))
    
    trends = generate_trend_detection(request.posts)
    
    return {"trends": trends}
```

### routers/graph.py
```python
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import random

from app.config import settings
from app.mock_data import generate_pagerank_scores, generate_communities

router = APIRouter(prefix="/analyze/graph", tags=["Graph Analysis"])


class GraphAnalysisRequest(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    algorithms: List[str] = ["pagerank", "community_detection"]
    config: Optional[Dict[str, Any]] = None


class PageRankRequest(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    damping: float = 0.85


class CommunityRequest(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]


async def simulate_delay():
    """Simulate processing time."""
    delay = random.uniform(settings.MOCK_DELAY_MIN, settings.MOCK_DELAY_MAX)
    await asyncio.sleep(delay)


@router.post("")
async def analyze_graph(request: GraphAnalysisRequest):
    """Full graph analysis."""
    await simulate_delay()
    
    result = {
        "node_count": len(request.nodes),
        "edge_count": len(request.edges)
    }
    
    if "pagerank" in request.algorithms:
        result["pagerank"] = generate_pagerank_scores(request.nodes)
    
    if "community_detection" in request.algorithms:
        result["communities"] = generate_communities(request.nodes)
    
    if "centrality" in request.algorithms:
        result["centrality"] = generate_pagerank_scores(request.nodes)
    
    return result


@router.post("/pagerank")
async def calculate_pagerank(request: PageRankRequest):
    """Calculate PageRank scores."""
    await simulate_delay()
    
    nodes = generate_pagerank_scores(request.nodes)
    
    return {
        "nodes": nodes,
        "damping": request.damping,
        "iterations": random.randint(10, 50)
    }


@router.post("/communities")
async def detect_communities(request: CommunityRequest):
    """Detect communities in graph."""
    await simulate_delay()
    
    result = generate_communities(request.nodes)
    
    return result


@router.post("/centrality")
async def calculate_centrality(request: GraphAnalysisRequest):
    """Calculate various centrality metrics."""
    await simulate_delay()
    
    results = []
    for node in request.nodes:
        results.append({
            "id": node.get("id"),
            "degree_centrality": round(random.uniform(0, 1), 4),
            "betweenness_centrality": round(random.uniform(0, 1), 4),
            "closeness_centrality": round(random.uniform(0, 1), 4),
            "eigenvector_centrality": round(random.uniform(0, 1), 4)
        })
    
    return {"nodes": results}
```

## Docker
### backend/docker-compose.yml
```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: sma_postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: persian_analytics
    volumes:
      - ../data/postgres:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - sma_network

  redis:
    image: redis:7-alpine
    container_name: sma_redis
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - ../data/redis:/data
    ports:
      - "6380:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - sma_network

  backend:
    build: .
    image: sma_backend:latest
    container_name: sma_backend
    restart: unless-stopped
    environment:
      - APP_NAME=Persian Social Analytics
      - DEBUG=True
      - SECRET_KEY=your-super-secret-key-change-this-in-production
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/persian_analytics
      - DATABASE_SYNC_URL=postgresql://postgres:postgres@postgres:5432/persian_analytics
      - REDIS_URL=redis://redis:6379/0
      - BRAIN_SERVICE_URL=http://sma_brain:8001
      - CELERY_BROKER_URL=redis://redis:6379/1
      - CELERY_RESULT_BACKEND=redis://redis:6379/2
      - DEFAULT_ADMIN_USERNAME=admin
      - DEFAULT_ADMIN_PASSWORD=Admin123!
      - AUTO_INIT_DB=True
    ports:
      - "18000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      start_period: 40s
      retries: 3
    networks:
      - sma_network

  celery:
    build: .
    image: sma_celery:latest
    container_name: sma_celery
    restart: unless-stopped
    command: celery -A app.services.celery_app worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/persian_analytics
      - DATABASE_SYNC_URL=postgresql://postgres:postgres@postgres:5432/persian_analytics
      - REDIS_URL=redis://redis:6379/0
      - BRAIN_SERVICE_URL=http://sma_brain:8001
      - CELERY_BROKER_URL=redis://redis:6379/1
      - CELERY_RESULT_BACKEND=redis://redis:6379/2
      - SECRET_KEY=your-super-secret-key-change-this-in-production
    depends_on:
      - backend
    networks:
      - sma_network

networks:
  sma_network:
    name: sma_network
    driver: bridge
```

### brain/docker-compose.yml
```yaml
services:
  brain:
    build: .
    image: sma_brain:latest
    container_name: sma_brain
    restart: unless-stopped
    ports:
      - "18001:8001"
    environment:
      - DEBUG=true
      - SIMULATE_GPU=true
    volumes:
      - ./app:/app/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      start_period: 10s
      retries: 3
    networks:
      - sma_network

networks:
  sma_network:
    external: true
```

## Requirements
### backend/requirements.txt
```
# FastAPI and Server
fastapi
uvicorn[standard]
python-multipart
python-jose[cryptography]

# Password Hashing
bcrypt

# Database
sqlalchemy
asyncpg
psycopg2-binary
alembic
redis

# HTTP Client
httpx
aiohttp

# Validation and Settings
pydantic
pydantic-settings
email-validator

# Celery for background tasks
celery

# Utilities
python-dateutil
orjson

# Testing
pytest
pytest-asyncio

# Logging
loguru
```

### brain/requirements.txt
```
fastapi
uvicorn[standard]
pydantic
pydantic-settings
python-multipart
orjson
loguru
httpx
```

## OpenAPI Specification
```json
{"error": "Backend not running"}
```
