import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import user as user_crud
from app.crud import post as post_crud
from app.crud import author as author_crud
from app.crud import data_source as data_source_crud
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.post import PostCreate, PostFilter
from app.schemas.author import AuthorCreate
from app.schemas.data_source import DataSourceCreate
from app.models.user import UserRole
from app.models.data_source import SourcePlatform


class TestUserCRUD:
    """Tests for User CRUD operations."""
    
    @pytest.mark.asyncio
    async def test_create_user(self, db_session: AsyncSession):
        """Test user creation."""
        user_in = UserCreate(
            email="crud@example.com",
            username="cruduser",
            password="CrudPass123!",
            full_name="CRUD User"
        )
        user = await user_crud.create(db_session, obj_in=user_in)
        
        assert user.id is not None
        assert user.email == "crud@example.com"
        assert user.username == "cruduser"
    
    @pytest.mark.asyncio
    async def test_get_user(self, db_session: AsyncSession, test_user):
        """Test getting user by ID."""
        user = await user_crud.get(db_session, test_user.id)
        
        assert user is not None
        assert user.id == test_user.id
    
    @pytest.mark.asyncio
    async def test_get_by_email(self, db_session: AsyncSession, test_user):
        """Test getting user by email."""
        user = await user_crud.get_by_email(db_session, email=test_user.email)
        
        assert user is not None
        assert user.email == test_user.email
    
    @pytest.mark.asyncio
    async def test_get_by_username(self, db_session: AsyncSession, test_user):
        """Test getting user by username."""
        user = await user_crud.get_by_username(db_session, username=test_user.username)
        
        assert user is not None
        assert user.username == test_user.username
    
    @pytest.mark.asyncio
    async def test_authenticate(self, db_session: AsyncSession):
        """Test user authentication."""
        # Create user first
        user_in = UserCreate(
            email="auth@example.com",
            username="authuser",
            password="AuthPass123!"
        )
        await user_crud.create(db_session, obj_in=user_in)
        
        # Test authentication
        user = await user_crud.authenticate(
            db_session,
            identifier="authuser",
            password="AuthPass123!"
        )
        
        assert user is not None
        assert user.username == "authuser"
    
    @pytest.mark.asyncio
    async def test_authenticate_wrong_password(self, db_session: AsyncSession, test_user):
        """Test authentication with wrong password."""
        user = await user_crud.authenticate(
            db_session,
            identifier=test_user.username,
            password="WrongPassword!"
        )
        
        assert user is None
    
    @pytest.mark.asyncio
    async def test_update_user(self, db_session: AsyncSession, test_user):
        """Test user update."""
        update_data = UserUpdate(full_name="Updated Name")
        updated = await user_crud.update(
            db_session,
            db_obj=test_user,
            obj_in=update_data
        )
        
        assert updated.full_name == "Updated Name"


class TestPostCRUD:
    """Tests for Post CRUD operations."""
    
    @pytest.mark.asyncio
    async def test_create_post(self, db_session: AsyncSession):
        """Test post creation."""
        post_in = PostCreate(
            platform_id="test_post_1",
            platform="twitter",
            content="Test content",
            language="fa"
        )
        post = await post_crud.create(db_session, obj_in=post_in)
        
        assert post.id is not None
        assert post.platform_id == "test_post_1"
    
    @pytest.mark.asyncio
    async def test_get_by_platform_id(self, db_session: AsyncSession):
        """Test getting post by platform ID."""
        post_in = PostCreate(
            platform_id="unique_post_123",
            platform="twitter",
            content="Content"
        )
        created = await post_crud.create(db_session, obj_in=post_in)
        
        post = await post_crud.get_by_platform_id(
            db_session,
            platform_id="unique_post_123"
        )
        
        assert post is not None
        assert post.id == created.id
    
    @pytest.mark.asyncio
    async def test_get_or_create_existing(self, db_session: AsyncSession):
        """Test get_or_create with existing post."""
        post_in = PostCreate(
            platform_id="existing_post",
            platform="twitter",
            content="Original"
        )
        original = await post_crud.create(db_session, obj_in=post_in)
        
        post, created = await post_crud.get_or_create(db_session, obj_in=post_in)
        
        assert created is False
        assert post.id == original.id
    
    @pytest.mark.asyncio
    async def test_get_filtered(self, db_session: AsyncSession):
        """Test filtered post retrieval."""
        # Create posts
        for i in range(5):
            post_in = PostCreate(
                platform_id=f"filter_post_{i}",
                platform="twitter",
                content=f"Content {i}",
                language="fa"
            )
            await post_crud.create(db_session, obj_in=post_in)
        
        # Filter
        filters = PostFilter(platform="twitter", language="fa")
        posts = await post_crud.get_filtered(db_session, filters=filters)
        
        assert len(posts) >= 5
    
    @pytest.mark.asyncio
    async def test_mark_processed(self, db_session: AsyncSession):
        """Test marking post as processed."""
        post_in = PostCreate(
            platform_id="process_test",
            platform="twitter",
            content="Content"
        )
        post = await post_crud.create(db_session, obj_in=post_in)
        
        updated = await post_crud.mark_processed(db_session, post_id=post.id)
        
        assert updated.is_processed is True


class TestAuthorCRUD:
    """Tests for Author CRUD operations."""
    
    @pytest.mark.asyncio
    async def test_create_author(self, db_session: AsyncSession):
        """Test author creation."""
        author_in = AuthorCreate(
            platform_id="author_test_1",
            platform="twitter",
            username="testauthor"
        )
        author = await author_crud.create(db_session, obj_in=author_in)
        
        assert author.id is not None
        assert author.username == "testauthor"
    
    @pytest.mark.asyncio
    async def test_get_or_create(self, db_session: AsyncSession):
        """Test get_or_create for author."""
        author_in = AuthorCreate(
            platform_id="unique_author",
            platform="twitter",
            username="uniqueauthor"
        )
        
        # First call should create
        author1, created1 = await author_crud.get_or_create(db_session, obj_in=author_in)
        assert created1 is True
        
        # Second call should get existing
        author2, created2 = await author_crud.get_or_create(db_session, obj_in=author_in)
        assert created2 is False
        assert author1.id == author2.id
    
    @pytest.mark.asyncio
    async def test_search(self, db_session: AsyncSession):
        """Test author search."""
        author_in = AuthorCreate(
            platform_id="search_author",
            platform="twitter",
            username="searchable_user"
        )
        await author_crud.create(db_session, obj_in=author_in)
        
        results = await author_crud.search(db_session, query_str="searchable")
        
        assert len(results) >= 1


class TestDataSourceCRUD:
    """Tests for DataSource CRUD operations."""
    
    @pytest.mark.asyncio
    async def test_create_data_source(self, db_session: AsyncSession):
        """Test data source creation."""
        source_in = DataSourceCreate(
            name="Test Source",
            platform=SourcePlatform.TWITTER,
            description="Test"
        )
        source = await data_source_crud.create(db_session, obj_in=source_in)
        
        assert source.id is not None
        assert source.name == "Test Source"
    
    @pytest.mark.asyncio
    async def test_get_active(self, db_session: AsyncSession):
        """Test getting active data sources."""
        source_in = DataSourceCreate(
            name="Active Source",
            platform=SourcePlatform.TELEGRAM
        )
        await data_source_crud.create(db_session, obj_in=source_in)
        
        sources = await data_source_crud.get_active(db_session)
        
        assert len(sources) >= 1
