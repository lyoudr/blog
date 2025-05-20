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
    orders: List[str] = []
    images: Optional[List[str]] = []
    created_time: datetime
    updated_time: datetime

    class Config:
        from_attributes = True
    
    @root_validator(pre=True)
    def generate_signed_urls(cls, values):
        """Generate signed URLs for images."""
        # Handle list of post images
        gcs = GoogleCloudStorage()

        images = values.get('images', [])
        if images:
            signed_urls = [gcs.generate_signed_url(img) for img in images]
            values['images'] = signed_urls
        
        # Handle user image
        user_image = values.get('user_image')
        if user_image:
            values['user_image'] = gcs.generate_signed_url(user_image)
        return values
