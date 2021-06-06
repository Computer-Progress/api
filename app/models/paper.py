from app.database.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, ARRAY
from sqlalchemy.orm import relationship


class Paper(Base):
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    link = Column(Integer)
    code_link = Column(Integer)
    publication_date = Column(Date)
    authors = Column(ARRAY(String))

    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship("User")

    models = relationship("Model", back_populates="paper")
    revision = relationship("Revision", uselist=False, back_populates='paper')
