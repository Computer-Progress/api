from typing import Optional

from pydantic import BaseModel


# Shared properties
class AccuracyTypeBase(BaseModel):
    name: str
    description: Optional[str]


# Properties to receive via API on creation
class AccuracyTypeCreate(AccuracyTypeBase):
    pass


# Properties to receive via API on update
class AccuracyTypeUpdate(AccuracyTypeBase):
    name: Optional[str]


class AccuracyTypeInDBBase(AccuracyTypeBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class AccuracyType(AccuracyTypeInDBBase):
    pass


# Additional properties stored in DB
class AccuracyTypeInDB(AccuracyTypeInDBBase):
    pass
