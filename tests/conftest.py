import pytest
from core_test import db_url
from httpx import ASGITransport, AsyncClient

from app.app_factory import create_app


@pytest.fixture(scope="function")
def app():
    return create_app(database_url=db_url)


@pytest.fixture
def client():
    return AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    )
