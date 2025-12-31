from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user, PaginationParams
from app.crud import author as author_crud
from app.models.user import User
from app.schemas.author import (
    AuthorCreate,
    AuthorUpdate,
    AuthorResponse,
    AuthorWithMetrics
)
from app.schemas.base import MessageResponse

router = APIRouter()


@router.get("", response_model=List[AuthorResponse])
async def get_authors(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    platform: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get all authors with optional filtering.
    """
    if search:
        authors = await author_crud.search(
            db,
            query_str=search,
            platform=platform,
            skip=pagination.skip,
            limit=pagination.limit
        )
    else:
        authors = await author_crud.get_multi(
            db,
            skip=pagination.skip,
            limit=pagination.limit
        )
    
    return [AuthorResponse.model_validate(a) for a in authors]


@router.get("/top/followers", response_model=List[AuthorResponse])
async def get_top_authors_by_followers(
    db: AsyncSession = Depends(get_db),
    platform: Optional[str] = None,
    limit: int = Query(default=10, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get top authors by follower count.
    """
    authors = await author_crud.get_top_by_followers(
        db,
        platform=platform,
        limit=limit
    )
    return [AuthorResponse.model_validate(a) for a in authors]


@router.get("/top/pagerank", response_model=List[AuthorResponse])
async def get_top_authors_by_pagerank(
    db: AsyncSession = Depends(get_db),
    platform: Optional[str] = None,
    limit: int = Query(default=10, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get top authors by PageRank score.
    """
    authors = await author_crud.get_top_by_pagerank(
        db,
        platform=platform,
        limit=limit
    )
    return [AuthorResponse.model_validate(a) for a in authors]


@router.get("/top/influence", response_model=List[AuthorResponse])
async def get_top_authors_by_influence(
    db: AsyncSession = Depends(get_db),
    platform: Optional[str] = None,
    limit: int = Query(default=10, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get top authors by influence score.
    """
    authors = await author_crud.get_top_by_influence(
        db,
        platform=platform,
        limit=limit
    )
    return [AuthorResponse.model_validate(a) for a in authors]


@router.get("/stats")
async def get_author_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get author statistics by platform.
    """
    stats = await author_crud.count_by_platform(db)
    total = sum(stats.values())
    
    return {
        "total": total,
        "by_platform": stats
    }


@router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(
    author_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get author by ID.
    """
    author = await author_crud.get(db, author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    
    return AuthorResponse.model_validate(author)


@router.post("", response_model=AuthorResponse)
async def create_author(
    author_in: AuthorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create new author.
    """
    # Check if exists
    existing = await author_crud.get_by_platform_id(
        db,
        platform_id=author_in.platform_id,
        platform=author_in.platform
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author already exists for this platform"
        )
    
    author = await author_crud.create(db, obj_in=author_in)
    return AuthorResponse.model_validate(author)


@router.put("/{author_id}", response_model=AuthorResponse)
async def update_author(
    author_id: int,
    author_in: AuthorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update author.
    """
    author = await author_crud.get(db, author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    
    updated = await author_crud.update(db, db_obj=author, obj_in=author_in)
    return AuthorResponse.model_validate(updated)


@router.delete("/{author_id}", response_model=MessageResponse)
async def delete_author(
    author_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete author.
    """
    author = await author_crud.delete(db, id=author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    
    return MessageResponse(message="Author deleted successfully")
