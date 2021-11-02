import pytest
from httpx import AsyncClient

from app.main import app
from app.settings import settings
from app.test.utils.constants import USER_BODY,          \
                                     USER_KEYS,          \
                                     USER_NEW,           \
                                     USER_BODY_AUTH,     \
                                     USER_SUPERUSER_BODY,\
                                     USER_SUPERUSER_NEW, \
                                     SUCCESS


@pytest.fixture(scope="module")
async def user_created(base_url):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/users/open", json=USER_BODY)
    return response


def test_user_create(user_created):
    assert user_created.status_code == SUCCESS
    assert set(user_created.json().keys()) == USER_KEYS


@pytest.mark.asyncio
async def test_user_create_auth(base_url, headers):
    settings.EMAILS_ENABLED = False
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/users/", headers=headers, json=USER_BODY_AUTH)
    assert response.status_code == SUCCESS
    del USER_BODY_AUTH["password"]
    assert USER_BODY_AUTH.items() <= response.json().items()
    assert set(response.json().keys()) == USER_KEYS


@pytest.mark.asyncio
async def test_user_get(user_created, headers, base_url):
    user_json = user_created.json()
    user_id = user_json["id"]
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get(f"/users/{user_id}", headers=headers)
    assert response.status_code == SUCCESS
    assert response.json() == user_json


@pytest.mark.asyncio
async def test_user_get_me(headers, base_url):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/users/me", headers=headers)
    json = response.json()
    assert response.status_code == SUCCESS
    assert USER_SUPERUSER_BODY.items() <= json.items()
    assert set(json.keys()) == USER_KEYS


@pytest.mark.asyncio
async def test_user_put(base_url, headers, user_created):
    user_json = user_created.json()
    user_id = user_json["id"]
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.put(f"/users/{user_id}", headers=headers, json=USER_NEW)
    assert response.status_code == SUCCESS
    assert USER_NEW.items() <= response.json().items()
    assert set(response.json().keys()) == USER_KEYS


@pytest.mark.asyncio
async def test_user_put_me(base_url, headers):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.put("/users/me", headers=headers, json=USER_SUPERUSER_NEW)
    assert response.status_code == SUCCESS
    assert USER_SUPERUSER_NEW.items() <= response.json().items()
    assert set(response.json().keys()) == USER_KEYS
