import uvicorn
from fastapi import FastAPI, status
from database import create_database, reset_database

from auth.router import auth_router
from file_service import clear_upload_folder
from tasks.router import tasks_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(tasks_router, prefix="/tasks")


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
    return {"msg": "База данных успешно очищена"}


if __name__ == "__main__":
    uvicorn.run(app)
