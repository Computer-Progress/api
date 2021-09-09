import pytest
from httpx import AsyncClient, Response

from app.main import app
from app.settings import settings

keys = ["updated_at", "name", "created_at", "id", "description"]
post_body = {
    "name": "Foo",
    "description": "foobar",
}


@pytest.fixture(scope="module")
async def accuracy_created(base_url: str, headers: dict) -> Response:
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.post("/accuracy_types", json=post_body)
    return response


def test_accuracy_post(accuracy_created: Response):
    assert accuracy_created.status_code == 200
    assert accuracy_created.json().items() >= post_body.items()
    assert list(accuracy_created.json().keys()) == ["name", "description", "id"]


@pytest.mark.asyncio
async def test_accuracy_get(headers: dict, base_url: str):
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get(f"/accuracy_types/?skip=0&limit=1", headers=headers)
    assert response.status_code == 200
    assert response.json()[0].items() >= post_body.items()
    assert list(response.json()[0].keys()) == keys
