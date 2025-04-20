from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy import create_engine

from src.core.config import settings

import psycopg2

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,  # How many "extra" connections can be opened beyond pool_size
    pool_timeout=30,  # wait time (seconds) to get a connection
    pool_recycle=1800,  # recycle connections after this many seconds
)
SessionLocal = sessionmaker(bind=engine)

meta = MetaData()
Base = declarative_base(metadata=meta)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# psycopg2
conn = psycopg2.connect(
    dbname=settings.DB_NAME,
    user=settings.DB_USER,
    password=settings.DB_PASS,
    host=settings.DB_HOST,
    port=5432,
)
