from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str
    BOT_TOKEN: str
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    PRIZE_POOL_PERCENT: float = 2.0  # % of net
    PRIZE_POOL_CAP_USD: float = 100.0
    PRIZE_POOL_MIN_USD: float = 10.0
    ALLOWED_ORIGINS: str = "*"
    SEASON_LENGTH_DAYS: int = 30


class Config:
    env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
