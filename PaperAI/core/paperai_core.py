"""
Core processing and pipeline threading for PaperAI.
Separates non-UI logic from the Qt interface.
"""

import logging

from PyQt5.QtCore import QThread, pyqtSignal

import config
from core.pdf_processor import PDFProcessor, TextChunker
from core.embeddings import EmbeddingGenerator
from core.vector_db import VectorDatabase
from core.rag_pipeline import RAGPipeline

logger = logging.getLogger(__name__)


def create_app_context():
    """Create and preload the core application context."""
    app_context = {
        "vector_db": VectorDatabase(config.EMBEDDING_DIMENSION, str(config.VECTOR_DB_PATH)),
        "embedding_gen": EmbeddingGenerator(config.EMBEDDING_MODEL),
        "rag_pipeline": RAGPipeline(config.GROQ_API_KEY, model=config.LLM_MODEL),
        "current_pdf": None,
    }
    try:
        app_context["vector_db"].load(str(config.VECTOR_DB_PATH))
    except Exception:
        pass

    return app_context


class ProcessingThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, pdf_path: str, app_context):
        super().__init__()
        self.pdf_path = pdf_path
        self.app_context = app_context

    def run(self):
        try:
            self.progress.emit("Validating PDF…")
            processor = PDFProcessor()
            is_valid, message = processor.validate_pdf(self.pdf_path)
            if not is_valid:
                self.finished.emit(False, f"Invalid PDF: {message}")
                return

            self.progress.emit("Extracting text from PDF…")
            text, metadata = processor.extract_text(self.pdf_path)

            self.progress.emit("Chunking text…")
            chunker = TextChunker(chunk_size=config.MAX_CHUNK_SIZE, overlap=config.CHUNK_OVERLAP)
            chunks = chunker.chunk_text(text, metadata)

            self.progress.emit("Generating embeddings…")
            embedding_gen = EmbeddingGenerator(config.EMBEDDING_MODEL)
            chunks = embedding_gen.embed_chunks(chunks)

            self.progress.emit("Storing in vector database…")
            embeddings = [chunk["embedding"] for chunk in chunks]
            chunk_texts = [chunk["text"] for chunk in chunks]
            chunk_metadata = [{"text": t, "source": metadata.get("file_name")} for t in chunk_texts]
            self.app_context["vector_db"].add_vectors(embeddings, chunk_metadata)
            self.app_context["vector_db"].save(str(config.VECTOR_DB_PATH))

            pages = metadata.get("pages", 0)
            self.progress.emit(f"Done! Processed {pages} pages.")
            self.finished.emit(True, f"✅ PDF processed!\n📄 Pages: {pages}\n🧩 Chunks: {len(chunks)}")

        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            self.finished.emit(False, f"Error: {e}")


class QueryThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, query: str, mode: str, app_context):
        super().__init__()
        self.query = query
        self.mode = mode  # "qa" | "concept" | "summarize"
        self.app_context = app_context

    def run(self):
        try:
            ctx = self.app_context
            if self.mode == "summarize":
                all_texts = [m["text"] for m in ctx["vector_db"].metadata]
                result = ctx["rag_pipeline"].summarize_paper(all_texts)
            else:
                emb = ctx["embedding_gen"].embed_text(self.query)
                results, _ = ctx["vector_db"].search(emb[0], k=config.TOP_K_RESULTS)
                chunks = [r["text"] for r in results]
                if self.mode == "concept":
                    result = ctx["rag_pipeline"].explain_concept(self.query, chunks)
                else:
                    result = ctx["rag_pipeline"].generate_answer(self.query, chunks)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
