import pytest
from httpx import AsyncClient, Response

from app.main import app
datasets_body = {
    "name": "string",
    "image": "string",
    "description": "string",
    "source": "string",
    "identifier": "string",
}
datasets_keys = {*datasets_body, "id"}


@pytest.fixture(scope="session")
async def datasets_created(base_url: str, headers: dict):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post("/datasets", json=datasets_body)
    yield response
    datasets_id = response.json()["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.delete(f"/datasets/{datasets_id}")
    assert response.status_code == 200
    assert datasets_keys == set(response.json().keys())


task = {
    "name": "bar",
    "image": "foo",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
}

task_keys = {**task, "id": 0, "number_of_benchmarks": 0}


@pytest.fixture(scope="session")
async def task_created(base_url: str, headers: dict):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post("/tasks", json=task)
    a = response.json()
    assert response.status_code == 200
    assert response.json().keys() == a.keys()
    yield response
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.delete(f"/tasks/{a['id']}")
    assert response.status_code == 200
    assert response.json().keys() == task_keys.keys()
