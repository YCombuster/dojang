"""
A stub implementation of pgvector.sqlalchemy module.
This allows the code to import without having the actual pgvector package installed.
For development purposes only.
"""

from sqlalchemy.types import TypeDecorator

class Vector(TypeDecorator):
    """Stub implementation of pgvector.sqlalchemy.Vector."""
    
    impl = str  # Using string as the implementation type
    
    def __init__(self, dimensions, *args, **kwargs):
        self.dimensions = dimensions
        super().__init__(*args, **kwargs) 