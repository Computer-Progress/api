import pytest
from httpx import AsyncClient

from app.main import app
from app.test.utils.constants import (
    DATASETS_KEYS,
    DATASETS_BODY,
    TASK_KEYS,
    TASK,
    PAPER_BODY,
    PAPER_KEYS,
    SUCCESS,
)


@pytest.fixture(scope="session")
async def datasets_created(base_url: str, headers: dict):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post("/datasets", json=DATASETS_BODY)
    yield response
    datasets_id = response.json()["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.delete(f"/datasets/{datasets_id}")
    assert response.status_code == SUCCESS
    assert DATASETS_KEYS == set(response.json().keys())


@pytest.fixture(scope="session")
async def task_created(base_url: str, headers: dict):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post("/tasks", json=TASK)
    a = response.json()
    assert response.status_code == SUCCESS
    assert response.json().keys() == a.keys()
    yield response
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.delete(f"/tasks/{a['id']}")
    assert response.status_code == SUCCESS
    assert response.json().keys() == TASK_KEYS.keys()


@pytest.fixture(scope="session")
async def paper_created(base_url: str, headers: dict):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post("/papers", json=PAPER_BODY)
    yield response
    paper_id = response.json()["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.delete(f"/papers/{paper_id}")
    assert response.status_code == SUCCESS
    assert PAPER_KEYS == set(response.json().keys())
