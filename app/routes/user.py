from fastapi import APIRouter, Header, Path

from app.crud import get_users, get_user_by_key, follow, unfollow
from app.schemas import ResponseWithBool

from core.models import User, db_helper

router = APIRouter()

ss = db_helper.session


@router.get("/user/")
async def api_get_user():
    return await get_users(ss)


@router.post("/user/")
async def api_post_user(api_key: str = Header(...)):
    return await get_user_by_key(ss, api_key=api_key)


@router.post("/api/users/{user_id}/follow/", response_model=ResponseWithBool)
async def api_follow(
        api_key: str = Header(...),
        user_id: int = Path(..., description="User ID")
) -> ResponseWithBool:

    follower: User = await get_user_by_key(session=ss, api_key=api_key)

    if await follow(ss, follower_id=follower.id, following_id=user_id):
        return ResponseWithBool(result=True)
    else:
        return ResponseWithBool(result=False)


@router.delete("/api/users/{user_id}/follow/", response_model=ResponseWithBool)
async def api_follow(
        api_key: str = Header(...),
        user_id: int = Path(..., description="User ID")
) -> ResponseWithBool:
    follower: User = await get_user_by_key(session=ss, api_key=api_key)

    if await unfollow(ss, follower_id=follower.id, following_id=user_id):
        return ResponseWithBool(result=True)
    else:
        return ResponseWithBool(result=False)