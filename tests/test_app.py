import pytest


@pytest.mark.asyncio
async def test_main_route(ac):
    response = await ac.get("http://test")
    assert response.status_code == 200