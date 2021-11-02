import pytest
from httpx import AsyncClient, Response

from app.main import app
from app.test.utils.constants import (
    SOTA_KEYS,
    SUCCESS,
    TASK_MODEL,
    TASK_DESCRIPTION,
    DATASET_MODEL,
)


@pytest.mark.asyncio
async def test_sota_get(headers: dict, base_url: str, get_test_model: Response):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/sota/?skip=0&limit=1", headers=headers)
    assert response.status_code == SUCCESS
    assert set(response.json()[0].keys()) == SOTA_KEYS


@pytest.mark.asyncio
async def test_sota_get_id(
    base_url: str,
    headers: dict,
    get_test_model: Response,
    submission_approved_created: Response,
):
    submission_data = {
        "sota_accuracy_value": submission_approved_created["data"]["models"][0][
            "accuracies"
        ][0]["value"],
        "sota_paper_publication_date": submission_approved_created["data"][
            "publication_date"
        ],
        "accuracy_name": submission_approved_created["data"]["models"][0]["accuracies"][
            0
        ]["accuracy_type"],
        "sota_paper_link": submission_approved_created["data"]["link"],
        "sota_paper_title": submission_approved_created["data"]["title"],
        "sota_name": submission_approved_created["data"]["models"][0]["name"]
    }
    sota_json = {
        **TASK_MODEL,
        "task_description": TASK_DESCRIPTION,
        "datasets": [
            {
                **DATASET_MODEL,
                **submission_data,
                "task_dataset_id": get_test_model["task_dataset_id"],
                "sota_id": get_test_model["id"],
                "sota_hardware_burden": get_test_model["hardware_burden"],
            }
        ],
    }
    task_id = sota_json["task_id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(f"/sota/{task_id}")
    print(response.json())
    print(sota_json)
    assert response.status_code == SUCCESS
    assert sota_json.keys() == response.json().keys()
    for i in range(len(sota_json['datasets'])):
        assert sota_json['datasets'][0].keys() == response.json()['datasets'][0].keys()
