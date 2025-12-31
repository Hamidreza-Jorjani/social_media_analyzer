import pytest
from httpx import AsyncClient


class TestHealthEndpoint:
    """Tests for health check endpoint."""
    
    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient):
        """Test health check endpoint."""
        response = await client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestRootEndpoint:
    """Tests for root endpoint."""
    
    @pytest.mark.asyncio
    async def test_root(self, client: AsyncClient):
        """Test root endpoint."""
        response = await client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data


class TestAuthEndpoints:
    """Tests for authentication endpoints."""
    
    @pytest.mark.asyncio
    async def test_register(self, client: AsyncClient):
        """Test user registration."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "NewPass123!",
                "full_name": "New User"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert "tokens" in data
        assert data["user"]["email"] == "newuser@example.com"
    
    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client: AsyncClient, test_user):
        """Test registration with duplicate email."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": test_user.email,
                "username": "different",
                "password": "Password123!"
            }
        )
        
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    async def test_login(self, client: AsyncClient, test_user):
        """Test user login."""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": "TestPass123!"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "tokens" in data
        assert "access_token" in data["tokens"]
    
    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client: AsyncClient, test_user):
        """Test login with wrong password."""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": "WrongPassword!"
            }
        )
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_get_me(self, client: AsyncClient, auth_headers: dict):
        """Test get current user."""
        response = await client.get(
            "/api/v1/auth/me",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
    
    @pytest.mark.asyncio
    async def test_get_me_unauthorized(self, client: AsyncClient):
        """Test get current user without auth."""
        response = await client.get("/api/v1/auth/me")
        
        assert response.status_code == 403


class TestUserEndpoints:
    """Tests for user endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_users_admin(self, client: AsyncClient, admin_auth_headers: dict):
        """Test getting users as admin."""
        response = await client.get(
            "/api/v1/users",
            headers=admin_auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @pytest.mark.asyncio
    async def test_get_users_non_admin(self, client: AsyncClient, auth_headers: dict):
        """Test getting users as non-admin."""
        response = await client.get(
            "/api/v1/users",
            headers=auth_headers
        )
        
        assert response.status_code == 403


class TestPostEndpoints:
    """Tests for post endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_posts(self, client: AsyncClient, auth_headers: dict):
        """Test getting posts."""
        response = await client.get(
            "/api/v1/posts",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @pytest.mark.asyncio
    async def test_create_post(self, client: AsyncClient, analyst_auth_headers: dict):
        """Test creating post."""
        response = await client.post(
            "/api/v1/posts",
            headers=analyst_auth_headers,
            json={
                "platform_id": "api_test_post",
                "platform": "twitter",
                "content": "Test post content",
                "language": "fa"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["platform_id"] == "api_test_post"
    
    @pytest.mark.asyncio
    async def test_get_post_stats(self, client: AsyncClient, auth_headers: dict):
        """Test getting post statistics."""
        response = await client.get(
            "/api/v1/posts/stats",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "total" in data


class TestAnalysisEndpoints:
    """Tests for analysis endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_analyses(self, client: AsyncClient, auth_headers: dict):
        """Test getting analyses."""
        response = await client.get(
            "/api/v1/analysis",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @pytest.mark.asyncio
    async def test_create_analysis(self, client: AsyncClient, analyst_auth_headers: dict):
        """Test creating analysis."""
        response = await client.post(
            "/api/v1/analysis",
            headers=analyst_auth_headers,
            json={
                "name": "Test Analysis",
                "description": "Test description",
                "analysis_type": "sentiment"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Analysis"


class TestTrendEndpoints:
    """Tests for trend endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_trends(self, client: AsyncClient, auth_headers: dict):
        """Test getting trends."""
        response = await client.get(
            "/api/v1/trends",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @pytest.mark.asyncio
    async def test_get_trending_hashtags(self, client: AsyncClient, auth_headers: dict):
        """Test getting trending hashtags."""
        response = await client.get(
            "/api/v1/trends/hashtags",
            headers=auth_headers
        )
        
        assert response.status_code == 200


class TestDashboardEndpoints:
    """Tests for dashboard endpoints."""
    
    @pytest.mark.asyncio
    async def test_get_overview(self, client: AsyncClient, auth_headers: dict):
        """Test getting dashboard overview."""
        response = await client.get(
            "/api/v1/dashboard/overview",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "posts" in data
    
    @pytest.mark.asyncio
    async def test_get_sentiment_overview(self, client: AsyncClient, auth_headers: dict):
        """Test getting sentiment overview."""
        response = await client.get(
            "/api/v1/dashboard/sentiment",
            headers=auth_headers
        )
        
        assert response.status_code == 200
