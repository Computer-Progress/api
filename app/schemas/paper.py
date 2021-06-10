from typing import List, Optional
from datetime import date

from pydantic import BaseModel, AnyHttpUrl


# Shared properties
class PaperBase(BaseModel):
    title: str
    link: Optional[AnyHttpUrl]
    code_link: Optional[AnyHttpUrl]
    publication_date: Optional[date]
    authors: Optional[List[str]]


# Properties to receive via API on creation
class PaperCreate(PaperBase):
    pass


# Properties to receive via API on update
class PaperUpdate(PaperBase):
    title: Optional[str]


class PaperInDBBase(PaperBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Paper(PaperInDBBase):
    pass


# Additional properties stored in DB
class PaperInDB(PaperInDBBase):
    pass
