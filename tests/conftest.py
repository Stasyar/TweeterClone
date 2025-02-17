import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest_asyncio.fixture(scope="session")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as async_test_client:
        yield async_test_client


