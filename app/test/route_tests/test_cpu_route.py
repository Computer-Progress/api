import pytest
from httpx import AsyncClient, Response

from app.main import app
from app.test.utils.constants import CPU_BODY, CPU_KEYS, CPU_NEW, SUCCESS


def test_cpu_post(cpu_created: Response):
    assert cpu_created.status_code == SUCCESS
    assert cpu_created.json().items() >= CPU_BODY.items()
    assert set(cpu_created.json().keys()) == CPU_KEYS


@pytest.mark.asyncio
async def test_cpu_get(headers: dict, base_url: str, cpu_created: Response):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/cpus/?skip=0&limit=1", headers=headers)
    assert response.status_code == SUCCESS
    assert set(response.json()[0].keys()) == CPU_KEYS


@pytest.mark.asyncio
async def test_cpu_get_id(base_url: str, headers: dict, cpu_created: Response):
    cpu_json = cpu_created.json()
    cpu_id = cpu_json["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(f"/cpus/{cpu_id}")
    assert response.status_code == SUCCESS
    assert cpu_json == response.json()


@pytest.mark.asyncio
async def test_cpu_put(base_url: str, headers: dict, cpu_created: Response):
    cpu_json = cpu_created.json()
    cpu_id = cpu_json["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.put(f"/cpus/{cpu_id}", json=CPU_NEW)
    assert response.status_code == SUCCESS
    assert {**CPU_NEW, "id": cpu_id} == response.json()
