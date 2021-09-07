import pytest

# import alembic.config
from httpx import AsyncClient
from typing import Generator
from sqlalchemy_utils import create_database, database_exists

from app.database.base import Base
from app.settings import settings
from app.database.init_db import init_db
from app.main import app
from app.deps import get_db
from app.test.utils.overrides import override_get_db
from app.test.utils.test_db import (
    TestSessionLocal,
    engine,
    SQLALCHEMY_TEST_DATABASE_URI,
)
from .utils.test_db import TestSessionLocal

app.dependency_overrides[get_db] = override_get_db
if not database_exists(SQLALCHEMY_TEST_DATABASE_URI):
    create_database(SQLALCHEMY_TEST_DATABASE_URI)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
init_db(TestSessionLocal())


@pytest.fixture
def base_url():
    return "http://localhost:8000/api/v1"


@pytest.fixture
async def headers(base_url):
    body = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/login/access-token", data=body)
    json = response.json()
    assert json == {"token_type": "bearer", **json }
    return  {"Authorization": f"{json['token_type']} {json['access_token']}"}
