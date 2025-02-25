from dotenv import load_dotenv
from pydantic_settings import BaseSettings

import os

# ENV_FILE = ".env"
# load_dotenv(ENV_FILE)
#
# DB_PASS = os.getenv("db_pass")
# DB_USER = os.getenv("db_user")
# DB_NAME = os.getenv("db_name")
#
# DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@db:5432/{DB_NAME}"

DATABASE_URL = f"postgresql+asyncpg://postgres:postgres@db:5432/microservice"


class Settings(BaseSettings):
    db_url: str = DATABASE_URL
    db_echo: bool = False


settings = Settings()
