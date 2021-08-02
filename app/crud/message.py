from app.crud.base import CRUDBase
from app.models.message import Message
from app.schemas.message import MessageCreate


class CRUDMessage(CRUDBase[Message, MessageCreate, MessageCreate]):
    def get_multi(
        self, db, *, skip: int = 0, limit: int = 100, submission_id: int = None
    ):
        return db.query(Message).filter(Message.submission_id == submission_id)\
            .order_by(Message.created_at.desc()).offset(skip).limit(limit).all()


message = CRUDMessage(Message)
