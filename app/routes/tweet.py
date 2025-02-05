from fastapi import APIRouter, Header, Path

from app.schemas import TweetCreateRequest, TweetCreateResponse, TweetDeleteResponse
from core.models import Tweet, db_helper, User
from app.crud import get_user_by_key, post_tweet, get_tweet_by_id, delete_tweet

router = APIRouter()
ss = db_helper.session


@router.post("/tweet", response_model=TweetCreateResponse, status_code=201)
async def api_post_tweet(data: TweetCreateRequest, api_key: str = Header(...)) -> TweetCreateResponse:
    user: User = await get_user_by_key(session=ss, api_key=api_key)

    new_tweet: Tweet = Tweet(author_id=user.id, content=data.content, media=data.media if data.media else None)
    tweet_id: int = await post_tweet(ss, new_tweet)
    return TweetCreateResponse(result=True, tweet_id=tweet_id)


@router.delete("/api/tweets/{tweet_id}", response_model=TweetDeleteResponse)
async def api_delete_tweet(
        api_key: str = Header(...),
        tweet_id: int = Path(..., description="Tweet ID")
) -> TweetDeleteResponse:
    user: User = await get_user_by_key(session=ss, api_key=api_key)
    tweet: Tweet = await get_tweet_by_id(session=ss, tweet_id=tweet_id)

    if user.id == tweet.author_id:
        if await delete_tweet(session=ss, tweet_id=tweet_id):
            return TweetDeleteResponse(result=True)
    else:
        return TweetDeleteResponse(result=False)
