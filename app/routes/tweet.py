from fastapi import APIRouter

from app.schemas import TweetCreateRequest, TweetCreateResponse

router = APIRouter()


@router.get("/")
def hello():
    return {"message": "hello"}


@router.post("/tweet", response_model=TweetCreateResponse, status_code=201)
async def post_tweet(data: TweetCreateRequest):

    return {"result": True, "tweet_id": 123}
