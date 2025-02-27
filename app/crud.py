from typing import Optional, Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import LikesSchema
from app.schemas.get_all_tweets import AuthorSchema
from core.models import Follow, Like, Media, Tweet, User


async def check_user(
    session: AsyncSession,
    api_key: str,
) -> User:
    """
    Проверяет api_key пользователя который делает запрос
    и добавляет его в базу данных
    если он не был добавлен ранее.

    :param session: Асинхронная сессия.
    :param api_key: api-key пользователя.
    :return: объект User.
    """

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
    except SQLAlchemyError as e:
        print(f"Error during user check (database error): {e}")
        await session.rollback()
        raise


async def get_user_by_id(
    session: AsyncSession, user_id: int
) -> Optional[User]:
    """
    Возвращает информацию про пользователя по его id.

    :param: user_id: id пользователя.
    :param session: Асинхронная сессия.
    :return: объект User или None если пользователь не существует.
    """
    try:
        result = await session.execute(select(User).where(user_id == User.id))
        user = result.scalars().first()

        if not user:
            raise HTTPException(404, "User not found")

        return user

    except SQLAlchemyError as e:
        print(f"Error during get_user_by_id (database error): {e}")
        await session.rollback()
        raise


async def get_followings(
    session: AsyncSession, user_id: int
) -> Optional[Sequence[int]]:
    """
    Возвращает список пользователей на которых подписан данный
    пользователь по его id.

    :param: user_id: id пользователя.
    :param session: Асинхронная сессия.
    :return: список объектов User или None если пользователей не существует.
    """
    try:
        result = await session.execute(
            select(Follow.following_id).where(Follow.follower_id == user_id)
        )

        return result.scalars().all()
    except SQLAlchemyError as e:
        print(f"Error during get_followings (database error): {e}")
        await session.rollback()
        raise


async def get_followers(
    session: AsyncSession, user_id: int
) -> Optional[Sequence[int]]:
    """
    Возвращает список пользователей которые подписаны на данного
    пользователя по его id.

    :param: user_id: id пользователя.
    :param session: Асинхронная сессия.
    :return: список объектов User или None если пользователей не существует.
    """
    try:
        result = await session.execute(
            select(Follow.follower_id).where(Follow.following_id == user_id)
        )

        return result.scalars().all()
    except SQLAlchemyError as e:
        print(f"Error during get_followers (database error): {e}")
        await session.rollback()
        raise


async def get_likes(
    session: AsyncSession, tweet_id: int
) -> Sequence[LikesSchema]:
    """
    Возвращает список лайков поставленных твиту по его id.

    :param: tweet_id: id твита.
    :param session: Асинхронная сессия.
    :return: список объектов Like или None если их не существует.
    """
    try:
        result = await session.execute(
            select(Like.user_id).where(Like.tweet_id == tweet_id)
        )
        likes_user_ids = result.scalars().all()

        return [LikesSchema(user_id=us_id) for us_id in likes_user_ids]
    except SQLAlchemyError as e:
        print(f"Error during get_likes (database error): {e}")
        await session.rollback()
        raise


async def get_tweets(
    session: AsyncSession, user_id: int
) -> Optional[Sequence[Tweet]]:
    """
    Возвращает список твитов пользователя по его id.

    :param: user_id: id пользователя.
    :param session: Асинхронная сессия.
    :return: список объектов Tweet или None если их не существует.
    """
    try:
        result = await session.execute(
            select(Tweet).where(Tweet.author_id == user_id)
        )
        return result.scalars().all()
    except SQLAlchemyError as e:
        print(f"Error during get_tweets (database error): {e}")
        await session.rollback()
        raise


async def get_author_info(session: AsyncSession, user_id: int) -> AuthorSchema:
    """
    Возвращает информацию про автора поста
    (используется в схеме для возврата поста).
    :param session: Асинхронная сессия.
    :param user_id: id пользователя.
    :return: json ответ {"id": int, "name": Optional[str]}
    """
    try:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        return AuthorSchema(id=user.id, name=user.name)
    except SQLAlchemyError as e:
        print(f"Error during get_author_info (database error): {e}")
        await session.rollback()
        raise


async def get_tweet_by_id(
    session: AsyncSession, tweet_id: int
) -> Optional[Tweet]:
    """
    Возвращает твит по его id.

    :param: tweet_id: id твита.
    :param session: Асинхронная сессия.
    :return: объект Tweet или None если его не существует.
    """
    try:
        result = await session.execute(
            select(Tweet).where(Tweet.id == tweet_id)
        )
        return result.scalars().first()
    except SQLAlchemyError as e:
        print(f"Error during get_tweet_by_id (database error): {e}")
        await session.rollback()
        raise


