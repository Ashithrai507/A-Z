"""
Configuration management for PaperAI
Load settings from .env file and provide defaults
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root
PROJECT_ROOT = Path(__file__).parent

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Paths
DATA_DIR = PROJECT_ROOT / "data"
UPLOAD_DIR = DATA_DIR / os.getenv("PDF_UPLOAD_DIR", "uploads")
VECTOR_DB_PATH = DATA_DIR / os.getenv("VECTOR_DB_PATH", "vector_store")

# Create directories if they don't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)

# LLM Configuration
# Available models: llama-3.1-8b-instant, mixtral-8x7b-32768, gemma-7b-it
LLM_MODEL = "llama-3.1-8b-instant"  # Groq model (current supported default)
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 2048

# Embeddings Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # sentence-transformers model
EMBEDDING_DIMENSION = 384

# Chunking Configuration
MAX_CHUNK_SIZE = int(os.getenv("MAX_CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))

# Application Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
MAX_PDF_SIZE_MB = 50  # Maximum PDF file size in MB

# Vector DB Configuration
SIMILARITY_THRESHOLD = 0.5
TOP_K_RESULTS = 5  # Number of relevant chunks to retrieve

# RAG Configuration
SYSTEM_PROMPT = """You are an expert research paper assistant. You help users understand complex research papers.
Your role is to:
1. Provide clear, accurate explanations based on the paper content
2. Break down complex concepts into simple language
3. Answer questions with relevant citations from the paper
4. Suggest related concepts when applicable

Always ground your answers in the provided paper content."""
