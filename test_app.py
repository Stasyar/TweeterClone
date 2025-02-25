import pytest

from good_response import get_user, get_result, get_user_after_follow_test


@pytest.mark.asyncio
async def test_main_route(client):
    response = client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_me(client, db_session):
    """Проверяем, данные при запросе нашего профиля."""
    response = client.get("/api/users/me", headers={"api-key": "test_1"})
    user_data = response.json()
    assert response.status_code == 200
    assert user_data == get_user


@pytest.mark.asyncio
async def test_get_user_by_id(client, db_session):
    """Проверяем, данные при запросе нашего профиля."""
    response = client.get("/api/users/1")
    user_data = response.json()
    assert response.status_code == 200
    assert user_data == get_user


@pytest.mark.asyncio
async def test_follow(client, db_session):
    """Проверяем, данные при запросе нашего профиля."""
    response = client.get("/api/users/1/follow", headers={"api-key": "test_3_follow"})
    user_data = response.json()
    assert response.status_code == 200
    assert user_data == get_result
    response = client.get("/api/users/me", headers={"api-key": "test_1"})
    user_data = response.json()
    assert response.status_code == 200
    assert user_data == get_user_after_follow_test



