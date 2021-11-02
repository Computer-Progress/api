import pytest
from httpx import AsyncClient, Response

from app.main import app
from app.test.utils.constants import GPU_BODY, GPU_KEYS, GPU_NEW, SUCCESS


def test_gpu_post(gpu_created: Response):
    assert gpu_created.status_code == SUCCESS
    assert gpu_created.json().items() >= GPU_BODY.items()
    assert set(gpu_created.json().keys()) == GPU_KEYS


@pytest.mark.asyncio
async def test_gpu_get(headers: dict, base_url: str, gpu_created: Response):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/gpus/?skip=0&limit=1", headers=headers)
    assert response.status_code == SUCCESS
    assert set(response.json()[0].keys()) == GPU_KEYS


@pytest.mark.asyncio
async def test_gpu_get_id(base_url: str, headers: dict, gpu_created: Response):
    gpu_json = gpu_created.json()
    gpu_id = gpu_json["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(f"/gpus/{gpu_id}")
    assert response.status_code == SUCCESS
    assert gpu_json == response.json()


@pytest.mark.asyncio
async def test_gpu_put(base_url: str, headers: dict, gpu_created: Response):
    gpu_json = gpu_created.json()
    gpu_id = gpu_json["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.put(f"/gpus/{gpu_id}", json=GPU_NEW)
    assert response.status_code == SUCCESS
    assert {**GPU_NEW, "id": gpu_id} == response.json()
