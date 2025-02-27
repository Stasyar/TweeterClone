from tests.good_response import (
    get_result,
    get_user,
    get_user_after_follow_test,
    get_user_after_unfollow_test,
)


async def test_get_me(ac):
    """Проверяем данные при запросе нашего профиля."""
    response = await ac.get("/api/users/me", headers={"api-key": "test_1"})
    user_data = response.json()
    assert response.status_code == 200
    assert user_data == get_user


async def test_get_user_by_id(ac):
    """Проверяем данные при запросе профиля по id."""
    response = await ac.get("/api/users/1")
    user_data = response.json()
    assert response.status_code == 200
    assert user_data == get_user


async def test_follow(ac):
    """Проверяем данные при отправлении запроса на подписку."""
    response = await ac.post(
        "/api/users/1/follow", headers={"api-key": "test_3_follow"}
    )
    user_data = response.json()
    assert response.status_code == 200
    assert user_data == get_result
    response = await ac.get("/api/users/me", headers={"api-key": "test_1"})
    user_data = response.json()
    assert response.status_code == 200
    assert user_data == get_user_after_follow_test


async def test_unfollow(ac):
    """Проверяем данные при отписке."""
    response = await ac.delete(
        "/api/users/1/follow", headers={"api-key": "test_2"}
    )
    user_data = response.json()
    assert response.status_code == 200
    assert user_data == get_result
    response = await ac.get("/api/users/me", headers={"api-key": "test_1"})
    user_data = response.json()
    assert response.status_code == 200
    assert user_data == get_user_after_unfollow_test
