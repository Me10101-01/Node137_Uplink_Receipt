"""
OpenAI API adapter (optional dependency).

Only used if client wants to evaluate OpenAI models.
Requires: pip install openai
"""

from typing import Dict, List, Any, Optional
from document_refinery.models.adapter import ModelAdapter, ModelResponse


class OpenAIAdapter(ModelAdapter):
    """
    Adapter for OpenAI API models.
    
    This is a placeholder that can be activated with the openai dependency.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize OpenAI adapter.
        
        Args:
            config: Configuration including api_key, model name, etc.
        """
        super().__init__(config)
        self.api_key = config.get("api_key")
        
        # Only import if being used
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "OpenAI support requires: pip install openai\n"
                "Or install with: pip install strategickhaos-document-refinery[openai]"
            )
    
    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs,
    ) -> ModelResponse:
        """
        Generate text using OpenAI API.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional OpenAI parameters
            
        Returns:
            ModelResponse with generated text
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs,
        )
        
        return ModelResponse(
            text=response.choices[0].message.content,
            metadata={
                "finish_reason": response.choices[0].finish_reason,
                "model": response.model,
            },
            model_name=self.model_name,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
        )
    
    def batch_generate(
        self,
        prompts: List[str],
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs,
    ) -> List[ModelResponse]:
        """
        Generate text for multiple prompts.
        
        Args:
            prompts: List of input prompts
            max_tokens: Maximum tokens per generation
            temperature: Sampling temperature
            **kwargs: Additional parameters
            
        Returns:
            List of ModelResponse objects
        """
        return [
            self.generate(prompt, max_tokens, temperature, **kwargs)
            for prompt in prompts
        ]
