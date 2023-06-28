from fastapi_security import FastAPISecurity

from fastapi_test.config import settings

security = FastAPISecurity()

if settings.oidc_discovery_url:
    security.init_oauth2_through_oidc(settings.oidc_discovery_url, audiences=settings.oauth2_audiences)

security.add_permission_overrides(settings.permission_overrides)
