import uvicorn

from app.app_factory import create_app
from app.routes.tweet import register_tweet_routers
from app.routes.user import register_user_routers
from core.models import db_helper, Base


ss = db_helper.session


app = create_app(db_hpr=db_helper)


@app.on_event("startup")
async def startup():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("База данных создана и подключена.")


@app.on_event("shutdown")
async def shutdown():
    await db_helper.engine.dispose()
    print("Соединение с базой данных закрыто.")


register_tweet_routers(app=app, ss=ss)
register_user_routers(app=app, ss=ss)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

