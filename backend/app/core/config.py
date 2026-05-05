from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "TradingStation"
    debug: bool = True
    
    database_url: str = "postgresql+asyncpg://tradingstation:tradingstation123@localhost:5432/tradingstation"
    sync_database_url: str = "postgresql://tradingstation:tradingstation123@localhost:5432/tradingstation"
    
    redis_url: str = "redis://localhost:6379/0"
    
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
