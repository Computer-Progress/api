from app.database.base import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship


class Dataset(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    image = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    source = Column(String, nullable=True)
    tasks = relationship(
        "Task",
        secondary="task_dataset", back_populates="datasets")
