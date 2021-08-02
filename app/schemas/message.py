from typing import Optional

from pydantic import BaseModel


# Shared properties
class MessageBase(BaseModel):
    body: str


# Properties to receive via API on creation
class MessageCreate(MessageBase):
    author_id: Optional[int]
    submission_id: Optional[int]


class MessageInDBBase(MessageBase):
    id: Optional[int] = None
    author_id: Optional[int]
    submission_id: Optional[int]

    class Config:
        orm_mode = True


# Additional properties to return via API
class Message(MessageInDBBase):
    pass


# Additional properties stored in DB
class MessageInDB(MessageInDBBase):
    pass
