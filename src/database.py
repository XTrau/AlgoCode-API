from fastapi import HTTPException, status
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from config import settings


engine = create_async_engine(url=settings.db.database_asyncpg_url)
new_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def create_database():
    try:
        async with engine.begin() as conn:
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
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Произошла ошибка при подключении к базе данных",
        )
