from uuid import UUID, uuid4

from pydantic import BaseModel


class Host(BaseModel):
    id: UUID = uuid4()
    name: str
    status: str
