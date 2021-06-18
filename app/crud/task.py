import logging
from typing import List
from sqlalchemy.sql.functions import func
from app.models.task_dataset import TaskDataset
from app.crud.base import CRUDBase
from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy.orm import Session
from app import schemas
from app.models import Task, Dataset, Model


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def get_multi_and_count_benchmarks(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[schemas.Task]:
        tasks = db.query(*Task.__table__.columns, func.count(TaskDataset.id).label('benchmarks')).join(
            TaskDataset
        ).group_by(*Task.__table__.columns).offset(skip).limit(limit).all()
        return tasks

    def get_tasks_with_models(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ):

        tasks = db.query(Task).all()
        dataset = db.query(Dataset).all()
        models = db.query(Model).all()

        return tasks


task = CRUDTask(Task)
