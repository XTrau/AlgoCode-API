import pytest
from httpx import AsyncClient

from conftest import reset_backend


@pytest.mark.usefixtures("reset_backend")
@pytest.mark.asyncio(loop_scope="session")
async def test_main(client: AsyncClient, reset_backend):
    response = await client.get("/api/ping")
    data = response.json()
    assert data == {"message": "pong"}
