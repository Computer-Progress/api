import pytest
from httpx import AsyncClient, Response

from app.main import app

task = {
  "name": "bar",
  "image": "foo",
  "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
}

task_keys = {**task, "id":0, "number_of_benchmarks":0}

new_task = {
  "name": "foo",
  "image": "bar",
  "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
}

@pytest.fixture(scope="module")
async def task_created(base_url: str, headers: dict):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post("/tasks", json=task)
    yield response
    a = response.json()
    assert response.status_code == 200
    assert response.json().keys() == a.keys()
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.delete(f"/tasks/{a['id']}")
    assert response.status_code == 200
    assert response.json().keys() == task_keys.keys()

def test_task_creation(task_created: Response):
    json = task_created.json()
    assert json.keys() == task_keys.keys()
    for key in task:
        assert json[key] == task[key]

@pytest.mark.asyncio
async def test_task_get(base_url: str, headers:dict, task_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get("/tasks")
    res_json = response.json()
    assert response.status_code == 200
    assert isinstance(res_json, list)

@pytest.mark.asyncio
async def test_task_put(base_url: str, headers: dict, task_created: Response):
    res = task_created.json()

    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.put(f"/tasks/{res['id']}", json=new_task)
    json = response.json()
    assert response.status_code == 200
    for key in new_task.keys():
        assert new_task[key] == json[key]
    assert json.keys() == task_keys.keys()
