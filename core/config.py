from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/microservice"
    db_echo: bool = False


settings = Settings()
