from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from core.models import User


async def get_users(session: sessionmaker[AsyncSession]) -> Sequence[User] | None:

    async with session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()


async def post_user(session: sessionmaker[AsyncSession], user: User):
    async with session() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user.id


async def post_tweet(session: AsyncSession, tweet_data: str, media: list):

    pass
