from functools import lru_cache
from pathlib import Path
from pydantic import SecretStr
from pydantic import AnyHttpUrl, BaseSettings, Field

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

    class Config:
        env_file = ".env"
        env_prefix = "netcore_"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
