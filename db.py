import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

from models import Base

load_dotenv()

logger = logging.getLogger(__name__)

# Create the engine and session
connection_string = os.getenv("DB_URL")
engine = create_engine(
    connection_string,
    pool_size=10,  # Maximum number of connections in the pool
    max_overflow=5,  # Additional connections allowed beyond pool_size
    pool_timeout=30,  # Seconds to wait before giving up on a connection
    pool_recycle=3600,  # Recycle connections after 1 hour to avoid stale ones
    pool_pre_ping=True,  # Checks if connections are alive before using them
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Create tables in the database (only if they don't exist)
Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency that yields a database session."""
    db = SessionLocal()
    try:
        print("Creating conn")
        yield db
    finally:
        db.close()
