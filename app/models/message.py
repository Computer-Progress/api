from app.database.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Text, String
from sqlalchemy.orm import relationship


class Message(Base):
    id = Column(Integer, primary_key=True, index=True)

    body = Column(Text, nullable=False)
    type = Column(String)
    submission_id = Column(Integer, ForeignKey('submission.id'))
    submission = relationship("Submission", back_populates="messages")

    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship("User")
