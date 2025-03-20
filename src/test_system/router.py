from fastapi import APIRouter, Path, status, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import get_current_active_user
from auth.schemas import UserInDbSchema
from database import get_async_session
from test_system.service import SolutionService

from test_system.tasks import check_solution
from test_system.config import test_system_config
from test_system.schemas import (
    LanguageResponseSchema,
    SolutionSchema,
    SolutionCreateSchema,
)

test_system_router = router = APIRouter(tags=["Тестирование решений"])


@router.get("/languages", status_code=status.HTTP_200_OK)
async def get_languages() -> list[LanguageResponseSchema]:
    languages: dict[str, dict] = test_system_config.languages_data
    return [
        LanguageResponseSchema(title=values["title"], mark=key)
        for key, values in languages.items()
    ]


@router.get("/task/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_solutions(
    task_id: int = Path(gt=0),
    user: UserInDbSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[SolutionSchema]:
    return await SolutionService.get_task_solutions(task_id, user.id, session)


@router.post("/task/{task_id}", status_code=status.HTTP_201_CREATED)
async def create_task_solution(
    solution: SolutionCreateSchema = Body(),
    task_id: int = Path(gt=0),
    user: UserInDbSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session),
) -> SolutionSchema:
    solution_schema: SolutionSchema = await SolutionService.create_solution(
        task_id=task_id, user_id=user.id, solution=solution, session=session
    )
    check_solution.apply_async(args=[solution_schema.id])
    return solution_schema


@router.get("/{solution_id}", status_code=status.HTTP_200_OK)
async def get_solution(
    solution_id: int = Path(gt=0),
    user: UserInDbSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session),
) -> SolutionSchema:
    solution_schema: SolutionSchema = await SolutionService.get_solution(
        solution_id=solution_id, user_id=user.id, session=session
    )
    return solution_schema
