from typing import Optional, List
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password, verify_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD operations for User model."""
    
    async def get_by_email(
        self,
        db: AsyncSession,
        *,
        email: str
    ) -> Optional[User]:
        """Get user by email."""
        query = select(User).where(User.email == email.lower())
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_username(
        self,
        db: AsyncSession,
        *,
        username: str
    ) -> Optional[User]:
        """Get user by username."""
        query = select(User).where(User.username == username.lower())
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_email_or_username(
        self,
        db: AsyncSession,
        *,
        identifier: str
    ) -> Optional[User]:
        """Get user by email or username."""
        identifier_lower = identifier.lower()
        query = select(User).where(
            or_(
                User.email == identifier_lower,
                User.username == identifier_lower
            )
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: UserCreate
    ) -> User:
        """Create a new user with hashed password."""
        db_obj = User(
            email=obj_in.email.lower(),
            username=obj_in.username.lower(),
            hashed_password=hash_password(obj_in.password),
            full_name=obj_in.full_name,
            is_active=True,
            is_superuser=False,
            role=UserRole.VIEWER
        )
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def create_superuser(
        self,
        db: AsyncSession,
        *,
        obj_in: UserCreate
    ) -> User:
        """Create a superuser."""
        db_obj = User(
            email=obj_in.email.lower(),
            username=obj_in.username.lower(),
            hashed_password=hash_password(obj_in.password),
            full_name=obj_in.full_name,
            is_active=True,
            is_superuser=True,
            role=UserRole.ADMIN
        )
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj
    
    async def authenticate(
        self,
        db: AsyncSession,
        *,
        identifier: str,
        password: str
    ) -> Optional[User]:
        """Authenticate user by email/username and password."""
        user = await self.get_by_email_or_username(db, identifier=identifier)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    async def update_password(
        self,
        db: AsyncSession,
        *,
        user: User,
        new_password: str
    ) -> User:
        """Update user password."""
        user.hashed_password = hash_password(new_password)
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user
    
    async def activate(
        self,
        db: AsyncSession,
        *,
        user: User
    ) -> User:
        """Activate a user account."""
        user.is_active = True
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user
    
    async def deactivate(
        self,
        db: AsyncSession,
        *,
        user: User
    ) -> User:
        """Deactivate a user account."""
        user.is_active = False
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user
    
    async def get_active_users(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Get all active users."""
        query = (
            select(User)
            .where(User.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())
    
    async def get_by_role(
        self,
        db: AsyncSession,
        *,
        role: UserRole,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Get users by role."""
        query = (
            select(User)
            .where(User.role == role)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())


# Create singleton instance
user = CRUDUser(User)
