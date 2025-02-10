from typing import Optional, Sequence

from app.schemas import BaseSchema


class FollowUserSchema(BaseSchema):
    id: int
    name: Optional[str] = None


class UserSchema(BaseSchema):
    id: int
    name: Optional[str] = None
    followers: Optional[Sequence[FollowUserSchema]] = None
    following: Optional[Sequence[FollowUserSchema]] = None


class MeResponceSchema(BaseSchema):
    result: bool
    user: UserSchema
