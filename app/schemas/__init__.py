__all__ = (
    "TweetCreateRequest",
    "TweetCreateResponse",
    "ResponseWithBool",
    "TweetsGetResponse",
    "ErrorResponse",
    "BaseSchema",
    "LikesSchema",
    "TweetsSchema",
    "UserSchema",
    "FollowUserSchema",
    "MeResponceSchema",
    "MediaUploadResponse",
)


from app.schemas.general import BaseSchema, ErrorResponse, ResponseWithBool
from app.schemas.get_all_tweets import (
    LikesSchema,
    TweetsGetResponse,
    TweetsSchema,
)
from app.schemas.tweet import (
    MediaUploadResponse,
    TweetCreateRequest,
    TweetCreateResponse,
)
from app.schemas.user import FollowUserSchema, MeResponceSchema, UserSchema
