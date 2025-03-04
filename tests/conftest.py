import asyncio
from typing import AsyncGenerator

import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from database import get_session
from main import app
from config import settings
from celery_config import celery_app

from httpx import AsyncClient, ASGITransport

engine = create_async_engine(settings.db.database_asyncpg_url)
TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


# Подмена зависимости в приложении
app.dependency_overrides[get_session] = override_get_async_session
celery_app.conf.update(
    task_always_eager=True,
    task_eager_propagates=True,
    broker_url="memory://",
    result_backend="rpc://",
)


@pytest.fixture(scope="session")
async def client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="function")
async def admin_client(client: AsyncClient) -> AsyncClient:
    user_data = {"login": "admin", "password": "admin"}
    response = await client.post("/login", data=user_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    yield client
    response = await client.post("/logout")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.fixture(scope="function")
async def reset_backend(client: AsyncClient):
    assert settings.MODE == "TEST"
    response = await client.post("/reset_backend")
    assert response.status_code == 200


@pytest.fixture(scope="class")
async def reset_backend_class(client: AsyncClient):
    assert settings.MODE == "TEST"
    response = await client.post("/reset_backend")
    assert response.status_code == 200
