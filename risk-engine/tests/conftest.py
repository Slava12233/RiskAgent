"""
Test configuration and fixtures for the Risk Engine tests.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import RiskEvaluation

# Create an in-memory SQLite database for testing
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)

# Create test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    """
    Create tables in the test database and yield a test database session.
    """
    # Create the tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new session for testing
    db = TestingSessionLocal()
    
    # Override the get_db dependency to use our test database
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    # Replace the app dependency
    app.dependency_overrides[get_db] = override_get_db
    
    yield db
    
    # Clean up after the test
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def setup_test_db(test_db):
    """
    Automatically use the test_db fixture for all tests.
    """
    return 