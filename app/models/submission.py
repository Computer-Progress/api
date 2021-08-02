import enum
from app.database.base import Base
from sqlalchemy import Column, Integer, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship


class StatusEnum(enum.Enum):
    pending = 'pending'
    need_information = 'need_information'
    approved = 'approved'
    declined = 'declined'


class Submission(Base):
    id = Column(Integer, primary_key=True, index=True)

    data = Column(JSON)

    status = Column(Enum(StatusEnum), server_default="pending")

    messages = relationship("Message")

    reviewer_id = Column(Integer, ForeignKey('user.id'))
    reviewer = relationship("User", foreign_keys=[reviewer_id])

    paper_id = Column(Integer, ForeignKey('paper.id'))
    paper = relationship("Paper", uselist=False, back_populates='submission')

    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship("User", foreign_keys=[owner_id])
