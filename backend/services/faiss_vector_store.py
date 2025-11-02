"""
FAISS Vector Store Service
Provides semantic search over knowledge base texts
"""

import os
import numpy as np
import pickle
from typing import List, Dict, Any, Optional, Tuple
import logging

try:
    import faiss
except ImportError:
    print("Warning: faiss-cpu not installed. Install with: pip install faiss-cpu")
    faiss = None

from backend.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class FAISSVectorStore:
    """
    Vector store using FAISS for semantic search
    
    Features:
    - IndexFlatL2 for exact search
    - Metadata tracking
    - Category weighting
    - Persistence
    """
    
    # Category weights (for relevance boosting)
    CATEGORY_WEIGHTS = {
        "01_voodoo_spiritual_apex": 1.5,      # Highest priority
        "02_vedic_core": 1.3,                 # High priority
        "03_vedic_advanced": 1.3,
        "04_dasha_timing": 1.2,
        "05_transit_timing": 1.1,
        "06_vedic_mythology": 1.1,
        "07_numerology": 1.1,
        "08_tarot": 1.1,
        "09_christian_astrology": 1.0,
        "10_islamic_astrology": 1.0,
        "11_crystal_healing": 1.0,
        "12_energy_work": 1.0,
        "13_chakras": 1.0,
        "14_meditation": 1.0,
        "15_ayurveda_medicine": 1.2,
        "16_herbalism": 1.0,
        "17_lunar_cycles": 1.1,
        "18_planetary_hours": 1.1,
        "19_misc": 1.0,
    }
    
    def __init__(
        self,
        embedding_service: Optional[EmbeddingService] = None,
        index_path: Optional[str] = None,
    ):
        """
        Initialize FAISS Vector Store
        
        Args:
            embedding_service: EmbeddingService instance (will create if not provided)
            index_path: Path to save/load index files
        """
        if faiss is None:
            raise ImportError("faiss-cpu not installed")
        
        self.embedding_service = embedding_service or EmbeddingService()
        self.index_path = index_path or os.getenv("FAISS_INDEX_PATH", "./vector_store")
        
        # Create index directory if needed
        os.makedirs(self.index_path, exist_ok=True)
        
        # Initialize index and metadata
        self.index = None
        self.metadata = []
        self.text_count = 0
        self.dimension = self.embedding_service.EMBEDDING_DIM
        
        logger.info(f"FAISSVectorStore initialized (dimension={self.dimension})")
    
    def add_texts(
        self,
        texts: List[str],
        metadata_list: List[Dict[str, Any]],
        batch_size: int = 32,
    ) -> None:
        """
        Add texts to vector store
        
        Args:
            texts: List of text strings
            metadata_list: List of metadata dicts (must have 'category' and 'source')
            batch_size: Batch size for embedding
        """
        if len(texts) != len(metadata_list):
            raise ValueError("texts and metadata_list must have same length")
        
        # Encode texts to embeddings
        embeddings = self.embedding_service.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
        )
        
        # Initialize or extend index
        if self.index is None:
            self.index = faiss.IndexFlatL2(self.dimension)
        
        # Convert to float32 (FAISS requirement)
        embeddings = embeddings.astype(np.float32)
        
        # Add to index
        self.index.add(embeddings)
        self.metadata.extend(metadata_list)
        self.text_count += len(texts)
        
        logger.info(f"Added {len(texts)} texts to index (total: {self.text_count})")
    
    def search(
        self,
        query: str,
        k: int = 5,
        category_filter: Optional[str] = None,
        threshold: float = 0.0,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar texts
        
        Args:
            query: Query text
            k: Number of results to return
            category_filter: Filter by category
            threshold: Minimum similarity threshold (0-1, inverted for L2)
            
        Returns:
            List of search results with text, score, and metadata
        """
        if self.index is None or self.text_count == 0:
            logger.warning("Index is empty")
            return []
        
        try:
            # Encode query
            query_embedding = self.embedding_service.encode_single(query)
            query_embedding = query_embedding.astype(np.float32).reshape(1, -1)
            
            # Search index (k + buffer for filtering)
            search_k = min(k * 3, self.text_count)
            distances, indices = self.index.search(query_embedding, search_k)
            
            results = []
            
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx < 0:  # Invalid index
                    continue
                
                metadata = self.metadata[idx]
                category = metadata.get("category", "misc")
                
                # Apply category filter
                if category_filter and category != category_filter:
                    continue
                
                # Convert L2 distance to similarity (lower distance = higher similarity)
                # L2 distance ranges from 0 to inf, similarity should be 0 to 1
                similarity = 1.0 / (1.0 + distance)
                
                if similarity < threshold:
                    continue
                
                # Apply category weight
                weight = self.CATEGORY_WEIGHTS.get(category, 1.0)
                weighted_similarity = similarity * weight
                
                results.append({
                    "text": metadata.get("source", f"unknown_{idx}"),
                    "similarity": float(similarity),
                    "weighted_similarity": float(weighted_similarity),
                    "distance": float(distance),
                    "category": category,
                    "weight": weight,
                    "index": int(idx),
                })
                
                if len(results) >= k:
                    break
            
            # Sort by weighted similarity
            results.sort(key=lambda x: x["weighted_similarity"], reverse=True)
            
            logger.info(f"Search returned {len(results)} results")
            return results[:k]
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []
    
    def save(self) -> bool:
        """
        Save index and metadata to disk
        
        Returns:
            Success status
        """
        if self.index is None:
            logger.warning("No index to save")
            return False
        
        try:
            index_file = os.path.join(self.index_path, "faiss.index")
            metadata_file = os.path.join(self.index_path, "metadata.pkl")
            
            faiss.write_index(self.index, index_file)
            
            with open(metadata_file, "wb") as f:
                pickle.dump(self.metadata, f)
            
            logger.info(f"Saved index and metadata to {self.index_path}")
            return True
            
        except Exception as e:
            logger.error(f"Save error: {str(e)}")
            return False
    
    def load(self) -> bool:
        """
        Load index and metadata from disk
        
        Returns:
            Success status
        """
        try:
            index_file = os.path.join(self.index_path, "faiss.index")
            metadata_file = os.path.join(self.index_path, "metadata.pkl")
            
            if not os.path.exists(index_file) or not os.path.exists(metadata_file):
                logger.warning("Index files not found")
                return False
            
            self.index = faiss.read_index(index_file)
            
            with open(metadata_file, "rb") as f:
                self.metadata = pickle.load(f)
            
            self.text_count = len(self.metadata)
            logger.info(f"Loaded index with {self.text_count} texts")
            return True
            
        except Exception as e:
            logger.error(f"Load error: {str(e)}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        return {
            "text_count": self.text_count,
            "dimension": self.dimension,
            "index_type": "IndexFlatL2",
            "category_count": len(set(m.get("category") for m in self.metadata)),
            "index_size_mb": self.index.total_memory_allocated() / (1024 * 1024) if self.index else 0,
        }


# Factory function
def create_faiss_vector_store(embedding_service: Optional[EmbeddingService] = None) -> FAISSVectorStore:
    """Create FAISS vector store from environment variables"""
    index_path = os.getenv("FAISS_INDEX_PATH", "./vector_store")
    return FAISSVectorStore(embedding_service=embedding_service, index_path=index_path)
