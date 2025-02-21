from typing import Optional, Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.schemas import LikesSchema
from app.schemas.get_all_tweets import AuthorSchema
from core.models import Follow, Like, Media, Tweet, User


async def check_user(
    session: AsyncSession, api_key: str,
) -> Optional[User]:

    try:
        result = await session.execute(
            select(User).where(User.api_key == api_key)
        )
        user = result.scalars().first()

        if user is None:
            user = User(api_key=api_key)
            session.add(user)
            await session.commit()
            await session.refresh(user)

        return user
    except Exception as e:
        print(f"Error during user check: {e}")
        return None


async def get_user_by_id(
    session: AsyncSession, user_id: int
) -> Optional[User]:

    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(404, "User not found")

    return user


async def get_followings(
    session: AsyncSession, user_id: int
) -> Optional[Sequence[int]]:

    result = await session.execute(
        select(Follow.following_id).where(Follow.follower_id == user_id)
    )

    return result.scalars().all()


async def get_followers(
    session: AsyncSession, user_id: int
) -> Optional[Sequence[int]]:

    result = await session.execute(
        select(Follow.follower_id).where(Follow.following_id == user_id)
    )

    return result.scalars().all()


async def get_likes(
    session: AsyncSession, tweet_id: int
) -> [Sequence[LikesSchema]]:

    result = await session.execute(
        select(Like.user_id).where(Like.tweet_id == tweet_id)
    )
    likes_user_ids = result.scalars().all()

    return [LikesSchema(user_id=us_id) for us_id in likes_user_ids]


async def get_tweets(
    session: AsyncSession, user_id: int
) -> Optional[Sequence[Tweet]]:

    result = await session.execute(
        select(Tweet).where(Tweet.author_id == user_id)
    )
    return result.scalars().all()


async def get_author_info(
    session: AsyncSession, user_id: int
) -> AuthorSchema:

    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().first()

    return AuthorSchema(id=user.id)


async def get_tweet_by_id(
    session: AsyncSession, tweet_id: int
) -> Tweet:
    result = await session.execute(
        select(Tweet).where(Tweet.id == tweet_id)
    )
    return result.scalars().first()


async def post_tweet(
    session: AsyncSession, tweet: Tweet
) -> Tweet:
    session.add(tweet)
    await session.commit()
    await session.refresh(tweet)
    return tweet


async def delete_tweet(
    session: AsyncSession, tweet_id: int
) -> bool:
    """Function deletes the tweet"""

    result = await session.execute(
        select(Tweet).where(Tweet.id == tweet_id)
    )
    tweet = result.scalars().first()
    if not tweet:
        raise ValueError("Tweet not found")

    await session.delete(tweet)
    await session.commit()
    return True


async def like_tweet(
    session: AsyncSession, tweet_id: int, user_id: int
) -> bool:

    like: Like = Like(user_id=user_id, tweet_id=tweet_id)
    session.add(like)
    await session.commit()
    return True


async def delete_like_tweet(
    session: AsyncSession, tweet_id: int, user_id: int
) -> bool:

    result = await session.execute(
        select(Like).where(
            Like.tweet_id == tweet_id, Like.user_id == user_id
        )
    )

    like = result.scalars().first()

    if like:
        await session.delete(like)
        await session.commit()
        return True
    else:
        return False


async def follow(
    session: AsyncSession, follower_id: int, following_id: int
) -> bool:
    follow_: Follow = Follow(
        follower_id=follower_id, following_id=following_id
    )
    if follow_:
        session.add(follow_)
        await session.commit()
        return True
    else:
        raise ValueError("Follow error")


async def unfollow(
    session: AsyncSession, follower_id: int, following_id: int
) -> bool:

    result = await session.execute(
        select(Follow).where(
            Follow.follower_id == follower_id,
            Follow.following_id == following_id,
        )
    )
    follow_ = result.scalars().first()

    if follow_:
        await session.delete(follow_)
        await session.commit()
        return True
    else:
        raise ValueError("Unfollow error")


async def upload_media(
    session: AsyncSession, file_path: str
) -> int:

    media = Media(filename=file_path)
    session.add(media)
    await session.commit()
    await session.refresh(media)

    return media.id


async def get_links(session: AsyncSession, media_id: int) -> str:

    result = await session.execute(
        select(Media.filename).where(Media.id == media_id)
    )
    res = result.scalars().first()
    return f"http://localhost/{res}"


