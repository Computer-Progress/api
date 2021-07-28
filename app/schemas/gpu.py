from typing import Optional

from pydantic import BaseModel


# Shared properties
class GpuBase(BaseModel):
    name: str
    transistors: Optional[int]
    tdp: Optional[int]
    gflops: Optional[float]


# Properties to receive via API on creation
class GpuCreate(GpuBase):
    pass


# Properties to receive via API on update
class GpuUpdate(GpuBase):
    name: Optional[str]
    transistors: Optional[int]
    tdp: Optional[int]
    gflops: Optional[float]


class GpuInDBBase(GpuBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Gpu(GpuInDBBase):
    pass


# Additional properties stored in DB
class GpuInDB(GpuInDBBase):
    pass
