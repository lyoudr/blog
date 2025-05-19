from sqlalchemy import (
    Column,
    BigInteger,
    String,
    ForeignKey,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship
from src.models.database import Base


class Image(Base):
    __tablename__ = "image"

    id = Column(BigInteger, primary_key=True)
    url = Column(String(255), nullable=False)
    post_id = Column(BigInteger, ForeignKey("post.id"), nullable=False)
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationship back to Post
    post = relationship("Post", back_populates="images")


class Video(Base):
    __tablename__ = "video"
    
    id = Column(BigInteger, primary_key=True)
    url = Column(String(255), nullable=False)
    post_id = Column(BigInteger, ForeignKey("post.id"), nullable=False)
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationship back to Post
    post = relationship("Post", back_populates="videos")