from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, status, Response

from auth.auth import register_user, authenticate_user, get_current_active_user
from auth.jwt import create_access_token, create_refresh_token
from auth.schemas import UserCreateSchema, UserInDbSchema, UserSchema

from auth.schemas import get_user_create_schema
from config import settings

auth_router = router = APIRouter(tags=["Аутентификация"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreateSchema = Depends(get_user_create_schema)):
    print(user.__dict__)
    user = await register_user(user)
    return {"message": "Successfully registered", "user": user}
    # TODO: email verify


@router.post("/login")
async def login_user(
    response: Response, user: UserInDbSchema = Depends(authenticate_user)
):
    refresh_token = create_access_token({"email": user.email})
    access_token = create_refresh_token({"email": user.email})
    response.set_cookie(
        key=settings.jwt.ACCESS_TOKEN_NAME,
        value=access_token,
        expires=datetime.now(timezone.utc)
        + timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_TIME + 30),
        httponly=True,
    )
    response.set_cookie(
        key=settings.jwt.REFRESH_TOKEN_NAME,
        value=refresh_token,
        expires=datetime.now(timezone.utc)
        + timedelta(minutes=settings.jwt.REFRESH_TOKEN_EXPIRE_TIME + 30),
        httponly=True,
    )
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key=settings.jwt.ACCESS_TOKEN_NAME)
    response.delete_cookie(key=settings.jwt.REFRESH_TOKEN_NAME)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/me", response_model=UserSchema)
async def get_account(user: UserSchema = Depends(get_current_active_user)):
    return user
