from app.database.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship

import enum


class StatusEnum(enum.Enum):
    pending = 'pending'
    need_information = 'need_information'
    approved = 'approved'
    declined = 'declined'


class Revision(Base):
    id = Column(Integer, primary_key=True, index=True)

    status = Column(Enum(StatusEnum), server_default="pending")

    messages = relationship("Message")

    reviewer_id = Column(Integer, ForeignKey('user.id'))
    reviewer = relationship("User")

    paper_id = Column(Integer, ForeignKey('paper.id'))
    paper = relationship("Paper", uselist=False, back_populates='revision')
