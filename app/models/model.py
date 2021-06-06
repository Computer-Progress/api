from app.database.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship


class Model(Base):
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    hardware_burden = Column(Float(precision=3))

    training_time = Column(Integer)
    gflops = Column(Float(precision=3))
    epochs = Column(Integer)
    number_of_parameters = Column(Integer)
    multiply_adds = Column(Float(precision=3))

    number_of_cpus = Column(Integer)
    number_of_gpus = Column(Integer)
    number_of_tpus = Column(Integer)

    task_dataset_id = Column(Integer, ForeignKey('task_dataset.id'))

    accuracy_values = relationship("AccuracyValue")

    paper_id = Column(Integer, ForeignKey('paper.id'))
    paper = relationship("Paper", uselist=False, back_populates="models")

    cpu_id = Column(Integer, ForeignKey('cpu.id'))
    cpu = relationship("Cpu")

    tpu_id = Column(Integer, ForeignKey('tpu.id'))
    tpu = relationship("Tpu")

    gpu_id = Column(Integer, ForeignKey('gpu.id'))
    gpu = relationship("Gpu")
