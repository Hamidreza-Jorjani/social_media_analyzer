import pytest
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.models.data_source import DataSource, SourcePlatform
from app.models.author import Author
from app.models.post import Post
from app.models.analysis import Analysis, AnalysisType, AnalysisStatus
from app.core.security import hash_password


class TestUserModel:
    """Tests for User model."""
    
    @pytest.mark.asyncio
    async def test_create_user(self, db_session: AsyncSession):
        """Test user creation."""
        user = User(
            email="new@example.com",
            username="newuser",
            hashed_password=hash_password("Password123!"),
            full_name="New User",
            is_active=True,
            is_superuser=False,
            role=UserRole.VIEWER
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        assert user.id is not None
        assert user.email == "new@example.com"
        assert user.username == "newuser"
        assert user.role == UserRole.VIEWER
    
    @pytest.mark.asyncio
    async def test_user_role_enum(self, db_session: AsyncSession):
        """Test user roles."""
        assert UserRole.ADMIN.value == "admin"
        assert UserRole.ANALYST.value == "analyst"
        assert UserRole.VIEWER.value == "viewer"


class TestDataSourceModel:
    """Tests for DataSource model."""
    
    @pytest.mark.asyncio
    async def test_create_data_source(self, db_session: AsyncSession):
        """Test data source creation."""
        source = DataSource(
            name="Test Source",
            platform=SourcePlatform.TWITTER,
            description="Test description",
            is_active=True
        )
        db_session.add(source)
        await db_session.commit()
        await db_session.refresh(source)
        
        assert source.id is not None
        assert source.name == "Test Source"
        assert source.platform == SourcePlatform.TWITTER
    
    @pytest.mark.asyncio
    async def test_platform_enum(self, db_session: AsyncSession):
        """Test platform types."""
        assert SourcePlatform.TWITTER.value == "twitter"
        assert SourcePlatform.TELEGRAM.value == "telegram"
        assert SourcePlatform.INSTAGRAM.value == "instagram"


class TestAuthorModel:
    """Tests for Author model."""
    
    @pytest.mark.asyncio
    async def test_create_author(self, db_session: AsyncSession):
        """Test author creation."""
        author = Author(
            platform_id="user123",
            platform="twitter",
            username="testauthor",
            display_name="Test Author",
            followers_count=1000,
            following_count=500
        )
        db_session.add(author)
        await db_session.commit()
        await db_session.refresh(author)
        
        assert author.id is not None
        assert author.platform_id == "user123"
        assert author.username == "testauthor"


class TestPostModel:
    """Tests for Post model."""
    
    @pytest.mark.asyncio
    async def test_create_post(self, db_session: AsyncSession):
        """Test post creation."""
        post = Post(
            platform_id="post123",
            platform="twitter",
            content="Test content #test",
            language="fa",
            likes_count=10,
            hashtags=["test"],
            is_processed=False
        )
        db_session.add(post)
        await db_session.commit()
        await db_session.refresh(post)
        
        assert post.id is not None
        assert post.platform_id == "post123"
        assert post.content == "Test content #test"
        assert post.hashtags == ["test"]
    
    @pytest.mark.asyncio
    async def test_post_with_author(self, db_session: AsyncSession):
        """Test post with author relationship."""
        # Create author
        author = Author(
            platform_id="author123",
            platform="twitter",
            username="author"
        )
        db_session.add(author)
        await db_session.commit()
        await db_session.refresh(author)
        
        # Create post with author
        post = Post(
            platform_id="post456",
            platform="twitter",
            content="Post with author",
            author_id=author.id
        )
        db_session.add(post)
        await db_session.commit()
        await db_session.refresh(post)
        
        assert post.author_id == author.id


class TestAnalysisModel:
    """Tests for Analysis model."""
    
    @pytest.mark.asyncio
    async def test_create_analysis(self, db_session: AsyncSession, test_user: User):
        """Test analysis creation."""
        analysis = Analysis(
            name="Test Analysis",
            description="Test description",
            analysis_type=AnalysisType.SENTIMENT,
            status=AnalysisStatus.PENDING,
            user_id=test_user.id
        )
        db_session.add(analysis)
        await db_session.commit()
        await db_session.refresh(analysis)
        
        assert analysis.id is not None
        assert analysis.name == "Test Analysis"
        assert analysis.status == AnalysisStatus.PENDING
    
    @pytest.mark.asyncio
    async def test_analysis_status_enum(self, db_session: AsyncSession):
        """Test analysis status values."""
        assert AnalysisStatus.PENDING.value == "pending"
        assert AnalysisStatus.PROCESSING.value == "processing"
        assert AnalysisStatus.COMPLETED.value == "completed"
        assert AnalysisStatus.FAILED.value == "failed"
