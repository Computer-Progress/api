import pytest
from httpx import AsyncClient, Response

from app.main import app

tpu_creation_body = {
  "name": "foobar",
  "transistors": 10,
  "tdp": 20,
  "gflops": 5
}

@pytest.fixture(scope="module")
async def tpu_created(base_url: str, headers: dict):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post("/tpus", json=tpu_creation_body)
    yield response
    json = response.json()
    tpu_id = json["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.delete(f"/tpus/{tpu_id}")
    assert response.status_code == 200
    assert response.json().keys() == json.keys()

def test_tpu_post(tpu_created: Response):
    json = tpu_created.json()
    body_keys = list(tpu_creation_body.keys())
    body_keys.append('id')
    assert tpu_created.status_code == 200
    assert json.pop('id', None) == 1
    assert json.items() == tpu_creation_body.items()
    assert list(tpu_created.json().keys()) == body_keys

@pytest.mark.asyncio
async def test_tpu_get_id(headers: dict, base_url: str, tpu_created: Response):
    json = tpu_created.json()
    tpu_id = json["id"]

    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(f"/tpus/{tpu_id}")
    assert response.status_code == 200
    assert response.json() == json

@pytest.mark.asyncio
async def test_tpu_get(headers: dict, base_url: str, tpu_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get("/tpus")
    assert response.status_code == 200

    for item in response.json():
        assert list(item.keys()) == list(tpu_created.json().keys())

@pytest.mark.asyncio
async def test_tpu_put(headers: dict, base_url: str, tpu_created: Response):
    id = tpu_created.json()["id"]
    new_json = {
        "name": "barfoo",
        "transistors": 50,
        "tdp": 21,
        "gflops": 3
    }
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.put(f"/tpus/{id}", json=new_json)
    assert response.status_code == 200
    assert {**new_json, "id": id} == response.json()
