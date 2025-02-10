from typing import List, Optional

from app.schemas import BaseSchema


class TweetCreateRequest(BaseSchema):
    content: str
    media: Optional[List[int]] = None


class TweetCreateResponse(BaseSchema):
    result: bool
    tweet_id: int
