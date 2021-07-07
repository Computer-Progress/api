from app.database.base import Base
from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from slugify import slugify


def generate_identifier(context):
    return slugify(
        context.get_current_parameters()['name'],
        max_length=45,
        word_boundary=True
    )


class Model(Base):
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String,
                        default=generate_identifier, onupdate=generate_identifier)

    name = Column(String, nullable=False)

    hardware_burden = Column(Float(precision=3))

    training_time = Column(BigInteger)
    gflops = Column(Float(precision=3))
    epochs = Column(BigInteger)
    number_of_parameters = Column(BigInteger)
    multiply_adds = Column(Float(precision=3))

    number_of_cpus = Column(Integer)
    number_of_gpus = Column(Integer)
    number_of_tpus = Column(Integer)

    task_dataset_id = Column(Integer, ForeignKey('task_dataset.id'))

    accuracy_values = relationship("AccuracyValue")
    extra_training_time = Column(Boolean)
    paper_id = Column(Integer, ForeignKey('paper.id'))
    paper = relationship("Paper", uselist=False, back_populates="models")

    cpu_id = Column(Integer, ForeignKey('cpu.id'))
    cpu = relationship("Cpu")

    tpu_id = Column(Integer, ForeignKey('tpu.id'))
    tpu = relationship("Tpu")

    gpu_id = Column(Integer, ForeignKey('gpu.id'))
    gpu = relationship("Gpu")
