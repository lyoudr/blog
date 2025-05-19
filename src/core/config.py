from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()


def get_env(name):
    if os.getenv("ENV") == "local":
        return os.getenv(name)


class Settings(BaseSettings):
    DATABASE_URL: str = get_env("DATABASE_URL")
    DB_USER: str = get_env("DB_USER")
    DB_PASS: str = get_env("DB_PASS")
    DB_NAME: str = get_env("DB_NAME")
    DB_HOST: str = get_env("DB_HOST")
    DB_PORT: str = get_env("DB_PORT")
    GCS_BUCKET_NAME: str = get_env("GCS_BUCKET_NAME")
    SECRET_KEY: str = get_env("SECRET_KEY")
    ALGORITHM: str = get_env("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = get_env("ACCESS_TOKEN_EXPIRE_MINUTES")
    model_config = SettingsConfigDict(env_prefix=".env")


settings = Settings()


def get_settings() -> Settings:
    return settings
