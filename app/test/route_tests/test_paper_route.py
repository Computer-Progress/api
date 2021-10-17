import pytest
from httpx import AsyncClient, Response

from app.main import app
from app.test.utils.constants import (
    PAPER_GET,
    PAPER_KEYS,
    PAPER_KEYS_POST,
    SUCCESS,
)


def test_paper_post(paper_created: Response) -> None:
    assert paper_created.status_code == SUCCESS
    assert paper_created.json().items() >= PAPER_GET.items()
    assert set(paper_created.json().keys()) == PAPER_KEYS_POST
