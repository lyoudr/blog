from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime

from src.utils.gcs import GoogleCloudStorage


class PostBase(BaseModel):
    user_id: int
    title: str
    content: str
    tag_ids: List[int]


class PostResponse(BaseModel):
    id: int
    title: str
    content: Optional[str] = None
    user_id: int
    images: Optional[List[str]] = []
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True

    @field_validator("images")
    # The pre=True tells Pydantic to apply this validator before trying to parse the field
    # always=True makes sure it's called even if the field is missing.
    def generate_signed_urls(cls, value):
        if value is None:
            return []
        gcs = GoogleCloudStorage()
        return [gcs.generate_signed_url(image.url) for image in value]
