from sqlalchemy import event
import logging
from sqlalchemy.sql.expression import bindparam, select, text
from app.models import Dataset, Task
from sqlalchemy.sql.functions import func
from app.database.base import Base
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship


class TaskDataset(Base):
    id = Column(Integer, primary_key=True, index=True)

    task_id = Column(Integer, ForeignKey('task.id'))
    dataset_id = Column(Integer, ForeignKey('dataset.id'))
    identifier = Column(String, unique=True)

    accuracy_types = relationship("TaskDatasetAccuracyType")
    models = relationship("Model")
    task = relationship("Task",
                        backref='datasets_association')
    dataset = relationship("Dataset",
                           backref='tasks_association')


def my_before_insert_listener(mapper, connection, target):
    target.identifier = connection.execute(
        text("select concat(task.identifier,'-on-', dataset.identifier) from task, dataset where task.id = %d and dataset.id = %d" %
             (target.task_id, target.dataset_id))
    ).scalar()


event.listen(TaskDataset, 'before_insert', my_before_insert_listener)
