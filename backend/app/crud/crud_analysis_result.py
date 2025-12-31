from typing import Optional, List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.analysis_result import AnalysisResult
from app.schemas.analysis_result import AnalysisResultCreate


class CRUDAnalysisResult(CRUDBase[AnalysisResult, AnalysisResultCreate, AnalysisResultCreate]):
    """CRUD operations for AnalysisResult model."""
    
    async def get_by_post(
        self,
        db: AsyncSession,
        *,
        post_id: int
    ) -> List[AnalysisResult]:
        """Get all results for a post."""
        query = (
            select(AnalysisResult)
            .where(AnalysisResult.post_id == post_id)
            .order_by(AnalysisResult.created_at.desc())
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_analysis(
        self,
        db: AsyncSession,
        *,
        analysis_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[AnalysisResult]:
        """Get results for an analysis."""
        query = (
            select(AnalysisResult)
            .where(AnalysisResult.analysis_id == analysis_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_with_post(
        self,
        db: AsyncSession,
        *,
        id: int
    ) -> Optional[AnalysisResult]:
        """Get result with post info."""
        query = (
            select(AnalysisResult)
            .options(selectinload(AnalysisResult.post))
            .where(AnalysisResult.id == id)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def bulk_create(
        self,
        db: AsyncSession,
        *,
        results_in: List[AnalysisResultCreate]
    ) -> List[AnalysisResult]:
        """Bulk create analysis results."""
        results = []
        for result_in in results_in:
            result = await self.create(db, obj_in=result_in)
            results.append(result)
        return results
    
    async def get_sentiment_distribution(
        self,
        db: AsyncSession,
        *,
        analysis_id: int
    ) -> Dict[str, int]:
        """Get sentiment distribution for an analysis."""
        query = (
            select(
                AnalysisResult.sentiment_label,
                func.count(AnalysisResult.id)
            )
            .where(
                AnalysisResult.analysis_id == analysis_id,
                AnalysisResult.sentiment_label.isnot(None)
            )
            .group_by(AnalysisResult.sentiment_label)
        )
        result = await db.execute(query)
        return {row[0]: row[1] for row in result.all()}
    
    async def get_emotion_distribution(
        self,
        db: AsyncSession,
        *,
        analysis_id: int
    ) -> Dict[str, int]:
        """Get dominant emotion distribution for an analysis."""
        query = (
            select(
                AnalysisResult.dominant_emotion,
                func.count(AnalysisResult.id)
            )
            .where(
                AnalysisResult.analysis_id == analysis_id,
                AnalysisResult.dominant_emotion.isnot(None)
            )
            .group_by(AnalysisResult.dominant_emotion)
        )
        result = await db.execute(query)
        return {row[0]: row[1] for row in result.all()}
    
    async def get_average_sentiment(
        self,
        db: AsyncSession,
        *,
        analysis_id: int
    ) -> Optional[float]:
        """Get average sentiment score for an analysis."""
        query = (
            select(func.avg(AnalysisResult.sentiment_score))
            .where(
                AnalysisResult.analysis_id == analysis_id,
                AnalysisResult.sentiment_score.isnot(None)
            )
        )
        result = await db.execute(query)
        return result.scalar()
    
    async def get_by_sentiment(
        self,
        db: AsyncSession,
        *,
        analysis_id: int,
        sentiment: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[AnalysisResult]:
        """Get results by sentiment label."""
        query = (
            select(AnalysisResult)
            .where(
                AnalysisResult.analysis_id == analysis_id,
                AnalysisResult.sentiment_label == sentiment
            )
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_community(
        self,
        db: AsyncSession,
        *,
        analysis_id: int,
        community_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[AnalysisResult]:
        """Get results by community ID."""
        query = (
            select(AnalysisResult)
            .where(
                AnalysisResult.analysis_id == analysis_id,
                AnalysisResult.community_id == community_id
            )
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def aggregate_keywords(
        self,
        db: AsyncSession,
        *,
        analysis_id: int,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Aggregate keywords from analysis results."""
        query = (
            select(AnalysisResult.keywords)
            .where(
                AnalysisResult.analysis_id == analysis_id,
                AnalysisResult.keywords.isnot(None)
            )
        )
        result = await db.execute(query)
        
        # Count keyword occurrences
        keyword_counts: Dict[str, int] = {}
        for row in result.all():
            keywords = row[0] or []
            for keyword in keywords:
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        # Sort and limit
        sorted_keywords = sorted(
            keyword_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        return [{"keyword": k, "count": v} for k, v in sorted_keywords]
    
    async def count_by_analysis(
        self,
        db: AsyncSession,
        *,
        analysis_id: int
    ) -> int:
        """Count results for an analysis."""
        query = (
            select(func.count())
            .select_from(AnalysisResult)
            .where(AnalysisResult.analysis_id == analysis_id)
        )
        result = await db.execute(query)
        return result.scalar() or 0
    
    async def delete_by_analysis(
        self,
        db: AsyncSession,
        *,
        analysis_id: int
    ) -> int:
        """Delete all results for an analysis."""
        from sqlalchemy import delete
        query = delete(AnalysisResult).where(
            AnalysisResult.analysis_id == analysis_id
        )
        result = await db.execute(query)
        await db.flush()
        return result.rowcount


# Create singleton instance
analysis_result = CRUDAnalysisResult(AnalysisResult)
