"""
Base tool interface for OpenAgents framework.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Callable, Optional, List
import inspect


@dataclass
class Tool:
    """Represents a tool that can be called by an agent"""
    name: str
    description: str
    function: Callable
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def execute(self, **kwargs) -> Any:
        """Execute the tool with the given arguments
        
        Args:
            **kwargs: Arguments to pass to the tool function
            
        Returns:
            Result of the tool execution
        """
        return self.function(**kwargs)
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the JSON schema for this tool
        
        Returns:
            Tool schema in JSON format suitable for LLM function calling
        """
        # Extract parameter information from function signature
        sig = inspect.signature(self.function)
        parameters = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for param_name, param in sig.parameters.items():
            if param.default == inspect.Parameter.empty:
                parameters["required"].append(param_name)
            
            # Get type annotation if available
            param_type = "string"  # Default type
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"
                elif param.annotation == list or param.annotation == List:
                    param_type = "array"
            
            # If no type annotation, infer from default value
            elif param.default != inspect.Parameter.empty:
                if isinstance(param.default, int):
                    param_type = "integer"
                elif isinstance(param.default, float):
                    param_type = "number"
                elif isinstance(param.default, bool):
                    param_type = "boolean"
                elif isinstance(param.default, list):
                    param_type = "array"
            
            # Add parameter description from docstring if available
            param_desc = f"Parameter: {param_name}"
            if self.function.__doc__:
                doclines = self.function.__doc__.split('\n')
                for line in doclines:
                    if f"{param_name}:" in line:
                        param_desc = line.split(f"{param_name}:")[1].strip()
                        break
            
            parameters["properties"][param_name] = {
                "type": param_type,
                "description": param_desc
            }
        
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": parameters
            }
        }


class BaseToolProvider(ABC):
    """Base class for tool providers"""
    
    @abstractmethod
    def get_tools(self) -> List[Tool]:
        """Get all tools provided by this provider
        
        Returns:
            List of tools
        """
        pass
