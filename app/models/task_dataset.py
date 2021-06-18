from app.database.base import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref


class TaskDataset(Base):
    id = Column(Integer, primary_key=True, index=True)

    task_id = Column(Integer, ForeignKey('task.id'), primary_key=True)
    dataset_id = Column(Integer, ForeignKey('dataset.id'), primary_key=True)
    accuracy_types = relationship("TaskDatasetAccuracyType")
    models = relationship("Model")
    task = relationship("Task", backref=backref(
        "task_dataset", cascade="all, delete-orphan"))
    dataset = relationship("Dataset", backref=backref(
        "task_dataset", cascade="all, delete-orphan"))
