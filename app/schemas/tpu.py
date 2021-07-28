from typing import Optional

from pydantic import BaseModel


# Shared properties
class TpuBase(BaseModel):
    name: str
    transistors: Optional[int]
    tdp: Optional[int]
    gflops: Optional[float]


# Properties to receive via API on creation
class TpuCreate(TpuBase):
    pass


# Properties to receive via API on update
class TpuUpdate(TpuBase):
    name: Optional[str]
    transistors: Optional[int]
    tdp: Optional[int]
    gflops: Optional[float]


class TpuInDBBase(TpuBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Tpu(TpuInDBBase):
    pass


# Additional properties stored in DB
class TpuInDB(TpuInDBBase):
    pass
