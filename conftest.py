import pytest

from fastapi.testclient import TestClient
from core.models import Base, DBHelper, db_helper
from app.main import app
from fill_bd import users, follows
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@test_db:5433/test_db"

test_db_helper = DBHelper(url=TEST_DATABASE_URL, echo=True)
app.dependency_overrides[db_helper] = test_db_helper

@pytest.fixture
def prepare_db():
    Base.metadata.create_all(test_db_helper.engine)
    print("\nБаза данных для тестов создана и подключена.")

    yield

    Base.metadata.drop_all(test_db_helper.engine)
    print("\nБаза данных для тестов удалена.")


@pytest.fixture
def db_session():
    session = test_db_helper.session()

    yield session

    session.close()


@pytest.fixture
def client():

    with TestClient(app) as c:
        yield c
