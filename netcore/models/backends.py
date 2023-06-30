from pydantic import BaseModel, AnyHttpUrl
from uuid import UUID
from netcore.models.secrets import Account, Secret
from typing import Any
from abc import ABC, abstractmethod
import requests
from netcore.models.secrets import SecretType
from uuid import uuid4


class Backend(BaseModel, ABC):
    id: UUID = uuid4()

    def ping(self) -> bool:
        """
        This method ensure the backend is still reachable.

        Raises:
            NotImplementedError: it will raise NotImplementedError if the subclass does not implement this method.
        """
        return requests.get(self.url).status_code == 200


class APIBackend(Backend, ABC):
    """
    This class will be the abstraction layer for all the backends used by this app that have an API.

    In this class, url is mandatory because it's needed to reach any API.
    Either account or token can be given, account can be a username/password or only a username. It should cover most of cases in the future for any application.
    """

    url: AnyHttpUrl
    account: Account | None = None
    token: str = None
    ssl_verify: bool = True
