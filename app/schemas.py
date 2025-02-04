from typing import List, Optional

from pydantic import BaseModel


class TweetCreateRequest(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = None


class TweetCreateResponse(BaseModel):
    result: bool
    tweet_id: int
