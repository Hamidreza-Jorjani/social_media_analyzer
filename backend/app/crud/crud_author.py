from typing import Optional, List, Dict, Any
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate


class CRUDAuthor(CRUDBase[Author, AuthorCreate, AuthorUpdate]):
    """CRUD operations for Author model."""
    
    async def get_by_platform_id(
        self,
        db: AsyncSession,
        *,
        platform_id: str,
        platform: str
    ) -> Optional[Author]:
        """Get author by platform-specific ID."""
        query = select(Author).where(
            Author.platform_id == platform_id,
            Author.platform == platform
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_username(
        self,
        db: AsyncSession,
        *,
        username: str,
        platform: Optional[str] = None
    ) -> List[Author]:
        """Get authors by username."""
        query = select(Author).where(Author.username == username)
        if platform:
            query = query.where(Author.platform == platform)
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_or_create(
        self,
        db: AsyncSession,
        *,
        obj_in: AuthorCreate
    ) -> tuple[Author, bool]:
        """Get existing author or create new one. Returns (author, created)."""
        existing = await self.get_by_platform_id(
            db,
            platform_id=obj_in.platform_id,
            platform=obj_in.platform
        )
        if existing:
            return existing, False
        
        new_author = await self.create(db, obj_in=obj_in)
        return new_author, True
    
    async def search(
        self,
        db: AsyncSession,
        *,
        query_str: str,
        platform: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Author]:
        """Search authors by username or display name."""
        search_pattern = f"%{query_str}%"
        query = select(Author).where(
            or_(
                Author.username.ilike(search_pattern),
                Author.display_name.ilike(search_pattern)
            )
        )
        if platform:
            query = query.where(Author.platform == platform)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_top_by_followers(
        self,
        db: AsyncSession,
        *,
        platform: Optional[str] = None,
        limit: int = 10
    ) -> List[Author]:
        """Get top authors by follower count."""
        query = select(Author).order_by(Author.followers_count.desc())
        if platform:
            query = query.where(Author.platform == platform)
        query = query.limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_top_by_pagerank(
        self,
        db: AsyncSession,
        *,
        platform: Optional[str] = None,
        limit: int = 10
    ) -> List[Author]:
        """Get top authors by PageRank score."""
        query = (
            select(Author)
            .where(Author.pagerank_score.isnot(None))
            .order_by(Author.pagerank_score.desc())
        )
        if platform:
            query = query.where(Author.platform == platform)
        query = query.limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_top_by_influence(
        self,
        db: AsyncSession,
        *,
        platform: Optional[str] = None,
        limit: int = 10
    ) -> List[Author]:
        """Get top authors by influence score."""
        query = (
            select(Author)
            .where(Author.influence_score.isnot(None))
            .order_by(Author.influence_score.desc())
        )
        if platform:
            query = query.where(Author.platform == platform)
        query = query.limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def update_metrics(
        self,
        db: AsyncSession,
        *,
        author_id: int,
        metrics: Dict[str, Any]
    ) -> Optional[Author]:
        """Update author metrics."""
        author = await self.get(db, author_id)
        if not author:
            return None
        
        for key, value in metrics.items():
            if hasattr(author, key):
                setattr(author, key, value)
        
        db.add(author)
        await db.flush()
        await db.refresh(author)
        return author
    
    async def bulk_create(
        self,
        db: AsyncSession,
        *,
        authors_in: List[AuthorCreate]
    ) -> List[Author]:
        """Bulk create authors."""
        authors = []
        for author_in in authors_in:
            author, _ = await self.get_or_create(db, obj_in=author_in)
            authors.append(author)
        return authors
    
    async def count_by_platform(
        self,
        db: AsyncSession
    ) -> Dict[str, int]:
        """Count authors by platform."""
        query = (
            select(Author.platform, func.count(Author.id))
            .group_by(Author.platform)
        )
        result = await db.execute(query)
        return {row[0]: row[1] for row in result.all()}


# Create singleton instance
author = CRUDAuthor(Author)
