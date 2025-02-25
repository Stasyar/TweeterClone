import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient

from core.models import Base

from fastapi.testclient import TestClient

from core.models import db_helper
from app.main import app
from core.models.fill_bd import insert_data


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Предоставляет сессию базы данных для тестов."""
    async with db_helper.engine.begin() as conn:

        await conn.run_sync(Base.metadata.drop_all)
        print("Данные очищены")

        await conn.run_sync(Base.metadata.create_all)
        print("Данные созданы")

        await insert_data(conn)
        print("Данные вставлены")
        await conn.commit()

        yield


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        print("Тестовый клиент создан")
        yield c
