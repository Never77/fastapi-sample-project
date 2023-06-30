from pydantic import BaseModel
from uuid import UUID, uuid4

class Host(BaseModel):
    id: UUID = uuid4()
    name: str
    status: str