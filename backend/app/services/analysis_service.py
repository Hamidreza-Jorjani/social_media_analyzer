from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base import BaseService
from app.services.brain_service import brain_service, BrainServiceError
from app.services.redis_service import redis_service
from app.crud import analysis as analysis_crud
from app.crud import analysis_result as result_crud
from app.crud import post as post_crud
from app.crud import trend as trend_crud
from app.models.analysis import AnalysisStatus, AnalysisType
from app.schemas.analysis import AnalysisCreate, AnalysisConfig
from app.schemas.analysis_result import AnalysisResultCreate
from app.schemas.trend import TrendCreate


class AnalysisService(BaseService):
    """Service for managing analysis jobs."""
    
    def __init__(self):
        super().__init__("AnalysisService")
    
    async def create_analysis(
        self,
        db: AsyncSession,
        *,
        analysis_in: AnalysisCreate,
        user_id: int
    ):
        """Create a new analysis job."""
        analysis = await analysis_crud.create_with_user(
            db,
            obj_in=analysis_in,
            user_id=user_id
        )
        self.log_info(f"Created analysis {analysis.id} for user {user_id}")
        return analysis
    
    async def start_analysis(
        self,
        db: AsyncSession,
        *,
        analysis_id: int
    ) -> bool:
        """Start an analysis job."""
        analysis = await analysis_crud.get(db, analysis_id)
        if not analysis:
            self.log_error(f"Analysis {analysis_id} not found")
            return False
        
        if analysis.status != AnalysisStatus.PENDING:
            self.log_warning(f"Analysis {analysis_id} is not pending")
            return False
        
        # Update status to processing
        await analysis_crud.update_status(
            db,
            analysis_id=analysis_id,
            status=AnalysisStatus.PROCESSING,
            progress=0.0
        )
        
        # Update Redis progress
        await redis_service.set_analysis_progress(
            analysis_id,
            progress=0.0,
            status="processing"
        )
        
        self.log_info(f"Started analysis {analysis_id}")
        return True
    
    async def process_analysis(
        self,
        db: AsyncSession,
        *,
        analysis_id: int,
        config: Optional[AnalysisConfig] = None
    ) -> bool:
        """Process an analysis job."""
        analysis = await analysis_crud.get(db, analysis_id)
        if not analysis:
            return False
        
        # Get posts based on filters
        filters = analysis.query_filters or {}
        posts = await self._get_posts_for_analysis(db, filters, analysis.post_count)
        
        if not posts:
            await analysis_crud.update_status(
                db,
                analysis_id=analysis_id,
                status=AnalysisStatus.FAILED,
                error_message="No posts found matching filters"
            )
            return False
        
        # Prepare posts data
        posts_data = [
            {
                "id": p.id,
                "content": p.content,
                "platform": p.platform,
                "posted_at": p.posted_at.isoformat() if p.posted_at else None
            }
            for p in posts
        ]
        
        # Get config
        if config is None:
            config = AnalysisConfig()
        
        try:
            # Check BRAIN availability
            if not await brain_service.is_available():
                raise BrainServiceError("BRAIN service unavailable")
            
            # Submit batch analysis
            batch_response = await brain_service.submit_batch_analysis(
                analysis_id=analysis_id,
                posts=posts_data,
                config=config.model_dump()
            )
            
            self.log_info(
                f"Submitted analysis {analysis_id} to BRAIN, "
                f"task_id: {batch_response.task_id}"
            )
            
            return True
            
        except BrainServiceError as e:
            self.log_error(f"BRAIN service error: {e.message}")
            await analysis_crud.update_status(
                db,
                analysis_id=analysis_id,
                status=AnalysisStatus.FAILED,
                error_message=f"BRAIN service error: {e.message}"
            )
            return False
    
    async def _get_posts_for_analysis(
        self,
        db: AsyncSession,
        filters: Dict[str, Any],
        limit: Optional[int] = None
    ) -> List:
        """Get posts for analysis based on filters."""
        from app.schemas.post import PostFilter
        
        post_filter = PostFilter(**filters) if filters else PostFilter()
        
        posts = await post_crud.get_filtered(
            db,
            filters=post_filter,
            skip=0,
            limit=limit or 1000
        )
        
        return posts
    
    async def process_analysis_results(
        self,
        db: AsyncSession,
        *,
        analysis_id: int,
        results: List[Dict[str, Any]]
    ) -> int:
        """Process and store analysis results from BRAIN."""
        stored_count = 0
        
        for result_data in results:
            try:
                result_in = AnalysisResultCreate(
                    post_id=result_data.get("post_id") or result_data.get("text_id"),
                    analysis_id=analysis_id,
                    sentiment_label=result_data.get("sentiment", {}).get("label"),
                    sentiment_score=result_data.get("sentiment", {}).get("score"),
                    sentiment_confidence=result_data.get("sentiment", {}).get("confidence"),
                    emotions=result_data.get("emotions"),
                    dominant_emotion=result_data.get("dominant_emotion"),
                    summary=result_data.get("summary"),
                    keywords=result_data.get("keywords"),
                    topics=result_data.get("topics"),
                    entities=result_data.get("entities"),
                    raw_results=result_data
                )
                
                await result_crud.create(db, obj_in=result_in)
                stored_count += 1
                
                # Mark post as processed
                await post_crud.mark_processed(
                    db,
                    post_id=result_in.post_id
                )
                
            except Exception as e:
                self.log_error(f"Error storing result: {e}")
                continue
        
        # Update progress
        progress = (stored_count / len(results)) * 100 if results else 100
        await redis_service.set_analysis_progress(
            analysis_id,
            progress=progress,
            status="storing_results"
        )
        
        return stored_count
    
    async def complete_analysis(
        self,
        db: AsyncSession,
        *,
        analysis_id: int,
        summary: Optional[Dict[str, Any]] = None
    ):
        """Complete an analysis job."""
        # Generate summary if not provided
        if summary is None:
            summary = await self.generate_summary(db, analysis_id=analysis_id)
        
        # Update analysis
        await analysis_crud.update_status(
            db,
            analysis_id=analysis_id,
            status=AnalysisStatus.COMPLETED,
            progress=100.0
        )
        
        await analysis_crud.set_summary(
            db,
            analysis_id=analysis_id,
            summary=summary
        )
        
        # Update Redis
        await redis_service.set_analysis_progress(
            analysis_id,
            progress=100.0,
            status="completed"
        )
        
        # Cache summary
        await redis_service.cache_analysis_result(
            analysis_id,
            summary
        )
        
        self.log_info(f"Completed analysis {analysis_id}")
    
    async def generate_summary(
        self,
        db: AsyncSession,
        *,
        analysis_id: int
    ) -> Dict[str, Any]:
        """Generate summary for completed analysis."""
        # Get counts
        total_results = await result_crud.count_by_analysis(db, analysis_id=analysis_id)
        
        # Get distributions
        sentiment_dist = await result_crud.get_sentiment_distribution(
            db, analysis_id=analysis_id
        )
        emotion_dist = await result_crud.get_emotion_distribution(
            db, analysis_id=analysis_id
        )
        
        # Get average sentiment
        avg_sentiment = await result_crud.get_average_sentiment(
            db, analysis_id=analysis_id
        )
        
        # Get top keywords
        top_keywords = await result_crud.aggregate_keywords(
            db, analysis_id=analysis_id, limit=20
        )
        
        summary = {
            "total_posts": total_results,
            "processed_posts": total_results,
            "sentiment_distribution": sentiment_dist,
            "emotion_distribution": emotion_dist,
            "average_sentiment_score": avg_sentiment,
            "top_keywords": top_keywords,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return summary
    
    async def fail_analysis(
        self,
        db: AsyncSession,
        *,
        analysis_id: int,
        error_message: str
    ):
        """Mark analysis as failed."""
        await analysis_crud.update_status(
            db,
            analysis_id=analysis_id,
            status=AnalysisStatus.FAILED,
            error_message=error_message
        )
        
        await redis_service.set_analysis_progress(
            analysis_id,
            progress=0.0,
            status="failed"
        )
        
        self.log_error(f"Analysis {analysis_id} failed: {error_message}")
    
    async def get_progress(
        self,
        analysis_id: int
    ) -> Optional[Dict[str, Any]]:
        """Get analysis progress from cache."""
        return await redis_service.get_analysis_progress(analysis_id)
    
    async def cancel_analysis(
        self,
        db: AsyncSession,
        *,
        analysis_id: int
    ) -> bool:
        """Cancel an analysis job."""
        analysis = await analysis_crud.get(db, analysis_id)
        if not analysis:
            return False
        
        if analysis.status in [AnalysisStatus.COMPLETED, AnalysisStatus.FAILED]:
            return False
        
        await analysis_crud.update_status(
            db,
            analysis_id=analysis_id,
            status=AnalysisStatus.CANCELLED
        )
        
        await redis_service.set_analysis_progress(
            analysis_id,
            progress=0.0,
            status="cancelled"
        )
        
        self.log_info(f"Cancelled analysis {analysis_id}")
        return True


# Create singleton instance
analysis_service = AnalysisService()
