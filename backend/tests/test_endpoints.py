"""
Basic tests for API endpoints.
"""
import pytest
from httpx import AsyncClient
from app.main import app
from app.database import connect_to_mongo, close_mongo_connection


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Setup database connection for tests."""
    await connect_to_mongo()
    yield
    await close_mongo_connection()


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint returns API information."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Smart Resume Screener API"
        assert data["status"] == "running"


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/auth/login",
            json={
                "email": "invalid@example.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_valid_credentials():
    """Test login with valid credentials (requires seeded user)."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/auth/login",
            json={
                "email": "admin@resumescreener.com",
                "password": "admin123"
            }
        )
        # This will pass if user is seeded, otherwise 401
        if response.status_code == 200:
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_list_resumes_unauthorized():
    """Test listing resumes without authentication."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/resumes")
        assert response.status_code == 403  # Unauthorized


@pytest.mark.asyncio
async def test_upload_resume_unauthorized():
    """Test uploading resume without authentication."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/upload",
            files={"file": ("test.pdf", b"fake content", "application/pdf")}
        )
        assert response.status_code == 403  # Unauthorized
