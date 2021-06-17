from app import models
from fastapi.encoders import jsonable_encoder
import csv
from app.database.session import SessionLocal
from app.database.seeders.helper import parseFloat, parseInt


def init_db() -> None:
    db = SessionLocal()

    with open('app/database/seeders/cpu.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            obj_in = {
                'name': row['CPU'],
                'number_of_cores': parseInt(row['Cores']),
                'frequency': parseInt(row['Processor Clock [MHz]']) / 1000,
                'fp32_per_cycle': parseInt(row['FP32']),
                'transistors': parseInt(row['Transistors (mln)']),
                'tdp': parseFloat(row['TDP']),
                'gflops': parseFloat(row['GFLOPS(FP32)']),
                'die_size':  parseInt(row['Die size mmˆ2']),
                'year': parseInt(row['Year']),
            }

            obj_in_data = jsonable_encoder(obj_in)

            db_obj = models.Cpu(**obj_in_data)  # type: ignore

            db.add(db_obj)
    db.commit()


init_db()
