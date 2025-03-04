from sqlalchemy.ext.asyncio import AsyncSession

from file_service import create_test_files
from schemas import Pagination
from tasks.models import TaskModel, task_async_repo
from tasks.schemas import TaskCreateSchema, TaskInDBSchema


class TaskService:
    @staticmethod
    async def create_task(
        task_data: TaskCreateSchema,
        session: AsyncSession,
    ) -> TaskInDBSchema:
        example_tests = [
            {"input": example_test.input, "output": example_test.output}
            for example_test in task_data.example_tests
        ]

        task_model = TaskModel(
            text=task_data.text,
            title=task_data.title,
            example_tests=example_tests,
            memory=task_data.memory,
            time=task_data.time,
            test_count=len(task_data.example_tests),
        )
        task_model: TaskModel = await task_async_repo.create(task_model, session)
        create_test_files(task_model.id, task_data.example_tests)
        return TaskInDBSchema.model_validate(task_model, from_attributes=True)

    @staticmethod
    async def get_task(
        task_id: int,
        session: AsyncSession,
    ) -> TaskInDBSchema:
        task_model = await task_async_repo.get_one(task_id, session)
        return TaskInDBSchema.model_validate(task_model, from_attributes=True)

    @staticmethod
    async def get_tasks(
        pagination: Pagination,
        session: AsyncSession,
    ) -> list[TaskInDBSchema]:
        task_models = await task_async_repo.get_page(pagination, session)
        return [
            TaskInDBSchema.model_validate(task_model, from_attributes=True)
            for task_model in task_models
        ]
