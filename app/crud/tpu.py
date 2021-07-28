from app.crud.base import CRUDBase
from app.models.tpu import Tpu
from app.schemas.tpu import TpuCreate, TpuUpdate


class CRUDTpu(CRUDBase[Tpu, TpuCreate, TpuUpdate]):
    def get_multi(
        self, db, *, skip: int = 0, limit: int = 100, q: str = None
    ):
        if q:
            return db.query(Tpu).filter(Tpu.name.ilike("%{}%".format(q))).offset(skip)\
                .limit(limit).all()
        else:
            return db.query(Tpu).offset(skip).limit(limit).all()


tpu = CRUDTpu(Tpu)
