from fastapi import APIRouter

from app.crud import get_users, post_user
from app.schemas import UserCreate
from core.models import User, db_helper

router = APIRouter()

ss = db_helper.session


@router.get("/user/")
async def api_get_user():
    return await get_users(ss)


@router.post("/user/")
async def api_post_user(user: UserCreate):
    new_user = User(api_key=user.api_key)
    return await post_user(ss, new_user)
