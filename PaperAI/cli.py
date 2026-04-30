"""
CLI Interface for PaperAI
Commandline interface for testing without GUI
"""

import argparse
import logging
from pathlib import Path

import config
from core.pdf_processor import PDFProcessor, TextChunker
from core.embeddings import EmbeddingGenerator
from core.vector_db import VectorDatabase
from core.rag_pipeline import RAGPipeline
from utils import setup_logging, save_results

# Setup logging
setup_logging(logging.INFO)
logger = logging.getLogger(__name__)


class PaperAICLI:
    """Command-line interface for PaperAI"""

    def __init__(self):
        """Initialize CLI"""
        self.pdf_processor = PDFProcessor()
        self.text_chunker = TextChunker(
            chunk_size=config.MAX_CHUNK_SIZE,
            overlap=config.CHUNK_OVERLAP
        )
        self.embedding_gen = EmbeddingGenerator(config.EMBEDDING_MODEL)
        self.vector_db = VectorDatabase(config.EMBEDDING_DIMENSION, str(config.VECTOR_DB_PATH))
        self.rag_pipeline = RAGPipeline(config.GROQ_API_KEY)
        
        # Try to load existing database
        try:
            self.vector_db.load(str(config.VECTOR_DB_PATH))
            logger.info(f"Loaded vector database with {self.vector_db.get_size()} vectors")
        except:
            logger.info("Creating new vector database")

    def process_pdf(self, pdf_path: str):
        """Process a PDF file"""
        logger.info(f"Processing PDF: {pdf_path}")
        
        # Validate PDF
        is_valid, message = self.pdf_processor.validate_pdf(pdf_path)
        if not is_valid:
            logger.error(f"Invalid PDF: {message}")
            return
        
        # Extract text
        text, metadata = self.pdf_processor.extract_text(pdf_path)
        logger.info(f"Extracted {metadata['pages']} pages, {metadata['total_chars']} characters")
        
        # Chunk text
        chunks = self.text_chunker.chunk_text(text, metadata)
        logger.info(f"Created {len(chunks)} chunks")
        
        # Generate embeddings
        chunks = self.embedding_gen.embed_chunks(chunks)
        
        # Add to vector DB
        embeddings = [chunk["embedding"] for chunk in chunks]
        chunk_metadata = [{"text": chunk["text"], "source": metadata.get("file_name")} 
                         for chunk in chunks]
        self.vector_db.add_vectors(embeddings, chunk_metadata)
        
        # Save database
        self.vector_db.save(str(config.VECTOR_DB_PATH))
        logger.info("Vector database updated and saved")

    def ask_question(self, question: str):
        """Ask a question about the paper"""
        logger.info(f"Question: {question}")
        
        if self.vector_db.get_size() == 0:
            logger.error("No documents loaded. Please process a PDF first.")
            return
        
        # Generate question embedding
        question_embedding = self.embedding_gen.embed_text(question)
        
        # Search vector DB
        results, distances = self.vector_db.search(
            question_embedding[0], k=config.TOP_K_RESULTS
        )
        
        relevant_chunks = [result["text"] for result in results]
        logger.info(f"Found {len(relevant_chunks)} relevant chunks")
        
        # Generate answer
        answer = self.rag_pipeline.generate_answer(question, relevant_chunks)
        
        print("\n" + "=" * 70)
        print("ANSWER:")
        print("=" * 70)
        print(answer)
        print("=" * 70 + "\n")
        
        return answer

    def summarize_paper(self):
        """Generate paper summary"""
        logger.info("Generating paper summary")
        
        if self.vector_db.get_size() == 0:
            logger.error("No documents loaded. Please process a PDF first.")
            return
        
        all_texts = [meta["text"] for meta in self.vector_db.metadata]
        summary = self.rag_pipeline.summarize_paper(all_texts)
        
        print("\n" + "=" * 70)
        print("PAPER SUMMARY:")
        print("=" * 70)
        print(summary)
        print("=" * 70 + "\n")
        
        return summary

    def explain_concept(self, concept: str):
        """Explain a concept"""
        logger.info(f"Explaining concept: {concept}")
        
        if self.vector_db.get_size() == 0:
            logger.error("No documents loaded. Please process a PDF first.")
            return
        
        # Generate concept embedding
        concept_embedding = self.embedding_gen.embed_text(concept)
        
        # Search vector DB
        results, distances = self.vector_db.search(
            concept_embedding[0], k=config.TOP_K_RESULTS
        )
        
        relevant_chunks = [result["text"] for result in results]
        logger.info(f"Found {len(relevant_chunks)} relevant chunks")
        
        # Generate explanation
        explanation = self.rag_pipeline.explain_concept(concept, relevant_chunks)
        
        print("\n" + "=" * 70)
        print(f"EXPLANATION: {concept}")
        print("=" * 70)
        print(explanation)
        print("=" * 70 + "\n")
        
        return explanation


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Research Paper Assistant - RAG Based Paper Explainer"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Process command
    process_parser = subparsers.add_parser("process", help="Process a PDF file")
    process_parser.add_argument("pdf", help="Path to PDF file")
    
    # Ask command
    ask_parser = subparsers.add_parser("ask", help="Ask a question")
    ask_parser.add_argument("question", help="Question to ask")
    
    # Summarize command
    summarize_parser = subparsers.add_parser("summarize", help="Summarize the paper")
    
    # Explain command
    explain_parser = subparsers.add_parser("explain", help="Explain a concept")
    explain_parser.add_argument("concept", help="Concept to explain")
    
    # Interactive command
    interactive_parser = subparsers.add_parser("interactive", help="Interactive mode")
    interactive_parser.add_argument("--pdf", help="Optional PDF to load first")
    
    args = parser.parse_args()
    
    cli = PaperAICLI()
    
    if args.command == "process":
        cli.process_pdf(args.pdf)
    
    elif args.command == "ask":
        cli.ask_question(args.question)
    
    elif args.command == "summarize":
        cli.summarize_paper()
    
    elif args.command == "explain":
        cli.explain_concept(args.concept)
    
    elif args.command == "interactive":
        if args.pdf:
            cli.process_pdf(args.pdf)
        
        print("\n" + "=" * 70)
        print("Research Paper Assistant - Interactive Mode")
        print("=" * 70)
        print("Commands:")
        print("  process <path> - Process a PDF")
        print("  ask <question> - Ask a question")
        print("  summarize - Summarize the paper")
        print("  explain <concept> - Explain a concept")
        print("  exit - Exit interactive mode")
        print("=" * 70 + "\n")
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == "exit":
                    print("Exiting...")
                    break
                
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                args_str = parts[1] if len(parts) > 1 else ""
                
                if command == "process":
                    cli.process_pdf(args_str)
                elif command == "ask":
                    cli.ask_question(args_str)
                elif command == "summarize":
                    cli.summarize_paper()
                elif command == "explain":
                    cli.explain_concept(args_str)
                else:
                    print(f"Unknown command: {command}")
            
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                logger.error(f"Error: {str(e)}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
