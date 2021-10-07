import pytest
from httpx import AsyncClient, Response

from app.main import app
from app.test.utils.constants import TASK_KEYS, TASK, NEW_TASK


def test_task_creation(task_created: Response):
    json = task_created.json()
    assert json.keys() == TASK_KEYS.keys()
    for key in TASK:
        assert json[key] == TASK[key]


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
        response = await ac.put(f"/tasks/{res['id']}", json=NEW_TASK)
    json = response.json()
    assert response.status_code == 200
    for key in NEW_TASK.keys():
        assert NEW_TASK[key] == json[key]
    assert json.keys() == TASK_KEYS.keys()
