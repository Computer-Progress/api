import pytest
from httpx import AsyncClient, Response

from app.main import app

post_body = {
    "name": "string",
    "number_of_cores": 0,
    "frequency": 0,
    "fp32_per_cycle": 0,
    "transistors": 0,
    "tdp": 0,
    "gflops": 0,
    "year": 0,
    "die_size": 0,
}
keys = {*post_body, "id"}


@pytest.fixture(scope="module")
async def cpu_created(base_url: str, headers: dict):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post("/cpus", json=post_body)
    yield response
    cpu_id = response.json()["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.delete(f"/cpus/{cpu_id}")
    assert response.status_code == 200
    assert keys == set(response.json().keys())


def test_cpu_post(cpu_created: Response):
    assert cpu_created.status_code == 200
    assert cpu_created.json().items() >= post_body.items()
    assert set(cpu_created.json().keys()) == keys


