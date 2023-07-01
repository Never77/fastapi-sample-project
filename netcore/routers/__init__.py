from netcore.config import settings
from netcore.routers.users import router as UserRouter

if settings.vault.url:
    from netcore.routers.secrets import router as SecretsRouter

if settings.nautobot.url:
    from netcore.routers.hosts import router as HostsRouter

if settings.oauth2.oidc_discovery_url:
    from netcore.routers.auth import router as AuthRouter

if settings.celery.broker_url:
    from netcore.routers.tasks import router as TasksRouter

if settings.mongodb_url:
    from netcore.routers.posts import router as PostsRouter

__all__ = (
    "HostsRouter",
    "SecretsRouter",
    "UserRouter",
    "AuthRouter",
    "TasksRouter",
    "PostsRouter",
)
