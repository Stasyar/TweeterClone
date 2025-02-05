from typing import List, Optional

from pydantic import BaseModel


class TweetCreateRequest(BaseModel):
    content: str
    media: Optional[List[int]] = None


class TweetCreateResponse(BaseModel):
    result: bool
    tweet_id: int


class ResponseWithBool(BaseModel):
    result: bool









