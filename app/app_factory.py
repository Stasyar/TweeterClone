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

    return app
