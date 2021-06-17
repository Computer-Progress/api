from app.database.base import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship


class Task(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    image = Column(String)
    description = Column(Text)
    datasets = relationship(
        "TaskDataset", back_populates="task")
