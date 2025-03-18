from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

try:
    from pgvector.sqlalchemy import Vector
except ImportError:
    # Use our stub implementation if pgvector is not available
    from .pgvector_stub import Vector

from .database import Base


class KnowledgeBaseSource(Base):
    __tablename__ = "knowledge_base_sources"
    
    source_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    source_type = Column(String(50))
    author = Column(String(255))
    publisher = Column(String(255))
    publication_date = Column(Date)
    license = Column(String(100))
    language = Column(String(50))
    url = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationship
    contents = relationship("KnowledgeBaseContent", back_populates="source")


class KnowledgeBaseContent(Base):
    __tablename__ = "knowledge_base_content"
    
    content_id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("knowledge_base_sources.source_id", ondelete="CASCADE"))
    parent_content_id = Column(Integer, ForeignKey("knowledge_base_content.content_id", ondelete="CASCADE"), nullable=True)
    title = Column(String(255))
    content = Column(Text)
    content_type = Column(String(50))
    embedding = Column(Vector(768))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    source = relationship("KnowledgeBaseSource", back_populates="contents")
    parent = relationship("KnowledgeBaseContent", remote_side=[content_id], backref="children")
    tags = relationship("Tag", secondary="content_tags", back_populates="contents")


class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    activities = relationship("UserActivityLog", back_populates="user")


class Tag(Base):
    __tablename__ = "tags"
    
    tag_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    
    # Relationships
    contents = relationship("KnowledgeBaseContent", secondary="content_tags", back_populates="tags")


class ContentTag(Base):
    __tablename__ = "content_tags"
    
    content_id = Column(Integer, ForeignKey("knowledge_base_content.content_id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.tag_id", ondelete="CASCADE"), primary_key=True)


class UserActivityLog(Base):
    __tablename__ = "user_activity_log"
    
    activity_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    content_id = Column(Integer, ForeignKey("knowledge_base_content.content_id", ondelete="SET NULL"), nullable=True)
    activity_type = Column(String(50))
    activity_timestamp = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="activities")
    content = relationship("KnowledgeBaseContent") 