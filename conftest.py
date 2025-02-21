import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from dotenv import load_dotenv

from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from core.models import Base, DBHelper, db_helper
from app.main import app
from fill_bd import insert_data


TEST_DATABASE_URL = f"postgresql+asyncpg://test:test@test_db:5433/test_db"


test_engine = create_async_engine(url=TEST_DATABASE_URL, echo=True)
test_session = async_sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    )


@pytest_asyncio.fixture(autouse=True, scope="session")
async def prepare_db():
    """Создаёт и очищает тестовую базу данных."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Тестовая база данных создана и подключена.")

        await insert_data(test_session)

        yield

        await conn.run_sync(Base.metadata.drop_all)
        await test_engine.engine.dispose()
    print("Соединение с тестовой базой данных закрыто.")


@pytest_asyncio.fixture(scope="session")
async def db_session():
    """Предоставляет сессию базы данных для тестов."""
    async with test_session() as session:
        yield session
        await session.close()


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_session() as session:
        yield session

app.dependency_overrides[db_helper.session_getter] = override_get_session
print("База данный переопределена")


@pytest.fixture
def client():

    with TestClient(app) as c:
        print("Тестовый клиент создан")
        yield c
