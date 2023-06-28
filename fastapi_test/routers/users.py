from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_redis_cache import cache
from fastapi_security import User as SecurityUser

from fastapi_test.config import settings
from fastapi_test.crud import user as crud
from fastapi_test.schemas import users as schemas
from fastapi_test.security import security

router = APIRouter(prefix="/users", tags=["users"])

# Security purpose

if settings.oidc_discovery_url:

    @cache(expire=300)
    @router.get("/me")
    async def get_user_details(user: SecurityUser = Depends(security.user_with_info)) -> SecurityUser:
        """
        Returns user details, regardless of whether user is authenticated or not.

        Args:
            user (SecurityUser, optional): User send by SSO. Defaults to Depends(security.user_with_info).

        Returns:
            security.User: User send by SSO and read by fastapi_security package.
        """
        return user.without_access_token()

    @cache(expire=300)
    @router.get("/me/permissions", response_model=List[str])
    async def get_user_permissions(user: SecurityUser = Depends(security.authenticated_user_or_401)) -> List[str]:
        """
        This function returns the permissions of the user if he's authenticated by SSO.
        TODO: need to check here what the SSO send and maybe how to convert datas to fit with custom SSO.

        Args:
            user (SecurityUser, optional): code sent by the SSO. Defaults to Depends(security.authenticated_user_or_401). # noqa

        Returns:
            List[str]: List of permissions the user holds.
        """
        return user.permissions


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
