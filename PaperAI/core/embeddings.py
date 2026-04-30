"""
Embeddings Module
Handles vector embedding generation using sentence-transformers
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
import logging

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """Generates embeddings for text using sentence-transformers"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding generator
        
        Args:
            model_name: Name of sentence-transformers model to use
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        
        logger.info(f"Loaded embedding model: {model_name} (dimension: {self.embedding_dim})")

    def embed_text(self, text: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for text
        
        Args:
            text: Single text string or list of strings
            
        Returns:
            Numpy array of embeddings (shape: [n, embedding_dim])
        """
        if isinstance(text, str):
            text = [text]
        
        embeddings = self.model.encode(text, convert_to_numpy=True)
        
        logger.debug(f"Generated embeddings for {len(text)} text(s)")
        return embeddings

    def embed_chunks(self, chunks: List[dict]) -> List[dict]:
        """
        Generate embeddings for list of text chunks
        
        Args:
            chunks: List of chunk dictionaries with 'text' key
            
        Returns:
            List of chunks with added 'embedding' key
        """
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embed_text(texts)
        
        # Add embeddings to chunks
        for i, chunk in enumerate(chunks):
            chunk["embedding"] = embeddings[i]
        
        logger.info(f"Generated embeddings for {len(chunks)} chunks")
        return chunks

    def get_embedding_dimension(self) -> int:
        """Get dimension of embeddings"""
        return self.embedding_dim
