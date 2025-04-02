from datetime import date
import pytest
from sqlalchemy.orm import Session

from app.services.source_intake import InformationSource, SourceIntakeService
from app.models import KnowledgeBaseSource, KnowledgeBaseContent

def test_information_source_to_db_models():
    # Create a sample information source
    source = InformationSource(
        name="The Science of Biology",
        source="OpenStax",
        source_description="A comprehensive biology textbook",
        source_type="textbook",
        author="Jane Doe",
        publisher="OpenStax",
        publication_date=date(2023, 1, 1),
        license="CC BY 4.0",
        language="en",
        url="https://assets.openstax.org/oscms-prodcms/media/documents/Biology2e-WEB_ICOFkGu.pdf",
        content_text="Introduction to Biology...",
        content_type="chapter"
    )
    
    # Convert to DB models
    db_source, db_contents = source.to_db_models()
    
    # Verify source model
    assert isinstance(db_source, KnowledgeBaseSource)
    assert db_source.name == "The Science of Biology"
    assert db_source.source_type == "textbook"
    assert db_source.author == "Jane Doe"
    
    # Verify content model
    assert len(db_contents) == 1
    assert isinstance(db_contents[0], KnowledgeBaseContent)
    assert db_contents[0].title == "The Science of Biology"
    assert db_contents[0].content == "Introduction to Biology..."

def test_information_source_with_sections():
    # Create a source with sections
    source = InformationSource(
        name="Chapter 1: Cell Biology",
        source="OpenStax",
        source_description="First chapter of biology textbook",
        source_type="textbook",
        author="Jane Doe",
        publisher="OpenStax",
        publication_date=date(2023, 1, 1),
        license="CC BY 4.0",
        language="en",
        url="https://openstax.org/biology/ch1",
        content_text="Overview of cell biology...",
        content_type="chapter",
        sections=[
            InformationSource(
                name="1.1 Cell Structure",
                source="OpenStax",
                source_description="Section on cell structure",
                source_type="textbook",
                author="Jane Doe",
                publisher="OpenStax",
                publication_date=date(2023, 1, 1),
                license="CC BY 4.0",
                language="en",
                url="https://openstax.org/biology/ch1/sec1",
                content_text="The cell structure consists of...",
                content_type="section"
            )
        ]
    )
    
    # Convert to DB models
    db_source, db_contents = source.to_db_models()
    
    # Verify source and contents
    assert isinstance(db_source, KnowledgeBaseSource)
    assert len(db_contents) == 2  # Main content + 1 section
    assert db_contents[0].title == "Chapter 1: Cell Biology"
    assert db_contents[1].title == "1.1 Cell Structure" 