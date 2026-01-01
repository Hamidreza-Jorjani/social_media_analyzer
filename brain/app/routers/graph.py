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
