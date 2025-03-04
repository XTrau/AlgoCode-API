from typing import TypeVar, Generic, Type

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base
from schemas import Pagination

ModelType = TypeVar("ModelType", bound=Base)


class GenericAsyncRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_all(self, session: AsyncSession) -> list[ModelType]:
        query = select(self.model)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_one(self, obj_id: int, session: AsyncSession) -> ModelType | None:
        query = select(self.model).filter_by(id=obj_id)
        result = await session.execute(query)
        return result.scalar()

    async def filter(self, session: AsyncSession, **conditions) -> ModelType:
        stmt = select(self.model).filter_by(**conditions)
        result = await session.execute(stmt)
        model = result.scalar()
        return model

    async def filter_all(self, session: AsyncSession, **conditions) -> list[ModelType]:
        stmt = select(self.model).filter_by(**conditions)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def complex_filter(self, *conditions, session: AsyncSession):
        stmt = select(self.model).filter(*conditions)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_page(
        self, pagination: Pagination, session: AsyncSession
    ) -> list[ModelType]:

        query = (
            select(self.model)
            .offset(pagination.page * pagination.count)
            .limit(pagination.count)
        )
        result = await session.execute(query)
        task_models = result.scalars().all()
        return task_models

    async def create(self, obj: ModelType, session: AsyncSession) -> ModelType:
        session.add(obj)
        await session.flush()
        await session.commit()
        return obj

    async def create_all(
        self, objs: list[ModelType], session: AsyncSession
    ) -> list[ModelType]:
        session.add_all(objs)
        await session.flush()
        await session.commit()
        return objs

    async def update(
        self, obj_id: int, new_obj: ModelType, session: AsyncSession
    ) -> ModelType:
        stmt = (
            update(self.model).where(self.model.id == obj_id).values(**new_obj.__dict__)
        )
        await session.execute(stmt)
        await session.flush()
        await session.commit()
        return new_obj

    async def patch(self, obj_id: int, session: AsyncSession, **kwargs) -> ModelType:
        stmt = update(self.model).where(self.model.id == obj_id).values(**kwargs)
        await session.execute(stmt)
        await session.commit()
        return await self.get_one(obj_id, session)

    async def delete(self, obj_id: int, session: AsyncSession):
        obj = await session.query(self.model).filter_by(id=obj_id).first()
        await session.delete(obj)
        await session.commit()


class GenericSyncRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_all(self, session: Session) -> list[ModelType]:
        query = select(self.model)
        result = session.execute(query)
        return result.scalars().all()

    def get_one(self, obj_id: int, session: Session) -> ModelType | None:
        query = select(self.model).filter_by(id=obj_id)
        result = session.execute(query)
        return result.scalar()

    def filter(self, session: Session, **conditions) -> ModelType:
        stmt = select(self.model).filter_by(**conditions)
        result = session.execute(stmt)
        model = result.scalar()
        return model

    def filter_all(self, session: Session, **conditions) -> list[ModelType]:
        stmt = select(self.model).filter_by(**conditions)
        result = session.execute(stmt)
        return result.scalars().all()

    def complex_filter(self, *conditions, session: Session):
        stmt = select(self.model).filter(*conditions)
        result = session.execute(stmt)
        return result.scalars().all()

    def get_page(self, pagination: Pagination, session: Session) -> list[ModelType]:

        query = (
            select(self.model)
            .offset(pagination.page * pagination.count)
            .limit(pagination.count)
        )
        result = session.execute(query)
        task_models = result.scalars().all()
        return task_models

    def create(self, obj: ModelType, session: Session) -> ModelType:
        session.add(obj)
        session.flush()
        session.commit()
        return obj

    def create_all(self, objs: list[ModelType], session: Session) -> list[ModelType]:
        session.add_all(objs)
        session.flush()
        session.commit()
        return objs

    def update(self, obj_id: int, new_obj: ModelType, session: Session) -> ModelType:
        stmt = (
            update(self.model).where(self.model.id == obj_id).values(**new_obj.__dict__)
        )
        session.execute(stmt)
        session.flush()
        session.commit()
        return new_obj

    def patch(self, obj_id: int, session: Session, **kwargs) -> ModelType:
        stmt = update(self.model).where(self.model.id == obj_id).values(**kwargs)
        session.execute(stmt)
        session.commit()
        return self.get_one(obj_id, session)

    def delete(self, obj_id: int, session: Session):
        obj = session.query(self.model).filter_by(id=obj_id).first()
        session.delete(obj)
        session.commit()
