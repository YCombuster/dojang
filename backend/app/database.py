import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database URL from environment variable or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@db:5432/studyai"
)

# Create SQLAlchemy async engine
engine = create_async_engine(DATABASE_URL)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Create base class for models
Base = declarative_base()

async def get_db():
    """
    Dependency for getting an async database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 