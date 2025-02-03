from datetime import datetime, timezone, timedelta

from fastapi import status, HTTPException, Response

from auth.auth import get_password_hash, verify_password
from auth.jwt import create_access_token, create_refresh_token
from auth.models import UserModel, user_repo
from auth.schemas import (
    UserSchema,
    UserCreateSchema,
    UserLoginSchema,
    UserInDbSchema,
)
from config import settings


class AuthService:
    @staticmethod
    async def register_user(user_data: UserCreateSchema) -> UserSchema:
        user_model_email = await user_repo.filter(email=user_data.email)
        user_model_username = await user_repo.filter(username=user_data.username)
        if user_model_email is not None or user_model_username is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Пользователь уже существует",
            )

        hashed_password: str = get_password_hash(user_data.password)
        user_model = UserModel(
            username=user_data.username,
            email=user_data.email.__str__(),
            password_hash=hashed_password,
        )
        user_model = await user_repo.create(user_model)
        return UserSchema.model_validate(user_model, from_attributes=True)

    @staticmethod
    async def authenticate_user(user_data: UserLoginSchema) -> UserInDbSchema:
        incorrect_fields_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Неправильный логин или пароль",
        )

        user_model_email = await user_repo.filter(email=user_data.login)
        user_model_username = await user_repo.filter(username=user_data.login)
        if user_model_email is None and user_model_username is None:
            raise incorrect_fields_exception
        user_model = (
            user_model_username if user_model_username is not None else user_model_email
        )
        if not verify_password(user_data.password, user_model.password_hash):
            raise incorrect_fields_exception

        return UserInDbSchema.model_validate(user_model, from_attributes=True)

    @staticmethod
    async def set_response_tokens(user: UserInDbSchema, response: Response):
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

    @staticmethod
    async def delete_auth_cookies(response: Response):
        response.delete_cookie(key=settings.jwt.ACCESS_TOKEN_NAME)
        response.delete_cookie(key=settings.jwt.REFRESH_TOKEN_NAME)
