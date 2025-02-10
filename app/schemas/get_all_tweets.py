from typing import List, Optional, Sequence

from app.schemas import BaseSchema


class LikesSchema(BaseSchema):
    user_id: int
    name: Optional[str] = None


class AuthorSchema(BaseSchema):
    id: int
    name: Optional[str] = None


class TweetsSchema(BaseSchema):
    id: int
    content: str
    attachments: Optional[List[int]] = None
    author: AuthorSchema
    likes: Optional[Sequence[LikesSchema]] = None


class TweetsGetResponse(BaseSchema):
    result: bool
    tweets: List[TweetsSchema]
