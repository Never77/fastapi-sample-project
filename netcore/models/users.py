from uuid import UUID

from pydantic import BaseModel


class UserIn(BaseModel):
    first_name: str
    last_name: str
    email: str


class User(UserIn):
    id: UUID
    is_active: bool

    class Config:
        orm_mode = True
