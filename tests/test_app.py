import pytest


@pytest.mark.asyncio
async def test_root2(client):
    response = await client.post(
        "/tweet",
        json={"tweet_data": "hello tweet"},
    )
    assert response.status_code == 201
    assert response.json() == {"result": True, "tweet_id": 123}
