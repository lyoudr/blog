from pydantic import BaseModel


class ImageUploadResponse(BaseModel):
    id: int
    url: str
    post_id: int
