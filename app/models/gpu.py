from app.database.base import Base
from sqlalchemy import Column, Integer, String, Float
# from sqlalchemy.orm import relationship


class Gpu(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    transistors = Column(Integer)
    tdp = Column(Float(precision=3))
    gflops = Column(Float(precision=3))
    die_size = Column(Integer)
    year = Column(Integer)