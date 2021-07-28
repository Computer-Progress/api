from app.crud.base import CRUDBase
from app.models.accuracy_type import AccuracyType
from app.schemas.accuracy_type import AccuracyTypeCreate, AccuracyTypeUpdate
from app.models import TaskDatasetAccuracyType, TaskDataset


class CRUDAccuracyType(CRUDBase[AccuracyType, AccuracyTypeCreate, AccuracyTypeUpdate]):

    def get_multi_by_task_dataset_identifier(
        self, db, *, skip: int = 0, limit: int = 100, task_dataset_identifier
    ):
        return db.query(
            AccuracyType.id,
            AccuracyType.name,
            TaskDatasetAccuracyType.required,
            TaskDatasetAccuracyType.main
        )\
            .join(TaskDatasetAccuracyType)\
            .join(TaskDataset)\
            .filter(TaskDataset.identifier == task_dataset_identifier)\
            .offset(skip).limit(limit).all()


accuracy_type = CRUDAccuracyType(AccuracyType)
