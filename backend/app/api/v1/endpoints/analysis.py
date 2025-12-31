from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user, get_current_analyst, PaginationParams
from app.crud import analysis as analysis_crud
from app.crud import analysis_result as result_crud
from app.models.user import User
from app.models.analysis import AnalysisType, AnalysisStatus
from app.services.analysis_service import analysis_service
from app.services.tasks import process_analysis
from app.schemas.analysis import (
    AnalysisCreate,
    AnalysisUpdate,
    AnalysisResponse,
    AnalysisWithUser,
    AnalysisConfig,
    AnalysisProgress
)
from app.schemas.analysis_result import (
    AnalysisResultResponse,
    AnalysisSummary
)
from app.schemas.base import MessageResponse

router = APIRouter()


@router.get("", response_model=List[AnalysisResponse])
async def get_analyses(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    status_filter: Optional[AnalysisStatus] = None,
    type_filter: Optional[AnalysisType] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get all analyses for current user.
    """
    if status_filter:
        analyses = await analysis_crud.get_by_status(
            db,
            status=status_filter,
            skip=pagination.skip,
            limit=pagination.limit
        )
    elif type_filter:
        analyses = await analysis_crud.get_by_type(
            db,
            analysis_type=type_filter,
            skip=pagination.skip,
            limit=pagination.limit
        )
    else:
        analyses = await analysis_crud.get_by_user(
            db,
            user_id=current_user.id,
            skip=pagination.skip,
            limit=pagination.limit
        )
    
    return [AnalysisResponse.model_validate(a) for a in analyses]


@router.get("/stats")
async def get_analysis_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get analysis statistics.
    """
    stats = await analysis_crud.get_stats(db, user_id=current_user.id)
    return stats


@router.get("/pending", response_model=List[AnalysisResponse])
async def get_pending_analyses(
    db: AsyncSession = Depends(get_db),
    limit: int = 10,
    current_user: User = Depends(get_current_analyst)
):
    """
    Get pending analyses (analyst only).
    """
    analyses = await analysis_crud.get_pending(db, limit=limit)
    return [AnalysisResponse.model_validate(a) for a in analyses]


@router.get("/{analysis_id}", response_model=AnalysisWithUser)
async def get_analysis(
    analysis_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get analysis by ID.
    """
    analysis = await analysis_crud.get_with_user(db, id=analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    return AnalysisWithUser.model_validate(analysis)


@router.get("/{analysis_id}/progress")
async def get_analysis_progress(
    analysis_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get analysis progress.
    """
    analysis = await analysis_crud.get(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    # Try to get from cache first
    cached = await analysis_service.get_progress(analysis_id)
    if cached:
        return cached
    
    return {
        "analysis_id": analysis_id,
        "status": analysis.status.value,
        "progress": analysis.progress
    }


@router.get("/{analysis_id}/results", response_model=List[AnalysisResultResponse])
async def get_analysis_results(
    analysis_id: int,
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_user)
):
    """
    Get results for an analysis.
    """
    analysis = await analysis_crud.get(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    results = await result_crud.get_by_analysis(
        db,
        analysis_id=analysis_id,
        skip=pagination.skip,
        limit=pagination.limit
    )
    
    return [AnalysisResultResponse.model_validate(r) for r in results]


@router.get("/{analysis_id}/summary")
async def get_analysis_summary(
    analysis_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get analysis summary.
    """
    analysis = await analysis_crud.get(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    if analysis.summary:
        return analysis.summary
    
    # Generate summary if not exists
    summary = await analysis_service.generate_summary(db, analysis_id=analysis_id)
    return summary


@router.post("", response_model=AnalysisResponse)
async def create_analysis(
    analysis_in: AnalysisCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Create new analysis.
    """
    analysis = await analysis_service.create_analysis(
        db,
        analysis_in=analysis_in,
        user_id=current_user.id
    )
    
    return AnalysisResponse.model_validate(analysis)


@router.post("/{analysis_id}/start", response_model=MessageResponse)
async def start_analysis(
    analysis_id: int,
    config: Optional[AnalysisConfig] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Start processing an analysis.
    """
    analysis = await analysis_crud.get(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    if analysis.status != AnalysisStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Analysis is already {analysis.status.value}"
        )
    
    # Queue task for processing
    config_dict = config.model_dump() if config else None
    process_analysis.delay(analysis_id, config_dict)
    
    # Update status to queued
    await analysis_crud.update_status(
        db,
        analysis_id=analysis_id,
        status=AnalysisStatus.QUEUED
    )
    
    return MessageResponse(message="Analysis queued for processing")


@router.post("/{analysis_id}/cancel", response_model=MessageResponse)
async def cancel_analysis(
    analysis_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Cancel an analysis.
    """
    success = await analysis_service.cancel_analysis(db, analysis_id=analysis_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel this analysis"
        )
    
    return MessageResponse(message="Analysis cancelled")


@router.put("/{analysis_id}", response_model=AnalysisResponse)
async def update_analysis(
    analysis_id: int,
    analysis_in: AnalysisUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Update analysis.
    """
    analysis = await analysis_crud.get(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    updated = await analysis_crud.update(db, db_obj=analysis, obj_in=analysis_in)
    return AnalysisResponse.model_validate(updated)


@router.delete("/{analysis_id}", response_model=MessageResponse)
async def delete_analysis(
    analysis_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Delete analysis and its results.
    """
    analysis = await analysis_crud.get(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    # Delete results first
    await result_crud.delete_by_analysis(db, analysis_id=analysis_id)
    
    # Delete analysis
    await analysis_crud.delete(db, id=analysis_id)
    
    return MessageResponse(message="Analysis deleted successfully")
