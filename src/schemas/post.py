from pydantic import BaseModel, root_validator
from typing import Optional, List
from datetime import datetime

from src.utils.gcs import GoogleCloudStorage


class PostBase(BaseModel):
    title: str
    content: List[str]
    tag_ids: List[int]

class CreatePostResponse(BaseModel):
    id: int
    title: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: List[str]
    user_id: int
    user_name: str
    user_image: str
    images: Optional[List[str]] = []
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True
    
    @root_validator(pre=True)
    def generate_signed_urls(cls, values):
        """Generate signed URLs for images."""
        images = values.get('images', [])

        if images:
            gcs = GoogleCloudStorage()
            signed_urls = [gcs.generate_signed_url(img) for img in images]
            values['images'] = signed_urls
        
        return values
