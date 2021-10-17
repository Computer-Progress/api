import pytest
from httpx import AsyncClient, Response

from app.main import app
from app.test.utils.constants import (
    PAPER_GET,
    PAPER_KEYS,
    PAPER_KEYS_POST,
    PAPER_NEW,
    SUCCESS,
)


def test_paper_post(paper_created: Response) -> None:
    assert paper_created.status_code == SUCCESS
    assert paper_created.json().items() >= PAPER_GET.items()
    assert set(paper_created.json().keys()) == PAPER_KEYS_POST


@pytest.mark.asyncio
async def test_paper_get(headers: dict, base_url: str) -> None:
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/papers/?skip=0&limit=1", headers=headers)
    assert response.status_code == SUCCESS
    assert set(response.json()[0].keys()) == PAPER_KEYS


@pytest.mark.asyncio
async def test_paper_get_id(
    base_url: str, headers: dict, paper_created: Response
) -> None:
    paper_id = paper_created.json()["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.get(f"/papers/{paper_id}")
    assert response.status_code == SUCCESS
    assert {**PAPER_GET, "id": paper_id} == response.json()


@pytest.mark.asyncio
async def test_cpu_put(base_url: str, headers: dict, paper_created: Response) -> None:
    paper_json = paper_created.json()
    paper_id = paper_json["id"]
    async with AsyncClient(app=app, base_url=base_url, headers=headers) as ac:
        response = await ac.put(f"/papers/{paper_id}", json=PAPER_NEW)
    assert response.status_code == SUCCESS
    assert {**PAPER_NEW, "id": paper_id} == response.json()
