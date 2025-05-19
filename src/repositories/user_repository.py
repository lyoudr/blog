from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from src.models.user import User
from src.utils.auth import get_password_hash

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


def get_user_by_email(db: Session, email: str) -> bool:
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail='Email already registered'
        )
    return False

def create_user(
    db: Session, 
    username: str,
    email: str,
    password: str,
    image_url: str,
) -> User:
    hashed_pass = get_password_hash(password)
    new_user = User(
        name = username,
        email = email,
        password = hashed_pass,
        image_url= image_url,
        is_verified = True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user