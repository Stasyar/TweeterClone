from fastapi import HTTPException
from fastapi.security import APIKeyHeader

from app.crud import check_user
from core.models import db_helper

ss = db_helper.session
api_key_header = APIKeyHeader(name="Authorization")


async def get_current_user(api_key: str = api_key_header):
    user = await check_user(session=ss, api_key=api_key)
    if user is None:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return user
