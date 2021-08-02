from app.database.seeders.helper import executeSQLfromFile

from app.database.session import SessionLocal
import os


def seed() -> None:
    db = SessionLocal()
    executeSQLfromFile(db, 'app/database/seeders/initial_seed.sql')
    if os.path.isfile('app/database/seeders/data_seed.sql'):
        executeSQLfromFile(db, 'app/database/seeders/data_seed.sql')
    db.commit()
