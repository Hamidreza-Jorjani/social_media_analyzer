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
