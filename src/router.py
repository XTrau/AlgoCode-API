from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session, reset_database
from file_service import clear_upload_folder
from seed import seed_database

from auth.router import auth_router
from solutions.router import solutions_router
from tasks.router import tasks_router
from test_system.router import test_system_router


main_router = APIRouter()

main_router.include_router(auth_router, prefix="/auth")
main_router.include_router(tasks_router, prefix="/tasks")
main_router.include_router(solutions_router, prefix="/solutions")
main_router.include_router(test_system_router)


# Test router
@main_router.get("/ping")
async def ping():
    return {"message": "pong"}


@main_router.post("/reset_backend", status_code=status.HTTP_200_OK)
async def reset_backend(session: AsyncSession = Depends(get_async_session)):
    await reset_database()
    clear_upload_folder()
    await seed_database(session)
    return {"msg": "База данных успешно очищена, суперюзер admin создан"}
