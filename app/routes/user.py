from typing import Union

from fastapi import Header, HTTPException, Path

from app.crud import (
    check_user,
    follow,
    get_followers,
    get_followings,
    get_user_by_id,
    unfollow,
)
from app.schemas import (
    ErrorResponse,
    FollowUserSchema,
    MeResponceSchema,
    ResponseWithBool,
    UserSchema,
)

default_api_key = Header(...)
default_path = Path(...)


def register_user_routers(app, ss):
    @app.post("/api/users/{user_id}/follow")
    async def api_follow(
        api_key: str = default_api_key,
        user_id: int = default_path,
    ) -> Union[ResponseWithBool, ErrorResponse]:

        try:
            follower = await check_user(session=ss, api_key=api_key)
            if await follow(ss, follower_id=follower.id, following_id=user_id):
                return ResponseWithBool(result=True)
            else:
                return ResponseWithBool(result=False)

        except Exception as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )

    @app.delete("/api/users/{user_id}/follow")
    async def api_unfollow(
        api_key: str = default_api_key,
        user_id: int = default_path,
    ) -> Union[ResponseWithBool, ErrorResponse]:
        try:
            follower = await check_user(session=ss, api_key=api_key)
            await unfollow(ss, follower_id=follower.id, following_id=user_id)
            return ResponseWithBool(result=True)

        except Exception as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )

    @app.get("/api/users/me")
    async def api_get_me(
        api_key: str = default_api_key,
    ) -> Union[MeResponceSchema, ErrorResponse]:
        try:
            me = await check_user(session=ss, api_key=api_key)
            followers_ids = await get_followers(session=ss, user_id=me.id)
            following_ids = await get_followings(session=ss, user_id=me.id)

            followers = [
                FollowUserSchema(id=fr_id, name=None)
                for fr_id in followers_ids
            ]
            following = [
                FollowUserSchema(id=fg_id, name=None)
                for fg_id in following_ids
            ]

            user = UserSchema(
                id=me.id,
                name=None,
                followers=followers,
                following=following,
            )
            return MeResponceSchema(result=True, user=user)

        except Exception as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )

    @app.get("/api/users/{user_id}")
    async def api_get_user(
        user_id: int = default_path,
    ) -> Union[MeResponceSchema, ErrorResponse]:
        try:
            me = await get_user_by_id(session=ss, user_id=user_id)
            if not me:
                raise HTTPException(404, "User not found")
            followers_ids = await get_followers(session=ss, user_id=me.id)
            following_ids = await get_followings(session=ss, user_id=me.id)

            followers = [
                FollowUserSchema(id=fr_id, name=None)
                for fr_id in followers_ids
            ]
            following = [
                FollowUserSchema(id=fg_id, name=None)
                for fg_id in following_ids
            ]

            user = UserSchema(
                id=me.id,
                name=None,
                followers=followers,
                following=following,
            )
            return MeResponceSchema(result=True, user=user)

        except HTTPException as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )
