import pytest
from pathlib import Path
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from fastapi.testclient import TestClient
from io import BytesIO

from app.services.document_processor import DocumentProcessor
from app.main import app

def create_test_pdf():
    """Create a test PDF with some content."""
    # Create a temporary PDF file
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
        # Create PDF
        c = canvas.Canvas(tmp_pdf.name, pagesize=letter)
        
        # Add some text to first page
        c.drawString(100, 750, "Chapter 1: Introduction to Biology")
        c.drawString(100, 700, "This is a test document about biology.")
        c.drawString(100, 650, "It contains multiple paragraphs of text.")
        
        # Add second page
        c.showPage()
        c.drawString(100, 750, "Chapter 2: Cell Structure")
        c.drawString(100, 700, "Cells are the basic unit of life.")
        
        # Save the PDF
        c.save()
        
        return tmp_pdf.name

@pytest.fixture
def pdf_file():
    """Fixture to create and cleanup a test PDF file."""
    file_path = create_test_pdf()
    yield file_path
    # Cleanup
    Path(file_path).unlink()

def test_document_processor_pdf(pdf_file):
    """Test that the document processor can handle PDFs."""
    processor = DocumentProcessor()
    chunks = processor.process_pdf(pdf_file)
    
    assert len(chunks) > 0
    assert any("Introduction to Biology" in chunk.content for chunk in chunks)
    assert any("Cell Structure" in chunk.content for chunk in chunks)
    
    # Test chunk properties
    first_chunk = chunks[0]
    assert first_chunk.page_number == 1
    assert first_chunk.chunk_number == 0
    assert isinstance(first_chunk.metadata, dict)

@pytest.mark.asyncio
async def test_upload_endpoint():
    """Test the PDF upload endpoint."""
    client = TestClient(app)
    
    # Create a test PDF in memory
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    c.drawString(100, 750, "Test PDF Content")
    c.save()
    pdf_buffer.seek(0)
    
    # Create test file to upload
    files = {
        "file": ("test.pdf", pdf_buffer, "application/pdf")
    }
    
    # Test upload
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert data["chunks_processed"] > 0
    assert "source_id" in data

def test_invalid_file_upload():
    """Test uploading an invalid file type."""
    client = TestClient(app)
    
    # Create a text file instead of PDF
    files = {
        "file": ("test.txt", b"This is not a PDF", "text/plain")
    }
    
    response = client.post("/upload", files=files)
    assert response.status_code == 400
    assert "Only PDF files are currently supported" in response.json()["detail"] 