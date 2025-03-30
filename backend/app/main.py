from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .database import get_db, engine, Base
from . import models
from .routers import sources

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Study AI API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sources.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Study AI API"}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/upload")
def upload_document(db: Session = Depends(get_db)):
    """Upload a document for processing."""

    # implement adding of content into here
    # so that means pdf to 
    return {"status": "success", "message": "Document uploaded"}

@app.post("/chat")
def chat(db: Session = Depends(get_db)):
    """Chat with the AI about uploaded documents."""
    return {"status": "success", "message": "Chat response"}

@app.get("/questions")
def get_questions(db: Session = Depends(get_db)):
    """Get generated questions about uploaded documents."""
    return {"status": "success", "questions": ["Sample question 1?", "Sample question 2?"]} 