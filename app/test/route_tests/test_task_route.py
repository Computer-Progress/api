import pytest
from httpx import AsyncClient, Response

from app.main import app
from .conftest import task, task_keys

new_task = {
    "name": "foo",
    "image": "bar",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
}


def test_task_creation(task_created: Response):
    json = task_created.json()
    assert json.keys() == task_keys.keys()
    for key in task:
        assert json[key] == task[key]


@pytest.mark.asyncio
async def test_task_get(base_url: str, headers: dict, task_created: Response):
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
