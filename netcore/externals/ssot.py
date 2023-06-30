from typing import Any

import pynautobot

from netcore.config import settings
from netcore.models.backends import APIBackend


class Nautobot(APIBackend):
    client: Any

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        data["client"] = pynautobot.api(url=data.get("url"), token=data.get("token"))
        data["client"].http_session.verify = data.get("ssl_verify")
        super().__init__(**data)


ssot = Nautobot(url=settings.nautobot.url, token=settings.nautobot.token, ssl_verify=settings.nautobot.ssl_verify)
