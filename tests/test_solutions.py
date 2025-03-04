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

        response = await admin_client.post("/tasks/1/solutions", json=solution)
        assert response.status_code == 201
