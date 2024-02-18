from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    PROJECT_NAME: str
    DEBUG: bool
    DATABASE_URL: PostgresDsn

    CORS_ORIGINS: list[str] = ['*']
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] = ['*']

    JWT_ALG: str
    JWT_SECRET: str
    JWT_EXP: int = 5  # minutes

    class Config:
        env_file = '.env'


settings = Config()
