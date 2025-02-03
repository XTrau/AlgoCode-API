from typing import TypeVar, Generic, Type

from sqlalchemy import select, update

from database import Base, new_session
from schemas import Pagination

ModelType = TypeVar("ModelType", bound=Base)


class GenericRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_all(self) -> list[ModelType]:
        async with new_session() as session:
            return session.query(self.model).all()

    async def get_one(self, obj_id: int) -> ModelType | None:
        async with new_session() as session:
            query = select(self.model).filter_by(id=obj_id)
            result = await session.execute(query)
            return result.scalar()

    async def filter(self, **conditions) -> ModelType:
        async with new_session() as session:
            stmt = select(self.model).filter_by(**conditions)
            result = await session.execute(stmt)
            return result.scalars().first()

    async def filter_all(self, **conditions) -> list[ModelType]:
        async with new_session() as session:
            stmt = select(self.model).filter_by(**conditions)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def complex_filter(self, *conditions):
        async with new_session() as session:
            stmt = select(self.model).filter(*conditions)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_page(self, pagination: Pagination) -> list[ModelType]:
        async with new_session() as session:
            query = (
                select(self.model)
                .offset(pagination.page * pagination.count)
                .limit(pagination.count)
            )
            result = await session.execute(query)
            task_models = result.scalars().all()
            return task_models

    async def create(self, obj: ModelType) -> ModelType:
        async with new_session() as session:
            session.add(obj)
            await session.flush()
            await session.commit()
        return obj

    async def create_all(self, objs: list[ModelType]) -> list[ModelType]:
        async with new_session() as session:
            session.add_all(objs)
            await session.flush()
            await session.commit()
        return objs

    async def update(self, obj_id: int, new_obj: ModelType) -> ModelType:
        async with new_session() as session:
            stmt = (
                update(self.model)
                .where(self.model.id == obj_id)
                .values(**new_obj.__dict__)
            )
            await session.execute(stmt)
            await session.flush()
            await session.commit()
        return new_obj

    async def delete(self, obj_id: int):
        async with new_session() as session:
            obj = session.query(self.model).filter_by(id=obj_id).first()
            session.delete(obj)
            await session.commit()
