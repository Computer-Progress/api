import pytest
from httpx import AsyncClient, Response

from app.main import app
from app.test.utils.constants import MODEL_KEYS, SUCCESS


@pytest.mark.asyncio
async def test_model_get_id(headers: dict, base_url: str, get_test_model: Response):
    model_id = get_test_model["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(f"/models/{model_id}")
    assert response.status_code == SUCCESS
    assert get_test_model == response.json()


@pytest.mark.asyncio
async def test_model_put(headers: dict, base_url: str, get_test_model: Response):
    model_id = get_test_model["id"]
    put_body = {**get_test_model, "name": "fooo", "gflops": 2.0, "epochs": 3}
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.put(f"/models/{model_id}", json=put_body)
    assert response.status_code == SUCCESS
    assert {**put_body, "id": model_id} == response.json()
