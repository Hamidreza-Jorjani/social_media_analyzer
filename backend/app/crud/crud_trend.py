from typing import Optional, List, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.trend import Trend
from app.schemas.trend import TrendCreate, TrendUpdate


class CRUDTrend(CRUDBase[Trend, TrendCreate, TrendUpdate]):
    """CRUD operations for Trend model."""
    
    async def get_active(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[Trend]:
        """Get active trends."""
        query = (
            select(Trend)
            .where(Trend.is_active == "active")
            .order_by(Trend.volume.desc())
            .offset(skip)
            .limit(limit)
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
    ) -> List[Trend]:
        """Get trends from an analysis."""
        query = (
            select(Trend)
            .where(Trend.analysis_id == analysis_id)
            .order_by(Trend.volume.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_top_by_volume(
        self,
        db: AsyncSession,
        *,
        limit: int = 10
    ) -> List[Trend]:
        """Get top trends by volume."""
        query = (
            select(Trend)
            .where(Trend.is_active == "active")
            .order_by(Trend.volume.desc())
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_top_by_growth(
        self,
        db: AsyncSession,
        *,
        limit: int = 10
    ) -> List[Trend]:
        """Get top trends by growth rate."""
        query = (
            select(Trend)
            .where(
                Trend.is_active == "active",
                Trend.growth_rate.isnot(None)
            )
            .order_by(Trend.growth_rate.desc())
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def search_by_name(
        self,
        db: AsyncSession,
        *,
        query_str: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Trend]:
        """Search trends by name."""
        query = (
            select(Trend)
            .where(Trend.name.ilike(f"%{query_str}%"))
            .order_by(Trend.volume.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def search_by_keyword(
        self,
        db: AsyncSession,
        *,
        keyword: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Trend]:
        """Search trends containing a keyword."""
        query = (
            select(Trend)
            .where(Trend.keywords.contains([keyword]))
            .order_by(Trend.volume.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def update_status(
        self,
        db: AsyncSession,
        *,
        trend_id: int,
        status: str
    ) -> Optional[Trend]:
        """Update trend status (active, declining, ended)."""
        trend = await self.get(db, trend_id)
        if not trend:
            return None
        
        trend.is_active = status
        db.add(trend)
        await db.flush()
        await db.refresh(trend)
        return trend
    
    async def bulk_create(
        self,
        db: AsyncSession,
        *,
        trends_in: List[TrendCreate]
    ) -> List[Trend]:
        """Bulk create trends."""
        trends = []
        for trend_in in trends_in:
            trend = await self.create(db, obj_in=trend_in)
            trends.append(trend)
        return trends
    
    async def get_stats(
        self,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Get trend statistics."""
        # Total count
        total_query = select(func.count()).select_from(Trend)
        total_result = await db.execute(total_query)
        total = total_result.scalar() or 0
        
        # Active count
        active_query = (
            select(func.count())
            .select_from(Trend)
            .where(Trend.is_active == "active")
        )
        active_result = await db.execute(active_query)
        active = active_result.scalar() or 0
        
        # Average volume
        avg_query = select(func.avg(Trend.volume))
        avg_result = await db.execute(avg_query)
        avg_volume = avg_result.scalar() or 0
        
        return {
            "total": total,
            "active": active,
            "declining": total - active,
            "average_volume": float(avg_volume)
        }


# Create singleton instance
trend = CRUDTrend(Trend)
