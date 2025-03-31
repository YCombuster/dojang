import PyPDF2
from typing import List, Dict, Optional
import re
from pathlib import Path
import tempfile
from datetime import datetime

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
        
    def process_pdf(self, file_path: str) -> List[DocumentChunk]:
        """
        Process a PDF file and return a list of document chunks.
        """
        chunks = []
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Extract metadata if available
            metadata = self._extract_pdf_metadata(pdf_reader)
            
            # Process each page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                # Split page into chunks
                page_chunks = self._split_into_chunks(
                    text, 
                    page_number=page_num + 1,
                    metadata=metadata
                )
                chunks.extend(page_chunks)
        
        return chunks

    def _extract_pdf_metadata(self, pdf_reader: PyPDF2.PdfReader) -> Dict:
        """Extract metadata from PDF document."""
        metadata = {}
        
        try:
            info = pdf_reader.metadata
            if info:
                metadata = {
                    "title": info.get("/Title", ""),
                    "author": info.get("/Author", ""),
                    "subject": info.get("/Subject", ""),
                    "creator": info.get("/Creator", ""),
                    "producer": info.get("/Producer", ""),
                    "creation_date": info.get("/CreationDate", ""),
                }
        except Exception:
            # If metadata extraction fails, return empty dict
            pass
            
        return metadata

    def _split_into_chunks(
        self, 
        text: str, 
        page_number: int,
        metadata: Dict
    ) -> List[DocumentChunk]:
        """
        Split text into chunks while trying to preserve semantic meaning.
        """
        chunks = []
        chunk_number = 0
        
        # Clean the text
        text = self._clean_text(text)
        
        # First try to split by sections/paragraphs
        paragraphs = text.split('\n\n')
        current_chunk = ""
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                continue
                
            # If adding this paragraph would exceed max_chunk_size,
            # save current chunk and start new one
            if len(current_chunk) + len(paragraph) > self.max_chunk_size and current_chunk:
                chunks.append(DocumentChunk(
                    content=current_chunk.strip(),
                    page_number=page_number,
                    chunk_number=chunk_number,
                    metadata=metadata
                ))
                chunk_number += 1
                current_chunk = paragraph
            else:
                if current_chunk:
                    current_chunk += "\n\n"
                current_chunk += paragraph
        
        # Don't forget the last chunk
        if current_chunk:
            chunks.append(DocumentChunk(
                content=current_chunk.strip(),
                page_number=page_number,
                chunk_number=chunk_number,
                metadata=metadata
            ))
        
        return chunks

    def _clean_text(self, text: str) -> str:
        """Clean extracted text by removing artifacts and normalizing whitespace."""
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove header/footer artifacts (common in PDFs)
        text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)  # Page numbers
        
        # Normalize newlines
        text = text.replace('\r', '\n')
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()

    async def process_file(self, file_path: str, file_type: str) -> List[DocumentChunk]:
        """
        Process a file based on its type and return chunks.
        Currently supports PDF, can be extended for other formats.
        """
        if file_type.lower() == 'pdf':
            return self.process_pdf(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    @staticmethod
    async def save_upload_file(file) -> str:
        """
        Save an uploaded file to a temporary location and return the path.
        """
        # Create a temporary file with the original filename
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            return tmp.name 