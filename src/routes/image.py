from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from fastapi import UploadFile, File

from src.schemas.image import ImageUploadResponse
from src.models.database import get_db
from src.models.image import Image
from src.models.user import User
from src.utils.gcs import GoogleCloudStorage
from src.utils.auth import get_current_user

router = APIRouter(tags=["image"], prefix="/image")


@router.post(
    "/upload-image",
    summary="Upload an image.",
    response_model=List[ImageUploadResponse],
)
def upload_image(
    post_id: int, 
    files: List[UploadFile] = File(...), 
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    gcs = GoogleCloudStorage()
    uploaded_images = []
    
    for file in files:
        gcs_path = gcs.upload_to_gcs(file.file, file.filename, file.content_type)
        image = Image(url=gcs_path, post_id=post_id)
        db.add(image)
        uploaded_images.append(image)
    
    db.commit()
    
    for image in uploaded_images:
        db.refresh(image)

    return [
        ImageUploadResponse(id=img.id, url=img.url, post_id=img.post_id)
        for img in uploaded_images
    ]
