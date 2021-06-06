from app.crud.base import CRUDBase
from app.models.tpu import Tpu
from app.schemas.tpu import TpuCreate, TpuUpdate


class CRUDTpu(CRUDBase[Tpu, TpuCreate, TpuUpdate]):
    pass


tpu = CRUDTpu(Tpu)
