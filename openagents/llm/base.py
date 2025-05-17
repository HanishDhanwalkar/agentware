"""
Base LLM client interface for OpenAgents framework.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseLLM(ABC):
    """Base abstract class for LLM providers"""
    
    @abstractmethod
    def __init__(self, model: str, **kwargs):
        """Initialize the LLM provider"""
        self.model = model
        self.kwargs = kwargs
    
    @abstractmethod
    def generate_response(self, 
                         messages: List[Dict[str, Any]], 
                         tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Generate a response from the LLM
        
        Args:
            messages: List of message objects with role and content
            tools: Optional list of tools in a format understood by the model
            
        Returns:
            Dictionary containing the response with content and possibly tool calls
        """
        pass
    
    @abstractmethod
    def get_tools_format(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tools to the format expected by the LLM provider
        
        Args:
            tools: List of tools in the standard OpenAgents format
            
        Returns:
            List of tools in the format expected by the LLM provider
        """
        pass
