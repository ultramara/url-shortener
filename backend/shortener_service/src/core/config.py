import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # База данных
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str

    # Начальный URL скоращенной ссылки
    BASE_URL: str

    # Секретный ключ для Фейстеля
    FEISTEL_SECRET_KEY: int

    # Порт gRPC
    GRPC_PORT: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore" 
    )

settings = Settings()

