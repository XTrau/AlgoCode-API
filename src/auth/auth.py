from fastapi import Depends, HTTPException, Request
from jwt import InvalidTokenError
from passlib.context import CryptContext
from starlette import status

from auth.jwt import decode_jwt
from auth.repository import UserRepository
from auth.schemas import (
    TokenPair,
    UserLoginSchema,
    UserInDbSchema,
    UserSchema,
    UserCreateSchema,
    get_user_login_schema,
)
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"])


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


async def get_tokens_from_cookies(request: Request) -> TokenPair:
    access_token = request.cookies.get(settings.jwt.ACCESS_TOKEN_NAME, None)
    refresh_token = request.cookies.get(settings.jwt.REFRESH_TOKEN_NAME, None)
    if not access_token or not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неавторизованный пользователь",
        )
    return TokenPair(access_token=access_token, refresh_token=refresh_token)


async def authenticate_user(
    user_data: UserLoginSchema = Depends(get_user_login_schema),
) -> UserInDbSchema:
    incorrect_fields_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Неправильный логин или пароль",
    )

    user_model_email = await UserRepository.get_user_by_email(user_data.login)
    user_model_username = await UserRepository.get_user_by_username(user_data.login)
    if user_model_email is None and user_model_username is None:
        raise incorrect_fields_exception
    user_model = (
        user_model_username if user_model_username is not None else user_model_email
    )
    if not verify_password(user_data.password, user_model.password_hash):
        raise incorrect_fields_exception

    return UserInDbSchema.model_validate(user_model, from_attributes=True)


async def get_current_user(
    token_pair: TokenPair = Depends(get_tokens_from_cookies),
) -> UserInDbSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неавторизованный пользователь",
    )
    try:
        payload_dict = decode_jwt(token_pair.access_token)
        if payload_dict is None:
            raise credentials_exception
        email = payload_dict.get("email")
    except InvalidTokenError:
        raise credentials_exception

    user_model = await UserRepository.get_user_by_email(email=email)
    return UserInDbSchema.model_validate(user_model, from_attributes=True)


async def get_current_active_user(
    user: UserInDbSchema = Depends(get_current_user),
) -> UserInDbSchema:
    if user.banned is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь заблокирован"
        )
    return user


async def get_current_superuser(
    user: UserInDbSchema = Depends(get_current_active_user),
) -> UserInDbSchema:
    if user.is_superuser is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Недостаточно прав"
        )
    return user


async def register_user(user: UserCreateSchema) -> UserSchema:
    user_model_username = await UserRepository.get_user_by_username(user.username)
    user_model_email = await UserRepository.get_user_by_email(user.email.__str__())
    if user_model_email is not None or user_model_username is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь уже существует",
        )

    hashed_password: str = get_password_hash(user.password)
    await UserRepository.create_user(user, hashed_password)
    user_model = await UserRepository.get_user_by_username(user.username)
    return UserSchema.model_validate(user_model, from_attributes=True)
