from app.crud.base import CRUDBase
from app.models.cpu import Cpu
from app.schemas.cpu import CpuCreate, CpuUpdate


class CRUDCpu(CRUDBase[Cpu, CpuCreate, CpuUpdate]):
    def get_multi(
        self, db, *, skip: int = 0, limit: int = 100, q: str = None
    ):
        if q:
            return db.query(Cpu).filter(Cpu.name.ilike("%{}%".format(q))).offset(skip)\
                .limit(limit).all()
        else:
            return db.query(Cpu).offset(skip).limit(limit).all()


cpu = CRUDCpu(Cpu)
