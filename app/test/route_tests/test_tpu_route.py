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
    res_body = response.json()

def test_tpu_post(tpu_created: Response):
    json = tpu_created.json()
    body_keys = list(tpu_creation_body.keys())
    body_keys.append('id')
    assert tpu_created.status_code == 200
    assert json.pop('id', None) == 1
    assert json.items() == tpu_creation_body.items()
    assert list(tpu_created.json().keys()) == body_keys
