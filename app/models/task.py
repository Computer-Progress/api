from app import models
from app.database.base import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.associationproxy import association_proxy
from slugify import slugify


def generate_identifier(context):
    return slugify(
        context.get_current_parameters()['name'],
        max_length=45,
        word_boundary=True
    )


class Task(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    identifier = Column(String, unique=True,
                        default=generate_identifier, onupdate=generate_identifier)
    image = Column(String)
    description = Column(Text)
    datasets = association_proxy(
        'datasets_association',
        'dataset', creator=lambda d: models.TaskDataset(dataset=d))
