from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.user import User
from src.models.follow import Follow
from src.schemas.follow import FollowBase


def get_followers(db: Session, user_id: int):
    followers = (
        db.query(Follow.follower_id.label("user_id"), User.name.label("name"))
        .join(User, Follow.follower_id == User.id)
        .filter(Follow.user_id == user_id)
        .all()
    )
    return followers


def create_follow(
    db: Session,
    payload: FollowBase,
):
    follows = [
        Follow(user_id=payload.user_id, follower_id=follower_id)
        for follower_id in payload.followers
    ]

    db.add_all(follows)

    try:
        db.flush()  # Will raise IntegrityError if any duplicates
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Some follows already exist.")
