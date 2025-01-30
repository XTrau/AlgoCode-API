from auth.auth import get_password_hash
from auth.models import UserModel
from database import new_session


async def seed_database():
    async with new_session() as session:
        user = UserModel(
            username="admin",
            password_hash=get_password_hash("admin"),
            is_superuser=True,
            email="admin@mail.ru",
        )
        session.add(user)
        await session.commit()
