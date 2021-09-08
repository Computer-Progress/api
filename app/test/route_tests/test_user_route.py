import pytest
from typing import Any
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.routes.user import router
from app.main import app
from app.settings import settings


@pytest.fixture(scope="module")
async def user_created(base_url):
    user_id = []
    body = {
        "email": "barbar@foofoo.com",
        "first_name": "Foo",
        "last_name": "bar",
        "password": "foobar",
    }
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/users/open", json=body)
    return response


def test_user_create(user_created):
    assert user_created.status_code == 200
    assert list(user_created.json().keys()) == [
        "email",
        "is_active",
        "role",
        "first_name",
        "last_name",
        "id",
    ]


@pytest.mark.asyncio
async def test_user_create_auth(base_url, headers):
    settings.EMAILS_ENABLED = False
    body = {
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "password": "string",
    }
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post(f"/users/", headers=headers, json=body)
    assert response.status_code == 200
    del body["password"]
    assert body.items() <= response.json().items()
    assert list(response.json().keys()) == [
        "email",
        "is_active",
        "role",
        "first_name",
        "last_name",
        "id",
    ]


@pytest.mark.asyncio
async def test_user_get(user_created, headers, base_url):
    user_json = user_created.json()
    user_id = user_json["id"]
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get(f"/users/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == user_json


@pytest.mark.asyncio
async def test_user_get_me(headers, base_url):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get(f"/users/me", headers=headers)
    json = response.json()
    assert response.status_code == 200
    assert {
        "email": settings.FIRST_SUPERUSER,
        "role": "super_admin",
    }.items() <= json.items()
    assert list(json.keys()) == [
        "email",
        "is_active",
        "role",
        "first_name",
        "last_name",
        "id",
    ]


@pytest.mark.asyncio
async def test_user_put(base_url, headers, user_created):
    user_json = user_created.json()
    user_id = user_json["id"]
    body = {
        "email": user_json["email"],
        "first_name": "bazbazbaz",
        "last_name": "foooooo",
    }
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.put(f"/users/{user_id}", headers=headers, json=body)
    assert response.status_code == 200
    assert body.items() <= response.json().items()
    assert list(response.json().keys()) == [
        "email",
        "is_active",
        "role",
        "first_name",
        "last_name",
        "id",
    ]

@pytest.mark.asyncio
async def test_user_put_me(base_url, headers):
    body = {
        "email": settings.FIRST_SUPERUSER,
        "first_name": "administrator",
        "last_name": "big boss",
    }
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.put(f"/users/me", headers=headers, json=body)
    assert response.status_code == 200
    assert body.items() <= response.json().items()
    assert list(response.json().keys()) == [
        "email",
        "is_active",
        "role",
        "first_name",
        "last_name",
        "id",
    ]