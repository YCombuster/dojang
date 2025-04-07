"""
This is a very important file. It uploads our PDFs to the database, no matter how large the PDF is

- User uploads PDF
- process_file → split into text chunks (for preview maybe) →
- pdf_to_json → semantic JSON from Marker
- sub_chunk → create source metadata row in KnowledgeBaseSource
- traverse_blocks → recurse over semantic blocks and call insert_content depending on the type
- insert_content → save each paragraph/section/list/etc into KnowledgeBaseContent.

"""

from typing import Dict, List, Optional, Any
from fastapi import UploadFile
import re
from pathlib import Path
import tempfile
import fitz # pymupdf
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.schema import BlockTypes
# from marker.schema import SourceMetadata
import openai
import asyncio
import asyncpg
import aiofiles
import uuid
import os
import json
from app import models  # Import models from app package

# for the sectioning of the chunks
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy.orm import Session

# TODO:
# - [x] (Optional) Bundle common params (db, source_id, section_stack) into a context object for cleaner recursion.
# - [ ] (Optional) Improve error handling around database commits (rollback on failure).
# - [ ] (Optional) Remove dead/commented out code (old config_parser stuff in `pdf_to_json`).
# - [ ] (Optional) Add type hints to all functions for better readability and IDE support.

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

class DocumentProcessingContext:
    def __init__(self, db: Session, source: "models.KnowledgeBaseSource"):
        self.db = db
        self.source = source
        self.section_stack = []
        self.metadata = {}  # optional extras
        self.content_buffer = [] # used to hold all the blocks before committing to database
        self.buffer_limit = 500   # how big the batch is before saving

# CONSTANTS
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
CHUNK_SIZE = 64 * 1024  # 64KB chunks for better performance

# -------------------

def flush_buffer(context):
    if context.content_buffer:
        context.db.bulk_save_objects(context.content_buffer)
        context.db.commit()
        context.content_buffer.clear()

# for the sectioning of the chunking

def html_to_text(html):
    return BeautifulSoup(html, "html.parser").get_text()

"""
What is a "block" in marker?
they are the "smallest structural units in the PDF"
e.g., a section header, a paragraph of text, a list, an image, a page footer
"""
def pdf_to_json(path, output_path):    
    """
    config reference
    config = settings (what output you want, OCR yes/no, use LLM yes/no)

    artifact_dict = the brains (the models/knowledge about documents)
    processor_list = cleanup helpers (optional extras to improve block extraction/formatting)
    renderer = pretty printer (turns blocks into Markdown/JSON/HTML)
    llm_service = smart assistant (an optional LLM to "fix" hard cases)

    config = {
    "output_format": "json",
    }
    config_parser = ConfigParser(config)
    """

    converter = PdfConverter(
        artifact_dict=create_model_dict(),
    )

    document = converter.build_document(
        path,
        output_format="json"
    )

    # TODO: update metadata retrieval
    # metadata = SourceMetadata(
    #     source=path  # Just use the file path or any identifier
    # )

    # TODO: pass in real metadata. relies on the above
    temp_dict = dict()
    temp_dict = {"placeholder": True}

    data = {
        "document": document,
        "metadata": temp_dict
    }

    # for debugging purposes
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(document.dict(), f, ensure_ascii=False, indent=2)

    return data

