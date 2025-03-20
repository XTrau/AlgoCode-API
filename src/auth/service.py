from fastapi import status, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import (
    verify_password,
    get_password_hash,
    find_user,
    set_response_tokens,
    create_token_pair,
)
from auth.exceptions import incorrect_fields_exception
from auth.models import UserModel, async_user_repo
from auth.schemas import (
    UserSchema,
    UserCreateSchema,
    UserLoginSchema,
    UserInDbSchema,
)


class AuthService:
    @staticmethod
    async def register_user(
        user_data: UserCreateSchema, session: AsyncSession
    ) -> UserSchema:
        user_model = await find_user(session, user_data.username, user_data.email)
        if user_model is not None:
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
        user_model = await async_user_repo.create(user_model, session)
        return UserSchema.model_validate(user_model, from_attributes=True)

    @staticmethod
    async def authenticate_user(
        user_data: UserLoginSchema, response: Response, session: AsyncSession
    ) -> UserInDbSchema:
        user_model = await find_user(session, user_data.login, user_data.login)
        if user_model is None:
            raise incorrect_fields_exception
        if not verify_password(user_data.password, user_model.password_hash):
            raise incorrect_fields_exception

        access_token, refresh_token = create_token_pair({"email": user_model.email})
        await set_response_tokens(access_token, refresh_token, response)

        return UserInDbSchema.model_validate(user_model, from_attributes=True)
