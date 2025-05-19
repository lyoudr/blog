from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime

from src.utils.gcs import GoogleCloudStorage


class PostBase(BaseModel):
    title: str
    content: List[str]
    tag_ids: List[int]


class PostResponse(BaseModel):
    id: int
    title: str
    content: List[str]
    user_id: int
    images: Optional[List[str]] = []
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True