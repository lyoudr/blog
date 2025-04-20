from sqlalchemy import (
    Column,
    BigInteger,
    String,
    DateTime,
    func,
)
from src.models.database import Base


class Tag(Base):
    __tablename__ = "tag"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(50), nullable=False)
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, server_default=func.now(), onupdate=func.now())
