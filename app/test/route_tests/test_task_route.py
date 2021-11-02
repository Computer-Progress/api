import pytest
from httpx import AsyncClient, Response

from app.main import app
from app.test.utils.constants import (
    TASK_KEYS,
    TASK,
    NEW_TASK,
    TASK_FAIL,
    VALIDATION_ERR,
    NOT_FOUND,
    INVALID_GET_PARAM,
    SUCCESS
)

@pytest.mark.order(1)
def test_task_creation(task_created: Response):
    json = task_created.json()
    assert json.keys() == TASK_KEYS.keys()
    for key in TASK:
        assert json[key] == TASK[key]


@pytest.mark.asyncio
@pytest.mark.order(2)
async def test_task_get(base_url: str, headers: dict, task_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get("/tasks")
    res_json = response.json()
    assert response.status_code == SUCCESS
    assert isinstance(res_json, list)


@pytest.mark.asyncio
@pytest.mark.order(3)
async def test_task_put(base_url: str, headers: dict, task_created: Response):
    res = task_created.json()

    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.put(f"/tasks/{res['id']}", json=NEW_TASK)
    json = response.json()
    assert response.status_code == SUCCESS
    for key in NEW_TASK.keys():
        assert NEW_TASK[key] == json[key]
    assert json.keys() == TASK_KEYS.keys()

# @pytest.mark.asyncio
# @pytest.mark.order(4)
# async def test_task_delete(base_url: str, headers: dict, task_created: Response):
#     id = task_created.json()['id']
#
#     async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
#         response = await ac.delete(f"/tasks/{id}")
#     assert response.status_code == SUCCESS
#     assert response.json().keys() == task_created.json().keys()


@pytest.mark.asyncio
@pytest.mark.order(5)
async def test_task_creation_fail(base_url: str, headers: dict):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post("/tasks")
    assert response.status_code == VALIDATION_ERR
    assert response.json() == TASK_FAIL

@pytest.mark.asyncio
@pytest.mark.order(6)
async def test_task_get_fail(base_url: str, headers: dict, task_created: Response):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get("/tasks?skip=a&limit=b")
    assert response.status_code == VALIDATION_ERR
    assert response.json() == INVALID_GET_PARAM
