import pytest
from httpx import AsyncClient


@pytest.mark.usefixtures("reset_backend")
class TestSolutions:
    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_programming_languages(self, client: AsyncClient):
        response = await client.get("/languages")
        obj = response.json()
        assert type(obj) is list
        assert len(obj) > 0
        for lang in obj:
            assert "mark" in lang
            assert "title" in lang

    @pytest.mark.asyncio(loop_scope="session")
    async def test_check_solution_test(self, admin_client: AsyncClient):
        solution = {
            "language": "python",
            "code": """a, b = map(int, input().split())\nprint(a + b)""",
        }

        response = await admin_client.post("/solutions/task/1", json=solution)
        assert response.status_code == 201

        solution_obj: dict = response.json()
        assert "id" in solution_obj

        response = await admin_client.get(f"/solutions/{solution_obj["id"]}")
        solution_obj = response.json()
        if response.status_code == 200:
            assert "language" in solution_obj
            assert solution_obj["language"] == "python"
            assert "code" in solution_obj
            assert "status" in solution_obj
            assert solution_obj["status"] == "Полное решение"
            assert "date_of_create" in solution_obj
