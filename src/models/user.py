from sqlalchemy import Column, BigInteger, String, DateTime, func
from sqlalchemy.orm import relationship
from src.models.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Using `back_populates` to link to Post model
    posts = relationship("Post", back_populates="user")
