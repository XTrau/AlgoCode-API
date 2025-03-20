from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неавторизованный пользователь",
)

incorrect_fields_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Неправильный логин или пароль",
)
