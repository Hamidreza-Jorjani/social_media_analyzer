import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate, UserUpdate
from app.schemas.post import PostCreate, PostFilter
from app.schemas.analysis import AnalysisCreate, AnalysisConfig
from app.models.analysis import AnalysisType


class TestUserSchemas:
    """Tests for User schemas."""
    
    def test_user_create_valid(self):
        """Test valid user creation schema."""
        user = UserCreate(
            email="test@example.com",
            username="testuser",
            password="Password123!",
            full_name="Test User"
        )
        
        assert user.email == "test@example.com"
        assert user.username == "testuser"
    
    def test_user_create_invalid_email(self):
        """Test user creation with invalid email."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="invalid-email",
                username="testuser",
                password="Password123!"
            )
    
    def test_user_create_short_username(self):
        """Test user creation with short username."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@example.com",
                username="ab",
                password="Password123!"
            )
    
    def test_user_create_weak_password(self):
        """Test user creation with weak password."""
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@example.com",
                username="testuser",
                password="weak"
            )
    
    def test_user_update_partial(self):
        """Test partial user update."""
        update = UserUpdate(full_name="Updated Name")
        
        assert update.full_name == "Updated Name"
        assert update.email is None


class TestPostSchemas:
    """Tests for Post schemas."""
    
    def test_post_create_valid(self):
        """Test valid post creation."""
        post = PostCreate(
            platform_id="post123",
            platform="twitter",
            content="Test content",
            language="fa"
        )
        
        assert post.platform_id == "post123"
        assert post.platform == "twitter"
    
    def test_post_create_with_hashtags(self):
        """Test post creation with hashtags."""
        post = PostCreate(
            platform_id="post123",
            platform="twitter",
            content="Content",
            hashtags=["test", "python"]
        )
        
        assert len(post.hashtags) == 2
    
    def test_post_filter(self):
        """Test post filter schema."""
        filter = PostFilter(
            platform="twitter",
            language="fa",
            is_processed=False
        )
        
        assert filter.platform == "twitter"
        assert filter.is_processed is False


class TestAnalysisSchemas:
    """Tests for Analysis schemas."""
    
    def test_analysis_create_valid(self):
        """Test valid analysis creation."""
        analysis = AnalysisCreate(
            name="Test Analysis",
            description="Test",
            analysis_type=AnalysisType.SENTIMENT
        )
        
        assert analysis.name == "Test Analysis"
        assert analysis.analysis_type == AnalysisType.SENTIMENT
    
    def test_analysis_config_defaults(self):
        """Test analysis config defaults."""
        config = AnalysisConfig()
        
        assert config.sentiment_enabled is True
        assert config.emotion_enabled is True
        assert config.num_topics == 10
    
    def test_analysis_config_custom(self):
        """Test custom analysis config."""
        config = AnalysisConfig(
            sentiment_enabled=False,
            num_topics=20
        )
        
        assert config.sentiment_enabled is False
        assert config.num_topics == 20
