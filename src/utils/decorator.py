from functools import wraps
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


def transaction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db: Session = kwargs.get("db")
        if db is None:
            raise RuntimeError("Database session not found in function arguments")

        try:
            with db.begin():
                return func(*args, **kwargs)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return wrapper
