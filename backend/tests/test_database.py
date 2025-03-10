import pytest
from sqlalchemy import text
from pgvector.sqlalchemy import Vector

def test_database_connection(test_session):
    """Test that we can connect to the database."""
    result = test_session.execute(text("SELECT 1"))
    assert result.scalar() == 1

def test_pgvector_extension(test_session):
    """Test that pgvector extension is available and working."""
    # Check if pgvector extension exists
    result = test_session.execute(
        text("SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector')")
    )
    assert result.scalar() is True

    # Test vector operations
    result = test_session.execute(
        text("SELECT '[1,2,3]'::vector <-> '[4,5,6]'::vector")
    )
    distance = result.scalar()
    assert isinstance(distance, float)
    assert distance > 0

def test_database_tables(test_session):
    """Test that all required tables exist in the database."""
    # Add this test once your models are defined
    pass 