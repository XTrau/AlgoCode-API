from pydantic import BaseModel, EmailStr, field_validator
from typing import ClassVar
from fastapi import HTTPException, status, Form


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    USERNAME_ALLOWED_CHARACTERS: ClassVar[str] = "1234567890abcdefghijklmnopqrstuvwxyz_"

    @field_validator("username", mode="before")
    def validate_username(cls, username: str):
        if len(username) == 0:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Username must be not null",
            )
        elif len(username) <= 4:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Username length must be more than 4 characters",
            )
        elif len(username) > 32:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Username length must be less or equal than 32 characters",
            )

        if not all(
            symbol in UserCreateSchema.USERNAME_ALLOWED_CHARACTERS
            for symbol in username.lower()
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Username must contain only numbers and latin symbols and signs _",
            )

        return username

    @field_validator("password", mode="before")
    def validate_password(cls, password: str):
        if len(password) < 8:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password length must be more than 7 characters",
            )
        return password


class UserLoginSchema(BaseModel):
    login: str
    password: str


class UserSchema(BaseModel):
    username: str
    email: str
    banned: bool
    is_superuser: bool


class UserInDbSchema(UserSchema):
    id: int
    password_hash: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
