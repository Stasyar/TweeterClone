import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def client():
    return AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    )


@pytest.mark.asyncio
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hello"}


@pytest.mark.asyncio
async def test_root2(client):
    response = await client.post(
        "/tweet",
        json={"tweet_data": "hello tweet"},
    )
    assert response.status_code == 201
    assert response.json() == {"result": True, "tweet_id": 123}
