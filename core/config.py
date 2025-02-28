from pydantic_settings import BaseSettings

DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/your_db"


class Settings(BaseSettings):
    db_url: str = DATABASE_URL
    db_echo: bool = False


settings = Settings()
