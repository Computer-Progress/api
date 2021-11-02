import pytest
from httpx import AsyncClient, Response

from app.main import app
from app.test.utils.constants import (
    DATASETS_BODY,
    DATASETS_KEYS,
    DATASETS_BODY_FAIL,
    DATASETS_INVALID_BODY,
    DATASETS_NO_BODY_FAIL,
    DATASETS_INVALID_GET,
    DATASETS_INVALID_GET_ID,
    SUCCESS,
    VALIDATION_ERR,
    NOT_FOUND
)


def test_datasets_post(datasets_created: Response):
    assert datasets_created.status_code == SUCCESS
    assert datasets_created.json().items() >= DATASETS_BODY.items()
    assert set(datasets_created.json().keys()) == DATASETS_KEYS


@pytest.mark.asyncio
async def test_datasets_get(headers: dict, base_url: str, datasets_created: Response):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/datasets/?skip=0&limit=1", headers=headers)
    assert response.status_code == SUCCESS
    assert set(response.json()[0].keys()) == DATASETS_KEYS


@pytest.mark.asyncio
async def test_datasets_get_id(
    base_url: str, headers: dict, datasets_created: Response
):
    datasets_json = datasets_created.json()
    datasets_id = datasets_json["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(f"/datasets/{datasets_id}")
    assert response.status_code == SUCCESS
    assert datasets_json == response.json()


@pytest.mark.asyncio
async def test_datasets_put(base_url: str, headers: dict, datasets_created: Response):
    datasets_json = datasets_created.json()
    datasets_id = datasets_json["id"]
    print(datasets_id)
    put_json = {
        "name": "foo",
        "image": "bar",
        "identifier": "foo bar",
        "description": "i changed my description because i want",
        "source": "example",
    }
    print(put_json)
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.put(f"/datasets/{datasets_id}", json=put_json)
        print(response.json())
    assert response.status_code == SUCCESS
    assert {**put_json, "id": datasets_id} == response.json()

@pytest.mark.asyncio
async def test_datasets_post_invalid_fail(base_url: str, headers: dict, datasets_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post('/datasets', json=DATASETS_BODY_FAIL)
    assert response.status_code == VALIDATION_ERR
    assert response.json() == DATASETS_INVALID_BODY

@pytest.mark.asyncio
async def test_datasets_post_no_body_fail(base_url: str, headers: dict, datasets_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post('/datasets')
    assert response.status_code == VALIDATION_ERR
    assert response.json() == DATASETS_NO_BODY_FAIL

@pytest.mark.asyncio
async def test_datasets_get(headers: dict, base_url: str, datasets_created: Response):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/datasets/?skip=b&limit=a", headers=headers)
    assert response.status_code == VALIDATION_ERR
    assert response.json() == DATASETS_INVALID_GET

@pytest.mark.asyncio
async def test_datasets_get_id(
    base_url: str, headers: dict, datasets_created: Response
):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(f"/datasets/999999")
    assert response.status_code == NOT_FOUND
    assert DATASETS_INVALID_GET_ID == response.json()
