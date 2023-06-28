from typing import List
from uuid import UUID

import strawberry

from fastapi_test import crud, schemas
from fastapi_test.graphql.users import User


@strawberry.type
class Query:
    @strawberry.field
    async def users(self) -> List[User]:
        return [schemas.User(**x.__dict__) for x in await crud.list_users()]  # Must return Pydantic BaseModel to work

    @strawberry.field
    async def user(self, id: UUID) -> User:
        user = await crud.get_user_by_id(id)
        return schemas.User(**user._asdict())
