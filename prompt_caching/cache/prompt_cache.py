"""
Prompt Caching System

This module implements a sophisticated caching system for AI responses with semantic search capabilities.
It uses sentence transformers for computing embeddings and supports both exact and semantic matching
of prompts for efficient response retrieval.

Features:
    - JSON-based storage
    - Semantic similarity search
    - Metadata tracking
    - Cache statistics
    - Automatic cache management
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer

# Configuration
CACHE_DIR = "./cache/data"
SIMILARITY_THRESHOLD = 0.85  # Threshold for semantic matching
os.makedirs(CACHE_DIR, exist_ok=True)

# Initialize the sentence transformer model for semantic search
model = SentenceTransformer('all-MiniLM-L6-v2')

def _hash_key(prompt: str) -> str:
    """
    Generate a hash key for the prompt.
    
    Args:
        prompt (str): The input prompt text
        
    Returns:
        str: MD5 hash of the normalized prompt
    """
    return hashlib.md5(prompt.strip().lower().encode()).hexdigest()

def _compute_embedding(text: str) -> np.ndarray:
    """
    Compute embedding for the given text using sentence transformer.
    
    Args:
        text (str): Input text to compute embedding for
        
    Returns:
        np.ndarray: Text embedding vector
    """
    return model.encode(text)

def _compute_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """
    Compute cosine similarity between two embeddings.
    
    Args:
        embedding1 (np.ndarray): First embedding vector
        embedding2 (np.ndarray): Second embedding vector
        
    Returns:
        float: Cosine similarity score between 0 and 1
    """
    return float(np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2)))

def load_response(prompt: str, use_semantic_search: bool = True) -> Optional[Dict[str, Any]]:
    """
    Load response from cache, optionally using semantic search.
    
    This function first tries an exact match using the prompt hash. If that fails
    and semantic search is enabled, it looks for similar prompts using embedding
    similarity.
    
    Args:
        prompt (str): The input prompt
        use_semantic_search (bool): Whether to use semantic search for finding similar prompts
        
    Returns:
        Optional[Dict[str, Any]]: Dictionary containing response and metadata if found, None otherwise
    """
    # First try exact match
    key = _hash_key(prompt)
    path = os.path.join(CACHE_DIR, f"{key}.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)

    if not use_semantic_search:
        return None

    # Try semantic search
    prompt_embedding = _compute_embedding(prompt)
    best_match = None
    best_similarity = 0

    for filename in os.listdir(CACHE_DIR):
        if not filename.endswith('.json'):
            continue
            
        with open(os.path.join(CACHE_DIR, filename)) as f:
            cached_data = json.load(f)
            cached_embedding = _compute_embedding(cached_data['prompt'])
            similarity = _compute_similarity(prompt_embedding, cached_embedding)
            
            if similarity > best_similarity and similarity >= SIMILARITY_THRESHOLD:
                best_similarity = similarity
                best_match = cached_data

    return best_match

def save_response(prompt: str, response: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    """
    Save response to cache with metadata.
    
    Args:
        prompt (str): The input prompt
        response (str): The response to cache
        metadata (Optional[Dict[str, Any]]): Optional metadata about the response
    """
    key = _hash_key(prompt)
    cache_data = {
        "prompt": prompt,
        "response": response,
        "embedding": _compute_embedding(prompt).tolist(),
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata or {}
    }
    
    with open(os.path.join(CACHE_DIR, f"{key}.json"), "w") as f:
        print(f"🔁 Saving response to cache: {prompt[:50]}...")
        json.dump(cache_data, f)

def clear_cache() -> None:
    """
    Clear all cached responses.
    
    This function removes all JSON files from the cache directory,
    effectively resetting the cache to its initial state.
    """
    for filename in os.listdir(CACHE_DIR):
        if filename.endswith('.json'):
            os.remove(os.path.join(CACHE_DIR, filename))

def get_cache_stats() -> Dict[str, Any]:
    """
    Get statistics about the cache.
    
    Returns a dictionary containing:
    - total_entries: Number of cached responses
    - total_size_bytes: Total size of cache in bytes
    - oldest_entry: Timestamp of oldest cached response
    - newest_entry: Timestamp of newest cached response
    
    Returns:
        Dict[str, Any]: Dictionary containing cache statistics
    """
    stats = {
        "total_entries": 0,
        "total_size_bytes": 0,
        "oldest_entry": None,
        "newest_entry": None
    }
    
    for filename in os.listdir(CACHE_DIR):
        if not filename.endswith('.json'):
            continue
            
        path = os.path.join(CACHE_DIR, filename)
        stats["total_entries"] += 1
        stats["total_size_bytes"] += os.path.getsize(path)
        
        try:
            with open(path) as f:
                data = json.load(f)
                # Handle missing timestamp field
                if "timestamp" in data:
                    timestamp = datetime.fromisoformat(data["timestamp"])
                    
                    if stats["oldest_entry"] is None or timestamp < datetime.fromisoformat(stats["oldest_entry"]):
                        stats["oldest_entry"] = data["timestamp"]
                    if stats["newest_entry"] is None or timestamp > datetime.fromisoformat(stats["newest_entry"]):
                        stats["newest_entry"] = data["timestamp"]
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Warning: Error processing cache file {filename}: {e}")
            continue
    
    return stats
