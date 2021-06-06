from app.database.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Revision(Base):
    id = Column(Integer, primary_key=True, index=True)

    status = Column(String, nullable=False)

    messages = relationship("Message")

    reviewer_id = Column(Integer, ForeignKey('user.id'))
    reviewer = relationship("User")

    paper_id = Column(Integer, ForeignKey('paper.id'))
    paper = relationship("Paper", uselist=False, back_populates='revision')
