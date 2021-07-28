from typing import List, Optional, Union
from datetime import date

from pydantic import BaseModel

# Shared properties


class PaperBase(BaseModel):
    title: str
    link: Optional[str]
    code_link: Optional[str]
    publication_date: Optional[date]
    authors: Optional[List[str]]


# Properties to receive via API on creation
class AccuracyValuesCreate(BaseModel):
    accuracy_type: Union[int, str]
    value: float


class PaperModelsCreate(BaseModel):
    name: str
    task: Union[int, str]
    dataset: Union[int, str]
    cpu: Optional[Union[int, str]]
    gpu: Union[int, str]
    tpu: Optional[Union[int, str]]
    gflops: Optional[int]
    multiply_adds: Optional[int]
    number_of_parameters: Optional[int]
    training_time: Optional[int]
    epochs: Optional[int]
    extra_training_data: bool = False
    accuracies: List[AccuracyValuesCreate]


class PaperCreate(PaperBase):
    title: str
    link: str
    code_link: Optional[str]
    publication_date: date
    authors: List[str]
    models: List[PaperModelsCreate]
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
