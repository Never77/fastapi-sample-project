from authlib.integrations.starlette_client import OAuth
from netcore.config import settings

oauth = OAuth()

oauth.register(
    name="GAAP",
    client_id=settings.oauth2.client_id,
    client_secret=settings.oauth2.client_secret.get_secret_value(),
    server_metadata_url=settings.oauth2.oidc_discovery_url + "/.well-known/openid-configuration",
    client_kwargs={'scope': settings.oauth2.scopes}
)

gaap = oauth.create_client('GAAP')