import pytest
from core.models import User


def test_main_route(client):
    response = client.get("/docs")
    assert response.status_code == 200


def test_user_exists(db_session):
    """Проверяем, что тестовые пользователи добавлены."""

