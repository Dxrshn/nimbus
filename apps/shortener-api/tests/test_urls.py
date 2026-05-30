import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from src.main import app
from src.database import get_db


async def override_get_db():
    mock_db = AsyncMock()
    yield mock_db


@pytest.mark.asyncio
async def test_shorten_url():
    mock_result = {"short_code": "abc123", "short_url": "http://test/r/abc123"}

    app.dependency_overrides[get_db] = override_get_db
    with patch("src.routes.urls.create_short_url", return_value=mock_result), \
         patch("src.routes.urls.set_cached_url", new_callable=AsyncMock):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/api/v1/shorten", json={"url": "https://github.com"})
    app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json()["short_code"] == "abc123"


@pytest.mark.asyncio
async def test_shorten_url_invalid():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/shorten", json={"url": "not-a-url"})

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_urls():
    app.dependency_overrides[get_db] = override_get_db
    with patch("src.routes.urls.get_all_urls", return_value=[]):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/v1/urls")
    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_delete_url_not_found():
    app.dependency_overrides[get_db] = override_get_db
    with patch("src.routes.urls.get_url_by_short_code", return_value=None), \
         patch("src.routes.urls.delete_url", return_value=False):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.delete(f"/api/v1/urls/{uuid4()}")
    app.dependency_overrides.clear()

    assert response.status_code == 404
