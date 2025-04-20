from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.schemas.follow import (
    FollowBase,
    FollowResponse,
    FollowerResponse,
    ListFollowResponse,
)
from src.models.database import get_db
from src.utils.decorator import transaction
from src.repositories import follow_repository

router = APIRouter(tags=["follow"], prefix="/follow")


@router.get(
    "/{user_id}/get-followers",
    summary="Get followers",
    response_model=ListFollowResponse,
)
def get_followers(user_id: int, db: Session = Depends(get_db)):
    followers = follow_repository.get_followers(db, user_id)
    return ListFollowResponse(
        data=[
            FollowerResponse(user_id=follower.user_id, name=follower.name)
            for follower in followers
        ]
    )


@router.post("/create-follow", summary="Create follow", response_model=FollowResponse)
@transaction
def add_follow(payload: FollowBase, db: Session = Depends(get_db)):
    follow_repository.create_follow(db, payload)

    return FollowResponse(status="sccess")
