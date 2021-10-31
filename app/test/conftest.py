import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy_utils import create_database, database_exists
from os import system, name
from time import sleep

from app.database.base import Base
from app.settings import settings
from app.database.init_db import init_db
from app.main import app
from app.deps import get_db
from app.test.utils.overrides import override_get_db
from app.test.utils.test_db import (
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

with open('app/test/utils/initial_seed.sql') as sql_file:
    for statement in sql_file.read().split(';'):
        if len(statement.strip()) > 0:
             engine.execute(statement + ';')

if name == 'nt':
  _ = system('cls')

else:
  _ = system('clear')

@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
def base_url() -> str:
    return "http://localhost:8000/api/v1"


@pytest.fixture(scope="session")
async def headers(base_url) -> dict:
    body = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/login/access-token", data=body)
    json = response.json()
    assert json == {"token_type": "bearer", **json}
    return {"Authorization": f"{json['token_type']} {json['access_token']}"}
