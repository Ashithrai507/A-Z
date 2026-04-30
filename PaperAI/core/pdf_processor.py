"""
PDF Processing Module
Handles PDF extraction, chunking, and text preprocessing
"""

import pymupdf  # PyMuPDF
from pathlib import Path
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Handles PDF file processing and text extraction"""

    def __init__(self, max_size_mb: int = 50):
        """
        Initialize PDF processor
        
        Args:
            max_size_mb: Maximum PDF file size in MB
        """
        self.max_size_bytes = max_size_mb * 1024 * 1024

    def validate_pdf(self, file_path: str) -> Tuple[bool, str]:
        """
        Validate PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Tuple of (is_valid, message)
        """
        path = Path(file_path)
        
        # Check if file exists
        if not path.exists():
            return False, "File does not exist"
        
        # Check file extension
        if path.suffix.lower() != ".pdf":
            return False, "File is not a PDF"
        
        # Check file size
        file_size = path.stat().st_size
        if file_size > self.max_size_bytes:
            return False, f"File size exceeds {self.max_size_bytes / 1024 / 1024:.0f}MB limit"
        
        # Try to open PDF
        try:
            with pymupdf.open(file_path) as doc:
                if len(doc) == 0:
                    return False, "PDF has no pages"
            return True, "Valid PDF"
        except Exception as e:
            return False, f"Error opening PDF: {str(e)}"

    def extract_text(self, file_path: str) -> Tuple[str, dict]:
        """
        Extract text from PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Tuple of (extracted_text, metadata)
        """
        metadata = {
            "file_name": Path(file_path).name,
            "pages": 0,
            "total_chars": 0
        }
        
        try:
            full_text = ""
            with pymupdf.open(file_path) as doc:
                metadata["pages"] = len(doc)
                
                for page_num, page in enumerate(doc):
                    text = page.get_text()
                    full_text += f"\n--- Page {page_num + 1} ---\n{text}"
                
                metadata["total_chars"] = len(full_text)
                
                # Try to extract metadata
                if doc.metadata:
                    metadata.update({
                        "title": doc.metadata.get("title", ""),
                        "author": doc.metadata.get("author", ""),
                    })
            
            logger.info(f"Extracted {metadata['pages']} pages from {metadata['file_name']}")
            return full_text, metadata
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise


class TextChunker:
    """Handles text chunking for embedding"""

    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        """
        Initialize text chunker
        
        Args:
            chunk_size: Size of each chunk in characters
            overlap: Overlap between consecutive chunks in characters
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, metadata: dict = None) -> List[dict]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to chunk
            metadata: Additional metadata to attach to chunks
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        chunks = []
        step = self.chunk_size - self.overlap
        
        for i in range(0, len(text), step):
            chunk_text = text[i : i + self.chunk_size]
            
            chunk_data = {
                "text": chunk_text.strip(),
                "start_char": i,
                "end_char": min(i + self.chunk_size, len(text)),
                "metadata": metadata or {}
            }
            
            chunks.append(chunk_data)
        
        logger.info(f"Created {len(chunks)} chunks from text")
        return chunks

    def chunk_by_sentences(self, text: str, max_chunk_size: int = None, 
                          metadata: dict = None) -> List[dict]:
        """
        Split text into chunks preserving sentence boundaries
        (More advanced approach)
        
        Args:
            text: Text to chunk
            max_chunk_size: Maximum size per chunk
            metadata: Additional metadata
            
        Returns:
            List of chunk dictionaries
        """
        if max_chunk_size is None:
            max_chunk_size = self.chunk_size
        
        sentences = text.replace(".", ".\n").replace("!", "!\n").replace("?", "?\n").split("\n")
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_chunk_size:
                current_chunk += " " + sentence
            else:
                if current_chunk.strip():
                    chunks.append({
                        "text": current_chunk.strip(),
                        "metadata": metadata or {}
                    })
                current_chunk = sentence
        
        if current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                "metadata": metadata or {}
            })
        
        logger.info(f"Created {len(chunks)} sentence-based chunks")
        return chunks
