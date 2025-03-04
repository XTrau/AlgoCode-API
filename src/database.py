from typing import AsyncIterator

from fastapi import HTTPException, status, Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings


sync_engine = create_engine(
    url=settings.db.database_psycopg2_url, pool_size=10, max_overflow=5
)
sync_session_maker = sessionmaker(bind=sync_engine)

async_engine = create_async_engine(url=settings.db.database_asyncpg_url)
async_session_maker = async_sessionmaker(bind=async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    id: int


async def get_async_session() -> AsyncIterator[AsyncSession]:
    async with async_session_maker() as session:
        yield session


def get_sync_session():
    session = sync_session_maker()
    try:
        yield session
    finally:
        session.close()


async def create_database():
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()
            return {"success": True, "msg": "База данных успешно создана"}
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Произошла ошибка при подключении к базе данных",
        )


async def reset_database():
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Произошла ошибка при подключении к базе данных",
        )
