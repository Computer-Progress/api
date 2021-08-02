from app.models.task_dataset import TaskDataset
from app.crud.base import CRUDBase
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetCreate, DatasetUpdate


class CRUDDataset(CRUDBase[Dataset, DatasetCreate, DatasetUpdate]):
    def get_multi(
        self, db, *, skip: int = 0, limit: int = 100, q: str = None, task_id: int = None
    ):
        dataset = db.query(Dataset)
        if task_id:
            dataset = dataset.join(TaskDataset).filter(TaskDataset.task_id == task_id)
        if q:
            dataset = dataset.filter(Dataset.name.ilike("%{}%".format(q)))

        return dataset.offset(skip).limit(limit).all()


dataset = CRUDDataset(Dataset)
