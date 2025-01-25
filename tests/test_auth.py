import pytest
from fastapi.testclient import TestClient
from fastapi import status

from config import settings


@pytest.mark.usefixtures("reset_database_class")
class TestAuth:
    @pytest.mark.parametrize(
        "username, email, password, status_code",
        [
            ("XTray", "example@mail", "qweqweqwe", 422),
            ("XTray", "example@mail.ru", "qwe", 422),
            ("XTray", "example@mail.ru", "qweqweqwe", 201),
            ("XTra1", "example1@mail.ru", "qweqweqwe", 201),
            ("XTray", "example@mail.ru", "qweqwe1e", 403),
            ("XTray", "example2@mail.ru", "qweqwe1e", 403),
            ("XTray2", "example@mail.ru", "qweqwe1e", 403),
        ],
    )
    def test_register_user(
        self,
        username: str,
        email: str,
        password: str,
        status_code: int,
        client: TestClient,
    ):
        user_data = {
            "username": username,
            "email": email,
            "password": password,
        }
        response = client.post("/register", data=user_data)
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "login, password, status_code",
        [
            ("XTray", "", 401),
            ("", "qweqweqweqwe", 401),
            ("username123", "qweqweqweqwe", 401),
            ("XTray", "qweqweqweqwe", 401),
            ("XTray", "qweqweqwe", 204),
        ],
    )
    def test_login_user(
        self,
        login,
        password,
        status_code,
        client: TestClient,
    ):
        login_data = {
            "login": login,
            "password": password,
        }
        response = client.post("/login", data=login_data)
        assert response.status_code == status_code
