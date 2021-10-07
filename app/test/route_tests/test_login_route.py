import pytest
from httpx import AsyncClient

from app.main import app
from app.test.utils.constants import LOGIN_EXPECTED_JSON


@pytest.mark.asyncio
async def test_test_token_route(headers, base_url):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/login/test-token", headers=headers)
    assert response.status_code == 200
    json = response.json()

    assert json.items() >= LOGIN_EXPECTED_JSON.items()
    assert set(json.keys()) == {*LOGIN_EXPECTED_JSON, "id"}


# password-recovery and reset-password routes depends on sending email.
