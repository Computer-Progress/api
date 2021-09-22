from typing import Optional

from pydantic import BaseModel, EmailStr, constr

from app.models.user import RoleEnum


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    role: RoleEnum = 'default'
    first_name: Optional[str] = None
    last_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: constr(min_length=8)


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[constr(min_length=8)] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
