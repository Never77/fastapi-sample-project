from pydantic import BaseSettings, Field, validator
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str | None = None
    environment: str | None = None
    log_level: str  = "info"
    port : int | None = Field(8000, ge=0, le=65535)  # In case of 0, it will take the first free port
    access_log: bool = False
    host: str = "127.0.0.1"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
