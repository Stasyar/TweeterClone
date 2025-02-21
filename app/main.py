import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Base


from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.routes.tweet import register_tweet_routers
from app.routes.user import register_user_routers

app = FastAPI()
app.mount("/medias", StaticFiles(directory="medias"), name="medias")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tweet_routers(app=app)
register_user_routers(app=app)


# @app.on_event("startup")
# async def startup():
#     async with db_helper.engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     print("База данных создана и подключена.")
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await db_helper.engine.dispose()
#     print("Соединение с базой данных закрыто.")



if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

