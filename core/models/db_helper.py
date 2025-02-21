from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.config import settings


class DBHelper:
    def __init__(self, url: str, echo: bool = False):

        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with db_helper.session() as async_session:
            yield async_session


db_helper = DBHelper(url=settings.db_url, echo=False)

