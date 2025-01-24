from datetime import datetime, timezone, timedelta

import jwt

from config import settings


def encode_jwt(
    payload: dict,
    expire_time: int,
    token_type: str,
    secret_key: str = settings.jwt.private_key_path.read_text(),
    algorithm: str = settings.jwt.ALGORITHM,
):
    to_encode = {"sub": payload}
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_time)
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(payload, key=secret_key, algorithm=algorithm)


def create_access_token(payload: dict):
    return encode_jwt(
        payload, settings.jwt.ACCESS_TOKEN_EXPIRE_TIME, settings.jwt.ACCESS_TOKEN_NAME
    )


def create_refresh_token(payload: dict):
    return encode_jwt(
        payload, settings.jwt.REFRESH_TOKEN_EXPIRE_TIME, settings.jwt.REFRESH_TOKEN_NAME
    )


def decode_jwt(
    token: str,
    public_key: str = settings.jwt.public_key_path.read_text(),
    algorithm: str = settings.jwt.ALGORITHM,
) -> dict:
    return jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
