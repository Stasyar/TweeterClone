import pytest

from good_response import get_user


@pytest.mark.asyncio
async def test_main_route(client):
    response = client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_me(client, prepare_db, db_session):
    """Проверяем, данные при запросе нашего профиля."""
    response = client.get("/api/users/me", headers={"api-key": "test_1"})
    user_data = response.json()
    assert response.status_code == 200
    assert user_data == get_user
