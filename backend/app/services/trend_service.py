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
