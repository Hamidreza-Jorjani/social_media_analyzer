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