async def post_tweet(session: AsyncSession, tweet: Tweet) -> Tweet:
    """
    Добавляет твит в базу данных.

    :param: tweet: объект Tweet.
    :param session: Асинхронная сессия.
    :return: добавленный объект Tweet.
    """
    try:
        session.add(tweet)
        await session.commit()
        await session.refresh(tweet)
        return tweet
    except SQLAlchemyError as e:
        print(f"Error during get_tweets (database error): {e}")
        await session.rollback()
        raise


async def delete_tweet(session: AsyncSession, tweet_id: int) -> bool:
    """
    Удаляет твит по его id.

    :param: tweet_id: id твита.
    :param session: Асинхронная сессия.
    :return: возвращает True если твит удален и возбуждает
    исключение если твит не найден.
    """
    try:
        result = await session.execute(
            select(Tweet).where(Tweet.id == tweet_id)
        )
        tweet = result.scalars().first()
        if not tweet:
            raise ValueError("Tweet not found")

        await session.delete(tweet)
        await session.commit()
        return True
    except ValueError as e:
        print(f"Error during delete_tweet: {e}")
        raise
    except SQLAlchemyError as e:
        print(f"Error during delete_tweet (database error): {e}")
        await session.rollback()
        raise


async def like_tweet(
    session: AsyncSession, tweet_id: int, user_id: int
) -> bool:
    """
    Добавляет лайк твиту.

    :param: tweet_id: id твита.
    :param: user_id: id пользователя.
    :param session: Асинхронная сессия.
    :return: возвращает True если лайк добавлен.
    """
    try:
        like: Like = Like(user_id=user_id, tweet_id=tweet_id)
        session.add(like)
        await session.commit()
        return True
    except SQLAlchemyError as e:
        print(f"Error during like_tweet (database error): {e}")
        await session.rollback()
        raise


async def delete_like_tweet(
    session: AsyncSession, tweet_id: int, user_id: int
) -> bool:
    """
    Удаляет лайк твиту.

    :param: tweet_id: id твита.
    :param: user_id: id пользователя.
    :param session: Асинхронная сессия.
    :return: возвращает True если лайк добавлен, False если лайк не был найден.
    """
    try:
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
    except SQLAlchemyError as e:
        print(f"Error during delete_like_tweet (database error): {e}")
        await session.rollback()
        raise


async def follow(
    session: AsyncSession, follower_id: int, following_id: int
) -> bool:
    """
    Добавляет подписку.

    :param: follower_id: id подписчика.
    :param: following_id: id того на кого подписаны.
    :param session: Асинхронная сессия.
    :return: возвращает True если подписка добавлена, возбуждает
    ошибку если подписка не была добавлена.
    """
    try:
        follow_: Follow = Follow(
            follower_id=follower_id, following_id=following_id
        )
        if follow_:
            session.add(follow_)
            await session.commit()
            return True
        else:
            raise ValueError("follow_ is empty")
    except ValueError as e:
        print(f"Error during follow: {e}")
        raise
    except SQLAlchemyError as e:
        print(f"Error during follow (database error): {e}")
        await session.rollback()
        raise


async def unfollow(
    session: AsyncSession, follower_id: int, following_id: int
) -> bool:
    """
    Удаляет подписку.

    :param: follower_id: id подписчика.
    :param: following_id: id того на кого подписаны.
    :param session: Асинхронная сессия.
    :return: возвращает True если подписка удалена, возбуждает
    ошибку если подписка не была удалена.
    """
    try:
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
    except SQLAlchemyError as e:
        print(f"Error during unfollow (database error): {e}")
        await session.rollback()
        raise


async def upload_media(session: AsyncSession, file_path: str) -> int:
    """
    Записывает путь к файлу с картинкой в базу данных.

    :param session: Асинхронная сессия.
    :param file_path: путь к файлу с картинкой.
    :return: id которое было присвоено пути в базе данных.
    """
    try:
        media = Media(filename=file_path)
        session.add(media)
        await session.commit()
        await session.refresh(media)

        return media.id
    except SQLAlchemyError as e:
        print(f"Error during upload_media (database error): {e}")
        await session.rollback()
        raise


async def get_links(session: AsyncSession, media_id: int) -> str:
    """
    Формирует ссылки на картинки на сервере для отображения их на веб-странице.

    :param session: Асинхронная сессия
    :param media_id: id пути записанного в базе данных.
    :return: ссылка на картинку.
    """
    try:
        result = await session.execute(
            select(Media.filename).where(Media.id == media_id)
        )
        res = result.scalars().first()
        return f"http://localhost/{res}"
    except SQLAlchemyError as e:
        print(f"Error during get_links (database error): {e}")
        await session.rollback()
        raise
