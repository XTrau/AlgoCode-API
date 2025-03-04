from fastapi import APIRouter, Path, status, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import get_current_superuser
from auth.schemas import UserInDbSchema
from database import get_async_session
from schemas import Pagination, get_pagination
from tasks.schemas import TaskInDBSchema, TaskCreateSchema
from tasks.service import TaskService

tasks_router = router = APIRouter(tags=["Задачи"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreateSchema = Body(),
    session: AsyncSession = Depends(get_async_session),
    admin: UserInDbSchema = Depends(get_current_superuser),
) -> TaskInDBSchema:
    return await TaskService.create_task(task_data, session)


@router.get("/{task_id}", status_code=status.HTTP_200_OK)
async def get_task(
    task_id: int = Path(gt=0), session: AsyncSession = Depends(get_async_session)
) -> TaskInDBSchema | None:
    return await TaskService.get_task(task_id, session)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_tasks(
    pagination: Pagination = Depends(get_pagination),
    session: AsyncSession = Depends(get_async_session),
) -> list[TaskInDBSchema]:
    return await TaskService.get_tasks(pagination, session)
