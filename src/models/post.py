from sqlalchemy import (
    Column,
    BigInteger,
    String,
    DateTime,
    ForeignKey,
    func,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from src.models.database import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(BigInteger, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(JSON, nullable=False)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False, index=True)
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())
    orders = Column(JSON, nullable=True)
    # Relationships
    user = relationship("User", back_populates="posts")
    images = relationship("Image", back_populates="post", cascade="all, delete-orphan")
    videos = relationship("Video", back_populates="post", cascade="all, delete-orphan")


class PostTag(Base):
    __tablename__ = "post_tag"

    post_id = Column(BigInteger, ForeignKey("post.id"), nullable=False)
    tag_id = Column(BigInteger, ForeignKey("tag.id"), nullable=False)
    created_time = Column(DateTime, server_default=func.now())

    __table_args__ = (PrimaryKeyConstraint("post_id", "tag_id"),)
