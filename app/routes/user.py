from typing import Union

from fastapi import Depends, Header, HTTPException, Path
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

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
from core.models import db_helper

DEFAULT_API_KEY = Header(...)
DEFAULT_PATH = Path(...)
DEPENDENCY = Depends(db_helper.session_getter)


def register_user_routers(app):
    """
    Функция для регистрации эндпоинтов /api/tweet и api/media

    :param app: FastAPI приложение
    :return: None
    """

    @app.post("/api/users/{user_id}/follow")
    async def api_follow(
        ss: AsyncSession = DEPENDENCY,
        api_key: str = DEFAULT_API_KEY,
        user_id: int = DEFAULT_PATH,
    ) -> Union[ResponseWithBool, ErrorResponse]:
        """
        Обработчик событий POST endpoint /api/users/{user_id}/follow

        :param ss: Асинхронная сессия
        :param api_key: Ключ аутентификации пользователя (по умолчанию - test)
        :param user_id: id пользователя из строки запроса
        :return: - При успешной отработке: json с  ответом {"result": "True"}
                 - При неуспешной отработке: json с  ответом
                   {"result": "False"}
                 - При возникновении исключения: json с  ответом
                 {"result": "False", "error_type": str, "error_message": str}
        """

        try:
            follower = await check_user(session=ss, api_key=api_key)
            if await follow(ss, follower_id=follower.id, following_id=user_id):
                return ResponseWithBool(result=True)
            else:
                return ResponseWithBool(result=False)

        except SQLAlchemyError as e:
            await ss.rollback()
            raise HTTPException(status_code=500, detail=e)
        except ValueError as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )
        except HTTPException as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )

    @app.delete("/api/users/{user_id}/follow")
    async def api_unfollow(
        ss: AsyncSession = DEPENDENCY,
        api_key: str = DEFAULT_API_KEY,
        user_id: int = DEFAULT_PATH,
    ) -> Union[ResponseWithBool, ErrorResponse]:
        """
        Обработчик событий DELETE endpoint /api/users/{user_id}/follow

        :param ss: Асинхронная сессия
        :param api_key: Ключ аутентификации пользователя (по умолчанию - test)
        :param user_id: id пользователя из строки запроса
        :return: - При успешной отработке: json с  ответом {"result": "True"}
                 - При неуспешной отработке: json с  ответом
                   {"result": "False"}
                 - При возникновении исключения: json с  ответом
                 {"result": "False", "error_type": str, "error_message": str}
        """
        try:
            follower = await check_user(session=ss, api_key=api_key)
            await unfollow(ss, follower_id=follower.id, following_id=user_id)
            return ResponseWithBool(result=True)

        except SQLAlchemyError as e:
            await ss.rollback()
            raise HTTPException(status_code=500, detail=e)
        except ValueError as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )
        except HTTPException as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )

    @app.get("/api/users/me")
    async def api_get_me(
        ss: AsyncSession = DEPENDENCY,
        api_key: str = DEFAULT_API_KEY,
    ) -> Union[MeResponceSchema, ErrorResponse]:
        """
        Обработчик событий GET endpoint /api/users/me

        :param ss: Асинхронная сессия
        :param api_key: Ключ аутентификации пользователя (по умолчанию - test)
        :return: - При успешной отработке: json с  ответом и информацией о
                   пользователе
                 - При возникновении исключения: json с  ответом
                 {"result": "False", "error_type": str, "error_message": str}
        """

        try:
            me = await check_user(session=ss, api_key=api_key)
            followers_ids = await get_followers(session=ss, user_id=me.id)
            following_ids = await get_followings(session=ss, user_id=me.id)

            if followers_ids:
                followers = [
                    FollowUserSchema(id=fr_id, name=None)
                    for fr_id in followers_ids
                ]
            else:
                followers = None

            if following_ids:
                following = [
                    FollowUserSchema(id=fg_id, name=None)
                    for fg_id in following_ids
                ]
            else:
                following = None

            user = UserSchema(
                id=me.id,
                name=None,
                followers=followers,
                following=following,
            )
            return MeResponceSchema(result=True, user=user)

        except SQLAlchemyError as e:
            await ss.rollback()
            raise HTTPException(status_code=500, detail=e)
        except ValueError as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )
        except HTTPException as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )

    @app.get("/api/users/{user_id}")
    async def api_get_user(
        ss: AsyncSession = DEPENDENCY,
        user_id: int = DEFAULT_PATH,
    ) -> Union[MeResponceSchema, ErrorResponse]:
        """
        Обработчик событий POST endpoint /api/users/{user_id}/follow

        :param ss: Асинхронная сессия
        :param user_id: id пользователя из строки запроса
        :return: - При успешной отработке: json с  ответом и информацией о
                   пользователе
                 - При возникновении исключения: json с  ответом
                 {"result": "False", "error_type": str, "error_message": str}
        """

        try:
            me = await get_user_by_id(session=ss, user_id=user_id)
            if not me:
                raise HTTPException(404, "User not found")
            followers_ids = await get_followers(session=ss, user_id=me.id)
            following_ids = await get_followings(session=ss, user_id=me.id)

            if followers_ids:
                followers = [
                    FollowUserSchema(id=fr_id, name=None)
                    for fr_id in followers_ids
                ]
            else:
                followers = None

            if following_ids:
                following = [
                    FollowUserSchema(id=fg_id, name=None)
                    for fg_id in following_ids
                ]
            else:
                following = None

            user = UserSchema(
                id=me.id,
                name=None,
                followers=followers,
                following=following,
            )
            return MeResponceSchema(result=True, user=user)

        except SQLAlchemyError as e:
            await ss.rollback()
            raise HTTPException(status_code=500, detail=e)
        except ValueError as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )
        except HTTPException as e:
            return ErrorResponse(
                result=False, error_type=type(e).__name__, error_message=str(e)
            )
