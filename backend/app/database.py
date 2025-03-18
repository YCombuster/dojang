import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import psycopg2 with fallback to stub
try:
    import psycopg2
except ImportError:
    # Use our stub implementation if psycopg2 is not available
    from .psycopg2_stub import connect as psycopg2_connect
    # Create a fake psycopg2 module
    import sys
    import types
    psycopg2 = types.ModuleType('psycopg2')
    psycopg2.connect = psycopg2_connect
    sys.modules['psycopg2'] = psycopg2

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/studyai"
)

# Create SQLAlchemy engine with proper dialect options for development
try:
    engine = create_engine(DATABASE_URL)
except Exception as e:
    print(f"WARNING: Could not connect to database: {e}")
    # Create a dummy engine for development
    engine = None

# Create session factory (only if engine is available)
if engine:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    # Dummy session for development
    SessionLocal = None

# Create base class for models
Base = declarative_base()

def get_db():
    """
    Dependency for getting a database session.
    """
    if not SessionLocal:
        raise Exception("Database connection not available")
        
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 