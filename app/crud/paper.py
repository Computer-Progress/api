from app.crud.base import CRUDBase
from app.models.paper import Paper
from app.schemas.paper import PaperCreate, PaperUpdate


class CRUDPaper(CRUDBase[Paper, PaperCreate, PaperUpdate]):
    pass        



paper = CRUDPaper(Paper)
