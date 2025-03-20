from datetime import datetime, timezone, timedelta

from fastapi import Request, Response, Depends, HTTPException, status
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from auth.exceptions import credentials_exception
from auth.jwt import JwtAPI
from auth.models import async_user_repo
from auth.schemas import TokenPair, UserInDbSchema
from config import settings
from database import get_async_session

pwd_context = CryptContext(schemes=["bcrypt"])


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_token_pair(payload: dict) -> tuple[str, str]:
    access_token = JwtAPI.create_refresh_token(payload)
    refresh_token = JwtAPI.create_access_token(payload)
    return access_token, refresh_token


async def set_response_tokens(
    access_token: str, refresh_token: str, response: Response
):
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


async def delete_auth_cookies(response: Response):
    response.delete_cookie(key=settings.jwt.ACCESS_TOKEN_NAME)
    response.delete_cookie(key=settings.jwt.REFRESH_TOKEN_NAME)


async def find_user(
    session: AsyncSession, username: str | None = None, email: str | None = None
) -> UserInDbSchema:
    user_model = await async_user_repo.filter(session, email=email)
    if user_model is not None:
        return UserInDbSchema.model_validate(user_model, from_attributes=True)
    else:
        user_model = await async_user_repo.filter(session, username=username)
        if user_model is not None:
            return UserInDbSchema.model_validate(user_model, from_attributes=True)


async def get_tokens_from_cookies(request: Request, response: Response) -> TokenPair:
    access_token = request.cookies.get(settings.jwt.ACCESS_TOKEN_NAME, None)
    refresh_token = request.cookies.get(settings.jwt.REFRESH_TOKEN_NAME, None)

    if access_token is None:
        if refresh_token is None:
            raise credentials_exception
        refresh_dict = JwtAPI.decode_jwt(refresh_token)
        if refresh_dict is None:
            raise credentials_exception

        email = refresh_dict.get("email")
        access_token, refresh_token = create_token_pair({"email": email})
        await set_response_tokens(access_token, refresh_token, response)

    return TokenPair(access_token=access_token, refresh_token=refresh_token)


async def get_current_user(
    session: AsyncSession = Depends(get_async_session),
    token_pair: TokenPair = Depends(get_tokens_from_cookies),
) -> UserInDbSchema:
    try:
        payload_dict = JwtAPI.decode_jwt(token_pair.access_token)
        if payload_dict is None:
            raise credentials_exception
        email = payload_dict.get("email")
    except InvalidTokenError:
        raise credentials_exception

    user_model = await async_user_repo.filter(session, email=email)
    return UserInDbSchema.model_validate(user_model, from_attributes=True)


async def get_current_active_user(
    user: UserInDbSchema = Depends(get_current_user),
) -> UserInDbSchema:
    if user.banned is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь заблокирован",
        )
    return user


async def get_current_superuser(
    user: UserInDbSchema = Depends(get_current_active_user),
) -> UserInDbSchema:
    if not user.is_superuser is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Недостаточно прав"
        )
    return user
