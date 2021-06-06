from typing import List, Optional

from pydantic import BaseModel
from .dataset import Dataset


# Shared properties
class TaskBase(BaseModel):
    name: str
    image: Optional[str]
    description: Optional[str]
    datasets: Optional[List[Dataset]]


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
    pass


# Additional properties stored in DB
class TaskInDB(TaskInDBBase):
    pass
