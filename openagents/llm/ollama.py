"""
Ollama integration for OpenAgents framework.
"""
import json
import requests
from typing import Dict, List, Any, Optional
import logging

from ollama import chat

from openagents.llm.base import BaseLLM

logger = logging.getLogger(__name__)


class OllamaLLM(BaseLLM):
    """LLM client for Ollama"""
    
    def __init__(self, model: str, base_url: str = "http://localhost:11434", **kwargs):
        """Initialize the Ollama LLM client
        
        Args:
            model: Name of the Ollama model to use (e.g., "llama2", "mistral", "phi")
            base_url: Base URL for the Ollama API
            **kwargs: Additional parameters to pass to Ollama
        """
        super().__init__(model, **kwargs)
        self.base_url = base_url
        # self.chat_endpoint = f"{base_url}/api/chat"
        
    def generate_response(self, 
                         messages: List[Dict[str, Any]], 
                         stream: bool = False,
                         tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Generate a response using Ollama
        
        Args:
            messages: List of message objects with role and content
            tools: Optional list of tools to make available to the model
            
        Returns:
            Dictionary with the response content and any tool calls
        """
        # Prepare the API call
        data = {
            "model": self.model,
            "messages": self._format_messages(messages),
            "stream": stream,
            **self.kwargs
        }
        
        # Add tools if provided and the model supports it
        if tools:
            ollama_tools = self.get_tools_format(tools)
            data["tools"] = ollama_tools
        
        try:
            response = chat(
                data
            )

            # Process the response
            result = {
                "content": response.get("message", {}).get("content", ""),
                "tool_calls": None
            }
            
            # Extract tool calls if present
            if tools and "tool_calls" in response.get("message", {}):
                tool_calls = response["message"]["tool_calls"]
                result["tool_calls"] = []
                
                for tool_call in tool_calls:
                    result["tool_calls"].append({
                        "id": tool_call.get("id", ""),
                        "name": tool_call.get("name", ""),
                        "arguments": self._parse_tool_arguments(tool_call.get("arguments", "{}"))
                    })
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama API: {e}")
            return {"content": f"Error: {str(e)}", "tool_calls": None}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"content": f"Error: {str(e)}", "tool_calls": None}
    
    def get_tools_format(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tools to the format expected by Ollama
        
        Args:
            tools: List of tools in the standard OpenAgents format
            
        Returns:
            List of tools in the format expected by Ollama
        """
        # Ollama expects tools in a similar format to OpenAI
        # Some models may require specific formats based on their training
        return tools
    
    def _format_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Format messages for Ollama API
        
        Args:
            messages: Messages in OpenAgents format
            
        Returns:
            Messages formatted for Ollama API
        """
        formatted_messages = []
        
        for message in messages:
            # Only include messages with content
            if "content" in message and message["content"] is not None:
                formatted_message = {
                    "role": message["role"],
                    "content": message["content"]
                }
                formatted_messages.append(formatted_message)
        
        return formatted_messages
    
    def _parse_tool_arguments(self, arguments: str) -> Dict[str, Any]:
        """Parse tool arguments from string to dictionary
        
        Args:
            arguments: JSON string of arguments
            
        Returns:
            Dictionary of argument name-value pairs
        """
        try:
            return json.loads(arguments)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse tool arguments: {arguments}")
            return {}
