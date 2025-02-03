from auth.auth import get_password_hash
from auth.models import UserModel
from database import new_session
from solutions.models import LanguageModel


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

    async with new_session() as session:
        models = [
            LanguageModel(
                title="C++20 (g++)",
                compile="g++ {source} -o {executable} -O2 -std=c++20",
                run="{executable}",
                extension="cpp",
                compiled=True,
            ),
            LanguageModel(
                title="Python 3.10",
                run="python3 {executable}",
                extension="py",
                compiled=False,
            ),
            LanguageModel(
                title="Java 8",
                compile="javac {source}",
                run="java -cp {directory} {classname}",
                extension="java",
                compiled=True,
            ),
        ]
        session.add_all(models)
        await session.commit()
