import uvicorn
from fastapi import FastAPI
from router import main_router

from database import async_engine

from admin import UserAdmin, TaskAdmin
from sqladmin import Admin


app = FastAPI()
app.include_router(main_router)

# Admin config
admin = Admin(app, async_engine)
admin.add_view(UserAdmin)
admin.add_view(TaskAdmin)

if __name__ == "__main__":
    uvicorn.run(app, port=8000, workers=1)
