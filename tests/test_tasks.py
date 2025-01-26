import pytest
from fastapi import status


@pytest.mark.usefixtures("reset_backend_class")
class TestTasks:
    @pytest.mark.parametrize(
        "task_data, status_code",
        [
            (
                {
                    "title": "Супер мега задача",
                    "text": "Напишите программу которая принимает два целых числа a, b и выводит их сумму.",
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
                    "time": 0.5,
                    "memory": 0,
                    "example_tests": [],
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            ),
        ],
    )
    def test_task_create(
        self,
        task_data: dict,
        status_code: int,
        client,
    ):
        response = client.post("/tasks", json=task_data)
        assert response.status_code == status_code
        if response.status_code // 200 == 1:
            obj = response.json()
            assert obj["title"] == task_data["title"]
            assert "id" in obj

    def test_task_get(self, client):
        task_id = 1
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        obj = response.json()
        assert "id" in obj
        assert "title" in obj
