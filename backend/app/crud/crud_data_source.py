from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.data_source import DataSource, SourcePlatform
from app.schemas.data_source import DataSourceCreate, DataSourceUpdate


class CRUDDataSource(CRUDBase[DataSource, DataSourceCreate, DataSourceUpdate]):
    """CRUD operations for DataSource model."""
    
    async def get_by_name(
        self,
        db: AsyncSession,
        *,
        name: str
    ) -> Optional[DataSource]:
        """Get data source by name."""
        query = select(DataSource).where(DataSource.name == name)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_platform(
        self,
        db: AsyncSession,
        *,
        platform: SourcePlatform,
        skip: int = 0,
        limit: int = 100
    ) -> List[DataSource]:
        """Get data sources by platform."""
        query = (
            select(DataSource)
            .where(DataSource.platform == platform)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_active(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[DataSource]:
        """Get all active data sources."""
        query = (
            select(DataSource)
            .where(DataSource.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def activate(
        self,
        db: AsyncSession,
        *,
        db_obj: DataSource
    ) -> DataSource:
        """Activate a data source."""
        db_obj.is_active = True
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def deactivate(
        self,
        db: AsyncSession,
        *,
        db_obj: DataSource
    ) -> DataSource:
        """Deactivate a data source."""
        db_obj.is_active = False
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def update_last_sync(
        self,
        db: AsyncSession,
        *,
        db_obj: DataSource,
        sync_time: str
    ) -> DataSource:
        """Update last sync timestamp."""
        db_obj.last_sync_at = sync_time
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def get_stats(
        self,
        db: AsyncSession,
        *,
        data_source_id: int
    ) -> dict:
        """Get statistics for a data source."""
        from app.models.post import Post
        from app.models.author import Author
        
        # Count posts
        posts_query = (
            select(func.count())
            .select_from(Post)
            .where(Post.data_source_id == data_source_id)
        )
        posts_result = await db.execute(posts_query)
        total_posts = posts_result.scalar() or 0
        
        # Count unique authors
        authors_query = (
            select(func.count(func.distinct(Post.author_id)))
            .where(Post.data_source_id == data_source_id)
        )
        authors_result = await db.execute(authors_query)
        total_authors = authors_result.scalar() or 0
        
        return {
            "total_posts": total_posts,
            "total_authors": total_authors
        }


# Create singleton instance
data_source = CRUDDataSource(DataSource)
