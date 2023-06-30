from typing import List
from uuid import uuid4

import hvac

from netcore.config import settings
from netcore.models import APIBackend
from netcore.models.secrets import Secret

# TODO: make work this class


class HashicorpVault(APIBackend):
    """
    Wrapper for the Hashicorp Vault backend.
    """

    client: hvac.Client = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        kwargs["client"] = hvac.Client(
            url=kwargs.get("url"),
            token=kwargs.get("token"),
            verify=kwargs.get("ssl_verify"),
            cert=(settings.vault.cert_path, settings.vault.cert_key) or None,
        )
        super().__init__(**kwargs)

    def ping(self):
        return self.client.is_authenticated()

    def list_secrets(self, path) -> List[Secret]:
        return self.client.kv.list_secrets(mount_point="secret", path=path)

    def get_secret(self, path: str) -> Secret:
        self.client.is_authenticated()
        if self.client.sys.is_sealed():
            # TODO: Unseal it
            raise Exception("Vault is sealed")
        return self.client.secrets.kv.v1.read_secret_version(mount_point="secret", path=path)


# HashicorpVault.update_forward_refs()
vault = HashicorpVault(
    id=uuid4(),
    token=settings.vault.token,
    url=settings.vault.url,
    ssl_verify=settings.vault.ssl_verify,
)
