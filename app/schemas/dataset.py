from typing import List, Optional

from pydantic import BaseModel
from .task import Task


# Shared properties
class DatasetBase(BaseModel):
    name: str
    image: Optional[str]
    description: Optional[str]
    source: Optional[str]
    tasks: Optional[List[Task]]


# Properties to receive via API on creation
class DatasetCreate(DatasetBase):
    pass


# Properties to receive via API on update
class DatasetUpdate(DatasetBase):
    name: Optional[str]


class DatasetInDBBase(DatasetBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Dataset(DatasetInDBBase):
    pass


# Additional properties stored in DB
class DatasetInDB(DatasetInDBBase):
    pass
