from fastapi import FastAPI
from database import create_database, reset_database
from auth.router import auth_router

app = FastAPI()

app.include_router(auth_router)


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.post("/create_database")
async def reset():
    return await create_database()


@app.post("/reset_database")
async def reset():
    return await reset_database()
