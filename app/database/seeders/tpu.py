from app import models
from fastapi.encoders import jsonable_encoder
import csv
from app.database.session import SessionLocal
from app.database.seeders.helper import parseFloat, parseInt


def seed() -> None:
    db = SessionLocal()

    with open('app/database/seeders/tpu.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            obj_in = {
                'name': row['TPU'],
                'gflops': parseFloat(row['GFLOPS (FP32)']),
                'year': parseInt(row['Release Year'])
            }

            obj_in_data = jsonable_encoder(obj_in)

            db_obj = models.Tpu(**obj_in_data)  # type: ignore

            db.add(db_obj)
    db.commit()
