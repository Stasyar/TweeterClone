from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from core.models import User, Tweet, Like, Follow


async def get_user_by_key(session: sessionmaker[AsyncSession], api_key: str) -> User:
    async with session() as async_session:
        result = await async_session.execute(select(User).where(User.api_key == api_key))
        user = result.scalars().first()

        if not user:
            user = User(api_key=api_key)
            async_session.add(user)
            await async_session.commit()
            await async_session.refresh(user)

        return user


async def get_users(session: sessionmaker[AsyncSession]) -> Sequence[User] | None:

    async with session() as async_session:
        result = await async_session.execute(select(User))
        return result.scalars().all()


# async def post_user(session: sessionmaker[AsyncSession], user: User) -> int:
#     async with session() as async_session:
#         async_session.add(user)
#         await async_session.commit()
#         await async_session.refresh(user)
#         return user.id


async def get_tweet_by_id(session: sessionmaker[AsyncSession], tweet_id: int) -> Tweet:
    async with session() as async_session:
        result = await async_session.execute(select(Tweet).where(Tweet.id == tweet_id))
        return result.scalars().first()


async def post_tweet(session: sessionmaker[AsyncSession], tweet: Tweet) -> int:
    async with session() as async_session:
        async_session.add(tweet)
        await async_session.commit()
        await async_session.refresh(tweet)
        return tweet.id


async def delete_tweet(session: sessionmaker[AsyncSession], tweet_id: int) -> bool:
    """Function deletes the tweet"""
    async with session() as async_session:
        result = await async_session.execute(select(Tweet).where(Tweet.id == tweet_id))
        tweet = result.scalars().first()
    if not tweet:
        raise ValueError("Tweet not found")

    await async_session.delete(tweet)
    await async_session.commit()
    return True


async def like_tweet(session: sessionmaker[AsyncSession], tweet_id: int, user_id: int) -> bool:
    async with session() as async_session:
        like: Like = Like(user_id=user_id, tweet_id=tweet_id)
        async_session.add(like)
        await async_session.commit()
        return True


async def delete_like_tweet(session: sessionmaker[AsyncSession], tweet_id: int, user_id: int) -> bool:
    async with session() as async_session:
        result = await async_session.execute(select(Like).where(
            Like.tweet_id == tweet_id,
            Like.user_id == user_id))

        like = result.scalars().first()

        if like:
            await async_session.delete(like)
            await async_session.commit()
            return True


async def follow(session: sessionmaker[AsyncSession], follower_id: int, following_id: int) -> bool:
    async with session() as async_session:
        follow_: Follow = Follow(follower_id=follower_id, following_id=following_id)
        async_session.add(follow_)
        await async_session.commit()
        return True


async def unfollow(session: sessionmaker[AsyncSession], follower_id: int, following_id: int) -> bool:
    async with session() as async_session:
        result = await async_session.execute(select(Follow).where(
            Follow.follower_id == follower_id,
            Follow.following_id == following_id))
        follow_ = result.scalars().first()

        if follow_:
            await async_session.delete(follow_)
            await async_session.commit()
            return True
