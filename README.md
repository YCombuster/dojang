# Study AI Application

A modern study application built with Next.js, FastAPI, and PostgreSQL with pgvector for vector similarity search.

-   personalized learning experience through features like
    -   curriculum-specific practice questions
    -   flashcards
    -   mini-lessons
    -   AI-driven feedback.
-   content sourced from open educational resources, e.g. openstax

goal: implement a CDN that integrates with vectors so the AI features can be done easily, and then open source it

## Project Structure

```
.
├── frontend/          # Next.js frontend application
├── backend/          # FastAPI backend application
├── docker-compose.yml
└── README.md
```

## Prerequisites

-   Docker
-   Docker Compose

## Getting Started

1. Clone the repository:

```bash
git clone <repository-url>
cd study-ai
```

2. Create necessary environment files:

For frontend (.env.local):

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For backend (.env):

```
DATABASE_URL=postgresql://postgres:postgres@db:5432/studyai
```

3. Start the application:

```bash
docker compose up --build
```

This will start:

-   Frontend at http://localhost:3000
-   Backend API at http://localhost:8000
-   PostgreSQL database at localhost:5432

## Development

-   The application uses hot-reloading for both frontend and backend
-   Any changes to the code will automatically reflect in the running application
-   Database data is persisted in a Docker volume

## Services

### Frontend (Next.js)

-   Modern React application with TypeScript
-   Tailwind CSS for styling
-   Server and Client Components
-   Optimized for performance

### Backend (FastAPI)

-   Modern Python web framework
-   AsyncIO support
-   Automatic API documentation (Swagger UI at /docs)
-   Type hints and validation

### Database (PostgreSQL)

-   Persistent storage using Docker volumes
-   pgvector extension for vector similarity search
-   Secure default configuration
