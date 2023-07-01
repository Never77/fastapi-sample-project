from contextlib import asynccontextmanager
from typing import AsyncGenerator
from bson import ObjectId
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker

from netcore.config import settings
import motor.motor_asyncio

engine = create_async_engine(settings.database_url, future=True, echo=True)
async_session = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession, autocommit=False, autoflush=False
)


@as_declarative()
class Base:
    """
    Base class to inherit from when we want to create a table in the database.
    I customized it to be able to give ORM object as dict to convert them into Pydantic objects if needed.
    You can see an example in graphql module.
    """

    def _asdict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """_summary_
    This function return a session usable within an async context manager in another submodule for example.
    The goal is to have access to the database as easy as possible.

    Returns:
        AsyncGenerator[AsyncSession, None]

    Yields:
        Iterator[AsyncGenerator[AsyncSession, None]]
    """
    async with async_session() as session:
        async with session.begin():
            try:
                yield session
            finally:
                await session.close()

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)
mongodb = client.netcore  # it is the database name right here

class PyObjectId(ObjectId):
    """
    MongoDB stores objects as BSON, ObjectId let us convert it as JSON dict easily with Python.
    This class allow us to use ObjectId stored in MongoDB as Pydantic Field.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")