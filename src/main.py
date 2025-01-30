import uvicorn
from fastapi import FastAPI, status

from admin import UserAdmin, TaskAdmin
from database import create_database, reset_database, engine

from auth.router import auth_router
from file_service import clear_upload_folder
from seed import seed_database
from tasks.router import tasks_router

from sqladmin import Admin

app = FastAPI()

app.include_router(auth_router)
app.include_router(tasks_router, prefix="/tasks")


admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(TaskAdmin)


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.post("/create_database")
async def create():
    return await create_database()


@app.post("/reset_backend", status_code=status.HTTP_200_OK)
async def reset_backend():
    await reset_database()
    clear_upload_folder()
    await seed_database()
    return {"msg": "База данных успешно очищена, суперюзер admin создан"}


if __name__ == "__main__":
    uvicorn.run(app)
