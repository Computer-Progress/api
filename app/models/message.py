from app.database.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship


class Message(Base):
    id = Column(Integer, primary_key=True, index=True)

    body = Column(Text, nullable=False)

    revision_id = Column(Integer, ForeignKey('revision.id'))
    revision = relationship("Revision")

    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship("User")
