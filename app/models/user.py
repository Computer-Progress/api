from app.database.base import Base
from sqlalchemy import Boolean, Column, Integer, String, Enum
# from sqlalchemy.orm import relationship
import enum


class RoleEnum(enum.Enum):
    default = 'default'
    reviewer = 'reviewer'
    admin = 'admin'
    super_admin = 'super_admin'


class User(Base):
    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    role = Column(Enum(RoleEnum), server_default="default")

    country = Column(String(100), unique=False)
    state = Column(String(100), unique=False)
    city = Column(String(100), unique=False)
    institution = Column(String(100), unique=False)
    position = Column(String(100), unique=False)
