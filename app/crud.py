from typing import Optional, Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.schemas import LikesSchema
from app.schemas.get_all_tweets import AuthorSchema
from core.models import Follow, Like, Media, Tweet, User


async def check_user(
    session: sessionmaker[AsyncSession], api_key: str,
) -> Optional[User]:
    async with session() as async_session:

        try:
            result = await async_session.execute(
                select(User).where(User.api_key == api_key)
            )
            user = result.scalars().first()

            if user is None:
                user = User(api_key=api_key)
                async_session.add(user)
                await async_session.commit()
                await async_session.refresh(user)

            return user
        except Exception as e:
            print(f"Error during user check: {e}")
            return None


async def get_user_by_id(
    session: sessionmaker[AsyncSession], user_id: int
) -> Optional[User]:
    async with session() as async_session:

        result = await async_session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalars().first()

        if not user:
            raise HTTPException(404, "User not found")

        return user


async def get_followings(
    session: sessionmaker[AsyncSession], user_id: int
) -> Optional[Sequence[int]]:
    async with session() as async_session:
        result = await async_session.execute(
            select(Follow.following_id).where(Follow.follower_id == user_id)
        )

        return result.scalars().all()


async def get_followers(
    session: sessionmaker[AsyncSession], user_id: int
) -> Optional[Sequence[int]]:
    async with session() as async_session:
        result = await async_session.execute(
            select(Follow.follower_id).where(Follow.following_id == user_id)
        )

        return result.scalars().all()


async def get_likes(
    session: sessionmaker[AsyncSession], tweet_id: int
) -> [Sequence[LikesSchema]]:

    async with session() as async_session:
        result = await async_session.execute(
            select(Like.user_id).where(Like.tweet_id == tweet_id)
        )
        likes_user_ids = result.scalars().all()

        return [LikesSchema(user_id=us_id) for us_id in likes_user_ids]


async def get_tweets(
    session: sessionmaker[AsyncSession], user_id: int
) -> Optional[Sequence[Tweet]]:
    async with session() as async_session:
        result = await async_session.execute(
            select(Tweet).where(Tweet.author_id == user_id)
        )
        return result.scalars().all()


async def get_author_info(
    session: sessionmaker[AsyncSession], user_id: int
) -> AuthorSchema:

    async with session() as async_session:
        result = await async_session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalars().first()

        return AuthorSchema(id=user.id)


async def get_tweet_by_id(
    session: sessionmaker[AsyncSession], tweet_id: int
) -> Tweet:
    async with session() as async_session:
        result = await async_session.execute(
            select(Tweet).where(Tweet.id == tweet_id)
        )
        return result.scalars().first()


async def post_tweet(
    session: sessionmaker[AsyncSession], tweet: Tweet
) -> Tweet:
    async with session() as async_session:
        async_session.add(tweet)
        await async_session.commit()
        await async_session.refresh(tweet)
        return tweet


async def delete_tweet(
    session: sessionmaker[AsyncSession], tweet_id: int
) -> bool:
    """Function deletes the tweet"""
    async with session() as async_session:
        result = await async_session.execute(
            select(Tweet).where(Tweet.id == tweet_id)
        )
        tweet = result.scalars().first()
    if not tweet:
        raise ValueError("Tweet not found")

    await async_session.delete(tweet)
    await async_session.commit()
    return True


async def like_tweet(
    session: sessionmaker[AsyncSession], tweet_id: int, user_id: int
) -> bool:
    async with session() as async_session:
        like: Like = Like(user_id=user_id, tweet_id=tweet_id)
        async_session.add(like)
        await async_session.commit()
        return True


async def delete_like_tweet(
    session: sessionmaker[AsyncSession], tweet_id: int, user_id: int
) -> bool:
    async with session() as async_session:
        result = await async_session.execute(
            select(Like).where(
                Like.tweet_id == tweet_id, Like.user_id == user_id
            )
        )

        like = result.scalars().first()

        if like:
            await async_session.delete(like)
            await async_session.commit()
            return True
        else:
            return False


async def follow(
    session: sessionmaker[AsyncSession], follower_id: int, following_id: int
) -> bool:
    async with session() as async_session:
        follow_: Follow = Follow(
            follower_id=follower_id, following_id=following_id
        )
        if follow_:
            async_session.add(follow_)
            await async_session.commit()
            return True
        else:
            raise ValueError("Follow error")


async def unfollow(
    session: sessionmaker[AsyncSession], follower_id: int, following_id: int
) -> bool:
    async with session() as async_session:
        result = await async_session.execute(
            select(Follow).where(
                Follow.follower_id == follower_id,
                Follow.following_id == following_id,
            )
        )
        follow_ = result.scalars().first()

        if follow_:
            await async_session.delete(follow_)
            await async_session.commit()
            return True
        else:
            raise ValueError("Unfollow error")


async def upload_media(
    session: sessionmaker[AsyncSession], file_path: str
) -> int:
    async with session() as async_session:
        media = Media(filename=file_path)
        async_session.add(media)
        await async_session.commit()
        await async_session.refresh(media)

        return media.id


async def get_links(session: sessionmaker[AsyncSession], media_id: int) -> str:
    async with session() as async_session:
        result = await async_session.execute(
            select(Media.filename).where(Media.id == media_id)
        )
        res = result.scalars().first()
        return f"http://localhost/{res}"
