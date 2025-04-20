from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.models.tag import Tag
from src.models.post import PostTag


def list_tags(db: Session) -> List[Tag]:
    tags = db.query(Tag).all()
    return [] if not tags else tags


def create_tag(db: Session, name: str) -> Tag:
    existing_tag = db.query(Tag).filter(Tag.name == name).first()
    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Tag already exists"
        )
    new_tag = Tag(name=name)

    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)

    return new_tag


def create_post_tag(db: Session, post_id: int, tag_ids: List[int]) -> None:
    post_tags = [PostTag(post_id=post_id, tag_id=tag_id) for tag_id in tag_ids]
    db.bulk_save_objects(post_tags)
    db.commit()
