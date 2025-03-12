import pytest
from fastapi import status
from httpx import AsyncClient

from conftest import admin_client

test_register_user_params = [
    ("XTray", "exam@mail", "qweqweqw", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ("XTray", "example@mail.ru", "qwe", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ("XTray", "example@mail.ru", "qweqweqwe", status.HTTP_201_CREATED),
    ("XTra1", "example1@mail.ru", "qweqweqwe", status.HTTP_201_CREATED),
    ("XTray", "example@mail.ru", "qweqwe1e", status.HTTP_403_FORBIDDEN),
    ("XTray", "example2@mail.ru", "qweqwe1e", status.HTTP_403_FORBIDDEN),
    ("XTray2", "example@mail.ru", "qweqwe1e", status.HTTP_403_FORBIDDEN),
]

test_login_user_params = [
    ("XTray", "", status.HTTP_403_FORBIDDEN),
    ("XTray", 23, status.HTTP_403_FORBIDDEN),
    ("", "qweqweqweqwe", status.HTTP_403_FORBIDDEN),
    ("username123", "qweqweqweqwe", status.HTTP_403_FORBIDDEN),
    ("XTray", "qweqweqweqwe", status.HTTP_403_FORBIDDEN),
    ("XTray", "qweqweqwe", status.HTTP_204_NO_CONTENT),
]


@pytest.mark.usefixtures("reset_backend_class")
class TestAuth:
    @pytest.mark.asyncio(loop_scope="session")
    async def test_admin(self, admin_client: AsyncClient):
        response = await admin_client.get("/auth/me")
        obj = response.json()
        assert obj["username"] == "admin"
        assert obj["is_superuser"] == True

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.parametrize(
        "username, email, password, status_code", test_register_user_params
    )
    async def test_register_user(
        self,
        username: str,
        email: str,
        password: str,
        status_code: int,
        client: AsyncClient,
    ):
        user_data = {
            "username": username,
            "email": email,
            "password": password,
        }
        response = await client.post("/auth/register", data=user_data)
        assert response.status_code == status_code

        if status_code // 2 == 100:
            user = response.json()
            assert username == user["username"]
            assert email == user["email"]
            assert user["is_superuser"] is False
            assert user["banned"] is False

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.parametrize("login, password, status_code", test_login_user_params)
    async def test_login_user(
        self,
        login,
        password,
        status_code,
        client: AsyncClient,
    ):
        login_data = {
            "login": login,
            "password": password,
        }
        response = await client.post("/auth/login", data=login_data)
        assert response.status_code == status_code

        if status_code // 2 == 100:
            response = await client.get("/auth/me")
            obj = response.json()
            assert obj["username"] == login or obj["email"] == login
            assert "is_superuser" in obj
            assert "banned" in obj
