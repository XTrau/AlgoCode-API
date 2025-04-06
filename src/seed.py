from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import get_password_hash
from auth.models import UserModel
from tasks.schemas import TaskCreateSchema, TestSchema
from tasks.service import TaskService


async def seed_database(session: AsyncSession):
    user = UserModel(
        username="admin",
        password_hash=get_password_hash("admin"),
        is_superuser=True,
        email="admin@mail.ru",
    )
    session.add(user)
    await session.commit()

    task_data: TaskCreateSchema = TaskCreateSchema(
        title="Сумма",
        text="Напишите программу которая принимает два числа и выводи их сумму",
        input_format="В первой строке вводятся два числа a, b (0 <= a <= 10e9, 0 <= b <= 10e9)\nНеобходимо вывести сумму этих чисел.",
        time=1,
        memory=64,
        example_tests=[
            TestSchema(input="1 2", output="3"),
            TestSchema(input="10 -20", output="-10"),
        ],
    )
    await session.commit()
    await TaskService.create_task(task_data, session)