def sub_chunk(json_data: dict[str, Any], db: Session, source_metadata: dict[str, Any]) -> dict[str, Any]:
    """
    This function takes our marker JSON, takes the sections, 
    and formulates metadata and extracts content. It saves it into the database with insert_content
    It prepares for block traversal.
    
    Args: JSON data from marker, database session, a dictionary which we plug into the knowledge_base_source
    Returns: success if we get through all of the subchunks
    """
    # 1. Insert knowledge_base_sources row (created empty one) AKA the metadata
    # remember that this is from @models.py courtesy of SQLAlchemy

    # error: models is not defined
    source = models.KnowledgeBaseSource(
        name=source_metadata.get("title", "Untitled"),
        author=source_metadata.get("author", "Unknown"),
        language=source_metadata.get("language", "en"),
        license=source_metadata.get("license", "unknown"),
        source_type="textbook",
        # TODO: figure out non-deprecated version
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    # ADD to database (stages it)
    db.add(source)
    db.commit()
    db.refresh(source)

    # initialize the context
    context = DocumentProcessingContext(db=db, source=source)

    try:
        # Pass db and stack
        traverse_blocks(json_data.get("children", []), parent_id=None, context=context)

         # Final flush if anything remains in buffer
        flush_buffer(context)

    except Exception as e:
        context.db.rollback()
        raise e

    return {"status": "success", "source_id": source.source_id}

def insert_content(block, parent_id=None, context: DocumentProcessingContext = None):
    """
    Inserts the HTML that we got from the marker JSON
    into the corresponding database table

    title:         

    Args:
    Returns:
    """

    if not context or not context.source:
        raise ValueError("Context with source is required")

    # GET THE TEXT
    # TODO: update how we get this
    # it should be extracting from json
    content_text = html_to_text(block.get("html", ""))
    block_type = block.get("block_type", "Unknown")
    # embedding = generate_embedding(content_text)  # your embedding function

    # the reason why title is None for only text and not all others: blocks can be SectionHeader, ListGroup, ListItem, Page, so it makes sense to keep track of those
    # we don't want to embed the text itself as a title
    
    # also, source is from sub_chunk, our parent function
    # so we're updating the knowledge_base_content row with SQLAlchemy ORM

    # error: models is not defined
    content = models.KnowledgeBaseContent(
        source_id=context.source.source_id, # we keep the key consistent
        parent_content_id=parent_id, # parent is from params
        title=None if block_type == "Text" else content_text[:100], # add a label if it's not pure text
        content=content_text, # content is as extracted
        content_type=block_type, # keep track of type
        # embedding=embedding, # TODO: add embedding
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    context.content_buffer.append(content)

    # If buffer is full, bulk save and reset
    if len(context.content_buffer) >= context.buffer_limit:
        flush_buffer(context)

    return content

def traverse_blocks(blocks: list, parent_id=None, context: DocumentProcessingContext = None):
    section_stack = context.section_stack

    for block in blocks:
        block_type = block.get("block_type")
        
        # if page, then recurse through it as pages are containers not content
        # if section header (like "Chapter 1: Limits"), then insert the block with parent id being the page
        # if text OR ListItem, then we insert the block with parent id being the latest nest (if exists)
        # if ListGroup, then recurse through the bullet points/numbered list containers with parent id being latest nest (if exists)

        # note: section stack keeps track of nested section headers. [-1][0] gets the top of the stack.
        if block_type == "Page":
            traverse_blocks(block.get("children", []), parent_id=parent_id, context=context)
        elif block_type == "SectionHeader":
            section_id = insert_content(block, db=db, parent_id=parent_id)
            # update the stack for this new section level
            section_stack.append((section_id, block.get("section_hierarchy", {})))
            traverse_blocks(block.get("children", []), parent_id=section_id, context=context)
        elif block_type in {"Text", "ListItem"}:
            # its parent is the latest nested item if we even have one. else it's just the page.
            insert_content(block, db=db, parent_id=section_stack[-1][0] if section_stack else parent_id)
        elif block_type == "ListGroup":
            traverse_blocks(block.get("children", []), parent_id=section_stack[-1][0], context=context)

    # 2. Begin traversal

    return {"status": "success", "source_id": context.source.source_id}

# -------------------

# for the chunking

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
    This gets us our chunk #1 (from the entire pdf, we chunk into chunks of size X)
    Note that this is different from taking a chunk and splitting into sections
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

# TODO: rename to be more descriptive   
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
        # now we need to take this, and then run marker on it
        return await self._split_pdf_into_chunks(upload_file, source_id, metadata or {})
    else:
        raise ValueError(f"Unsupported file type: {content_type}")