from typing import List
from uuid import uuid4

import hvac

from netcore.config import settings
from netcore.models import APIBackend
from netcore.models.secrets import Secret, Account

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

    def list_secrets(self, mount_point) -> List[Secret]:
        if not self.client.is_authenticated():
            raise Exception("Application is not authenticated by Vault")
        if self.client.sys.is_sealed():
            # TODO: Unseal it
            raise Exception("Vault is sealed")
        response = self.client.kv.list_secrets(mount_point=mount_point, path="/")
        result = []
        for key in response.get("data").get("keys"):
            response = self.client.secrets.kv.v2.read_secret_version(mount_point=mount_point, path=key, version=1)
            for k, v in response.get("data").get("data").items():
                result.append(Account(username=k, password=v))
        return result

    def get_secret(self, mount_point: str, path: str) -> Secret:
        if not self.client.is_authenticated():
            raise Exception("Application is not authenticated by Vault")
        if self.client.sys.is_sealed():
            # TODO: Unseal it
            raise Exception("Vault is sealed")
        return self.client.secrets.kv.v2.read_secret_version(mount_point=mount_point, path=path)


# HashicorpVault.update_forward_refs()
vault = HashicorpVault(
    id=uuid4(),
    token=settings.vault.token,
    url=settings.vault.url,
    ssl_verify=settings.vault.ssl_verify,
)
