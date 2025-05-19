from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from src.models.database import get_db
from src.repositories import user_repository
from src.schemas.user import Login, Token, RegisterResponse
from src.utils.email import send_verification_email
from src.utils.auth import authenticate_user, create_access_token, get_password_hash
from src.utils.gcs import GoogleCloudStorage
import uuid

router = APIRouter(tags=["auth"], prefix="/auth")
gcs = GoogleCloudStorage()

@router.post(
    "/register",
    summary="Register user",
    response_model=RegisterResponse
)
async def register_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db) 
):
    user_repository.get_user_by_email(db, email)
    unique_filename = f"{uuid.uuid4().hex}_{image.filename}"
    gcs_path = gcs.upload_to_gcs(image.file, unique_filename, image.content_type)
    new_user = user_repository.create_user(
        db=db,
        username=username,
        email=email,
        password=password,
        image_url=gcs_path,
    )
    return RegisterResponse(
        status=f'Dear {new_user.name}: You have successfully registered our website.'
    )

@router.post(
    "/login",
    summary="Login user",
    response_model=Token,
)
def login(
    payload: Login,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        payload.username,
        payload.password
    )
    if not user:
        raise HTTPException(
            detail="Invalid credentials",
            status_code=401,
        )

    token = create_access_token({"user_id": user.id})
    return Token(access_token=token, token_type="bearer")