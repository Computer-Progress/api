import pytest
from httpx import AsyncClient, Response

from app.main import app

post_body = {
    "name": "string",
    "image": "string",
    "description": "string",
    "source": "string",
    "identifier": "string"
}
keys = {*post_body, "id"}


@pytest.fixture(scope="module")
async def datasets_created(base_url: str, headers: dict):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post("/datasets", json=post_body)
    yield response
    datasets_id = response.json()["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.delete(f"/datasets/{datasets_id}")
    assert response.status_code == 200
    assert keys == set(response.json().keys())


def test_datasets_post(datasets_created: Response):
    assert datasets_created.status_code == 200
    assert datasets_created.json().items() >= post_body.items()
    assert set(datasets_created.json().keys()) == keys



@pytest.mark.asyncio
async def test_datasets_get(headers: dict, base_url: str, datasets_created: Response):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get(f"/datasets/?skip=0&limit=1", headers=headers)
    assert response.status_code == 200
    assert set(response.json()[0].keys()) == keys


@pytest.mark.asyncio
async def test_datasets_get_id(
    base_url: str, headers: dict, datasets_created: Response
):
    datasets_json = datasets_created.json()
    datasets_id = datasets_json["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(f"/datasets/{datasets_id}")
    assert response.status_code == 200
    assert datasets_json == response.json()


@pytest.mark.asyncio
async def test_datasets_put(base_url: str, headers: dict, datasets_created: Response):
    datasets_json = datasets_created.json()
    datasets_id = datasets_json["id"]
    put_json = {
        **post_body,
        "description": "i changed my description because i want",
        "source": "example"
    }
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.put(f"/datasets/{datasets_id}", json=put_json)
    assert response.status_code == 200
    assert {**put_json, "id": datasets_id} == response.json()
