from setuptools import setup, find_packages

setup(
    name="study-ai-backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2-binary",
        "python-dotenv",
        "pydantic",
        "pydantic-settings",
        "pgvector",
        "alembic",
    ],
) 