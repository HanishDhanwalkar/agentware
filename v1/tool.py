from dataclasses import dataclass, field
from typing import Dict, List, Any, Callable, Optional, Union
import inspect



# ===================== TOOL REGISTRY =====================

@dataclass
class Tool:
    """Represents a tool that can be called by an agent"""
    name: str
    description: str
    function: Callable
    parameters: Dict[str, Any] = field(default_factory=dict)

class ToolRegistry:
    """Registry for all available tools"""
    
    def __init__(self):
        self.tools = {}
        
    def register_tool(self, tool: Tool) -> None:
        """Register a new tool"""
        self.tools[tool.name] = tool
        
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self.tools.get(name)
        
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all registered tools in a format suitable for LLM function calling"""
        tool_descriptions = []
        for name, tool in self.tools.items():
            # Extract parameter information from function signature
            sig = inspect.signature(tool.function)
            parameters = {
                "type": "object",
                "properties": {},
                "required": []
            }
            
            for param_name, param in sig.parameters.items():
                if param.default == inspect.Parameter.empty:
                    parameters["required"].append(param_name)
                
                # Simple type inference based on default values
                param_type = "string"  # Default type
                if param.default != inspect.Parameter.empty:
                    if isinstance(param.default, int):
                        param_type = "integer"
                    elif isinstance(param.default, float):
                        param_type = "number"
                    elif isinstance(param.default, bool):
                        param_type = "boolean"
                
                parameters["properties"][param_name] = {
                    "type": param_type,
                    "description": f"Parameter: {param_name}"
                }
            
            tool_descriptions.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool.description,
                    "parameters": parameters
                }
            })
        
        return tool_descriptions