"""
ELI5 Agent Implementation

This module implements an ELI5 (Explain Like I'm 5) agent using CrewAI.
It provides simple, easy-to-understand explanations for complex topics,
with built-in caching for improved performance.

Features:
    - Simple, clear explanations
    - Response caching
    - Configurable model and temperature
    - Metadata tracking
"""

import os
from typing import Tuple, Dict, Any
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from cache.prompt_cache import load_response, save_response, get_cache_stats
from datetime import datetime

# Load environment variables
load_dotenv()

class ELI5Agent:
    """
    ELI5 Agent for generating simple explanations.
    
    This agent uses CrewAI to generate explanations that are easy to understand,
    with built-in caching for improved performance and reduced API calls.
    
    Attributes:
        model (str): The language model to use
        temperature (float): Temperature for response generation
        cache_enabled (bool): Whether to use response caching
    """
    
    def __init__(self, model: str = None, temperature: float = 0.7, cache_enabled: bool = True):
        """
        Initialize the ELI5 agent.
        
        Args:
            model (str, optional): Language model to use. Defaults to environment variable.
            temperature (float, optional): Temperature for response generation. Defaults to 0.7.
            cache_enabled (bool, optional): Whether to use response caching. Defaults to True.
        """
        self.model = model or os.getenv("MODEL_NAME", "gpt-3.5-turbo")
        self.temperature = temperature
        self.cache_enabled = cache_enabled
        
        # Initialize the agent with CrewAI
        self.agent = Agent(
            role="ELI5 Tutor",
            goal="Explain complex topics in simple, easy-to-understand terms",
            backstory="""You are an expert at explaining complex topics in simple terms.
            You have a talent for breaking down difficult concepts into easy-to-understand explanations.""",
            verbose=True,
            allow_delegation=False,
            llm_model=self.model,
            temperature=self.temperature
        )

    def explain(self, topic: str) -> Tuple[str, Dict[str, Any]]:
        """
        Generate a simple explanation for a given topic.
        
        This method first checks the cache for a similar explanation. If none is found,
        it generates a new explanation using the ELI5 agent and caches the result.
        
        Args:
            topic (str): The topic to explain
            
        Returns:
            Tuple[str, Dict[str, Any]]: The explanation and metadata about the response
        """
        # Check cache first if enabled
        if self.cache_enabled:
            cached_response = load_response(topic)
            if cached_response:
                return cached_response["response"], cached_response["metadata"]
        
        # Create a task for the agent
        task = Task(
            description=f"""Explain the following topic in simple terms that a 5-year-old could understand:
            {topic}
            
            Make sure to:
            1. Use simple language
            2. Avoid technical terms
            3. Use analogies when helpful
            4. Keep it concise
            """,
            agent=self.agent
        )
        
        # Create and run the crew
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=True
        )
        
        # Get the response
        result = crew.kickoff()
        
        # Prepare metadata
        metadata = {
            "model": self.model,
            "temperature": self.temperature,
            "cached": False,
            "timestamp": datetime.now().isoformat()
        }
        
        # Cache the response if enabled
        if self.cache_enabled:
            save_response(topic, result, metadata)
        
        return result, metadata

    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get information about the cache.
        
        Returns:
            Dict[str, Any]: Dictionary containing cache statistics
        """
        return get_cache_stats()
