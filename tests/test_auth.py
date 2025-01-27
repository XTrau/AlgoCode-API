import pytest
from fastapi.testclient import TestClient
from fastapi import status


@pytest.mark.usefixtures("reset_backend_class")
class TestAuth:
    @pytest.mark.parametrize(
        "username, email, password, status_code",
        [
            ("XTray", "exam@mail", "qweqweqw", status.HTTP_422_UNPROCESSABLE_ENTITY),
            ("XTray", "example@mail.ru", "qwe", status.HTTP_422_UNPROCESSABLE_ENTITY),
            ("XTray", "example@mail.ru", "qweqweqwe", status.HTTP_201_CREATED),
            ("XTra1", "example1@mail.ru", "qweqweqwe", status.HTTP_201_CREATED),
            ("XTray", "example@mail.ru", "qweqwe1e", status.HTTP_403_FORBIDDEN),
            ("XTray", "example2@mail.ru", "qweqwe1e", status.HTTP_403_FORBIDDEN),
            ("XTray2", "example@mail.ru", "qweqwe1e", status.HTTP_403_FORBIDDEN),
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
            ("XTray", "", status.HTTP_403_FORBIDDEN),
            ("XTray", 23, status.HTTP_403_FORBIDDEN),
            ("", "qweqweqweqwe", status.HTTP_403_FORBIDDEN),
            ("username123", "qweqweqweqwe", status.HTTP_403_FORBIDDEN),
            ("XTray", "qweqweqweqwe", status.HTTP_403_FORBIDDEN),
            ("XTray", "qweqweqwe", status.HTTP_204_NO_CONTENT),
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
