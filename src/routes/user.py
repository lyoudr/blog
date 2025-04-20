from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.models.database import get_db
from src.schemas.user import UserResponse
from src.repositories import user_repository

router = APIRouter(tags=["user"], prefix="/user")


@router.get("/", summary="List users", response_model=List[UserResponse])
def list_user(db: Session = Depends(get_db)):
    users = user_repository.list_users(db)
    return users
