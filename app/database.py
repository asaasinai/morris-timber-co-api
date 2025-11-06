from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
import logging

logger = logging.getLogger(__name__)

# Get database URL from environment variable
# For Vercel/production, use PostgreSQL: postgresql://user:pass@host/dbname
# For local development, SQLite: sqlite:///./morris_timber.db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./morris_timber.db")

# Configure engine based on database type
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False},
        poolclass=NullPool  # SQLite doesn't need connection pooling
    )
else:
    # PostgreSQL or other databases
    # Use NullPool for serverless to avoid connection pool issues
    engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,
        pool_pre_ping=True,  # Verify connections before using
        echo=False
    )
    logger.info(f"Database engine created for: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'database'}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Get database session with error handling"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

