from pydantic_settings import BaseSettings

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/microservice"


class Settings(BaseSettings):
    db_url: str = DATABASE_URL
    db_echo: bool = False


settings = Settings()
