import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
db_user: str = os.getenv("db_user")
db_name: str = os.getenv("db_name")
db_password: str = os.getenv("db_password")

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_password}@db:5432/{db_name}"


class Settings(BaseSettings):
    db_url: str = DATABASE_URL
    db_echo: bool = False


settings = Settings()
