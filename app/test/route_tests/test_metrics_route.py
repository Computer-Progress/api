import pytest
from httpx import AsyncClient, Response

from app.main import app
from app.test.utils.constants import METRICS_KEYS, SUCCESS, TASK_DATASET_IDENTIFIER


def make_id(name: str):
    return name.replace(" ", "-").replace("_", "-").lower()


@pytest.mark.asyncio
async def test_paper_with_code_get(
    headers: dict, base_url: str, get_test_model: Response
):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get(
            f"/metrics/{TASK_DATASET_IDENTIFIER}/?skip=0&limit=1", headers=headers
        )
    assert response.status_code == SUCCESS
    assert set(response.json()[0].keys()) == METRICS_KEYS


@pytest.mark.asyncio
async def test_paper_with_code_get_model(
    base_url: str,
    headers: dict,
    get_test_model: Response,
    submission_approved_created: Response,
):
    model_identifier = make_id(get_test_model["name"])
    paper_identifier = make_id(submission_approved_created["data"]["title"])

    metrics_json = {
        "tasks_dataset_identifier": TASK_DATASET_IDENTIFIER,
        "model_identifier": model_identifier,
        "model_name": get_test_model["name"],
        "model_hardware_burden": get_test_model["hardware_burden"],
        "paper_identifier": paper_identifier,
    }
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(
            f"/metrics/{TASK_DATASET_IDENTIFIER}/{get_test_model['name']}"
        )
    assert response.status_code == SUCCESS
    assert set(metrics_json.items()) <= set(response.json().items())
