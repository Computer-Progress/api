import pytest
from httpx import AsyncClient, Response

from app.main import app
from app.test.utils.constants import (
    SUCCESS,
    TASK_MODEL,
    DATASET_MODEL,
    MODEL_TASK_DATASET_KEYS,
    MODEL_CSV_KEYS
)


@pytest.mark.asyncio
async def test_model_get_id(headers: dict, base_url: str, get_test_model: Response):
    model_id = get_test_model["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(f"/models/{model_id}")
    assert response.status_code == SUCCESS
    assert get_test_model == response.json()


@pytest.mark.asyncio
@pytest.mark.order(-1)
async def test_model_put(headers: dict, base_url: str, get_test_model: Response):
    model_id = get_test_model["id"]
    put_body = {**get_test_model, "name": "fooo", "gflops": 2.0, "epochs": 3}
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.put(f"/models/{model_id}", json=put_body)
    assert response.status_code == SUCCESS
    assert {**put_body, "id": model_id} == response.json()


@pytest.mark.asyncio
async def test_model_get_task_dataset(
    headers: dict,
    base_url: str,
    get_test_model: Response,
):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(
            f"/models/{TASK_MODEL['task_id']}/{DATASET_MODEL['dataset_id']}"
        )
    assert response.status_code == SUCCESS
    assert MODEL_TASK_DATASET_KEYS == set(response.json().keys())


@pytest.mark.asyncio
async def test_model_get_task_dataset_csv(
    headers: dict,
    base_url: str,
    get_test_model: Response,
):
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(
            f"/models/{TASK_MODEL['task_id']}/{DATASET_MODEL['dataset_id']}/csv"
        )
    response.encondig = "UTF-8"
    csvReader = response.text.replace('\n', ',', 1)
    csvReader = csvReader.split(",", maxsplit=len(MODEL_CSV_KEYS))
    print(csvReader)
    assert response.status_code == SUCCESS
    assert len(response.text) > 340
    assert set(csvReader[0:-1]) == MODEL_CSV_KEYS
