from functools import lru_cache
from typing import List, Optional
from netcore.models.secrets import SecretType
from pathlib import Path
from pydantic import BaseSettings, Field, AnyHttpUrl


class VaultSettings(BaseSettings):
    url: AnyHttpUrl | None = None
    token: str = None
    ssl_verify: bool = True
    cert_path: AnyHttpUrl | Path | None = None  # default using the certs of the machine
    cert_key: AnyHttpUrl | Path | None = None
    
    class Config:
        env_file = ".env"
        env_prefix = "netcore_vault_"

class NautobotSettings(BaseSettings):
    url: AnyHttpUrl | None = None
    token: str = None
    ssl_verify: bool = True
    
    class Config:
        env_file = ".env"
        env_prefix = "netcore_nautobot_"

class Settings(BaseSettings):
    database_url: str | None = None
    environment: str | None = None
    log_level: str = "info"
    port: int | None = Field(8000, ge=0, le=65535)  # In case of 0, it will take the first free port
    access_log: bool = False
    host: str = "127.0.0.1"
    redis_url: str | None = None
    prometheus: bool = False
    graphql: bool = False
    vault: VaultSettings = VaultSettings()
    nautobot: NautobotSettings = NautobotSettings()

    class Config:
        env_file = ".env"
        env_prefix = "netcore_"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
