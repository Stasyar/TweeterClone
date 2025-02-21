import imghdr
import os
import uuid
from typing import Union

import aiofiles
from fastapi import (
    APIRouter,
    File,
    Header,
    Path,
    UploadFile, Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import UPLOAD_FOLDER
from app.crud import (
    check_user,
    delete_like_tweet,
    delete_tweet,
    get_author_info,
    get_followings,
    get_likes,
    get_links,
    get_tweet_by_id,
    get_tweets,
    like_tweet,
    post_tweet,
    upload_media,
)
from app.schemas import (
    BaseSchema,
    ErrorResponse,
    MediaUploadResponse,
    ResponseWithBool,
    TweetCreateRequest,
    TweetCreateResponse,
    TweetsGetResponse,
    TweetsSchema,
)
from core.models import Tweet, db_helper

default_files = File(...)
default_api_key = Header(...)
default_path = Path(...)


def register_tweet_routers(app):
    @app.post("/api/tweets/{tweet_id}/likes")
    async def api_like_tweet(
            ss: AsyncSession = Depends(db_helper.session_getter),
        api_key: str = default_api_key,
        tweet_id: int = default_path,
    ) -> Union[ResponseWithBool, ErrorResponse]:

        try:
            user = await check_user(session=ss, api_key=api_key)
            tweet: Tweet = await get_tweet_by_id(session=ss, tweet_id=tweet_id)

            if tweet:
                if await like_tweet(
                    session=ss, tweet_id=tweet.id, user_id=user.id
                ):
                    return ResponseWithBool(result=True)
            else:
                return ResponseWithBool(result=False)
        except Exception as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )

    @app.delete("/api/tweets/{tweet_id}/likes")
    async def api_unlike_tweet(
            ss: AsyncSession = Depends(db_helper.session_getter),
        api_key: str = default_api_key,
        tweet_id: int = default_path,
    ) -> Union[ResponseWithBool, ErrorResponse]:

        try:
            user = await check_user(session=ss, api_key=api_key)

            if await delete_like_tweet(
                session=ss, tweet_id=tweet_id, user_id=user.id
            ):
                return ResponseWithBool(result=True)
            else:
                return ResponseWithBool(result=False)
        except Exception as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )

    @app.delete("/api/tweets/{tweet_id}")
    async def api_delete_tweet(
            ss: AsyncSession = Depends(db_helper.session_getter),
        api_key: str = default_api_key,
        tweet_id: int = default_path,
    ) -> Union[ResponseWithBool, ErrorResponse]:

        try:
            user = await check_user(session=ss, api_key=api_key)
            tweet: Tweet = await get_tweet_by_id(session=ss, tweet_id=tweet_id)

            if user.id == tweet.author_id:
                if await delete_tweet(session=ss, tweet_id=tweet_id):
                    return ResponseWithBool(result=True)
            else:
                return ResponseWithBool(result=False)
        except Exception as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )

    @app.get("/api/tweets", status_code=200)
    async def api_get_tweets_from_following(
            ss: AsyncSession = Depends(db_helper.session_getter),
        api_key: str = default_api_key,
    ) -> Union[TweetsGetResponse, ErrorResponse, None]:
        try:
            user = await check_user(session=ss, api_key=api_key)
            followings_ids = await get_followings(session=ss, user_id=user.id)

            # Временный вывод собственных твитов ПОТОМ УБРАТЬ!
            followings_ids = list(followings_ids)
            followings_ids.append(user.id)

            tweets_with_likes = []

            all_tweets = []

            for f in followings_ids:
                tweets = await get_tweets(session=ss, user_id=f)
                all_tweets.extend(tweets)

            for tw in all_tweets:
                likes = await get_likes(session=ss, tweet_id=tw.id)
                author = await get_author_info(
                    session=ss, user_id=tw.author_id
                )
                media_links = []
                if tw.media:
                    for m in tw.media:
                        link = await get_links(session=ss, media_id=m)
                        if link:
                            media_links.append(link)

                schemed_tweet = TweetsSchema(
                    id=tw.id,
                    content=tw.content,
                    attachments=media_links,
                    author=author,
                    likes=likes,
                )

                tweets_with_likes.append((schemed_tweet, len(likes)))
            sorted_tweets = sorted(
                tweets_with_likes, key=lambda x: x[1], reverse=True
            )
            schemed_tweets = [tw[0] for tw in sorted_tweets]

            return TweetsGetResponse(result=True, tweets=schemed_tweets)
        except Exception as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )

    @app.post("/api/tweets", status_code=201)
    async def api_post_tweet(
        data: TweetCreateRequest,
        api_key: str = default_api_key,
            ss: AsyncSession = Depends(db_helper.session_getter),
    ) -> Union[TweetCreateResponse, ErrorResponse]:
        try:
            user = await check_user(session=ss, api_key=api_key)
            new_tweet: Tweet = Tweet(
                author_id=user.id,
                content=data.tweet_data,
                media=data.tweet_media_ids,
            )
            print("router_tweets", data.tweet_media_ids)
            tweet: Tweet = await post_tweet(ss, new_tweet)
            return TweetCreateResponse(result=True, tweet_id=tweet.id)

        except Exception as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )

    @app.post("/api/medias")
    async def api_media(
        file: UploadFile = default_files,
            ss: AsyncSession = Depends(db_helper.session_getter),
    ) -> Union[MediaUploadResponse, BaseSchema]:

        try:
            first_bytes = await file.read(5120)
            ext = imghdr.what(None, first_bytes)

            if ext not in {"jpeg", "png", "gif", "webp"}:
                raise ValueError("Недопустимый формат файла")

            file_ext = f".{ext}"
            file_path = os.path.join(
                UPLOAD_FOLDER, f"{uuid.uuid4()}{file_ext}"
            )

            await file.seek(0)
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            async with aiofiles.open(file_path, "wb") as f:
                while True:
                    chunk = await file.read(1024)
                    if not chunk:
                        break
                    await f.write(chunk)

            media_id = await upload_media(session=ss, file_path=file_path)
            return MediaUploadResponse(result=True, media_id=media_id)
        except Exception as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )
