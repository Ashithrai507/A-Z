"""
Utility functions and helpers
"""

import logging
from typing import List, Dict
import json
from pathlib import Path


def setup_logging(log_level=logging.INFO, log_file: str = None):
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file path to save logs
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    handlers = [
        logging.StreamHandler()  # Console output
    ]
    
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=handlers
    )


def save_results(results: Dict, output_file: str):
    """
    Save results to JSON file
    
    Args:
        results: Dictionary of results
        output_file: Path to save JSON
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    logging.info(f"Results saved to {output_file}")


def format_answer(answer: str, max_length: int = None) -> str:
    """
    Format answer text
    
    Args:
        answer: Raw answer text
        max_length: Maximum length (None for no limit)
        
    Returns:
        Formatted answer
    """
    # Clean up whitespace
    answer = "\n".join(line.strip() for line in answer.split("\n"))
    
    if max_length and len(answer) > max_length:
        answer = answer[:max_length] + "..."
    
    return answer


def merge_metadata(*metadata_dicts: Dict) -> Dict:
    """
    Merge multiple metadata dictionaries
    
    Args:
        *metadata_dicts: Variable number of metadata dictionaries
        
    Returns:
        Merged metadata dictionary
    """
    merged = {}
    for meta in metadata_dicts:
        merged.update(meta)
    return merged
