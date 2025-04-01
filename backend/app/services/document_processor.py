from typing import Dict, List, Optional
from fastapi import UploadFile
import re
from pathlib import Path
import tempfile
import fitz  # PyMuPDF
from marker import extract_from_file
import openai
import asyncio
import asyncpg
import aiofiles
import uuid
import os


class DocumentChunk:
    def __init__(
        self,
        content: str,
        page_number: int,
        chunk_number: int,
        metadata: Optional[Dict] = None
    ):
        self.content = content
        self.page_number = page_number
        self.chunk_number = chunk_number
        self.metadata = metadata or {}

class DocumentProcessor:
    def __init__(self):
        # Configure chunking parameters
        self.min_chunk_size = 200  # minimum characters per chunk
        self.max_chunk_size = 1000  # maximum characters per chunk
        self.overlap = 50  # number of characters to overlap between chunks

# CONSTANTS
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
CHUNK_SIZE = 64 * 1024  # 64KB chunks for better performance

async def save_upload_file(upload_file: UploadFile) -> str:
    """
    Save an uploaded file asynchronously with improved error handling and cleanup.
    Args:
        upload_file: FastAPI UploadFile object
    Returns:
        str: Path to the saved file
    """
    try:
        # Create uploads directory if it doesn't exist
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        # Generate unique filename with original extension
        ext = Path(upload_file.filename).suffix or '.pdf'
        filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Save file in chunks
        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunk := await upload_file.read(CHUNK_SIZE):
                await out_file.write(chunk)
                
        return file_path
        
    except Exception as e:
        # Clean up partial file if save fails
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise RuntimeError(f"Failed to save upload file: {str(e)}")

async def _split_pdf_into_chunks(
    self, 
    upload_file: UploadFile, 
    source_id: int,
    metadata: Dict
) -> List[DocumentChunk]:
    """
    Split PDF into semantic chunks, extract text, and return document chunks.
    Args:
        upload_file: FastAPI UploadFile containing the PDF
        source_id: Unique identifier for this document source
        metadata: Additional metadata about the document
    Returns:
        List of DocumentChunk objects containing the processed content
    """
    # Save upload to temp file and get path
    path = await save_upload_file(upload_file)
    chunks = []

    try:
        # Open PDF handler
        doc = fitz.open(path)
        
        # Process PDF in chunks of pages
        chunk_size = 5

        for chunk_start in range(0, len(doc), chunk_size):
            # Get page range for this chunk
            chunk_end = min(chunk_start + chunk_size, len(doc))
            
            # Extract text from pages in this chunk
            chunk_text = ""
            for page_num in range(chunk_start, chunk_end):
                page = doc[page_num]
                chunk_text += page.get_text()
            
            # Clean and normalize the extracted text
            chunk_text = self._clean_text(chunk_text)
            
            # Create chunk object with metadata
            chunk = DocumentChunk(
                content=chunk_text,
                page_number=chunk_start,
                chunk_number=len(chunks),
                metadata={
                    "source_id": source_id,
                    "page_range": f"{chunk_start}-{chunk_end-1}",
                    **metadata
                }
            )
            chunks.append(chunk)
            
    finally:
        # Clean up temp file
        os.remove(path)
        
    return chunks

async def process_file(
    self, 
    upload_file: UploadFile,
    source_id: int,
    metadata: Dict = None
) -> List[DocumentChunk]:
    """
    Process an uploaded file and return chunks.
    Currently supports PDF, can be extended for other formats.
    Args:
        upload_file: FastAPI UploadFile object
        source_id: Unique identifier for the document
        metadata: Optional metadata about the document
    Returns:
        List[DocumentChunk]: Processed document chunks
    """
    content_type = upload_file.content_type or ''
    
    if 'pdf' in content_type.lower():
        return await self._split_pdf_into_chunks(upload_file, source_id, metadata or {})
    else:
        raise ValueError(f"Unsupported file type: {content_type}")