"""
RAG (Retrieval Augmented Generation) Module
Handles retrieval of relevant documents and LLM responses
"""

from groq import Groq
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class RAGPipeline:
    """Main RAG pipeline for paper understanding"""

    def __init__(self, groq_api_key: str, model: str = "llama-3.1-8b-instant"):
        """
        Initialize RAG pipeline
        
        Args:
            groq_api_key: API key for Groq
            model: Model name to use
        """
        self.client = Groq(api_key=groq_api_key)
        self.model = model
        
        self.system_prompt = """You are an expert research paper assistant. Your role is to help users understand complex research papers.

When answering questions:
1. Ground your answers in the provided paper content
2. Break down complex concepts into simple language
3. Cite relevant sections from the paper
4. Be accurate and avoid speculation
5. Suggest related concepts when applicable

If the information needed to answer the question is not in the provided content, clearly state that."""
        
        logger.info(f"Initialized RAG pipeline with model: {model}")

    def generate_answer(self, question: str, relevant_chunks: List[str], 
                       temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """
        Generate answer using LLM with retrieved context
        
        Args:
            question: User's question
            relevant_chunks: List of relevant text chunks
            temperature: LLM temperature setting
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated answer string
        """
        # Prepare context
        context = "\n\n".join([f"[Chunk {i+1}]\n{chunk}" 
                              for i, chunk in enumerate(relevant_chunks)])
        
        user_message = f"""Based on the following paper content, please answer this question:

Question: {question}

Paper Content:
{context}

Answer:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            answer = response.choices[0].message.content
            logger.info(f"Generated answer ({len(answer)} chars)")
            return answer
            
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise

    def summarize_paper(self, paper_chunks: List[str], max_tokens: int = 2048) -> str:
        """
        Generate summary of entire paper
        
        Args:
            paper_chunks: List of all paper chunks
            max_tokens: Maximum tokens in summary
            
        Returns:
            Paper summary
        """
        # Keep context within a safe request size for smaller models/TPM limits.
        # Rough heuristic: 1 token ~ 4 characters; keep ~12k chars for context.
        max_context_chars = 12000
        context_sections = []
        current_chars = 0

        for i, chunk in enumerate(paper_chunks):
            section_text = f"[Section {i+1}]\n{chunk}"
            if current_chars + len(section_text) > max_context_chars:
                break
            context_sections.append(section_text)
            current_chars += len(section_text)

        context = "\n\n".join(context_sections)
        
        user_message = f"""Please provide a comprehensive summary of this research paper. Include:
1. Main objective and research question
2. Key methodology
3. Major findings/contributions
4. Implications and future work

Paper Content:
{context}

Summary:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.5,
                max_tokens=max_tokens,
            )
            
            summary = response.choices[0].message.content
            logger.info(f"Generated summary ({len(summary)} chars)")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            raise

    def explain_concept(self, concept: str, relevant_chunks: List[str]) -> str:
        """
        Explain a difficult concept in simple language
        
        Args:
            concept: The concept to explain
            relevant_chunks: Relevant paper chunks
            
        Returns:
            Simplified explanation
        """
        context = "\n\n".join([f"[Reference {i+1}]\n{chunk}" 
                              for i, chunk in enumerate(relevant_chunks)])
        
        user_message = f"""Please explain the following concept in simple, beginner-friendly language.

Concept: {concept}

Reference Material:
{context}

Explanation:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful educator who explains complex concepts in simple, understandable language."},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.6,
                max_tokens=1024,
            )
            
            explanation = response.choices[0].message.content
            logger.info(f"Generated explanation ({len(explanation)} chars)")
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            raise
