from typing import Optional

from pydantic import BaseModel


# Shared properties
class CpuBase(BaseModel):
    name: str
    number_of_cores: int
    frequency: int
    fp32_per_cycle: int
    transistors: int
    tdp: int
    gflops: float


# Properties to receive via API on creation
class CpuCreate(CpuBase):
    pass


# Properties to receive via API on update
class CpuUpdate(CpuBase):
    name: Optional[str]
    number_of_cores: Optional[int]
    frequency: Optional[int]
    fp32_per_cycle: Optional[int]
    transistors: Optional[int]
    tdp: Optional[int]
    gflops: Optional[float]


class CpuInDBBase(CpuBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Cpu(CpuInDBBase):
    pass


# Additional properties stored in DB
class CpuInDB(CpuInDBBase):
    pass
