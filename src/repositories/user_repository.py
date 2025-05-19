from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from src.models.user import User


def get_user_by_name(db: Session, username: str) -> User:
    user = db.query(User).filter(User.name == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user

def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


def list_users(db: Session):
    return db.query(User).order_by(User.id).all()
