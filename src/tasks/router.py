from fastapi import APIRouter, Path, status, Body

from file_service import create_test_files
from schemas import Pagination
from tasks.models import TaskModel
from tasks.repository import TaskRepository
from tasks.schemas import TaskInDBSchema, TaskCreateSchema, Solution

tasks_router = router = APIRouter(tags=["Задачи"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreateSchema = Body()) -> TaskInDBSchema:
    task_model: TaskModel = await TaskRepository.create_task(task_data)
    create_test_files(task_model.id, task_data.example_tests)
    return TaskInDBSchema.model_validate(task_model, from_attributes=True)


@router.get("/{task_id}", status_code=status.HTTP_200_OK)
async def get_task(task_id: int = Path(gt=0)) -> TaskInDBSchema | None:
    task_model: TaskModel = await TaskRepository.get_one(task_id)
    return TaskInDBSchema.model_validate(task_model, from_attributes=True)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_tasks(pagination: Pagination) -> list[TaskInDBSchema]:
    task_models: list[TaskModel] = await TaskRepository.get_page(pagination)
    return [
        TaskInDBSchema.model_validate(task_model, from_attributes=True)
        for task_model in task_models
    ]


@router.post("/{task_id}/solutions")
async def create_task_solution(solution: Solution = Body(), task_id: int = Path(gt=0)):

    return {"msg": "Задача успешно отправлена"}


@router.get("/{task_id}/solutions")
async def get_task_solutions():
    pass
    # solutions =
    # return solutions
