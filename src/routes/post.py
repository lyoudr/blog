from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from src.models.database import get_db
from src.models.user import User
from src.schemas.post import PostBase, PostResponse, CreatePostResponse
from src.repositories import post_repository, tag_repository
from src.utils.pubsub import publish_new_post_event
from src.utils.auth import get_current_user


router = APIRouter(tags=["post"], prefix="/post")

@router.get(
    "/all",
    summary="Get all posts by user ID",
    response_model=List[PostResponse],
)
def get_posts(
    db: Session = Depends(get_db)
):
    posts = post_repository.list_posts(
        db
    )
    return [PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,  # Assuming content is a string
        user_id=post.user_id,
        user_name=post.user.name,
        created_time=post.created_time,
        updated_time=post.updated_time,
        images=[img.url for img in post.images]  # Passing raw image URLs to PostResponse
    ) for post in posts]

@router.get(
    "/",
    summary="Get all posts by user ID",
    response_model=List[PostResponse],
)
def get_posts_by_user_id(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    posts = post_repository.list_post_by_user_id(
        db, 
        user.id
    )
    return [PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,  # Assuming content is a string
        user_id=post.user_id,
        user_name=post.user.name,
        created_time=post.created_time,
        updated_time=post.updated_time,
        images=[img.url for img in post.images]  # Passing raw image URLs to PostResponse
    ) for post in posts]


@router.post(
    "/",
    summary="Create a new post",
    response_model=CreatePostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    payload: PostBase,
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db),
):
    post = post_repository.create_post(db, user.id, payload)
    tag_repository.create_post_tag(db, post.id, payload.tag_ids)
    # publish_new_post_event(post)
    return post


@router.get(
    "/{post_id}",
    summary="Get a post",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
def get_post(
    post_id: int,
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    post = post_repository.get_post(
        db, 
        post_id,
        user.id
    )
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,  # Assuming content is a string
        user_id=post.user_id,
        user_name=post.user.name,
        created_time=post.created_time,
        updated_time=post.updated_time,
        images=[img.url for img in post.images]  # Passing raw image URLs to PostResponse
    )
