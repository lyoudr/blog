from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from src.schemas.image import ImageUploadResponse
from src.models.database import get_db
from src.models.image import Image
from src.utils.gcs import GoogleCloudStorage

router = APIRouter(tags=["image"], prefix="/image")


@router.post(
    "/upload-image",
    summary="Upload an image.",
    response_model=ImageUploadResponse,
)
def upload_image(
    post_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)
):
    gcs = GoogleCloudStorage()
    gcs_path = gcs.upload_to_gcs(file.file, file.filename, file.content_type)

    # Save record in database
    image = Image(url=gcs_path, post_id=post_id)
    db.add(image)
    db.commit()
    db.refresh(image)

    return ImageUploadResponse(id=image.id, url=image.url, post_id=image.post_id)
