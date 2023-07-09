from typing import List
from uuid import UUID

import strawberry

from netcore import crud, models
from netcore.graphql.hosts import Host
from netcore.graphql.users import User
from netcore.graphql.secrets import Account
from netcore.graphql.posts import Post

from netcore.database import mongodb


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

    @strawberry.field
    async def accounts(self, mount_point: str) -> List[Account]:
        return crud.list_secrets(mount_point=mount_point)

    @strawberry.field
    async def posts(self, limit: int = 1000) -> List[Post]:
        return [Post(id=x.get("_id"), content=x.get("content")) for x in await mongodb["posts"].find().to_list(limit)]
