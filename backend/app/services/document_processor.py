import fitz  # PyMuPDF
from marker import extract_from_file
import openai
import asyncio
import asyncpg
import os

# class DocumentChunk:
#     def __init__(
#         self,
#         content: str,
#         page_number: int,
#         chunk_number: int,
#         metadata: Optional[Dict] = None
#     ):
#         self.content = content
#         self.page_number = page_number
#         self.chunk_number = chunk_number
#         self.metadata = metadata or {}

# class DocumentProcessor:
#     def __init__(self):
#         # Configure chunking parameters
#         self.min_chunk_size = 200  # minimum characters per chunk
#         self.max_chunk_size = 1000  # maximum characters per chunk
#         self.overlap = 50  # number of characters to overlap between chunks

    # MAIN FUNCTION

    # def process_pdf(self, file_path: str) -> List[DocumentChunk]:
    #     """
    #     Process a PDF file and return a list of document chunks.
    #     """

    #     chunks = []
    #     return

    # def _extract_pdf_metadata(self, pdf_reader: PyPDF2.PdfReader) -> Dict:
    #     """Extract metadata from PDF document."""

    #     return 


    def _split_into_chunks(
        self, 
        text: str, 
        page_number: int,
        metadata: Dict
    ) -> List[DocumentChunk]:
        """
        Split text into chunks while trying to preserve semantic meaning.
        """
        
        return 

    # def _clean_text(self, text: str) -> str:
    #     """Clean extracted text by removing artifacts and normalizing whitespace."""
    #     # Remove multiple spaces
    #     text = re.sub(r'\s+', ' ', text)
        
    #     # Remove header/footer artifacts (common in PDFs)
    #     text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)  # Page numbers
        
    #     # Normalize newlines
    #     text = text.replace('\r', '\n')
    #     text = re.sub(r'\n{3,}', '\n\n', text)
        
    #     return text.strip()

    # This one runs, to choose the corresponding type function i.e., PDF
    async def process_file(self, file_path: str, file_type: str) -> List[DocumentChunk]:
        """
        Process a file based on its type and return chunks.
        Currently supports PDF, can be extended for other formats.
        """
        if file_type.lower() == 'pdf':
            return self.process_pdf(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    # @staticmethod
    # async def save_upload_file(file) -> str:
    #     """
    #     Save an uploaded file to a temporary location and return the path.
    #     """
    #     # Create a temporary file with the original filename
    #     suffix = Path(file.filename).suffix
    #     with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
    #         content = await file.read()
    #         tmp.write(content)
    #         return tmp.name 