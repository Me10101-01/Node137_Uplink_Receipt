"""
Base model adapter interface.

Provides pluggable backend support for:
- Local models (Qwen, LLaMA, etc.)
- External APIs (OpenAI, Anthropic, etc.)
- Client's own models

Zero vendor lock-in principle.
"""

from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ModelResponse:
    """Standardized response from any model backend."""
    text: str
    metadata: Dict[str, Any]
    model_name: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ModelAdapter(ABC):
    """
    Abstract base class for model adapters.
    
    All model backends must implement this interface to ensure
    consistent evaluation across different systems.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize model adapter with configuration.
        
        Args:
            config: Model-specific configuration
        """
        self.config = config
        self.model_name = config.get("model_name", "unknown")
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs,
    ) -> ModelResponse:
        """
        Generate text from the model.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional model-specific parameters
            
        Returns:
            ModelResponse with generated text and metadata
        """
        pass
    
    @abstractmethod
    def batch_generate(
        self,
        prompts: List[str],
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs,
    ) -> List[ModelResponse]:
        """
        Generate text for multiple prompts (batch processing).
        
        Args:
            prompts: List of input prompts
            max_tokens: Maximum tokens per generation
            temperature: Sampling temperature
            **kwargs: Additional model-specific parameters
            
        Returns:
            List of ModelResponse objects
        """
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the model.
        
        Returns:
            Dictionary with model metadata
        """
        return {
            "name": self.model_name,
            "config": self.config,
        }
