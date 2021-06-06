from app.database.base import Base
from sqlalchemy import Column, Integer, String, Text
# from sqlalchemy.orm import relationship


class AccuracyType(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
