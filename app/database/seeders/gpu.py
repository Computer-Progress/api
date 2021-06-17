from app import models
from fastapi.encoders import jsonable_encoder
import csv
from app.database.session import SessionLocal
from app.database.seeders.helper import parseFloat, parseInt


def init_db() -> None:
    db = SessionLocal()

    with open('app/database/seeders/gpu.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            obj_in = {
                'name': row['GPU'],
                'transistors': parseInt(row['Transistors (mln)']),
                'tdp': parseFloat(row['TDP']),
                'gflops': parseFloat(row['GFLOPS']),
                'die_size':  parseInt(row['Die size mmˆ2']),
                'year': parseInt(row['Year'])
            }

            obj_in_data = jsonable_encoder(obj_in)

            db_obj = models.Gpu(**obj_in_data)  # type: ignore

            db.add(db_obj)
    db.commit()


init_db()
