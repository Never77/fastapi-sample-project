from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi_redis_cache import cache

from fastapi_test.crud import user as crud
from fastapi_test.schemas import users as schemas

router = APIRouter(prefix="/users", tags=["users"])


@cache(expire=300)
@router.get("/", response_model=List[schemas.User])
async def list_users(skip: int = 0, limit: int = 100):
    return await crud.list_users(skip=skip, limit=limit)


@cache(expire=300)
@router.get("/{id}", response_model=schemas.User)
async def get_user_by_id(id: UUID):
    return await crud.get_user_by_id(id=id)


@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserIn):
    return await crud.create_user(user=user)


@router.delete("/{id}", status_code=204)
async def delete_user_by_id(id: UUID):
    return await crud.delete_user_by_id(id=id)


# TODO: Need a route to update the user by id
