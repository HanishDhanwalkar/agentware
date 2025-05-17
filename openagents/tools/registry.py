"""
Tool registry for OpenAgents framework.
"""
from typing import Dict, List, Any, Type, Optional
import logging

from openagents.tools.base import BaseToolProvider, Tool

logger = logging.getLogger(__name__)


class ToolRegistry:
    """Registry for tools that can be used by agents"""
    
    def __init__(self):
        """Initialize the tool registry"""
        self.tools: Dict[str, Tool] = {}
        self.providers: List[BaseToolProvider] = []
    
    def register_tool(self, tool: Tool) -> None:
        """Register a single tool
        
        Args:
            tool: Tool to register
        """
        if tool.name in self.tools:
            logger.warning(f"Tool with name '{tool.name}' already registered. Overwriting.")
        
        self.tools[tool.name] = tool
        logger.debug(f"Registered tool: {tool.name}")
    
    def register_provider(self, provider: BaseToolProvider) -> None:
        """Register a tool provider and all its tools
        
        Args:
            provider: Tool provider to register
        """
        self.providers.append(provider)
        
        # Register all tools from this provider
        for tool in provider.get_tools():
            self.register_tool(tool)
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name
        
        Args:
            name: Name of the tool
            
        Returns:
            The tool, or None if not found
        """
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all registered tools in a format suitable for LLM function calling
        
        Returns:
            List of tool schemas
        """
        return [tool.get_schema() for tool in self.tools.values()]
    
    def get_tool_names(self) -> List[str]:
        """Get a list of all registered tool names
        
        Returns:
            List of tool names
        """
        return list(self.tools.keys())
