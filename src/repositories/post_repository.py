from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.post import Post
from src.schemas.post import PostBase
from src.repositories import user_repository


def list_post_by_user_id(db: Session, user_id: int):
    posts = (
        db.query(Post)
        .filter(Post.user_id == user_id)
        .order_by(Post.updated_time.desc())
        .all()
    )
    return [] if not posts else posts


def create_post(
    db: Session,
    payload: PostBase,
):
    # Step 1: Check if user exists
    user_repository.get_user(db, payload.user_id)

    # Step 2: Create Post object
    post = Post(
        title=payload.title,
        content=payload.content,
        user_id=payload.user_id,
    )

    # Step 3: Add to session and commit
    db.add(post)
    db.commit()
    db.refresh(post)

    return post


def get_post(
    db: Session,
    post_id: int,
) -> Post:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post
