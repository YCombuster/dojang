from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from pydantic import BaseModel

from ..database import get_db
from ..services.source_intake import InformationSource, SourceIntakeService

router = APIRouter(
    prefix="/sources",
    tags=["sources"]
)

class SourceCreate(BaseModel):
    name: str
    source: str
    source_description: Optional[str] = None
    source_type: str
    author: Optional[str] = None
    publisher: Optional[str] = None
    publication_date: Optional[date] = None
    license: Optional[str] = None
    language: str
    url: str
    content_text: str
    content_type: str

    class Config:
        from_attributes = True

@router.post("/", status_code=201)
def create_source(
    source_data: SourceCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new information source with its content.
    """
    try:
        # Convert Pydantic model to InformationSource
        source = InformationSource(
            **source_data.model_dump()
        )
        
        # Process the source
        service = SourceIntakeService(db)
        result = service.process_source(source)
        
        return {"message": "Source created successfully", "source_id": result.source_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 