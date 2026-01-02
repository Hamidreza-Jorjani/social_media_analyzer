"""
Initial data setup - runs on application startup.
Creates default admin user, data sources, etc.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from app.core.config import settings
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.models.data_source import DataSource


async def init_default_admin(db: AsyncSession) -> None:
    """Create default admin user if not exists."""
    
    # Check if admin exists
    result = await db.execute(
        select(User).where(User.username == settings.DEFAULT_ADMIN_USERNAME)
    )
    existing_admin = result.scalar_one_or_none()
    
    if existing_admin:
        logger.info(f"Admin user '{settings.DEFAULT_ADMIN_USERNAME}' already exists")
        return
    
    # Create admin user
    admin_user = User(
        email=settings.DEFAULT_ADMIN_EMAIL,
        username=settings.DEFAULT_ADMIN_USERNAME,
        hashed_password=hash_password(settings.DEFAULT_ADMIN_PASSWORD),
        full_name="System Administrator",
        is_active=True,
        is_superuser=True,
        role=UserRole.ADMIN
    )
    
    db.add(admin_user)
    await db.commit()
    
    logger.info(f"✅ Created default admin user: {settings.DEFAULT_ADMIN_USERNAME}")


async def init_default_data_sources(db: AsyncSession) -> None:
    """Create default data sources if not exist."""
    
    default_sources = [
        {
            "name": "Twitter Persian",
            "platform": "twitter",
            "description": "Persian Twitter/X data collection",
            "is_active": True
        },
        {
            "name": "Instagram Persian",
            "platform": "instagram",
            "description": "Persian Instagram data collection",
            "is_active": True
        },
        {
            "name": "Telegram Persian",
            "platform": "telegram",
            "description": "Persian Telegram channels and groups",
            "is_active": True
        }
    ]
    
    for source_data in default_sources:
        result = await db.execute(
            select(DataSource).where(
                DataSource.name == source_data["name"]
            )
        )
        existing = result.scalar_one_or_none()
        
        if not existing:
            source = DataSource(**source_data)
            db.add(source)
            logger.info(f"✅ Created data source: {source_data['name']}")
    
    await db.commit()


async def init_db_data(db: AsyncSession) -> None:
    """Initialize all default data."""
    logger.info("🔧 Initializing default data...")
    
    try:
        await init_default_admin(db)
        await init_default_data_sources(db)
        logger.info("✅ Default data initialization complete!")
    except Exception as e:
        logger.error(f"❌ Error initializing default data: {e}")
        raise
