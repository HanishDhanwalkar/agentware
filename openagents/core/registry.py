"""
Core registry interfaces for OpenAgents framework.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, TypeVar

T = TypeVar('T')


class BaseRegistry(ABC, Generic=T):
    """Base registry interface for OpenAgents"""
    
    @abstractmethod
    def register(self, name: str, item: T) -> None:
        """Register an item with the registry
        
        Args:
            name: Name of the item
            item: Item to register
        """
        pass
    
    @abstractmethod
    def get(self, name: str) -> Optional[T]:
        """Get an item by name
        
        Args:
            name: Name of the item
            
        Returns:
            The item, or None if not found
        """
        pass
    
    @abstractmethod
    def list(self) -> Dict[str, T]:
        """List all registered items
        
        Returns:
            Dictionary of items
        """
        pass


class AgentRegistry(BaseRegistry):
    """Registry for agent instances"""
    
    def __init__(self):
        """Initialize the agent registry"""
        self.agents: Dict[str, Any] = {}
    
    def register(self, name: str, agent: Any) -> None:
        """Register an agent
        
        Args:
            name: Name of the agent
            agent: Agent instance
        """
        self.agents[name] = agent
    
    def get(self, name: str) -> Optional[Any]:
        """Get an agent by name
        
        Args:
            name: Name of the agent
            
        Returns:
            The agent, or None if not found
        """
        return self.agents.get(name)
    
    def list(self) -> Dict[str, Any]:
        """List all registered agents
        
        Returns:
            Dictionary of agents
        """
        return self.agents
