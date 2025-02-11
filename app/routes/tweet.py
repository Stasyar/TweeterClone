import os
from typing import Union

import aiofiles
from fastapi import (
    APIRouter,
    File,
    Header,
    Path,
    UploadFile,
)

from app.config import UPLOAD_FOLDER
from app.crud import (
    check_user,
    delete_like_tweet,
    delete_tweet,
    get_author_info,
    get_followings,
    get_likes,
    get_tweet_by_id,
    get_tweets,
    like_tweet,
    post_tweet,
    upload_media,
)
from app.schemas import (
    BaseSchema,
    ErrorResponse,
    ResponseWithBool,
    TweetCreateRequest,
    TweetCreateResponse,
    TweetsGetResponse,
    TweetsSchema,
)
from core.models import Tweet, db_helper

router = APIRouter()
ss = db_helper.session
default_api_key = Header(...)
default_path = Path(...)
default_files = File(...)


@router.get("/api/tweets", status_code=200)
async def api_get_tweets_from_following(
    api_key: str = default_api_key,
) -> Union[TweetsGetResponse, ErrorResponse, None]:
    try:
        user = await check_user(session=ss, api_key=api_key)
        print("user", user)
        followings_ids = await get_followings(session=ss, user_id=user.id)
        print("followings_ids", followings_ids)
        schemed_tweets = []

        for f in followings_ids:
            tweets = await get_tweets(session=ss, user_id=f)
            print("tweets", tweets)

            for tw in tweets:
                likes = await get_likes(session=ss, tweet_id=tw.id)
                author = await get_author_info(
                    session=ss, user_id=tw.author_id
                )
                print("likes", likes)
                print("author", author)
                schemed_tweet = TweetsSchema(
                    id=tw.id,
                    content=tw.content,
                    attachments=tw.media,
                    author=author,
                    likes=likes,
                )
                print("До добавления schemed_tweet")
                schemed_tweets.append(schemed_tweet)
                print("После добавления schemed_tweet")
        print(schemed_tweets)
        return TweetsGetResponse(result=True, tweets=schemed_tweets)
    except Exception as e:
        return ErrorResponse(
            result=False, error_type=type(e).__name__, error_message=str(e)
        )


@router.post("/api/tweets", status_code=201)
async def api_post_tweet(
    data: TweetCreateRequest,
    api_key: str = default_api_key,
) -> Union[TweetCreateResponse, ErrorResponse]:
    try:
        user = await check_user(session=ss, api_key=api_key)
        print("user_id", user.id)
        print(data)
        new_tweet: Tweet = Tweet(
            author_id=user.id,
            content=data.content,
            media=data.media,
        )
        print(new_tweet)
        tweet: Tweet = await post_tweet(ss, new_tweet)
        return TweetCreateResponse(result=True, tweet_id=tweet.id)

    except Exception as e:
        return ErrorResponse(
            result=False, error_type=type(e).__name__, error_message=str(e)
        )


@router.delete("/api/tweets/{tweet_id}")
async def api_delete_tweet(
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


@router.post("/api/tweets/{tweet_id}/likes")
async def api_like_tweet(
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


@router.delete("/api/tweets/{tweet_id}/like")
async def api_unlike_tweet(
    api_key: str = default_api_key,
    tweet_id: int = default_path,
) -> Union[ResponseWithBool, ErrorResponse]:

    try:
        user = await check_user(session=ss, api_key=api_key)
        tweet: Tweet = await get_tweet_by_id(session=ss, tweet_id=tweet_id)

        if await delete_like_tweet(
            session=ss, tweet_id=tweet.id, user_id=user.id
        ):
            return ResponseWithBool(result=True)
        else:
            return ResponseWithBool(result=False)
    except Exception as e:
        return ErrorResponse(
            result=False, error_type=type(e).__name__, error_message=str(e)
        )


@router.post("/api/medias")
async def api_media(
    file: UploadFile = default_files,
) -> BaseSchema:

    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        bytes_data = await file.read()  # read bytes from an input file

        # write bytes to a file
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(bytes_data)

        media_id = await upload_media(session=ss, file_path=file_path)
        return TweetCreateResponse(result=True, tweet_id=media_id)
    except Exception as e:
        return ErrorResponse(
            result=False, error_type=type(e).__name__, error_message=str(e)
        )
