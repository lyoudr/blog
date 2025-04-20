from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.models.database import get_db
from src.schemas.post import PostBase, PostResponse
from src.repositories import post_repository, tag_repository
from src.utils.decorator import transaction
from src.utils.pubsub import publish_new_post_event

router = APIRouter(tags=["post"], prefix="/post")


@router.get(
    "/user/{user_id}",
    summary="Get all posts by user ID",
    response_model=List[PostResponse],
)
def get_posts_by_user_id(user_id: int, db: Session = Depends(get_db)):
    posts = post_repository.list_post_by_user_id(db, user_id)
    return posts


@router.post(
    "/",
    summary="Create a new post",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    payload: PostBase,
    db: Session = Depends(get_db),
):
    post = post_repository.create_post(db, payload)
    tag_repository.create_post_tag(db, post.id, payload.tag_ids)
    # publish_new_post_event(post)
    return post


@router.get(
    "/{post_id}",
    summary="Get a post",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = post_repository.get_post(db, post_id)
    return post
