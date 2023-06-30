from enum import Enum
from uuid import UUID

from pydantic import BaseModel, SecretStr


class SecretType(str, Enum):
    """
    If you need to add secret type, just add them here.
    """

    username = "username"
    password = "password"
    token = "token"


class Secret(BaseModel):
    id: UUID
    type: SecretType
    value: SecretStr


class Account(BaseModel):
    id: UUID
    username: str = None
    password: SecretStr = None
