from pydantic import PostgresDsn
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from app.settings import settings

SQLALCHEMY_TEST_DATABASE_URI = PostgresDsn.build(
            scheme="postgresql",
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_SERVER,
            path=f"/{settings.POSTGRES_DB}_test",
        )
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URI, pool_pre_ping=True)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
