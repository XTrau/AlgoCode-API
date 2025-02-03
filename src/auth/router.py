from fastapi import APIRouter, Depends, status, Response

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

auth_router = router = APIRouter(tags=["Аутентификация"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreateSchema = Depends(get_user_create_schema)):
    user = await AuthService.register_user(user)
    return {"message": "Successfully registered", "user": user}


@router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
async def login_user(
    response: Response, user_data: UserLoginSchema = Depends(get_user_login_schema)
) -> Response:
    user: UserInDbSchema = await AuthService.authenticate_user(user_data)
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
