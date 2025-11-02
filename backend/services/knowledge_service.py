"""Knowledge Base Service - Text extraction, chunking, embedding, and semantic search."""

import os
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import logging

import numpy as np

logger = logging.getLogger(__name__)


class TextChunk:
    """Represents a chunk of text from a knowledge source."""
    def __init__(self, content, source_file, category, chunk_index, confidence_score=1.0):
        self.content = content
        self.source_file = source_file
        self.category = category
        self.chunk_index = chunk_index
        self.confidence_score = confidence_score
    
    @property
    def content_hash(self):
        """Generate SHA256 hash of content for caching."""
        return hashlib.sha256(self.content.encode()).hexdigest()


class KnowledgeService:
    """Service for knowledge base operations."""
    
    # Category weights for search scoring
    CATEGORY_WEIGHTS = {
        "01_voodoo_spiritual_apex": 1.5,
        "02_vedic_core": 1.3,
        "03_vedic_advanced": 1.3,
        "04_dasha_timing": 1.2,
        "15_ayurveda_medicine": 1.2,
    }
    
    def __init__(self, kb_path="knowledge_base", chunk_size=512):
        """Initialize Knowledge Service."""
        self.kb_path = Path(kb_path)
        self.texts_path = self.kb_path / "texts"
        self.embeddings_path = self.kb_path / "embeddings"
        self.chunk_size = chunk_size
        self.embeddings_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Initialized KnowledgeService with path: {self.kb_path}")
    
    def get_category_weight(self, category: str) -> float:
        """Get weight multiplier for a category."""
        return self.CATEGORY_WEIGHTS.get(category, 1.0)
    
    def get_category_info(self, category: str) -> Dict:
        """Get metadata about a category."""
        return {
            'name': category,
            'weight': self.get_category_weight(category),
            'is_primary': category in [
                "01_voodoo_spiritual_apex",
                "02_vedic_core",
                "03_vedic_advanced",
                "04_dasha_timing"
            ],
        }
    
    def list_categories(self) -> List[Dict]:
        """List all knowledge base categories."""
        categories = []
        if self.texts_path.exists():
            for cat_dir in sorted(self.texts_path.glob("[0-9][0-9]_*")):
                if cat_dir.is_dir():
                    book_count = len(list(cat_dir.glob("*")))
                    categories.append({
                        'name': cat_dir.name,
                        'book_count': book_count,
                        'weight': self.get_category_weight(cat_dir.name),
                        'path': str(cat_dir),
                    })
        return categories
    
    def search_local(self, query: str, category: Optional[str] = None, limit: int = 5) -> List[Dict]:
        """Local keyword search in KB (placeholder for semantic search)."""
        results = []
        query_lower = query.lower()
        
        if self.texts_path.exists():
            search_dirs = [self.texts_path / category] if category else self.texts_path.glob("[0-9][0-9]_*")
            
            for cat_dir in search_dirs:
                if not cat_dir.is_dir():
                    continue
                
                for file_path in cat_dir.glob("*"):
                    if file_path.is_file() and query_lower in file_path.name.lower():
                        results.append({
                            'file': file_path.name,
                            'category': cat_dir.name,
                            'path': str(file_path),
                            'relevance': 0.8,
                        })
        
        return results[:limit]


def create_knowledge_service(kb_path: str = "knowledge_base") -> KnowledgeService:
    """Factory function to create Knowledge Service."""
    return KnowledgeService(kb_path=kb_path)
