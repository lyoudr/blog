from pydantic import BaseModel
from datetime import datetime


class TagResponse(BaseModel):
    id: int
    name: str
    updated_time: datetime

    class Config:
        from_attribute = True


class TagBase(BaseModel):
    name: str
