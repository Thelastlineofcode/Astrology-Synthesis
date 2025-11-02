"""
Embedding Service using Sentence Transformers
Provides embeddings for knowledge base texts
"""

import os
import numpy as np
from typing import List, Union
import logging

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Warning: sentence-transformers not installed. Install with: pip install sentence-transformers")
    SentenceTransformer = None

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for generating text embeddings using Sentence Transformers
    
    Model: all-MiniLM-L6-v2
    - 384-dimensional embeddings
    - Fast and lightweight
    - Good for semantic search
    """
    
    MODEL_NAME = "all-MiniLM-L6-v2"
    EMBEDDING_DIM = 384
    
    def __init__(self, model_name: str = MODEL_NAME):
        """
        Initialize Embedding Service
        
        Args:
            model_name: Model name from Hugging Face (default: all-MiniLM-L6-v2)
        """
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers not installed")
        
        try:
            self.model = SentenceTransformer(model_name)
            self.model_name = model_name
            logger.info(f"Embedding service initialized with model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {str(e)}")
            raise
    
    def encode(
        self,
        texts: Union[str, List[str]],
        batch_size: int = 32,
        show_progress_bar: bool = False,
    ) -> np.ndarray:
        """
        Encode text(s) to embeddings
        
        Args:
            texts: Single text string or list of texts
            batch_size: Batch size for encoding
            show_progress_bar: Whether to show progress bar
            
        Returns:
            Numpy array of embeddings (shape: (n_samples, 384))
        """
        if isinstance(texts, str):
            texts = [texts]
        
        try:
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=show_progress_bar,
                convert_to_numpy=True,
            )
            logger.info(f"Encoded {len(texts)} text(s) to embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"Error encoding texts: {str(e)}")
            raise
    
    def encode_single(self, text: str) -> np.ndarray:
        """
        Encode single text to embedding
        
        Args:
            text: Text to encode
            
        Returns:
            1D numpy array of shape (384,)
        """
        embedding = self.encode(text)
        return embedding[0]
    
    def similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (-1 to 1, typically 0 to 1 for text)
        """
        embeddings = self.encode([text1, text2])
        embedding1 = embeddings[0]
        embedding2 = embeddings[1]
        
        # Cosine similarity
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        similarity = dot_product / (norm1 * norm2) if (norm1 * norm2) > 0 else 0
        return float(similarity)
    
    def batch_similarity(
        self,
        query: str,
        candidates: List[str],
    ) -> List[float]:
        """
        Calculate similarity between query and multiple candidates
        
        Args:
            query: Query text
            candidates: List of candidate texts
            
        Returns:
            List of similarity scores
        """
        all_texts = [query] + candidates
        embeddings = self.encode(all_texts)
        
        query_embedding = embeddings[0]
        candidate_embeddings = embeddings[1:]
        
        similarities = []
        for candidate_embedding in candidate_embeddings:
            dot_product = np.dot(query_embedding, candidate_embedding)
            norm_q = np.linalg.norm(query_embedding)
            norm_c = np.linalg.norm(candidate_embedding)
            
            similarity = dot_product / (norm_q * norm_c) if (norm_q * norm_c) > 0 else 0
            similarities.append(float(similarity))
        
        return similarities
    
    def normalize(self, embeddings: np.ndarray) -> np.ndarray:
        """
        L2 normalize embeddings
        
        Args:
            embeddings: Array of embeddings
            
        Returns:
            Normalized embeddings
        """
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        normalized = embeddings / (norms + 1e-10)  # Add small epsilon to avoid division by zero
        return normalized
    
    def get_info(self) -> dict:
        """Get service information"""
        return {
            "model": self.model_name,
            "embedding_dimension": self.EMBEDDING_DIM,
            "framework": "sentence-transformers",
        }


# Factory function
def create_embedding_service() -> EmbeddingService:
    """Create embedding service from environment variables"""
    model_name = os.getenv("EMBEDDING_MODEL", EmbeddingService.MODEL_NAME)
    return EmbeddingService(model_name=model_name)
