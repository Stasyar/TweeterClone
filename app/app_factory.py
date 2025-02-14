from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from core.models import Base


def create_app(db_hpr) -> FastAPI:
    """Фабрика приложения FastAPI"""
    app = FastAPI()
    app.mount("/medias", StaticFiles(directory="medias"), name="medias")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup():
        async with db_hpr.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("База данных создана и подключена.")

    @app.on_event("shutdown")
    async def shutdown():
        await db_hpr.engine.dispose()
        print("Соединение с базой данных закрыто.")

    return app
