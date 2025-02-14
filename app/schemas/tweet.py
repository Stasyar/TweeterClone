from typing import List, Optional

from app.schemas import BaseSchema


class TweetCreateRequest(BaseSchema):
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = None


class TweetCreateResponse(BaseSchema):
    result: bool
    tweet_id: int


class MediaUploadResponse(BaseSchema):
    result: bool
    media_id: int
