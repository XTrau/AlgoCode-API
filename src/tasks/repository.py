from sqlalchemy import select

from database import new_session
from schemas import Pagination
from tasks.models import TaskModel
from tasks.schemas import TaskCreateSchema


class TaskRepository:
    @staticmethod
    async def create_task(task_data: TaskCreateSchema) -> TaskModel:
        async with new_session() as session:
            task_model = TaskModel(
                title=task_data.title,
                text=task_data.text,
                time=task_data.time,
                memory=task_data.memory,
                example_tests=[
                    {"input": test.input, "output": test.output}
                    for test in task_data.example_tests
                ],
            )
            session.add(task_model)
            await session.flush()
            await session.commit()
            return task_model

    @staticmethod
    async def get_one(task_id: int) -> TaskModel:
        async with new_session() as session:
            task_model = await session.get(TaskModel, task_id)
            return task_model

    @staticmethod
    async def get_page(pagination: Pagination) -> list[TaskModel]:
        async with new_session() as session:
            query = (
                select(TaskModel)
                .offset(pagination.page * pagination.count)
                .limit(pagination.count)
            )
            result = await session.execute(query)
            task_models = result.scalars()
            return task_models
