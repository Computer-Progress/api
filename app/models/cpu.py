from app.database.base import Base
from sqlalchemy import Column, Integer, String, Float
# from sqlalchemy.orm import relationship


class Cpu(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    number_of_cores = Column(Integer)
    frequency = Column(Float(precision=3))
    fp32_per_cycle = Column(Integer)
    transistors = Column(Integer)
    tdp = Column(Float(precision=3))
    gflops = Column(Float(precision=3))
    die_size = Column(Integer)
    year = Column(Integer)