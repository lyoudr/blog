from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.models.database import get_db
from src.repositories import tag_repository
from src.schemas.tags import TagResponse, TagBase

router = APIRouter(tags=["tags"], prefix="/tags")


@router.get("/", summary="List tags", response_model=List[TagResponse])
def list_tags(db: Session = Depends(get_db)):
    tags = tag_repository.list_tags(db)
    return tags


@router.post("/", summary="Create a tag", response_model=TagResponse)
def create_tag(payload: TagBase, db: Session = Depends(get_db)):
    tag = tag_repository.create_tag(db, payload.name)
    return tag
