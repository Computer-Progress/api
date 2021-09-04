import pytest
# import alembic.config
from typing import Generator
from sqlalchemy_utils import create_database, database_exists

from app.database.base import Base
from app.database.init_db import init_db
from app.main import app
from app.deps import get_db
from app.test.utils.overrides import override_get_db
from app.test.utils.test_db import TestSessionLocal, engine, SQLALCHEMY_TEST_DATABASE_URI

app.dependency_overrides[get_db] = override_get_db
if not database_exists(SQLALCHEMY_TEST_DATABASE_URI):
    create_database(SQLALCHEMY_TEST_DATABASE_URI)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
