import pytest
from fastapi import status
from httpx import AsyncClient

test_task_create_params = [
    (
        {
            "title": "Супер мега задача",
            "text": "Напишите программу которая принимает два целых числа a, b и выводит их сумму.",
            "input_format": "В первой строке вводятся два числа a, b (0 <= a <= 10e9, 0 <= b <= 10e9)\nНеобходимо вывести сумму этих чисел.",
            "time": 0.5,
            "memory": 64,
            "example_tests": [
                {"input": "1 2", "output": "3"},
                {"input": "0 3", "output": "3"},
            ],
        },
        status.HTTP_201_CREATED,
    ),
    (
        {
            "title": "Супер мега задача",
            "text": "Напишите программу которая принимает два целых числа a, b и выводит их сумму.",
            "input_format": "В первой строке вводятся два числа a, b (0 <= a <= 10e9, 0 <= b <= 10e9)\nНеобходимо вывести сумму этих чисел.",
            "time": 0,
            "memory": 64,
            "example_tests": [
                {"input": "1 2", "output": "3"},
                {"input": "0 3", "output": "3"},
            ],
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        {
            "title": "Супер мега задача",
            "text": "Напишите программу которая принимает два целых числа a, b и выводит их сумму.",
            "input_format": "В первой строке вводятся два числа a, b (0 <= a <= 10e9, 0 <= b <= 10e9)\nНеобходимо вывести сумму этих чисел.",
            "time": 0.5,
            "memory": 64,
            "example_tests": [],
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
    (
        {
            "title": "Супер мега задача",
            "text": "Напишите программу которая принимает два целых числа a, b и выводит их сумму.",
            "input_format": "В первой строке вводятся два числа a, b (0 <= a <= 10e9, 0 <= b <= 10e9)\nНеобходимо вывести сумму этих чисел.",
            "time": 0.5,
            "memory": 0,
            "example_tests": [],
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    ),
]


@pytest.mark.usefixtures("reset_backend")
class TestTasks:
    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.parametrize("task_data, status_code", test_task_create_params)
    async def test_task_create(
            self,
            task_data: dict,
            status_code: int,
            admin_client: AsyncClient,
    ):
        response = await admin_client.post("/api/tasks/", json=task_data)
        assert response.status_code == status_code
        if response.status_code // 200 == 1:
            obj = response.json()
            assert obj["title"] == task_data["title"]
            assert "id" in obj

    @pytest.mark.asyncio(loop_scope="session")
    async def test_task_create_not_superuser(
            self,
            client: AsyncClient,
    ):
        task_data = {
            "title": "Супер мега задача",
            "text": "Напишите программу которая принимает два целых числа a, b и выводит их сумму.",
            "time": 0.5,
            "memory": 64,
            "example_tests": [
                {"input": "1 2", "output": "3"},
                {"input": "0 3", "output": "3"},
            ],
        }
        response = await client.post("/api/tasks/", json=task_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio(loop_scope="session")
    async def test_task_get(self, client: AsyncClient):
        task_id = 1
        response = await client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        obj = response.json()

        assert "title" in obj
        assert "text" in obj
        assert "time" in obj
        assert "memory" in obj
        assert "example_tests" in obj
        assert "id" in obj
