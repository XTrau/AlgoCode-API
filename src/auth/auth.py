from fastapi import Depends, HTTPException, Request
from jwt import InvalidTokenError
from passlib.context import CryptContext
from starlette import status

from auth.jwt import decode_jwt
from auth.models import user_repo
from auth.schemas import (
    TokenPair,
    UserInDbSchema,
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

    user_model = await user_repo.filter(email=email)
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
