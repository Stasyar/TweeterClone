import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.tweet import router as tweet_router
from app.routes.user import router as user_router
from core.models import Base, db_helper

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("База данных создана и подключена.")


@app.on_event("shutdown")
async def shutdown():
    await db_helper.engine.dispose()
    print("Соединение с базой данных закрыто.")


app.include_router(tweet_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
