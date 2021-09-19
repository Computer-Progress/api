import pytest
from httpx import AsyncClient, Response

from app.main import app


post_body = {
    "name": "Foo",
    "description": "foobar",
}
keys = {*post_body ,"id"}
keys_get = {*keys ,"updated_at", "created_at"}


@pytest.fixture(scope="module")
async def accuracy_created(base_url: str, headers: dict):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post("/accuracy_types", json=post_body)
    yield response
    accuracy_id = response.json()["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.delete(f"/accuracy_types/{accuracy_id}")
    assert response.status_code == 200
    assert keys == set(response.json().keys())


def test_accuracy_post(accuracy_created: Response):
    assert accuracy_created.status_code == 200
    assert accuracy_created.json().items() >= post_body.items()
    assert set(accuracy_created.json().keys()) == keys


@pytest.mark.asyncio
async def test_accuracy_get(headers: dict, base_url: str, accuracy_created: Response):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get(f"/accuracy_types/?skip=0&limit=1", headers=headers)
    assert response.status_code == 200
    assert set(response.json()[0].keys()) == keys_get


@pytest.mark.asyncio
async def test_accuracy_get_id(
    base_url: str, headers: dict, accuracy_created: Response
):
    accuracy_json = accuracy_created.json()
    accuracy_id = accuracy_json["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(f"/accuracy_types/{accuracy_id}")
    assert response.status_code == 200
    assert accuracy_json == response.json()


@pytest.mark.asyncio
async def test_accuracy_put(base_url: str, headers: dict, accuracy_created: Response):
    accuracy_json = accuracy_created.json()
    accuracy_id = accuracy_json["id"]
    put_json = {
        "name": "bazz",
        "description": "jazz",
    }
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.put(f"/accuracy_types/{accuracy_id}", json=put_json)
    assert response.status_code == 200
    assert {**put_json, "id": accuracy_id} == response.json()
