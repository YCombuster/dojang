# Study AI

A web application for studying with AI assistance.

## Setup

1. Clone the repository
2. Start the Docker containers:
    ```
    docker compose up -d
    ```

## Development

### Backend

The backend is a FastAPI application with PostgreSQL and pgvector for vector storage.

#### Running Tests

Tests are run inside the Docker container to ensure consistent environment:

**Windows (PowerShell):**

```powershell
cd backend
.\run_tests.ps1
```

**Unix (Bash):**

```bash
cd backend
./run_tests.sh
```

To run specific tests:

```
cd backend
.\run_tests.ps1 tests/test_api.py::test_health_check
```

### Frontend

The frontend is a Next.js application.

## Database

The application uses PostgreSQL with pgvector extension for vector embeddings.

-   Database: `studyai`
-   Test Database: `test_study_ai`
-   Username: `postgres`
-   Password: `postgres`
