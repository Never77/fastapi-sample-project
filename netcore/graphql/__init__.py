from typing import List
from uuid import UUID

import strawberry

from netcore import crud, models
from netcore.graphql.users import User
from netcore.graphql.hosts import Host

@strawberry.type
class Query:
    @strawberry.field
    async def users(self) -> List[User]:
        return [models.User(**x.__dict__) for x in await crud.list_users()]  # Must return Pydantic BaseModel to work

    @strawberry.field
    async def user(self, id: UUID) -> User:
        user = await crud.get_user_by_id(id)
        return models.User(**user._asdict())
    
    @strawberry.field
    async def hosts(self) -> List[Host]:
        return crud.list_hosts()
