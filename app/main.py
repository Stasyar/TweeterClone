import uvicorn

from app.app_factory import create_app
from app.routes.tweet import register_tweet_routers
from app.routes.user import register_user_routers
from core.config import settings
from core.models import DBHelper

db_helper = DBHelper(url=settings.db_url, echo=False)

ss = db_helper.session


app = create_app(db_hpr=db_helper)
register_tweet_routers(app=app, ss=ss)
register_user_routers(app=app, ss=ss)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
