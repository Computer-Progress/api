from app.database.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship


class AccuracyValue(Base):
    id = Column(Integer, primary_key=True, index=True)

    model_id = Column(Integer, ForeignKey('model.id'))
    model = relationship("Model", back_populates="accuracy_values")

    accuracy_type_id = Column(Integer, ForeignKey('accuracy_type.id'))
    accuracy_type = relationship("AccuracyType")

    value = Column(Float(precision=3))
