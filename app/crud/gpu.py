from app.crud.base import CRUDBase
from app.models.gpu import Gpu
from app.schemas.gpu import GpuCreate, GpuUpdate


class CRUDGpu(CRUDBase[Gpu, GpuCreate, GpuUpdate]):
    def get_multi(
        self, db, *, skip: int = 0, limit: int = 100, q: str = None
    ):
        if q:
            return db.query(Gpu).filter(Gpu.name.ilike("%{}%".format(q))).offset(skip)\
                .limit(limit).all()
        else:
            return db.query(Gpu).offset(skip).limit(limit).all()


gpu = CRUDGpu(Gpu)
