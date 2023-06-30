from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.future import select

from netcore import models, schemas
from netcore.database import get_session


async def list_users(skip: int = 0, limit: int = 100):
    async with get_session() as session:
        query = select(schemas.User).offset(skip).limit(limit)
        return (await session.execute(query)).scalars().all()


async def create_user(user: models.UserIn):
    async with get_session() as session:
        db_user = schemas.User(**user.dict())
        session.add(db_user)
        await session.commit()
        return db_user


async def get_user_by_id(id: UUID):
    async with get_session() as session:
        query = await session.execute(select(schemas.User).where(schemas.User.id == id))
        return query.scalar_one()


async def delete_user_by_id(id: UUID):
    async with get_session() as session:
        query = delete(schemas.User).where(schemas.User.id == id)
        return await session.execute(query)
