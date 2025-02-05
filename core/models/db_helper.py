from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

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


db_helper = DBHelper(url=settings.db_url, echo=True)
