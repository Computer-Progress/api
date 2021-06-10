from typing import Optional

from pydantic import BaseModel


# Shared properties
class ModelBase(BaseModel):
    name: Optional[str]
    hardware_burden: Optional[float]
    training_time: Optional[int]
    gflops: Optional[float]
    epochs: Optional[int]
    number_of_parameters: Optional[int]
    multiply_adds: Optional[float]
    number_of_cpus: Optional[int]
    number_of_gpus: Optional[int]
    number_of_tpus: Optional[int]
    task_dataset_id: Optional[int]
    paper_id: Optional[int]
    cpu_id: Optional[int]
    tpu_id: Optional[int]
    gpu_id: Optional[int]


# Properties to receive via API on creation
class ModelCreate(ModelBase):
    pass


# Properties to receive via API on update
class ModelUpdate(ModelBase):
    pass


class ModelInDBBase(ModelBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Model(ModelInDBBase):
    pass


# Additional properties stored in DB
class ModelInDB(ModelInDBBase):
    pass
