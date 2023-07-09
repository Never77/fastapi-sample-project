import strawberry

from netcore.models.hosts import Host
from uuid import UUID


@strawberry.experimental.pydantic.type(model=Host)
class Host:
    id: UUID
    name: str
    address: str
    status: str
    manufacturer: str
