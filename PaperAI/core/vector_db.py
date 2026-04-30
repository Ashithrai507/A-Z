"""
Vector Database Module
Manages vector storage and similarity search using FAISS
"""

import faiss
import numpy as np
import pickle
from pathlib import Path
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class VectorDatabase:
    """FAISS-based vector database for storing and searching embeddings"""

    def __init__(self, dimension: int, db_path: str = None):
        """
        Initialize vector database
        
        Args:
            dimension: Dimension of embeddings
            db_path: Path to save/load database
        """
        self.dimension = dimension
        self.db_path = Path(db_path) if db_path else None
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance
        self.metadata = []  # Store metadata for each vector
        
        logger.info(f"Initialized FAISS index with dimension: {dimension}")

    def add_vectors(self, embeddings: np.ndarray, metadata: List[dict] = None):
        """
        Add vectors to database
        
        Args:
            embeddings: Numpy array of embeddings (shape: [n, dimension])
            metadata: List of metadata dictionaries corresponding to embeddings
        """
        if len(embeddings) == 0:
            logger.warning("No embeddings to add")
            return
        
        # Ensure embeddings are float32
        embeddings = np.asarray(embeddings, dtype=np.float32)
        
        self.index.add(embeddings)
        
        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{} for _ in range(len(embeddings))])
        
        logger.info(f"Added {len(embeddings)} vectors. Total: {self.index.ntotal}")

    def search(self, query_embedding: np.ndarray, k: int = 5) -> Tuple[List[dict], List[float]]:
        """
        Search for nearest neighbors
        
        Args:
            query_embedding: Query embedding vector
            k: Number of nearest neighbors to return
            
        Returns:
            Tuple of (list of metadata dicts, list of distances)
        """
        query_embedding = np.asarray(query_embedding, dtype=np.float32).reshape(1, -1)
        
        distances, indices = self.index.search(query_embedding, min(k, self.index.ntotal))
        
        results = []
        distances_list = []
        
        for i, idx in enumerate(indices[0]):
            if idx >= 0:  # Valid result
                results.append(self.metadata[idx])
                distances_list.append(float(distances[0][i]))
        
        logger.debug(f"Search returned {len(results)} results")
        return results, distances_list

    def save(self, save_path: str = None):
        """
        Save database to disk
        
        Args:
            save_path: Path to save database
        """
        save_path = Path(save_path or self.db_path)
        if not save_path:
            raise ValueError("No save path specified")
        
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, str(save_path / "index.faiss"))
        
        # Save metadata
        with open(save_path / "metadata.pkl", "wb") as f:
            pickle.dump(self.metadata, f)
        
        logger.info(f"Database saved to {save_path}")

    def load(self, load_path: str = None):
        """
        Load database from disk
        
        Args:
            load_path: Path to load database from
        """
        load_path = Path(load_path or self.db_path)
        if not load_path:
            raise ValueError("No load path specified")
        
        if not load_path.exists():
            raise FileNotFoundError(f"Database path not found: {load_path}")
        
        # Load FAISS index
        self.index = faiss.read_index(str(load_path / "index.faiss"))
        
        # Load metadata
        with open(load_path / "metadata.pkl", "rb") as f:
            self.metadata = pickle.load(f)
        
        logger.info(f"Database loaded from {load_path}")

    def get_size(self) -> int:
        """Get number of vectors in database"""
        return self.index.ntotal

    def reset(self):
        """Clear all data from database"""
        self.index.reset()
        self.metadata = []
        logger.info("Database reset")
