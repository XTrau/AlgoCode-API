import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.config import settings


@pytest.fixture(scope="session")
def client() -> TestClient:
    with TestClient(app) as client:
        yield client


@pytest.fixture
def reset_backend(client: TestClient):
    assert settings.MODE == "TEST"
    response = client.post("/reset_backend")
    assert response.status_code == 200


@pytest.fixture(scope="class")
def reset_backend_class(client: TestClient):
    assert settings.MODE == "TEST"
    response = client.post("/reset_backend")
    assert response.status_code == 200
