from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import get_current_active_user
from auth.schemas import (
    UserCreateSchema,
    UserInDbSchema,
    UserSchema,
    UserLoginSchema,
    get_user_login_schema,
)

from auth.schemas import get_user_create_schema
from auth.service import AuthService
from database import get_session

auth_router = router = APIRouter(tags=["Аутентификация"])


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserSchema
)
async def register(
    session: AsyncSession = Depends(get_session),
    user: UserCreateSchema = Depends(get_user_create_schema),
):
    user: UserSchema = await AuthService.register_user(user, session)
    return user


@router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
async def login_user(
    response: Response,
    session: AsyncSession = Depends(get_session),
    user_data: UserLoginSchema = Depends(get_user_login_schema),
) -> Response:
    user: UserInDbSchema = await AuthService.authenticate_user(user_data, session)
    await AuthService.set_response_tokens(user, response)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response) -> Response:
    await AuthService.delete_auth_cookies(response)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/me", response_model=UserSchema)
async def get_account(user: UserSchema = Depends(get_current_active_user)):
    return user
