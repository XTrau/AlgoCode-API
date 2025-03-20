from fastapi import APIRouter, Depends, status, Response, Form
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import get_current_active_user, set_response_tokens, delete_auth_cookies
from auth.schemas import (
    UserCreateSchema,
    UserInDbSchema,
    UserSchema,
    UserLoginSchema,
)

from auth.service import AuthService
from database import get_async_session

auth_router = router = APIRouter(tags=["Аутентификация"])


async def get_user_login_schema(
    login: str = Form(...), password: str = Form(...)
) -> UserLoginSchema:
    return UserLoginSchema(login=login, password=password)


async def get_user_create_schema(
    username: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
):
    return UserCreateSchema(
        username=username,
        email=email,
        password=password,
    )


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserSchema
)
async def register(
    session: AsyncSession = Depends(get_async_session),
    user: UserCreateSchema = Depends(get_user_create_schema),
):
    user: UserSchema = await AuthService.register_user(user, session)
    return user


@router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
async def login_user(
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    user_data: UserLoginSchema = Depends(get_user_login_schema),
) -> Response:
    user: UserInDbSchema = await AuthService.authenticate_user(
        user_data, response, session
    )
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response) -> Response:
    await delete_auth_cookies(response)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/me", response_model=UserSchema)
async def get_account(user: UserSchema = Depends(get_current_active_user)):
    return user
