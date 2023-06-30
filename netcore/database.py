from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker

from netcore.config import settings

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
