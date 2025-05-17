"""
Core agent implementation for OpenAgents framework.

This module provides the main Agent class that coordinates LLM interactions,
tool execution, and conversation management.
"""
import logging
from typing import Dict, List, Any, Optional, Union

from openagents.core.state import AgentState
from openagents.llm.base import BaseLLM
from openagents.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)


class Agent:
    """Agent class with tool-calling capabilities"""
    
    def __init__(self, 
                name: str, 
                system_prompt: str, 
                llm: BaseLLM, 
                tool_registry: ToolRegistry,
                verbose: bool = False):
        """Initialize the agent
        
        Args:
            name: Name of the agent
            system_prompt: System prompt to initialize the agent
            llm: LLM client
            tool_registry: Registry of tools available to the agent
            verbose: Whether to enable verbose logging
        """
        self.name = name
        self.system_prompt = system_prompt
        self.llm = llm
        self.tool_registry = tool_registry
        self.verbose = verbose
        self.state = AgentState()
                
        # Initialize conversation with system prompt
        self.state.add_message("system", system_prompt, None)
        
        # Set up logging
        if verbose:
            logging.basicConfig(level=logging.DEBUG)
    
    def add_message(self, role: str, content: str, tool_call=None) -> None:
        """Add a message to the conversation history
        
        Args:
            role: Role of the message sender (system, user, assistant, tool)
            content: Content of the message
            tool_call: Optional tool call information
        """
        self.state.add_message(role, content, tool_call)
        
        if self.verbose:
            if type(content) == str:
                logger.debug(f"Added message: {role} - {content[:50]}...")
            else:
                logger.debug(f"'content' is not a string. Added message: {role} - {content}")
                
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool by name with the given arguments
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            
        Returns:
            Result of the tool execution
        """
        tool = self.tool_registry.get_tool(tool_name)
        if not tool:
            error_msg = f"Error: Tool '{tool_name}' not found"
            logger.error(error_msg)
            return error_msg
        
        try:
            if self.verbose:
                logger.debug(f"Executing tool: {tool_name} with args: {arguments}")
                
            result = tool.execute(**arguments)
            
            # Store the result in the agent's state
            self.state.store_tool_result(tool_name, result)
            
            if self.verbose:
                logger.debug(f"Tool result: {str(result)[:100]}...")
                
            return result
        except Exception as e:
            error_msg = f"Error executing tool '{tool_name}': {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate a response
        
        Args:
            user_input: User input message
            
        Returns:
            Agent's response
        """
        # Add user message to conversation
        self.add_message("user", user_input, None)
        
        # Get response from LLM with tools
        tools = self.tool_registry.list_tools()
        
        if self.verbose:
            logger.debug(f"Sending request to LLM with {len(tools)} tools")
        
        response = self.llm.generate_response(
            self.state.get_messages(),
            tools=tools
        )
        
        # Process tool calls if present
        if response.get("tool_calls"):
            if self.verbose:
                logger.debug(f"LLM requested tool calls: {len(response['tool_calls'])}")
            
            for tool_call in response["tool_calls"]:
                tool_name = tool_call["name"]
                arguments = tool_call["arguments"]
                
                # Add the tool call to the conversation
                self.add_message("assistant", None, tool_call)
                
                # Execute the tool
                result = self.execute_tool(tool_name, arguments)
                
                # Add the tool result to the conversation
                self.add_message("tool", str(result), None)
            
            # Get final response from LLM after tool execution
            if self.verbose:
                logger.debug("Getting final response after tool execution")
                
            final_response = self.llm.generate_response(
                self.state.get_messages()
            )
            
            # Add assistant's final response to conversation
            self.add_message("assistant", final_response["content"], None)
            return final_response["content"]
        else:
            # No tool calls, just add the response to conversation
            if self.verbose:
                logger.debug("No tool calls requested, returning direct response")
                
            self.add_message("assistant", response["content"], None)
            return response["content"]
