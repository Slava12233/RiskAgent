"""
Database connection and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import sys
import logging

logger = logging.getLogger(__name__)

# Determine if we're in testing mode
is_testing = "pytest" in sys.modules

# Database connection URL - can be overridden with environment variable
# Use SQLite by default for easier setup and running
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./risk_engine.db"  # SQLite file in the current directory
)

# For testing, always use SQLite in-memory database
if is_testing:
    DATABASE_URL = "sqlite:///:memory:"
    logger.info("Using in-memory SQLite database for testing")
else:
    logger.info(f"Using database: {DATABASE_URL}")

# Create SQLAlchemy engine with appropriate configurations for SQLite
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    # Required for SQLite to handle concurrent requests properly
    connect_args = {"check_same_thread": False}

# Create engine with appropriate args
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    """
    Create a new database session for each request and close it when done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to test the database connection
def test_connection():
    """
    Test the database connection.
    Returns True if connection is successful, False otherwise.
    """
    try:
        conn = engine.connect()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return False 