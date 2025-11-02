"""Knowledge Base and Interpretation ORM Models"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, Text, Float, Integer, DateTime, Boolean, Index, ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base


class KnowledgeEntry(Base):
    """Knowledge Base entry with embeddings and metadata."""
    
    __tablename__ = "knowledge_entries"
    
    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    source = Column(String(255), nullable=False, index=True)  # Book/text name
    chunk_index = Column(Integer, nullable=False)  # Position in source
    
    # Embedding vector (stored as JSON for SQLite compatibility)
    embedding = Column(Text, nullable=True)  # JSON string of embedding
    embedding_model = Column(String(100), default="all-MiniLM-L6-v2")
    
    # Metadata
    category = Column(String(100), nullable=True, index=True)  # e.g., "birth_chart", "transit"
    keywords = Column(Text, nullable=True)  # Comma-separated keywords
    confidence_score = Column(Float, default=1.0)  # 0.0-1.0
    
    # Tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    interpretations = relationship(
        "Interpretation",
        back_populates="knowledge_source",
        foreign_keys="Interpretation.source_knowledge_id"
    )
    
    __table_args__ = (
        Index("ix_knowledge_source_chunk", "source", "chunk_index"),
        Index("ix_knowledge_category", "category"),
        Index("ix_knowledge_active", "is_active"),
    )
    
    def __repr__(self) -> str:
        return f"<KnowledgeEntry {self.id}: {self.title}>"


class InterpretationTemplate(Base):
    """Template for generating interpretations."""
    
    __tablename__ = "interpretation_templates"
    
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)  # e.g., "sun_sign", "house"
    
    # Template structure
    template_text = Column(Text, nullable=False)  # Jinja2 template
    required_data = Column(Text)  # JSON array of required fields
    optional_data = Column(Text)  # JSON array of optional fields
    
    # Configuration
    strategy = Column(String(50), default="template")  # "template", "knowledge", "llm", "hybrid"
    llm_enabled = Column(Boolean, default=False)
    knowledge_search_enabled = Column(Boolean, default=True)
    
    # Metadata
    description = Column(Text)
    example_output = Column(Text)
    
    # Tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    interpretations = relationship(
        "Interpretation",
        back_populates="template",
        foreign_keys="Interpretation.template_id"
    )
    
    __table_args__ = (
        Index("ix_template_category", "category"),
        Index("ix_template_active", "is_active"),
    )
    
    def __repr__(self) -> str:
        return f"<InterpretationTemplate {self.id}: {self.name}>"


class Interpretation(Base):
    """Generated interpretation for a birth chart or transit."""
    
    __tablename__ = "interpretations"
    
    id = Column(String(36), primary_key=True)
    chart_id = Column(String(36), ForeignKey("charts.id"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    
    # Interpretation details
    type = Column(String(100), nullable=False, index=True)  # e.g., "sun_sign", "transit"
    content = Column(Text, nullable=False)
    
    # Source information
    template_id = Column(String(36), ForeignKey("interpretation_templates.id"), nullable=True)
    source_knowledge_id = Column(String(36), ForeignKey("knowledge_entries.id"), nullable=True)
    
    # Scoring and confidence
    confidence_score = Column(Float, default=0.8)  # 0.0-1.0
    relevance_score = Column(Float, default=0.8)  # 0.0-1.0
    
    # Generation method
    generation_method = Column(String(50), default="template")  # "template", "knowledge", "llm", "hybrid"
    llm_model = Column(String(100), nullable=True)  # e.g., "gpt-4", "claude-3-opus"
    
    # Metadata
    interpretation_data = Column(Text, nullable=True)  # JSON with raw interpretation data
    context = Column(Text, nullable=True)  # JSON with context used
    
    # Tracking
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_verified = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)
    
    # Relationships
    template = relationship(
        "InterpretationTemplate",
        back_populates="interpretations",
        foreign_keys=[template_id]
    )
    knowledge_source = relationship(
        "KnowledgeEntry",
        back_populates="interpretations",
        foreign_keys=[source_knowledge_id]
    )
    
    __table_args__ = (
        Index("ix_interpretation_chart_type", "chart_id", "type"),
        Index("ix_interpretation_user_date", "user_id", "created_at"),
        Index("ix_interpretation_method", "generation_method"),
    )
    
    def __repr__(self) -> str:
        return f"<Interpretation {self.id}: {self.type}>"


class EmbeddingCache(Base):
    """Cache for embeddings to avoid regeneration."""
    
    __tablename__ = "embedding_cache"
    
    id = Column(String(36), primary_key=True)
    content_hash = Column(String(64), nullable=False, unique=True, index=True)
    
    # Embedding info
    embedding_model = Column(String(100), nullable=False)
    embedding = Column(Text, nullable=False)  # JSON string
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usage_count = Column(Integer, default=1)
    
    def __repr__(self) -> str:
        return f"<EmbeddingCache {self.id}>"


class SearchLog(Base):
    """Log for semantic search queries."""
    
    __tablename__ = "search_logs"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    
    # Search details
    query = Column(String(500), nullable=False)
    results_count = Column(Integer, default=0)
    execution_time_ms = Column(Float, nullable=False)
    
    # Result info
    top_result_id = Column(String(36), ForeignKey("knowledge_entries.id"), nullable=True)
    top_result_score = Column(Float, nullable=True)
    
    # Tracking
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    is_relevant = Column(Boolean, nullable=True)  # User feedback
    
    __table_args__ = (
        Index("ix_search_user_date", "user_id", "created_at"),
        Index("ix_search_performance", "execution_time_ms"),
    )
    
    def __repr__(self) -> str:
        return f"<SearchLog {self.id}>"
