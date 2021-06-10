from app.crud.base import CRUDBase
from app.models.model import Model
from app.schemas.model import ModelCreate, ModelUpdate


class CRUDModel(CRUDBase[Model, ModelCreate, ModelUpdate]):
    pass


model = CRUDModel(Model)
