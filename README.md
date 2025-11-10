# Dojang - AI-Powered Learning Platform

Transform your PDF textbooks into intelligent study materials with AI-generated flashcards, quizzes, and semantic search.

<div align="center">

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 15](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com/)

</div>

---

## 🎯 Project Overview

**Dojang** is an AI-powered learning platform that transforms large PDF textbooks into intelligent study materials. Upload a PDF, and the system:

1. **Extracts semantic content** using Marker (preserves structure: headings, lists, tables)
2. **Generates embeddings** with OpenAI (768-dimensional vectors)
3. **Stores in PostgreSQL** with pgvector for fast similarity search
4. **Enables learning features** like flashcards, quizzes, and spaced repetition (in development)

### Vision

Create a comprehensive CDN (Content Delivery Network) that integrates with vector databases, making AI-powered educational features easy to implement and open source for everyone.

---

## ✨ Features

### Currently Implemented ✅

- **PDF Processing Pipeline**
  - Semantic extraction with Marker
  - Hierarchical content storage
  - Memory-optimized for large textbooks
  
- **Vector Embeddings**
  - OpenAI text-embedding-ada-002
  - Batch processing (100 chunks at a time)
  - pgvector storage for similarity search

- **Beautiful UI**
  - Modern Next.js frontend
  - Drag-and-drop PDF upload
  - Real-time progress tracking

- **Robust Backend**
  - FastAPI with async support
  - PostgreSQL with pgvector
  - Comprehensive test suite

### In Development 🚧

- Vector similarity search (RAG)
- AI flashcard generation
- Quiz creation
- Spaced repetition system
- Chat with documents
- User authentication
- Study progress tracking

---

## 🚀 Quick Start

**Get up and running in 5 minutes:**

1. **Prerequisites:** Docker Desktop + OpenAI API key
2. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd dojang
   echo "OPENAI_API_KEY=your_key_here" > .env
   ```
3. **Start everything:**
   ```bash
   docker-compose up --build
   ```
4. **Access the app:** http://localhost:3000

**For detailed instructions, see [QUICKSTART.md](./QUICKSTART.md)**

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [**QUICKSTART.md**](./QUICKSTART.md) | Get started in 5 minutes with Docker |
| [**SETUP.md**](./SETUP.md) | Detailed development setup (Docker & manual) |
| [**ARCHITECTURE.md**](./ARCHITECTURE.md) | System design, data flow, and technical details |
| [**FEATURES.md**](./FEATURES.md) | Implementation guides for new features |

---

## 🏗️ Technology Stack

### Frontend
- **Framework:** Next.js 15 (React 18)
- **Language:** TypeScript
- **Styling:** Tailwind CSS + Shadcn UI
- **Testing:** Playwright

### Backend
- **Framework:** FastAPI
- **Language:** Python 3.11+
- **ORM:** SQLAlchemy (async)
- **PDF Processing:** PyMuPDF + Marker
- **AI:** OpenAI API
- **Testing:** Pytest

### Database
- **DBMS:** PostgreSQL 15+
- **Vector Search:** pgvector extension
- **Schema:** Hierarchical content storage

### Infrastructure
- **Containerization:** Docker + Docker Compose
- **Development:** Hot reload for frontend & backend

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend (Next.js)                                          │
│  • PDF Upload UI                                             │
│  • Flashcards (TODO)                                         │
│  • Quizzes (TODO)                                            │
└─────────────────────────────────────────────────────────────┘
                          │ HTTP/REST
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Backend (FastAPI)                                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Document Processing Pipeline                       │    │
│  │  PDF → Marker → JSON → DB → OpenAI → Embeddings    │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  PostgreSQL + pgvector                                       │
│  • Document metadata                                         │
│  • Hierarchical content                                      │
│  • 768-dim embeddings                                        │
└─────────────────────────────────────────────────────────────┘
```

For detailed architecture, see [ARCHITECTURE.md](./ARCHITECTURE.md)

---

## 🛠️ Development

### Running Tests

**Backend:**
```bash
# Inside Docker
docker exec -it dojang-backend-1 pytest

# Or use the script
cd backend
./run_tests.sh  # Unix/Mac
.\run_tests.ps1  # Windows
```

