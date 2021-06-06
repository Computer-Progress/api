from app.crud.base import CRUDBase
from app.models.cpu import Cpu
from app.schemas.cpu import CpuCreate, CpuUpdate


class CRUDCpu(CRUDBase[Cpu, CpuCreate, CpuUpdate]):
    pass


cpu = CRUDCpu(Cpu)
