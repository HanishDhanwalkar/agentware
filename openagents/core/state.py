"""
Core state management for OpenAgents framework.
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class AgentState:
    """Represents the state of an agent"""
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    memory: Dict[str, Any] = field(default_factory=dict)
    tool_results: Dict[str, Any] = field(default_factory=dict)
    
    def add_message(self, role: str, content: Optional[str], tool_call=None) -> None:
        """Add a message to the conversation history"""
        message = {"role": role}
        
        if content is not None:
            message["content"] = content
            
        if tool_call is not None:
            message["tool_call"] = tool_call
            
        self.conversation_history.append(message)
    
    def get_last_message(self) -> Optional[Dict[str, Any]]:
        """Get the last message in the conversation history"""
        if self.conversation_history:
            return self.conversation_history[-1]
        return None
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """Get all messages in conversation history"""
        return self.conversation_history
    
    def store_memory(self, key: str, value: Any) -> None:
        """Store a value in memory"""
        self.memory[key] = value
    
    def get_memory(self, key: str, default=None) -> Any:
        """Get a value from memory"""
        return self.memory.get(key, default)
    
    def store_tool_result(self, tool_name: str, result: Any) -> None:
        """Store the result of a tool execution"""
        self.tool_results[tool_name] = result
    
    def get_tool_result(self, tool_name: str, default=None) -> Any:
        """Get the result of a tool execution"""
        return self.tool_results.get(tool_name, default)
