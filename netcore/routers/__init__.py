from netcore.config import settings
from netcore.routers.users import router as UserRouter

if settings.vault.url:
    from netcore.routers.secrets import router as SecretsRouter

if settings.nautobot.url:
    from netcore.routers.hosts import router as HostsRouter

__all__ = (
    "HostsRouter",
    "SecretsRouter",
    "UserRouter",
)
