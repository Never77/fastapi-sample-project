from uuid import UUID, uuid4
import ipaddress
from pydantic import BaseModel


class HostIn(BaseModel):
    manufacturer: str
    name: str
    status: str
    address: ipaddress.IPv4Interface | None = ""


class Host(HostIn):
    id: UUID = uuid4()
