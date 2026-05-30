import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch

from src.main import app
from src.database import get_db


async def override_get_db():
    mock_db = AsyncMock()
    yield mock_db


@pytest.mark.asyncio
async def test_liveness():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_readiness_healthy():
    app.dependency_overrides[get_db] = override_get_db
    with patch("src.routes.health.redis_ping", return_value=True):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/ready")
    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_readiness_db_down():
    async def broken_db():
        mock_db = AsyncMock()
        mock_db.execute = AsyncMock(side_effect=Exception("db down"))
        yield mock_db

    app.dependency_overrides[get_db] = broken_db
    with patch("src.routes.health.redis_ping", return_value=True):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/ready")
    app.dependency_overrides.clear()

    assert response.json()["status"] == "error"
    assert response.json()["checks"]["database"] == "error"
