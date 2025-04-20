from sqlalchemy import (
    Column,
    BigInteger,
    DateTime,
    ForeignKey,
    func,
    UniqueConstraint,
)

from src.models.database import Base


class Follow(Base):
    __tablename__ = "follow"
    __table_args__ = (
        UniqueConstraint("user_id", "follower_id", name="uq_user_follower"),
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    follower_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())
