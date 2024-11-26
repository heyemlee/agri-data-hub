from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "postgresql://postgres:postgres@db/farm_management"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_NAME: str = "farm_management"
    DATABASE_HOST: str = "db"
    DATABASE_PORT: int = 5432

    # Redis Configuration
    REDIS_URL: str = "redis://redis:6379"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # CORS Configuration
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:3000"]

    # Data Collection Settings
    DATA_COLLECTION_INTERVAL: int = 15
    ALERT_CHECK_INTERVAL: int = 60

    # Alert Thresholds
    TEMPERATURE_MAX_THRESHOLD: float = 35.0
    TEMPERATURE_MIN_THRESHOLD: float = 10.0
    HUMIDITY_MAX_THRESHOLD: float = 80.0
    HUMIDITY_MIN_THRESHOLD: float = 30.0
    SOIL_MOISTURE_MIN_THRESHOLD: float = 20.0

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()