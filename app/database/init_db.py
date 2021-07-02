from sqlalchemy.orm import Session

from app import crud, schemas
from app.settings import settings
from app.database import base  # noqa: F401

from app.database.seeders import (
    cpu, gpu, tpu, conll2003, imagenet, ms_coco, squad_1_1, wmt2014_en_de,
    wmt2014_en_fr)

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            role='super_admin',
        )
        user = crud.user.create(db, obj_in=user_in)
        cpu.seed()
        gpu.seed()
        tpu.seed()
        imagenet.seed()
        conll2003.seed()
        ms_coco.seed()
        squad_1_1.seed()
        wmt2014_en_de.seed()
        wmt2014_en_fr.seed()
