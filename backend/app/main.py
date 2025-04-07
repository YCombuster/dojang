from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List

from .database import get_db, engine, Base
from . import models
from .routers import sources
from .services.document_processor import DocumentProcessor
from .services.source_intake import InformationSource

app = FastAPI(title="Study AI API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Include routers
app.include_router(sources.router)

@app.get("/")
def read_root():
    print("--- Root endpoint '/' was hit ---")
    return {"message": "Simple test response"}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)

):
    """
    Upload and process a document (currently supports PDF).
    
    The document will be:
    1. Saved temporarily
    2. Processed into chunks
    3. Each chunk will be saved as a KnowledgeBaseContent
    4. The document metadata will be saved as a KnowledgeBaseSource
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are currently supported")
        
        # Initialize document processor
        processor = DocumentProcessor()
        
        # Save uploaded file temporarily
        temp_path = await processor.save_upload_file(file)
        
        try:
            # Process the document
            chunks = await processor.process_file(temp_path, 'pdf')
            
            if not chunks:
                raise HTTPException(status_code=400, detail="Could not extract content from PDF")
            
            # Create a source from the first chunk's metadata
            first_chunk = chunks[0]
            metadata = first_chunk.metadata
            
            source = InformationSource(
                name=metadata.get('title', file.filename),
                source=metadata.get('creator', 'PDF Upload'),
                source_description=metadata.get('subject', ''),
                source_type='pdf_document',
                author=metadata.get('author', ''),
                publisher=metadata.get('producer', ''),
                publication_date=None,  # Could parse creation_date if needed
                license=None,
                language='en',  # Could use langdetect here
                url='',  # Local upload
                content_text=first_chunk.content,
                content_type='document'
            )
            
            # Create sections for remaining chunks
            source.sections = [
                InformationSource(
                    name=f"Page {chunk.page_number} - Chunk {chunk.chunk_number}",
                    source=source.source,
                    source_description=f"Extracted from page {chunk.page_number}",
                    source_type=source.source_type,
                    author=source.author,
                    publisher=source.publisher,
                    publication_date=source.publication_date,
                    license=source.license,
                    language=source.language,
                    url=source.url,
                    content_text=chunk.content,
                    content_type='section'
                )
                for chunk in chunks[1:]
            ]
            
            # Save to database using existing service
            from .services.source_intake import SourceIntakeService
            service = SourceIntakeService(db)
            result = await service.process_source(source)
            
            return {
                "status": "success",
                "message": "Document processed successfully",
                "source_id": result.source_id,
                "chunks_processed": len(chunks)
            }
            
        finally:
            # Clean up temporary file
            os.unlink(temp_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(db: AsyncSession = Depends(get_db)):
    """Chat with the AI about uploaded documents."""
    return {"status": "success", "message": "Chat response"}

@app.get("/questions")
async def get_questions(db: AsyncSession = Depends(get_db)):
    """Get generated questions about uploaded documents."""
    return {"status": "success", "questions": ["Sample question 1?", "Sample question 2?"]} 