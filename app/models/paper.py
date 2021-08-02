from app.database.base import Base
from sqlalchemy import Column, Integer, String, Date, ARRAY, Boolean
from sqlalchemy.orm import relationship
from slugify import slugify


def generate_identifier(context):
    return slugify(
        context.get_current_parameters()['title'],
        max_length=45,
        word_boundary=True
    )


class Paper(Base):
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String,
                        default=generate_identifier, onupdate=generate_identifier)
    title = Column(String)
    link = Column(String)
    code_link = Column(String)
    publication_date = Column(Date)
    authors = Column(ARRAY(String))

    is_public = Column(Boolean, default=True)
    models = relationship("Model", back_populates="paper")
    submission = relationship("Submission", uselist=False, back_populates='paper')
