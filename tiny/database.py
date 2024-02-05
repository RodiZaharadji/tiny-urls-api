from contextlib import asynccontextmanager
from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from tiny.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=settings.SQLALCHEMY_ECHO)
session_factory = sessionmaker(engine, class_=AsyncSession, autocommit=False, autoflush=False, expire_on_commit=False)


async def get_db_session() -> AsyncSession:
    session = None
    try:
        session = session_factory()
        yield session
    finally:
        await session.close()


def use_session():
    def _decorator(func):
        async def wrapper(*args, **kwargs):
            async with asynccontextmanager(get_db_session)() as session:
                return await func(*args, **kwargs, session=session)

        return wraps(func)(wrapper)

    return _decorator
