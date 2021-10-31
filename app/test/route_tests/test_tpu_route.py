import pytest
from httpx import AsyncClient, Response

from app.main import app
from app.test.utils.constants import TPU_BODY, TPU_NEW, SUCCESS


def test_tpu_post(tpu_created: Response):
    json = tpu_created.json()
    body_keys = list(TPU_BODY.keys())
    body_keys.append('id')
    assert tpu_created.status_code == SUCCESS
    assert json.pop('id', None) == 1
    assert json.items() == TPU_BODY.items()
    assert list(tpu_created.json().keys()) == body_keys


@pytest.mark.asyncio
async def test_tpu_get_id(headers: dict, base_url: str, tpu_created: Response):
    json = tpu_created.json()
    tpu_id = json["id"]

    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(f"/tpus/{tpu_id}")
    assert response.status_code == SUCCESS
    assert response.json() == json


@pytest.mark.asyncio
async def test_tpu_get(headers: dict, base_url: str, tpu_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get("/tpus")
    assert response.status_code == SUCCESS

    for item in response.json():
        assert list(item.keys()) == list(tpu_created.json().keys())


@pytest.mark.asyncio
async def test_tpu_put(headers: dict, base_url: str, tpu_created: Response):
    id = tpu_created.json()["id"]

    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.put(f"/tpus/{id}", json=TPU_NEW)
    assert response.status_code == SUCCESS
    assert {**TPU_NEW, "id": id} == response.json()
