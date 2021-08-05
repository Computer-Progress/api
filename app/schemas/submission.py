from app.models.submission import StatusEnum
from typing import List, Optional
from datetime import date, datetime

from pydantic import BaseModel, Json


class SubmissionDataAccuracyValues(BaseModel):
    accuracy_type: str
    value: float


class SubmissionDataModels(BaseModel):
    name: str
    task: str
    dataset: str
    cpu: Optional[str]
    gpu: str
    tpu: Optional[str]
    gflops: Optional[int]
    multiply_adds: Optional[int]
    number_of_parameters: Optional[int]
    training_time: Optional[int]
    epochs: Optional[int]
    extra_training_data: bool = False
    accuracies: List[SubmissionDataAccuracyValues]
    number_of_gpus: int
    number_of_cpus: Optional[int]
    number_of_tpus: Optional[int]
    extra_training_time: bool = False


class SubmissionData(BaseModel):
    title: str
    link: str
    code_link: Optional[str]
    publication_date: date
    authors: List[str]
    models: List[SubmissionDataModels]


class SubmissionBase(BaseModel):
    data: SubmissionData
    paper_id: Optional[int]
    owner_id: Optional[int]
    reviewer_id: Optional[int]
    status: StatusEnum


class Submission(SubmissionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
