import uvicorn
from fastapi import FastAPI, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from admin import UserAdmin, TaskAdmin
from database import create_database, reset_database, async_engine, get_session

from auth.router import auth_router
from file_service import clear_upload_folder
from solutions.router import solutions_router
from tasks.router import tasks_router

from seed import seed_database

from sqladmin import Admin

from test_system.config import test_system_config
from test_system.schemas import LanguageResponseSchema

app = FastAPI()

app.include_router(auth_router)
app.include_router(tasks_router, prefix="/tasks")
app.include_router(solutions_router, prefix="/tasks")


admin = Admin(app, async_engine)
admin.add_view(UserAdmin)
admin.add_view(TaskAdmin)


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.get("/languages", status_code=status.HTTP_200_OK)
async def get_languages() -> list[LanguageResponseSchema]:
    languages: dict[str, dict] = test_system_config.languages_data
    return [
        LanguageResponseSchema(title=values["title"], mark=key)
        for key, values in languages.items()
    ]


@app.post("/create_database")
async def create():
    return await create_database()


@app.post("/reset_backend", status_code=status.HTTP_200_OK)
async def reset_backend(session: AsyncSession = Depends(get_session)):
    await reset_database()
    clear_upload_folder()
    await seed_database(session)
    return {"msg": "База данных успешно очищена, суперюзер admin создан"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000, workers=1)
