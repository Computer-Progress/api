from app.database.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class TaskDatasetAccuracyType(Base):
    id = Column(Integer, primary_key=True, index=True)

    task_dataset_id = Column(Integer, ForeignKey('task_dataset.id'))
    accuracy_type_id = Column(Integer, ForeignKey('accuracy_type.id'))
    main = Column(Boolean, default=True)
    required = Column(Boolean, default=True)

    task_dataset = relationship("TaskDataset", back_populates="accuracy_types")
    accuracy_type = relationship("AccuracyType")