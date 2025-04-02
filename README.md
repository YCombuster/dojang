# Study AI

A web application for studying with AI assistance.

-   personalized learning experience through features like
    -   curriculum-specific practice questions
    -   flashcards
    -   mini-lessons
    -   AI-driven feedback.
-   content sourced from open educational resources, e.g. openstax

goal: implement a CDN that integrates with vectors so the AI features can be done easily, and then open source it

## Project Structure

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
-   Password: `zany12`
