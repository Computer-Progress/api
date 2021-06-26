from app import models
from pydantic.main import BaseModel
from typing import List, Optional

from .dataset import Dataset
from .model import Model

# Shared properties


class TaskBase(BaseModel):
    name: str
    image: Optional[str]
    description: Optional[str]


# Properties to receive via API on creation
class TaskCreate(TaskBase):
    pass


# Properties to receive via API on update
class TaskUpdate(TaskBase):
    name: Optional[str]


class TaskInDBBase(TaskBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Task(TaskInDBBase):
    number_of_benchmarks: Optional[int]


# Additional properties stored in DB
class TaskInDB(TaskInDBBase):
    pass


class DatasetModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str]
    image: Optional[str]
    description: Optional[str]
    source: Optional[str]
    models: List[Model]


class TaskDatasetModels(Task):
    datasets: List[DatasetModel]

    class Config:
        orm_mode = True
