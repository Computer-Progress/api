from app.models.task_dataset import TaskDataset
from app.database.base import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.associationproxy import association_proxy


class Task(Base):
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True)
    name = Column(String)
    image = Column(String)
    description = Column(Text)
    datasets = association_proxy(
        'datasets_association', 'dataset', creator=lambda d: TaskDataset(dataset=d))
