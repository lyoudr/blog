from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.models.database import get_db
from src.schemas.user import Login, Token
from src.utils.auth import authenticate_user, create_access_token

router = APIRouter(tags=["auth"], prefix="/auth")

@router.post(
    "/login",
    summary="Login user",
    response_model=Token,
)
def login(
    payload: Login,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        payload.username,
        payload.password
    )
    if not user:
        raise HTTPException(
            detail="Invalid credentials",
            status_code=401,
        )

    token = create_access_token({"user_id": user.id})
    return Token(access_token=token, token_type="bearer")