import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from router import main_router

from database import async_engine

from admin import UserAdmin, TaskAdmin
from sqladmin import Admin

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "https://localhost",
        "https://127.0.0.1",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(main_router, prefix="/api")

# Admin config
admin = Admin(app, async_engine)
admin.add_view(UserAdmin)
admin.add_view(TaskAdmin)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
