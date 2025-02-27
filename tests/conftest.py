from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.main import app
from core.models import Base, db_helper
from tests.fill_bd import insert_data

test_db_url = (
    "postgresql+asyncpg://postgres:postgres@localhost:5432/microservice"
)


test_engine = create_async_engine(test_db_url, poolclass=NullPool, echo=False)
test_async_session = async_sessionmaker(
    bind=test_engine, expire_on_commit=False
)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session() as session:
        yield session


app.dependency_overrides[db_helper.session_getter] = override_get_async_session


@pytest_asyncio.fixture(autouse=True, scope="function")
async def prepare_db():
    """
    Предоставляет сессию базы данных для тестов.
    """
    async with test_engine.begin() as conn:

        await conn.run_sync(Base.metadata.drop_all)
        print("Данные очищены")
        await conn.run_sync(Base.metadata.create_all)
        print("Данные созданы")

        await insert_data(conn)
        print("Данные вставлены")
        await conn.commit()

    yield


@pytest_asyncio.fixture(scope="function")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """
    Создаём асинхронный HTTP-клиент для выполнения тестов.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as async_test_client:
        yield async_test_client
