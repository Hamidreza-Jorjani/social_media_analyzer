from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_db,
    get_current_user,
    get_current_analyst,
    PaginationParams
)
from app.crud import data_source as data_source_crud
from app.models.user import User
from app.models.data_source import SourcePlatform
from app.schemas.data_source import (
    DataSourceCreate,
    DataSourceUpdate,
    DataSourceResponse,
    DataSourceStats
)
from app.schemas.base import MessageResponse

router = APIRouter()


@router.get("", response_model=List[DataSourceResponse])
async def get_data_sources(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    platform: SourcePlatform = None,
    active_only: bool = False,
    current_user: User = Depends(get_current_user)
):
    """
    Get all data sources.
    """
    if active_only:
        sources = await data_source_crud.get_active(
            db,
            skip=pagination.skip,
            limit=pagination.limit
        )
    elif platform:
        sources = await data_source_crud.get_by_platform(
            db,
            platform=platform,
            skip=pagination.skip,
            limit=pagination.limit
        )
    else:
        sources = await data_source_crud.get_multi(
            db,
            skip=pagination.skip,
            limit=pagination.limit
        )
    
    return [DataSourceResponse.model_validate(s) for s in sources]


@router.get("/{source_id}", response_model=DataSourceResponse)
async def get_data_source(
    source_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get data source by ID.
    """
    source = await data_source_crud.get(db, source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data source not found"
        )
    
    return DataSourceResponse.model_validate(source)


@router.get("/{source_id}/stats", response_model=DataSourceStats)
async def get_data_source_stats(
    source_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get statistics for a data source.
    """
    source = await data_source_crud.get(db, source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data source not found"
        )
    
    stats = await data_source_crud.get_stats(db, data_source_id=source_id)
    
    return DataSourceStats(
        id=source.id,
        name=source.name,
        platform=source.platform,
        total_posts=stats["total_posts"],
        total_authors=stats["total_authors"],
        last_sync_at=source.last_sync_at
    )


@router.post("", response_model=DataSourceResponse)
async def create_data_source(
    source_in: DataSourceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Create new data source (analyst or admin).
    """
    # Check if name exists
    existing = await data_source_crud.get_by_name(db, name=source_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data source with this name already exists"
        )
    
    source = await data_source_crud.create(db, obj_in=source_in)
    return DataSourceResponse.model_validate(source)


@router.put("/{source_id}", response_model=DataSourceResponse)
async def update_data_source(
    source_id: int,
    source_in: DataSourceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Update data source (analyst or admin).
    """
    source = await data_source_crud.get(db, source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data source not found"
        )
    
    updated = await data_source_crud.update(db, db_obj=source, obj_in=source_in)
    return DataSourceResponse.model_validate(updated)


@router.delete("/{source_id}", response_model=MessageResponse)
async def delete_data_source(
    source_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Delete data source (analyst or admin).
    """
    source = await data_source_crud.delete(db, id=source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data source not found"
        )
    
    return MessageResponse(message="Data source deleted successfully")


@router.post("/{source_id}/activate", response_model=DataSourceResponse)
async def activate_data_source(
    source_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Activate data source.
    """
    source = await data_source_crud.get(db, source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data source not found"
        )
    
    source = await data_source_crud.activate(db, db_obj=source)
    return DataSourceResponse.model_validate(source)


@router.post("/{source_id}/deactivate", response_model=DataSourceResponse)
async def deactivate_data_source(
    source_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Deactivate data source.
    """
    source = await data_source_crud.get(db, source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data source not found"
        )
    
    source = await data_source_crud.deactivate(db, db_obj=source)
    return DataSourceResponse.model_validate(source)
