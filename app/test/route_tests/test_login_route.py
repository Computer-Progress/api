import pytest
from httpx import AsyncClient

from app.main import app
from app.settings import settings


@pytest.mark.asyncio
async def test_test_token_route(headers, base_url):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/login/test-token", headers=headers)
    assert response.status_code == 200
    json = response.json()
    expected_json = {
        "email": settings.FIRST_SUPERUSER,
        "is_active": True,
        "role": "super_admin",
        "first_name": None,
        "last_name": None,
    }
    assert json.items() >= expected_json.items()
    assert set(json.keys()) == {*expected_json, "id"}


# password-recovery and reset-password routes depends on sending email.
