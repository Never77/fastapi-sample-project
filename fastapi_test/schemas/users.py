from pydantic import BaseModel, UUID4
from uuid import uuid4

class UserIn(BaseModel):
    first_name: str
    last_name: str
    email: str

class User(UserIn):
    id: UUID4
    is_active: bool

    class Config:
        orm_mode = True
