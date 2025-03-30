from dataclasses import dataclass
from typing import Optional, List
from datetime import date
from sqlalchemy.orm import Session

from ..models import KnowledgeBaseSource, KnowledgeBaseContent

@dataclass
class InformationSource:
    name: str
    source: str
    source_description: Optional[str]
    source_type: str  # e.g., 'textbook', 'course_material', 'research_paper'
    author: Optional[str]
    publisher: Optional[str]
    publication_date: Optional[date]
    license: Optional[str]
    language: str
    url: str
    content_text: str
    content_type: str  # e.g., 'chapter', 'section', 'article'
    sections: Optional[List['InformationSource']] = None

    def to_db_models(self) -> tuple[KnowledgeBaseSource, List[KnowledgeBaseContent]]:
        """
        Convert the InformationSource to database models.
        Returns a tuple of (source_model, list of content_models)
        """
        source = KnowledgeBaseSource(
            name=self.name,
            description=self.source_description,
            source_type=self.source_type,
            author=self.author,
            publisher=self.publisher,
            publication_date=self.publication_date,
            license=self.license,
            language=self.language,
            url=self.url
        )
        
        contents = []
        # Create main content
        main_content = KnowledgeBaseContent(
            title=self.name,
            content=self.content_text,
            content_type=self.content_type
        )
        contents.append(main_content)
        
        # Process nested sections if they exist
        if self.sections:
            for section in self.sections:
                section_content = KnowledgeBaseContent(
                    title=section.name,
                    content=section.content_text,
                    content_type=section.content_type
                )
                contents.append(section_content)
        
        return source, contents

class SourceIntakeService:
    def __init__(self, db: Session):
        self.db = db
    
    def process_source(self, source: InformationSource) -> KnowledgeBaseSource:
        """
        Process an information source and save it to the database.
        Returns the created KnowledgeBaseSource instance.
        """
        # Convert to DB models
        source_model, content_models = source.to_db_models()
        
        # Save source
        self.db.add(source_model)
        self.db.flush()  # Get the source_id
        
        # Link and save contents
        for content in content_models:
            content.source_id = source_model.source_id
            self.db.add(content)
        
        self.db.commit()
        return source_model 