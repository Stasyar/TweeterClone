from fastapi import APIRouter, Header

from app.crud import get_users, post_user

from core.models import User, db_helper

router = APIRouter()

ss = db_helper.session


@router.get("/user/")
async def api_get_user():
    return await get_users(ss)


@router.post("/user/")
async def api_post_user(api_key: str = Header(...)):
    new_user = User(api_key=api_key)
    return await post_user(ss, new_user)
