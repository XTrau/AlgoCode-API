from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from solutions.models import SolutionModel, solutions_async_repo
from solutions.schemas import SolutionCreateSchema, SolutionSchema


class SolutionService:
    @staticmethod
    async def get_task_solutions(
        task_id: int, user_id: int, session: AsyncSession
    ) -> list[SolutionSchema]:
        solution_models: list[SolutionModel] = (
            await solutions_async_repo.complex_filter(
                SolutionModel.task_id == task_id,
                SolutionModel.user_id == user_id,
                session=session,
            )
        )
        return [
            SolutionSchema.model_validate(solution_model, from_attributes=True)
            for solution_model in solution_models
        ]

    @staticmethod
    async def create_solution(
        solution: SolutionCreateSchema,
        task_id: int,
        user_id: int,
        session: AsyncSession,
    ) -> SolutionSchema:
        solution_model = SolutionModel(
            code=solution.code,
            language=solution.language,
            user_id=user_id,
            task_id=task_id,
        )
        solution_model = await solutions_async_repo.create(solution_model, session)
        return SolutionSchema.model_validate(solution_model, from_attributes=True)

    @staticmethod
    async def get_solution(
        solution_id: int, user_id: int, session: AsyncSession
    ) -> SolutionSchema:
        solution_model: SolutionModel | None = await solutions_async_repo.get_one(
            solution_id, session
        )
        if solution_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Решение с указанным id не найдено",
            )

        if solution_model.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав",
            )

        return SolutionSchema.model_validate(solution_model, from_attributes=True)
