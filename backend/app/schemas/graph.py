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
