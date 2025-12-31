from typing import Optional, List, Dict, Any
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.graph import GraphNode, GraphEdge
from app.schemas.graph import GraphNodeCreate, GraphNodeUpdate, GraphEdgeCreate


class CRUDGraphNode(CRUDBase[GraphNode, GraphNodeCreate, GraphNodeUpdate]):
    """CRUD operations for GraphNode model."""
    
    async def get_by_node_id(
        self,
        db: AsyncSession,
        *,
        node_id: str
    ) -> Optional[GraphNode]:
        """Get node by node_id."""
        query = select(GraphNode).where(GraphNode.node_id == node_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_or_create(
        self,
        db: AsyncSession,
        *,
        obj_in: GraphNodeCreate
    ) -> tuple[GraphNode, bool]:
        """Get existing node or create new one."""
        existing = await self.get_by_node_id(db, node_id=obj_in.node_id)
        if existing:
            return existing, False
        
        new_node = await self.create(db, obj_in=obj_in)
        return new_node, True
    
    async def get_by_type(
        self,
        db: AsyncSession,
        *,
        node_type: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[GraphNode]:
        """Get nodes by type."""
        query = (
            select(GraphNode)
            .where(GraphNode.node_type == node_type)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_community(
        self,
        db: AsyncSession,
        *,
        community_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[GraphNode]:
        """Get nodes by community."""
        query = (
            select(GraphNode)
            .where(GraphNode.community_id == community_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_top_by_pagerank(
        self,
        db: AsyncSession,
        *,
        node_type: Optional[str] = None,
        limit: int = 10
    ) -> List[GraphNode]:
        """Get top nodes by PageRank."""
        query = (
            select(GraphNode)
            .where(GraphNode.pagerank.isnot(None))
            .order_by(GraphNode.pagerank.desc())
        )
        if node_type:
            query = query.where(GraphNode.node_type == node_type)
        query = query.limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_top_by_degree(
        self,
        db: AsyncSession,
        *,
        node_type: Optional[str] = None,
        limit: int = 10
    ) -> List[GraphNode]:
        """Get top nodes by degree."""
        query = (
            select(GraphNode)
            .order_by(GraphNode.degree.desc())
        )
        if node_type:
            query = query.where(GraphNode.node_type == node_type)
        query = query.limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_top_by_betweenness(
        self,
        db: AsyncSession,
        *,
        limit: int = 10
    ) -> List[GraphNode]:
        """Get top nodes by betweenness centrality."""
        query = (
            select(GraphNode)
            .where(GraphNode.betweenness_centrality.isnot(None))
            .order_by(GraphNode.betweenness_centrality.desc())
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def bulk_create(
        self,
        db: AsyncSession,
        *,
        nodes_in: List[GraphNodeCreate]
    ) -> List[GraphNode]:
        """Bulk create nodes."""
        nodes = []
        for node_in in nodes_in:
            node, _ = await self.get_or_create(db, obj_in=node_in)
            nodes.append(node)
        return nodes
    
    async def bulk_update_metrics(
        self,
        db: AsyncSession,
        *,
        metrics: List[Dict[str, Any]]
    ) -> int:
        """Bulk update node metrics. Each dict should have node_id and metrics."""
        updated = 0
        for metric_data in metrics:
            node_id = metric_data.pop("node_id", None)
            if not node_id:
                continue
            
            node = await self.get_by_node_id(db, node_id=node_id)
            if not node:
                continue
            
            for key, value in metric_data.items():
                if hasattr(node, key):
                    setattr(node, key, value)
            
            db.add(node)
            updated += 1
        
        await db.flush()
        return updated
    
    async def get_stats(
        self,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Get node statistics."""
        # Total count
        total_query = select(func.count()).select_from(GraphNode)
        total_result = await db.execute(total_query)
        total = total_result.scalar() or 0
        
        # By type
        type_query = (
            select(GraphNode.node_type, func.count(GraphNode.id))
            .group_by(GraphNode.node_type)
        )
        type_result = await db.execute(type_query)
        by_type = {row[0]: row[1] for row in type_result.all()}
        
        # Community count
        community_query = (
            select(func.count(func.distinct(GraphNode.community_id)))
            .where(GraphNode.community_id.isnot(None))
        )
        community_result = await db.execute(community_query)
        communities = community_result.scalar() or 0
        
        # Average degree
        degree_query = select(func.avg(GraphNode.degree))
        degree_result = await db.execute(degree_query)
        avg_degree = degree_result.scalar() or 0
        
        return {
            "total_nodes": total,
            "by_type": by_type,
            "communities_count": communities,
            "average_degree": float(avg_degree)
        }


class CRUDGraphEdge(CRUDBase[GraphEdge, GraphEdgeCreate, GraphEdgeCreate]):
    """CRUD operations for GraphEdge model."""
    
    async def get_between(
        self,
        db: AsyncSession,
        *,
        source_id: int,
        target_id: int,
        edge_type: Optional[str] = None
    ) -> Optional[GraphEdge]:
        """Get edge between two nodes."""
        query = select(GraphEdge).where(
            GraphEdge.source_id == source_id,
            GraphEdge.target_id == target_id
        )
        if edge_type:
            query = query.where(GraphEdge.edge_type == edge_type)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_or_create(
        self,
        db: AsyncSession,
        *,
        obj_in: GraphEdgeCreate
    ) -> tuple[GraphEdge, bool]:
        """Get existing edge or create new one."""
        existing = await self.get_between(
            db,
            source_id=obj_in.source_id,
            target_id=obj_in.target_id,
            edge_type=obj_in.edge_type
        )
        if existing:
            # Increment occurrence count
            existing.occurrence_count += 1
            db.add(existing)
            await db.flush()
            await db.refresh(existing)
            return existing, False
        
        new_edge = await self.create(db, obj_in=obj_in)
        return new_edge, True
    
    async def get_by_source(
        self,
        db: AsyncSession,
        *,
        source_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[GraphEdge]:
        """Get edges from a source node."""
        query = (
            select(GraphEdge)
            .where(GraphEdge.source_id == source_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_target(
        self,
        db: AsyncSession,
        *,
        target_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[GraphEdge]:
        """Get edges to a target node."""
        query = (
            select(GraphEdge)
            .where(GraphEdge.target_id == target_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_type(
        self,
        db: AsyncSession,
        *,
        edge_type: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[GraphEdge]:
        """Get edges by type."""
        query = (
            select(GraphEdge)
            .where(GraphEdge.edge_type == edge_type)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def bulk_create(
        self,
        db: AsyncSession,
        *,
        edges_in: List[GraphEdgeCreate]
    ) -> List[GraphEdge]:
        """Bulk create edges."""
        edges = []
        for edge_in in edges_in:
            edge, _ = await self.get_or_create(db, obj_in=edge_in)
            edges.append(edge)
        return edges
    
    async def get_stats(
        self,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Get edge statistics."""
        # Total count
        total_query = select(func.count()).select_from(GraphEdge)
        total_result = await db.execute(total_query)
        total = total_result.scalar() or 0
        
        # By type
        type_query = (
            select(GraphEdge.edge_type, func.count(GraphEdge.id))
            .group_by(GraphEdge.edge_type)
        )
        type_result = await db.execute(type_query)
        by_type = {row[0]: row[1] for row in type_result.all()}
        
        # Average weight
        weight_query = select(func.avg(GraphEdge.weight))
        weight_result = await db.execute(weight_query)
        avg_weight = weight_result.scalar() or 0
        
        return {
            "total_edges": total,
            "by_type": by_type,
            "average_weight": float(avg_weight)
        }


# Create singleton instances
graph_node = CRUDGraphNode(GraphNode)
graph_edge = CRUDGraphEdge(GraphEdge)
