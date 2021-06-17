from app.database.base import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class TaskDataset(Base):
    id = Column(Integer, primary_key=True, index=True)

    task_id = Column(Integer, ForeignKey('task.id'))
    dataset_id = Column(Integer, ForeignKey('dataset.id'))
    accuracy_types = relationship("TaskDatasetAccuracyType")
    models = relationship("Model")
    task = relationship("Task", back_populates="datasets")
    dataset = relationship("Dataset", back_populates="tasks")
