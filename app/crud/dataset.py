from app.crud.base import CRUDBase
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetCreate, DatasetUpdate


class CRUDDataset(CRUDBase[Dataset, DatasetCreate, DatasetUpdate]):
    def get_multi(
        self, db, *, skip: int = 0, limit: int = 100, q: str = None
    ):
        if q:
            return db.query(Dataset.id, Dataset.name, Dataset.identifier)\
                .filter(Dataset.name.ilike("%{}%".format(q)))\
                .offset(skip)\
                .limit(limit).all()
        return db.query(Dataset).offset(skip).limit(limit).all()


dataset = CRUDDataset(Dataset)
