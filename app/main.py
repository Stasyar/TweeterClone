import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.fill_db.fill_db import insert_data
from app.routes.tweet import register_tweet_routers
from app.routes.user import register_user_routers
from core.models import Base, db_helper

load_dotenv()
app_host: str = os.getenv("app_host")

app = FastAPI()
app.mount("/medias", StaticFiles(directory="medias"), name="medias")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Закоментировать после первого запуска приложения и во время тестов.


@app.on_event("startup")
async def startup():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await insert_data(conn)
    print("База данных создана и подключена.")


@app.on_event("shutdown")
async def shutdown():
    await db_helper.engine.dispose()
    print("Соединение с базой данных закрыто.")


register_tweet_routers(app=app)
register_user_routers(app=app)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=app_host, port=8000, reload=False)
