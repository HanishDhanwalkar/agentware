"""
LLM provider registry for OpenAgents framework.
"""
from typing import Dict, Type
from openagents.llm.base import BaseLLM
from openagents.llm.ollama_me import OllamaLLM


class LLMRegistry:
    """Registry for LLM providers"""
    
    # Dictionary of registered LLM provider classes
    _providers: Dict[str, Type[BaseLLM]] = {}
    
    @classmethod
    def register_provider(cls, name: str, provider_class: Type[BaseLLM]) -> None:
        """Register an LLM provider
        
        Args:
            name: Name of the provider
            provider_class: Class implementing the BaseLLM interface
        """
        cls._providers[name] = provider_class
    
    @classmethod
    def get_provider(cls, name: str) -> Type[BaseLLM]:
        """Get an LLM provider by name
        
        Args:
            name: Name of the provider
            
        Returns:
            The provider class
            
        Raises:
            KeyError: If the provider is not registered
        """
        if name not in cls._providers:
            raise KeyError(f"LLM provider '{name}' not registered")
        return cls._providers[name]
    
    @classmethod
    def list_providers(cls) -> Dict[str, Type[BaseLLM]]:
        """List all registered providers
        
        Returns:
            Dictionary of provider names and classes
        """
        return cls._providers


# Register the built-in providers
LLMRegistry.register_provider("ollama", OllamaLLM)
