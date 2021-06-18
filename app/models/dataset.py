from sqlalchemy.ext.associationproxy import association_proxy
from app.models.task_dataset import TaskDataset
from app.database.base import Base
from sqlalchemy import Column, Integer, String, Text


class Dataset(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    image = Column(String)
    description = Column(Text)
    source = Column(String)
    tasks = association_proxy(
        'tasks_association', 'task', creator=lambda t: TaskDataset(task=t))