**Frontend:**
```bash
docker exec -it dojang-frontend-1 npx playwright test
```

### Making Changes

- **Backend:** Edit files in `backend/app/` - auto-reloads
- **Frontend:** Edit files in `frontend/` - Fast Refresh
- **Database:** Modify `backend/app/models.py` + create migration

### Viewing Logs

```bash
docker-compose logs -f              # All services
docker-compose logs -f backend      # Backend only
docker-compose logs -f frontend     # Frontend only
```

---

## 🗄️ Database Schema

### Core Tables

**knowledge_base_sources** - Document metadata
- source_id, name, author, publisher, etc.

**knowledge_base_content** - Hierarchical content with embeddings
- content_id, source_id, parent_content_id
- title, content, content_type
- **embedding** (VECTOR(768))

**users** - User management (for future auth)

**tags** - Content tagging system

**user_activity_log** - Track learning progress

See [ARCHITECTURE.md](./ARCHITECTURE.md) for full schema details.

---

## 🎓 Contributing Features

We welcome contributions! Here's how to get started:

1. **Pick a feature** from [FEATURES.md](./FEATURES.md)
2. **Read the architecture** in [ARCHITECTURE.md](./ARCHITECTURE.md)
3. **Set up your environment** with [SETUP.md](./SETUP.md)
4. **Create a feature branch:** `git checkout -b feat/your-feature`
5. **Implement & test**
6. **Submit a pull request**

### High-Priority Features

- 🔴 Vector Similarity Search
- 🔴 Flashcard Generation
- 🔴 Quiz Generation
- 🟡 Spaced Repetition System
- 🟡 Chat with Documents

See [FEATURES.md](./FEATURES.md) for detailed implementation guides.

---

## 📦 Project Structure

```
dojang/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app
│   │   ├── models.py                  # Database models
│   │   ├── database.py                # DB connection
│   │   ├── routers/                   # API endpoints
│   │   └── services/
│   │       ├── document_processor.py  # Core pipeline
│   │       └── source_intake.py       # Content ingestion
│   ├── tests/                         # Pytest tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/                           # Next.js pages
│   ├── components/
│   │   ├── FileUpload.tsx            # Upload UI
│   │   └── ui/                        # Shadcn components
│   ├── tests/                         # Playwright tests
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml                 # Multi-container setup
├── init-db.sh                         # Database initialization
├── QUICKSTART.md                      # Quick start guide
├── SETUP.md                           # Detailed setup
├── ARCHITECTURE.md                    # System design
└── FEATURES.md                        # Feature guides
```

---

## 🔐 Environment Variables

### Backend (.env)

```bash
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql+asyncpg://postgres:zany12@localhost:5433/studyai
UPLOAD_DIR=./uploads
```

---

## 🚢 Deployment

### Current: Development

All services run in Docker containers locally.

### Future: Production

- Frontend: Vercel/Netlify
- Backend: AWS ECS / GCP Cloud Run
- Database: AWS RDS / GCP Cloud SQL
- Background Jobs: Celery + Redis
- Monitoring: Sentry, Prometheus, Grafana

---

## 📝 License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

See [LICENSE](./LICENSE) for full details.

---

## 🙏 Acknowledgments

- **Marker** - Excellent PDF semantic extraction
- **pgvector** - PostgreSQL vector similarity search
- **OpenAI** - Embeddings and GPT models
- **FastAPI** - Modern Python web framework
- **Next.js** - React framework for production

---

## 📧 Contact & Support

- **Issues:** [GitHub Issues](../../issues)
- **Discussions:** [GitHub Discussions](../../discussions)
- **Documentation:** See docs folder

---

## 🗺️ Roadmap

- [x] PDF upload and processing
- [x] Semantic content extraction
- [x] Embedding generation
- [x] Vector storage (pgvector)
- [x] Beautiful UI
- [ ] Vector similarity search
- [ ] Flashcard generation
- [ ] Quiz creation
- [ ] Spaced repetition
- [ ] User authentication
- [ ] Progress tracking
- [ ] Multi-modal support (images, videos)
- [ ] Mobile app
- [ ] Open source CDN for education

---

**Ready to get started? See [QUICKSTART.md](./QUICKSTART.md) to begin!**
