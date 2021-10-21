from pydantic import PostgresDsn
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from app.settings import settings
import logging

SQLALCHEMY_TEST_DATABASE_URI = PostgresDsn.build(
            scheme="postgresql",
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_SERVER,
            path=f"/{settings.POSTGRES_DB}_test",
        )

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URI, pool_pre_ping=True, logging_name='sqlalchemy.engine')
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
levels = [logging.ERROR, logging.DEBUG, logging.INFO, logging.WARNING, logging.CRITICAL]
for i in range(len(levels)):
    sqla_logger = logging.getLogger('sqlalchemy.engine')
    sqla_logger.propagate = False
    sqla_logger.setLevel(levels[i])
    sqla_logger.addHandler(logging.FileHandler(f'/tmp/sqla_{i}.log'))
