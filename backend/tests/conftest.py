import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy_utils import database_exists, create_database

# Import your FastAPI app and database models here
from app.main import app
from app.database import Base, get_db

# Test database URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test_study_ai"

@pytest.fixture(scope="session")
def test_db():
    """Create a fresh database for testing."""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    if not database_exists(engine.url):
        create_database(engine.url)
    
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_client(test_db):
    """Create a test client with a test database."""
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def snapshot(request):
    """Snapshot testing fixture."""
    class Snapshot:
        def assert_match(self, value):
            snapshot_dir = request.config.rootdir / "tests" / "snapshots"
            snapshot_dir.mkdir(exist_ok=True)
            
            test_name = request.node.name
            snapshot_file = snapshot_dir / f"{test_name}.snap"
            
            if not snapshot_file.exists():
                # Create new snapshot
                snapshot_file.write_text(str(value))
                return
            
            # Compare with existing snapshot
            expected = snapshot_file.read_text().strip()
            assert str(value).strip() == expected, (
                f"Snapshot mismatch!\nExpected:\n{expected}\n\nGot:\n{value}"
            )
    
    return Snapshot() 