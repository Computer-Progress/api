from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

from app.settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
