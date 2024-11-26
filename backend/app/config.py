from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_HOST: str
    DATABASE_PORT: int

    # Redis
    REDIS_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str = ""

    # Server
    HOST: str
    PORT: int
    DEBUG: bool
    ENVIRONMENT: str

    # CORS
    CORS_ORIGINS: List[str]

    # Data Collection
    DATA_COLLECTION_INTERVAL: int
    ALERT_CHECK_INTERVAL: int

    # Alert Thresholds
    TEMPERATURE_MAX_THRESHOLD: float
    TEMPERATURE_MIN_THRESHOLD: float
    HUMIDITY_MAX_THRESHOLD: float
    HUMIDITY_MIN_THRESHOLD: float
    SOIL_MOISTURE_MIN_THRESHOLD: float

    # Socket.IO Config
    SOCKET_PING_TIMEOUT: int = 60
    SOCKET_PING_INTERVAL: int = 25

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()