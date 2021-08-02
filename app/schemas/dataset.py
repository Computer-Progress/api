from typing import Optional

from pydantic import BaseModel


# Shared properties
class DatasetBase(BaseModel):
    name: Optional[str]
    image: Optional[str]
    description: Optional[str]
    source: Optional[str]
    identifier: Optional[str]


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
