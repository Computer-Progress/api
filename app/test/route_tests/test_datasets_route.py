import pytest
from httpx import AsyncClient, Response

from app.main import app
from .conftest import datasets_body, datasets_keys


def test_datasets_post(datasets_created: Response):
    assert datasets_created.status_code == 200
    assert datasets_created.json().items() >= datasets_body.items()
    assert set(datasets_created.json().keys()) == datasets_keys


@pytest.mark.asyncio
async def test_datasets_get(headers: dict, base_url: str, datasets_created: Response):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/datasets/?skip=0&limit=1", headers=headers)
    assert response.status_code == 200
    assert set(response.json()[0].keys()) == datasets_keys


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
        **datasets_body,
        "description": "i changed my description because i want",
        "source": "example",
    }
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.put(f"/datasets/{datasets_id}", json=put_json)
    assert response.status_code == 200
    assert {**put_json, "id": datasets_id} == response.json()
