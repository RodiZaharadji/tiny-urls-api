import asyncio
from importlib import import_module
from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine

from tiny.__main__ import create_app
from tiny.common.models import Base
from tiny.config import settings


@pytest.fixture(scope="session", autouse=True)
def init_db():
    """Session-wide database initialization (drop/create)"""
    # Async engine doesn't support DDL operations by default, so we use a sync one for this fixture.
    sync_engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI.replace("postgresql+asyncpg", "postgresql"), future=True
    )

    for path in map(str, Path("tiny").rglob("*[!common]*/models.py")):
        python_path = path.strip(".py").replace("/", ".")
        import_module(python_path)

    Base.metadata.drop_all(bind=sync_engine)
    Base.metadata.create_all(bind=sync_engine)


@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def fastapi_app():
    return create_app()


@pytest.fixture()
async def routes_test_client(fastapi_app):
    async with AsyncClient(app=fastapi_app, base_url=settings.BASE_DOMAIN) as client:
        yield client
