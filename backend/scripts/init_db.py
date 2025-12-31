#!/usr/bin/env python3
"""
Initialize database with tables and default data.
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_engine, AsyncSessionLocal, Base
from app.models import User, UserRole
from app.core.security import hash_password
from loguru import logger


async def create_tables():
    """Create all database tables."""
    from app.models import (
        User, DataSource, Author, Post,
        Analysis, AnalysisResult, Trend,
        GraphNode, GraphEdge, Dashboard
    )
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database tables created successfully")


async def create_superuser(
    email: str = "admin@example.com",
    username: str = "admin",
    password: str = "Admin123!"
):
    """Create default superuser."""
    async with AsyncSessionLocal() as session:
        from sqlalchemy import select
        
        # Check if user exists
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        existing = result.scalar_one_or_none()
        
        if existing:
            logger.info(f"Superuser '{username}' already exists")
            return
        
        # Create superuser
        user = User(
            email=email,
            username=username,
            hashed_password=hash_password(password),
            full_name="System Administrator",
            is_active=True,
            is_superuser=True,
            role=UserRole.ADMIN
        )
        
        session.add(user)
        await session.commit()
        
        logger.info(f"Superuser '{username}' created successfully")
        logger.info(f"  Email: {email}")
        logger.info(f"  Password: {password}")


async def init_db():
    """Initialize database."""
    logger.info("Initializing database...")
    
    try:
        await create_tables()
        await create_superuser()
        logger.info("Database initialization completed!")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(init_db())
