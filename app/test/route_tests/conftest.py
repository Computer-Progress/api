import pytest
from httpx import AsyncClient, Response

from app.main import app
from app.test.utils.constants import (
    DATASETS_KEYS,
    DATASETS_BODY,
    TASK_KEYS,
    TASK,
    PAPER_BODY,
    PAPER_KEYS,
    SUBMISSION_ALT_BODY,
    MODEL_KEYS,
    SUCCESS,
    CPU_BODY,
    CPU_KEYS,
    TPU_BODY,
    GPU_BODY,
    GPU_KEYS,
)


@pytest.fixture(scope="session")
async def cpu_created(base_url: str, headers: dict):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post("/cpus", json=CPU_BODY)
    yield response
    # cpu_id = response.json()["id"]
    # async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
    #     response = await ac.delete(f"/cpus/{cpu_id}")
    # assert response.status_code == SUCCESS
    # assert CPU_KEYS == set(response.json().keys())


@pytest.fixture(scope="session")
async def tpu_created(base_url: str, headers: dict):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post("/tpus", json=TPU_BODY)
    yield response
    # json = response.json()
    # tpu_id = json["id"]
    # async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
    #     response = await ac.delete(f"/tpus/{tpu_id}")
    # assert response.status_code == SUCCESS
    # assert response.json().keys() == json.keys()


@pytest.fixture(scope="session")
async def gpu_created(base_url: str, headers: dict):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post("/gpus", json=GPU_BODY)
    yield response
    # gpu_id = response.json()["id"]
    # async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
    #     response = await ac.delete(f"/gpus/{gpu_id}")
    # assert response.status_code == SUCCESS
    # assert GPU_KEYS == set(response.json().keys())


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
async def submission_approved_created(
    base_url: str,
    headers: dict,
    datasets_created: Response,
    task_created: Response,
    tpu_created: Response,
    cpu_created: Response,
    gpu_created: Response
):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response_create = await ac.post("/submissions", json=SUBMISSION_ALT_BODY)
        response_update_status = await ac.put(
            f'/submissions/{response_create.json()["id"]}/status',
            json={"status": "approved"},
        )
    assert response_create.status_code == SUCCESS
    assert response_update_status.status_code == SUCCESS
    return response_update_status.json()


@pytest.fixture(scope="session")
async def get_test_model(
    headers: dict, base_url: str, submission_approved_created: Response
):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/models/?skip=0&limit=1", headers=headers)
    assert response.status_code == SUCCESS
    assert set(response.json()[0].keys()) == MODEL_KEYS
    yield response.json()[0]


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
