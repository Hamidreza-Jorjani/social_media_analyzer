from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user, get_current_analyst, PaginationParams
from app.crud import post as post_crud
from app.models.user import User
from app.schemas.post import (
    PostCreate,
    PostUpdate,
    PostResponse,
    PostWithRelations,
    PostBulkCreate,
    PostFilter
)
from app.schemas.base import MessageResponse

router = APIRouter()


@router.get("", response_model=List[PostResponse])
async def get_posts(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    platform: Optional[str] = None,
    language: Optional[str] = None,
    data_source_id: Optional[int] = None,
    author_id: Optional[int] = None,
    is_processed: Optional[bool] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get posts with filtering options.
    """
    filters = PostFilter(
        platform=platform,
        language=language,
        data_source_id=data_source_id,
        author_id=author_id,
        is_processed=is_processed,
        date_from=date_from,
        date_to=date_to,
        search=search
    )
    
    posts = await post_crud.get_filtered(
        db,
        filters=filters,
        skip=pagination.skip,
        limit=pagination.limit
    )
    
    return [PostResponse.model_validate(p) for p in posts]


@router.get("/stats")
async def get_post_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get post statistics.
    """
    stats = await post_crud.get_stats(db)
    return stats


@router.get("/unprocessed", response_model=List[PostResponse])
async def get_unprocessed_posts(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_user)
):
    """
    Get unprocessed posts.
    """
    posts = await post_crud.get_unprocessed(
        db,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return [PostResponse.model_validate(p) for p in posts]


@router.get("/search", response_model=List[PostResponse])
async def search_posts(
    q: str = Query(..., min_length=2),
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    platform: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Search posts by content.
    """
    posts = await post_crud.search(
        db,
        query_str=q,
        platform=platform,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return [PostResponse.model_validate(p) for p in posts]


@router.get("/by-hashtag/{hashtag}", response_model=List[PostResponse])
async def get_posts_by_hashtag(
    hashtag: str,
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_user)
):
    """
    Get posts containing a specific hashtag.
    """
    posts = await post_crud.get_by_hashtag(
        db,
        hashtag=hashtag,
        skip=pagination.skip,
        limit=pagination.limit
    )
    return [PostResponse.model_validate(p) for p in posts]


@router.get("/{post_id}", response_model=PostWithRelations)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get post by ID with relations.
    """
    post = await post_crud.get_with_relations(db, id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    return PostWithRelations.model_validate(post)


@router.post("", response_model=PostResponse)
async def create_post(
    post_in: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Create new post.
    """
    # Check if exists
    existing = await post_crud.get_by_platform_id(
        db,
        platform_id=post_in.platform_id
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post already exists"
        )
    
    post = await post_crud.create(db, obj_in=post_in)
    return PostResponse.model_validate(post)


@router.post("/bulk", response_model=dict)
async def bulk_create_posts(
    bulk_in: PostBulkCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Bulk create posts.
    """
    posts, created, existing = await post_crud.bulk_create(
        db,
        posts_in=bulk_in.posts
    )
    
    return {
        "total": len(posts),
        "created": created,
        "existing": existing
    }


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_in: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Update post.
    """
    post = await post_crud.get(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    updated = await post_crud.update(db, db_obj=post, obj_in=post_in)
    return PostResponse.model_validate(updated)


@router.delete("/{post_id}", response_model=MessageResponse)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_analyst)
):
    """
    Delete post.
    """
    post = await post_crud.delete(db, id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    return MessageResponse(message="Post deleted successfully")
