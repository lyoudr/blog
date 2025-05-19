from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.models.database import get_db
from src.models.user import User
from src.repositories import tag_repository
from src.schemas.tags import TagResponse, TagBase
from src.utils.auth import get_current_user
from src.utils.decorator import transaction

router = APIRouter(tags=["tags"], prefix="/tags")


@router.get(
    "/", 
    summary="List tags", 
    response_model=List[TagResponse]
)
def list_tags(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):    
    tags = tag_repository.list_tags(db)
    return tags


@router.post(
    "/", 
    summary="Create a tag", 
    response_model=TagResponse
)
def create_tag(
    payload: TagBase,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tag = tag_repository.create_tag(db, payload.name)
    return tag
