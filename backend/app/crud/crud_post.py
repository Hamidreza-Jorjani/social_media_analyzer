from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate, PostFilter


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    """CRUD operations for Post model."""
    
    async def get_by_platform_id(
        self,
        db: AsyncSession,
        *,
        platform_id: str
    ) -> Optional[Post]:
        """Get post by platform-specific ID."""
        query = select(Post).where(Post.platform_id == platform_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_with_relations(
        self,
        db: AsyncSession,
        *,
        id: int
    ) -> Optional[Post]:
        """Get post with author and data source."""
        query = (
            select(Post)
            .options(
                selectinload(Post.author),
                selectinload(Post.data_source)
            )
            .where(Post.id == id)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_or_create(
        self,
        db: AsyncSession,
        *,
        obj_in: PostCreate
    ) -> tuple[Post, bool]:
        """Get existing post or create new one. Returns (post, created)."""
        existing = await self.get_by_platform_id(
            db,
            platform_id=obj_in.platform_id
        )
        if existing:
            return existing, False
        
        new_post = await self.create(db, obj_in=obj_in)
        return new_post, True
    
    async def get_filtered(
        self,
        db: AsyncSession,
        *,
        filters: PostFilter,
        skip: int = 0,
        limit: int = 100
    ) -> List[Post]:
        """Get posts with filters."""
        query = select(Post)
        
        if filters.platform:
            query = query.where(Post.platform == filters.platform)
        if filters.language:
            query = query.where(Post.language == filters.language)
        if filters.data_source_id:
            query = query.where(Post.data_source_id == filters.data_source_id)
        if filters.author_id:
            query = query.where(Post.author_id == filters.author_id)
        if filters.is_processed is not None:
            query = query.where(Post.is_processed == filters.is_processed)
        if filters.date_from:
            query = query.where(Post.posted_at >= filters.date_from)
        if filters.date_to:
            query = query.where(Post.posted_at <= filters.date_to)
        if filters.search:
            query = query.where(Post.content.ilike(f"%{filters.search}%"))
        if filters.hashtags:
            # JSON contains for hashtags
            for tag in filters.hashtags:
                query = query.where(Post.hashtags.contains([tag]))
        
        query = query.order_by(Post.posted_at.desc())
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def count_filtered(
        self,
        db: AsyncSession,
        *,
        filters: PostFilter
    ) -> int:
        """Count posts with filters."""
        query = select(func.count()).select_from(Post)
        
        if filters.platform:
            query = query.where(Post.platform == filters.platform)
        if filters.language:
            query = query.where(Post.language == filters.language)
        if filters.data_source_id:
            query = query.where(Post.data_source_id == filters.data_source_id)
        if filters.author_id:
            query = query.where(Post.author_id == filters.author_id)
        if filters.is_processed is not None:
            query = query.where(Post.is_processed == filters.is_processed)
        if filters.date_from:
            query = query.where(Post.posted_at >= filters.date_from)
        if filters.date_to:
            query = query.where(Post.posted_at <= filters.date_to)
        
        result = await db.execute(query)
        return result.scalar() or 0
    
    async def get_unprocessed(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[Post]:
        """Get unprocessed posts."""
        query = (
            select(Post)
            .where(Post.is_processed == False)
            .order_by(Post.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def mark_processed(
        self,
        db: AsyncSession,
        *,
        post_id: int,
        error: Optional[str] = None
    ) -> Optional[Post]:
        """Mark post as processed."""
        post = await self.get(db, post_id)
        if not post:
            return None
        
        post.is_processed = True
        post.processing_error = error
        
        db.add(post)
        await db.flush()
        await db.refresh(post)
        return post
    
    async def bulk_create(
        self,
        db: AsyncSession,
        *,
        posts_in: List[PostCreate]
    ) -> tuple[List[Post], int, int]:
        """Bulk create posts. Returns (posts, created_count, existing_count)."""
        posts = []
        created = 0
        existing = 0
        
        for post_in in posts_in:
            post, is_new = await self.get_or_create(db, obj_in=post_in)
            posts.append(post)
            if is_new:
                created += 1
            else:
                existing += 1
        
        return posts, created, existing
    
    async def get_by_author(
        self,
        db: AsyncSession,
        *,
        author_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Post]:
        """Get posts by author."""
        query = (
            select(Post)
            .where(Post.author_id == author_id)
            .order_by(Post.posted_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_hashtag(
        self,
        db: AsyncSession,
        *,
        hashtag: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Post]:
        """Get posts containing a hashtag."""
        query = (
            select(Post)
            .where(Post.hashtags.contains([hashtag]))
            .order_by(Post.posted_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_stats(
        self,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Get post statistics."""
        # Total count
        total_query = select(func.count()).select_from(Post)
        total_result = await db.execute(total_query)
        total = total_result.scalar() or 0
        
        # Processed count
        processed_query = (
            select(func.count())
            .select_from(Post)
            .where(Post.is_processed == True)
        )
        processed_result = await db.execute(processed_query)
        processed = processed_result.scalar() or 0
        
        # By platform
        platform_query = (
            select(Post.platform, func.count(Post.id))
            .group_by(Post.platform)
        )
        platform_result = await db.execute(platform_query)
        by_platform = {row[0]: row[1] for row in platform_result.all()}
        
        # By language
        language_query = (
            select(Post.language, func.count(Post.id))
            .group_by(Post.language)
        )
        language_result = await db.execute(language_query)
        by_language = {row[0]: row[1] for row in language_result.all()}
        
        return {
            "total": total,
            "processed": processed,
            "unprocessed": total - processed,
            "by_platform": by_platform,
            "by_language": by_language
        }
    
    async def search(
        self,
        db: AsyncSession,
        *,
        query_str: str,
        platform: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Post]:
        """Search posts by content."""
        query = select(Post).where(Post.content.ilike(f"%{query_str}%"))
        if platform:
            query = query.where(Post.platform == platform)
        query = query.order_by(Post.posted_at.desc())
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())


# Create singleton instance
post = CRUDPost(Post)
