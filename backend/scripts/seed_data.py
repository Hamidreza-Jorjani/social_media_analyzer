#!/usr/bin/env python3
"""
Seed database with sample data for development.
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import AsyncSessionLocal
from app.models import (
    User, UserRole, DataSource, SourcePlatform,
    Author, Post
)
from app.core.security import hash_password
from loguru import logger


# Sample Persian content
SAMPLE_CONTENTS = [
    "سلام به همه! امروز هوا خیلی خوبه 🌞 #تهران #هوا",
    "این فیلم واقعا عالی بود، پیشنهاد میکنم ببینید #سینما #فیلم",
    "خیلی ناراحتم از اتفاقات اخیر 😢 #اخبار",
    "موفقیت بزرگی برای تیم ملی! 🎉 #ورزش #فوتبال",
    "کتاب جدیدی خوندم، خیلی آموزنده بود #کتاب #مطالعه",
    "غذای امروز خیلی خوشمزه بود 😋 #آشپزی #غذا",
    "سفر به شیراز فوق‌العاده بود #سفر #شیراز #گردشگری",
    "تکنولوژی هر روز پیشرفت میکنه #تکنولوژی #هوش_مصنوعی",
    "بازار امروز خیلی شلوغ بود #اقتصاد #بازار",
    "موسیقی این خواننده عالیه 🎵 #موسیقی",
]

SAMPLE_USERNAMES = [
    "ali_tehrani", "maryam_sh", "hassan123", "fateme_r",
    "mohammad_k", "zahra_n", "reza_m", "sara_a"
]


async def seed_users():
    """Create sample users."""
    async with AsyncSessionLocal() as session:
        users = [
            User(
                email="analyst@example.com",
                username="analyst",
                hashed_password=hash_password("Analyst123!"),
                full_name="Data Analyst",
                is_active=True,
                is_superuser=False,
                role=UserRole.ANALYST
            ),
            User(
                email="viewer@example.com",
                username="viewer",
                hashed_password=hash_password("Viewer123!"),
                full_name="Report Viewer",
                is_active=True,
                is_superuser=False,
                role=UserRole.VIEWER
            )
        ]
        
        for user in users:
            session.add(user)
        
        await session.commit()
        logger.info(f"Created {len(users)} sample users")


async def seed_data_sources():
    """Create sample data sources."""
    async with AsyncSessionLocal() as session:
        sources = [
            DataSource(
                name="Twitter Persian",
                platform=SourcePlatform.TWITTER,
                description="Persian Twitter data collection",
                is_active=True
            ),
            DataSource(
                name="Telegram Channels",
                platform=SourcePlatform.TELEGRAM,
                description="Popular Persian Telegram channels",
                is_active=True
            ),
            DataSource(
                name="Instagram Influencers",
                platform=SourcePlatform.INSTAGRAM,
                description="Persian Instagram influencers",
                is_active=True
            )
        ]
        
        for source in sources:
            session.add(source)
        
        await session.commit()
        logger.info(f"Created {len(sources)} data sources")
        return sources


async def seed_authors():
    """Create sample authors."""
    async with AsyncSessionLocal() as session:
        authors = []
        
        for i, username in enumerate(SAMPLE_USERNAMES):
            author = Author(
                platform_id=f"user_{i+1}",
                platform="twitter",
                username=username,
                display_name=username.replace("_", " ").title(),
                followers_count=random.randint(100, 10000),
                following_count=random.randint(50, 500),
                posts_count=random.randint(10, 100)
            )
            authors.append(author)
            session.add(author)
        
        await session.commit()
        logger.info(f"Created {len(authors)} sample authors")
        return authors


async def seed_posts(authors, num_posts: int = 50):
    """Create sample posts."""
    async with AsyncSessionLocal() as session:
        posts = []
        
        for i in range(num_posts):
            content = random.choice(SAMPLE_CONTENTS)
            author = random.choice(authors)
            posted_at = datetime.utcnow() - timedelta(
                hours=random.randint(1, 168)
            )
            
            # Extract hashtags from content
            import re
            hashtags = re.findall(r'#(\w+)', content)
            
            post = Post(
                platform_id=f"post_{i+1}",
                platform="twitter",
                content=content,
                language="fa",
                likes_count=random.randint(0, 1000),
                comments_count=random.randint(0, 100),
                shares_count=random.randint(0, 50),
                posted_at=posted_at,
                hashtags=hashtags if hashtags else None,
                author_id=author.id,
                is_processed=False
            )
            posts.append(post)
            session.add(post)
        
        await session.commit()
        logger.info(f"Created {len(posts)} sample posts")


async def seed_database():
    """Seed database with sample data."""
    logger.info("Seeding database with sample data...")
    
    try:
        await seed_users()
        await seed_data_sources()
        authors = await seed_authors()
        await seed_posts(authors, num_posts=100)
        
        logger.info("Database seeding completed!")
    except Exception as e:
        logger.error(f"Database seeding failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(seed_database())
