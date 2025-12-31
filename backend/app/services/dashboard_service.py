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
