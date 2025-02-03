from fastapi import APIRouter, Path, status, Body, Depends

from schemas import Pagination, get_pagination
from tasks.schemas import TaskInDBSchema, TaskCreateSchema
from tasks.service import TaskService

tasks_router = router = APIRouter(tags=["Задачи"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreateSchema = Body()) -> TaskInDBSchema:
    return await TaskService.create_task(task_data)


@router.get("/{task_id}", status_code=status.HTTP_200_OK)
async def get_task(task_id: int = Path(gt=0)) -> TaskInDBSchema | None:
    return await TaskService.get_task(task_id)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_tasks(
    pagination: Pagination = Depends(get_pagination),
) -> list[TaskInDBSchema]:
    return await TaskService.get_tasks(pagination)
