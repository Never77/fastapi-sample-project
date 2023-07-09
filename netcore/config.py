from functools import lru_cache
from pathlib import Path
from pydantic import SecretStr
from pydantic import AnyHttpUrl, BaseSettings, Field
from enum import Enum


class OAuth2Settings(BaseSettings):
    client_id: str = None
    client_secret: SecretStr = None
    oidc_discovery_url: AnyHttpUrl = None  # without the .well-known/openid-configuration
    scopes: str = "openid email profile"

    class Config:
        env_file = ".env"
        env_prefix = "netcore_oauth2_"


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


class CelerySettings(BaseSettings):
    broker_url: str
    result_backend: str

    class Config:
        env_file = ".env"
        env_prefix = "netcore_celery_"


class Algorithm(str, Enum):
    HS256 = "HS256"
    HS384 = "HS384"
    HS512 = "HS512"
    RS256 = "RS256"
    RS384 = "RS384"
    RS512 = "RS512"
    ES256 = "ES256"
    ES384 = "ES384"
    ES512 = "ES512"


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
    oauth2: OAuth2Settings = OAuth2Settings()
    secret_key: str = None
    celery: CelerySettings = CelerySettings()
    mongodb_url: str
    algorithm: Algorithm = "HS256"

    class Config:
        env_file = ".env"
        env_prefix = "netcore_"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
