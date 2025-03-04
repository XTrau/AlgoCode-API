from fastapi import APIRouter, Path, status, Body, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import get_current_active_user
from auth.schemas import UserInDbSchema
from database import get_async_session
from solutions.schemas import SolutionCreateSchema, SolutionSchema
from solutions.service import SolutionService
from test_system.tasks import check_solution

solutions_router = router = APIRouter(tags=["Тестирование решений"])


@router.post("/{task_id}/solutions", status_code=status.HTTP_201_CREATED)
async def create_task_solution(
    solution: SolutionCreateSchema = Body(),
    task_id: int = Path(gt=0),
    user: UserInDbSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    solution_schema: SolutionSchema = await SolutionService.create_solution(
        task_id=task_id, user_id=user.id, solution=solution, session=session
    )
    check_solution.apply_async(args=[solution_schema.id])
    return {"msg": "Задача успешно отправлена", "result": solution_schema}


@router.get("/{task_id}/solutions", status_code=status.HTTP_200_OK)
async def get_task_solutions(
    task_id: int = Path(gt=0),
    user: UserInDbSchema = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[SolutionSchema]:
    return await SolutionService.get_task_solutions(task_id, user.id, session)
