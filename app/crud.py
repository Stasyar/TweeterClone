from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from core.models import User, Tweet


async def get_user_by_key(session: sessionmaker[AsyncSession], api_key: str) -> User | None:

    async with session() as session:
        result = await session.execute(select(User).where(User.api_key == api_key))
        return result.scalars().first()


async def get_users(session: sessionmaker[AsyncSession]) -> Sequence[User] | None:

    async with session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()


async def post_user(session: sessionmaker[AsyncSession], user: User) -> int:
    async with session() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user.id


async def get_tweet_by_id(session: sessionmaker[AsyncSession], tweet_id: int) -> Tweet:
    async with session() as session:
        result = await session.execute(select(Tweet).where(Tweet.id == tweet_id))
        return result.scalars().first()


async def post_tweet(session: sessionmaker[AsyncSession], tweet: Tweet) -> int:
    async with session() as session:
        session.add(tweet)
        await session.commit()
        await session.refresh(tweet)
        return tweet.id


async def delete_tweet(session: sessionmaker[AsyncSession], tweet_id: int) -> bool:
    """Function deletes the tweet"""
    async with session() as session:
        result = await session.execute(select(Tweet).where(Tweet.id == tweet_id))
        tweet = result.scalars().first()
    if not tweet:
        raise ValueError("Tweet not found")

    await session.delete(tweet)
    await session.commit()
    return True
