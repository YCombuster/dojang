import pytest
from sqlalchemy import text, inspect
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
    
    # Test vector creation and comparison
    result = test_session.execute(
        text("SELECT '[1,2,3]'::vector")
    )
    vector = result.scalar()
    assert vector is not None
    
    # Test cosine distance
    result = test_session.execute(
        text("SELECT '[1,2,3]'::vector <=> '[4,5,6]'::vector")
    )
    cosine_distance = result.scalar()
    assert isinstance(cosine_distance, float)
    assert 0 <= cosine_distance <= 2  # Cosine distance is between 0 and 2

def test_database_tables(test_session):
    """Test that all required tables exist in the database."""
    inspector = inspect(test_session.bind)
    tables = inspector.get_table_names()
    
    # Add assertions for your expected tables once they're defined
    # For example:
    # assert "documents" in tables
    # assert "embeddings" in tables
    # assert "chat_history" in tables
    
    # For now, just check that we can inspect tables
    assert isinstance(tables, list) 