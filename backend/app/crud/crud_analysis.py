from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.analysis import Analysis, AnalysisType, AnalysisStatus
from app.schemas.analysis import AnalysisCreate, AnalysisUpdate


class CRUDAnalysis(CRUDBase[Analysis, AnalysisCreate, AnalysisUpdate]):
    """CRUD operations for Analysis model."""
    
    async def create_with_user(
        self,
        db: AsyncSession,
        *,
        obj_in: AnalysisCreate,
        user_id: int
    ) -> Analysis:
        """Create analysis with user ID."""
        obj_data = obj_in.model_dump(exclude_unset=True)
        obj_data["user_id"] = user_id
        obj_data["status"] = AnalysisStatus.PENDING
        obj_data["progress"] = 0.0
        
        db_obj = Analysis(**obj_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def get_with_user(
        self,
        db: AsyncSession,
        *,
        id: int
    ) -> Optional[Analysis]:
        """Get analysis with user info."""
        query = (
            select(Analysis)
            .options(selectinload(Analysis.user))
            .where(Analysis.id == id)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_user(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Analysis]:
        """Get analyses by user."""
        query = (
            select(Analysis)
            .where(Analysis.user_id == user_id)
            .order_by(Analysis.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_status(
        self,
        db: AsyncSession,
        *,
        status: AnalysisStatus,
        skip: int = 0,
        limit: int = 100
    ) -> List[Analysis]:
        """Get analyses by status."""
        query = (
            select(Analysis)
            .where(Analysis.status == status)
            .order_by(Analysis.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_type(
        self,
        db: AsyncSession,
        *,
        analysis_type: AnalysisType,
        skip: int = 0,
        limit: int = 100
    ) -> List[Analysis]:
        """Get analyses by type."""
        query = (
            select(Analysis)
            .where(Analysis.analysis_type == analysis_type)
            .order_by(Analysis.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_pending(
        self,
        db: AsyncSession,
        *,
        limit: int = 10
    ) -> List[Analysis]:
        """Get pending analyses for processing."""
        query = (
            select(Analysis)
            .where(Analysis.status == AnalysisStatus.PENDING)
            .order_by(Analysis.created_at.asc())
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def update_status(
        self,
        db: AsyncSession,
        *,
        analysis_id: int,
        status: AnalysisStatus,
        progress: Optional[float] = None,
        error_message: Optional[str] = None
    ) -> Optional[Analysis]:
        """Update analysis status."""
        analysis = await self.get(db, analysis_id)
        if not analysis:
            return None
        
        analysis.status = status
        
        if progress is not None:
            analysis.progress = progress
        
        if error_message is not None:
            analysis.error_message = error_message
        
        if status == AnalysisStatus.PROCESSING and not analysis.started_at:
            analysis.started_at = datetime.utcnow().isoformat()
        
        if status in [AnalysisStatus.COMPLETED, AnalysisStatus.FAILED]:
            analysis.completed_at = datetime.utcnow().isoformat()
        
        db.add(analysis)
        await db.flush()
        await db.refresh(analysis)
        return analysis
    
    async def update_progress(
        self,
        db: AsyncSession,
        *,
        analysis_id: int,
        progress: float
    ) -> Optional[Analysis]:
        """Update analysis progress."""
        analysis = await self.get(db, analysis_id)
        if not analysis:
            return None
        
        analysis.progress = min(progress, 100.0)
        
        db.add(analysis)
        await db.flush()
        await db.refresh(analysis)
        return analysis
    
    async def set_summary(
        self,
        db: AsyncSession,
        *,
        analysis_id: int,
        summary: Dict[str, Any]
    ) -> Optional[Analysis]:
        """Set analysis summary."""
        analysis = await self.get(db, analysis_id)
        if not analysis:
            return None
        
        analysis.summary = summary
        
        db.add(analysis)
        await db.flush()
        await db.refresh(analysis)
        return analysis
    
    async def cancel(
        self,
        db: AsyncSession,
        *,
        analysis_id: int
    ) -> Optional[Analysis]:
        """Cancel an analysis."""
        return await self.update_status(
            db,
            analysis_id=analysis_id,
            status=AnalysisStatus.CANCELLED
        )
    
    async def get_stats(
        self,
        db: AsyncSession,
        *,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get analysis statistics."""
        base_query = select(Analysis)
        if user_id:
            base_query = base_query.where(Analysis.user_id == user_id)
        
        # Total count
        total_query = select(func.count()).select_from(base_query.subquery())
        total_result = await db.execute(total_query)
        total = total_result.scalar() or 0
        
        # By status
        status_query = (
            select(Analysis.status, func.count(Analysis.id))
            .group_by(Analysis.status)
        )
        if user_id:
            status_query = status_query.where(Analysis.user_id == user_id)
        status_result = await db.execute(status_query)
        by_status = {row[0].value: row[1] for row in status_result.all()}
        
        # By type
        type_query = (
            select(Analysis.analysis_type, func.count(Analysis.id))
            .group_by(Analysis.analysis_type)
        )
        if user_id:
            type_query = type_query.where(Analysis.user_id == user_id)
        type_result = await db.execute(type_query)
        by_type = {row[0].value: row[1] for row in type_result.all()}
        
        return {
            "total": total,
            "by_status": by_status,
            "by_type": by_type
        }


# Create singleton instance
analysis = CRUDAnalysis(Analysis)
