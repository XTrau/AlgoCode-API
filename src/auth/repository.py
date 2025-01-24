from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import UserModel
from auth.schemas import UserCreateSchema
from database import new_session


class UserRepository:
    @staticmethod
    async def get_user_by_username(username: str):
        async with new_session() as session:
            query = select(UserModel).where(UserModel.username == username)
            result = await session.execute(query)
            user = result.scalar()
            return user

    @staticmethod
    async def get_user_by_email(email: str):
        async with new_session() as session:
            query = select(UserModel).where(UserModel.email == email)
            result = await session.execute(query)
            user = result.scalar()
            return user

    @staticmethod
    async def create_user(user: UserCreateSchema, password_hash: str):
        async with new_session() as session:
            user = UserModel(
                username=user.username,
                email=user.email.__str__(),
                password_hash=password_hash,
            )
            session.add(user)
            await session.commit()
