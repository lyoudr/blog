from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.post import Post
from src.schemas.post import PostBase, PostResponse
from src.utils.gcs import GoogleCloudStorage


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
    user_id: int,
    payload: PostBase,
):
    # Step 1: Create Post object
    post = Post(
        title=payload.title,
        content=payload.content,
        user_id=user_id,
    )

    # Step 3: Add to session and commit
    db.add(post)
    db.commit()
    db.refresh(post)

    return post


def get_post(
    db: Session,
    post_id: int,
    user_id: int,
) -> Post:
    post = db.query(
        Post
    ).filter(
        Post.id == post_id,
        Post.user_id == user_id
    ).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    signed_urls = []
    if post.images:
        gcs = GoogleCloudStorage()
        signed_urls = [gcs.generate_signed_url(img.url) for img in post.images]
    
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        user_id=post.user_id,
        created_time=post.created_time,
        updated_time=post.updated_time,
        images=signed_urls
    )

def delete_post(
    db: Session,
    post_id: int,
):
    # Step 1: Retrieve the post
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Step 2: Delete the post
    db.delete(post)
    db.commit()