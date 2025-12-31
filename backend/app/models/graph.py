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
