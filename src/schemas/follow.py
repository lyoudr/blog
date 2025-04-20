from pydantic import BaseModel
from typing import List


class FollowResponse(BaseModel):
    status: str


class FollowerResponse(BaseModel):
    user_id: int
    name: str


class ListFollowResponse(BaseModel):
    data: List[FollowerResponse]


class FollowBase(BaseModel):
    user_id: int
    followers: List[int]
