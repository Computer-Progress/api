from app.crud.base import CRUDBase
from app.models.accuracy_type import AccuracyType
from app.schemas.accuracy_type import AccuracyTypeCreate, AccuracyTypeUpdate


class CRUDAccuracyType(CRUDBase[AccuracyType, AccuracyTypeCreate, AccuracyTypeUpdate]):
    pass


accuracy_type = CRUDAccuracyType(AccuracyType)
