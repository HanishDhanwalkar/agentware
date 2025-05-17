"""
SimpleAgents: A minimal AI agents framework with tool calling capabilities
"""
import json
import os
import inspect
from typing import Dict, List, Any, Callable, Optional, Union
from dataclasses import dataclass, field

# Configure your LLM API key
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"  # Replace with your actual API key

# You can also use environment variables:
# import os
# os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")


# ===================== LLM CLIENT =====================

# ===================== AGENT =====================

@dataclass
class AgentState:
    """Represents the state of an agent"""
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    memory: Dict[str, Any] = field(default_factory=dict)
    tool_results: Dict[str, Any] = field(default_factory=dict)

class Agent:
    """Base agent class with tool-calling capabilities"""
    
    def __init__(self, name: str, system_prompt: str, llm_client: LLMClient, tool_registry: ToolRegistry):
        self.name = name
        self.system_prompt = system_prompt
        self.llm_client = llm_client
        self.tool_registry = tool_registry
        self.state = AgentState()
        
        # Initialize conversation with system prompt
        self.state.conversation_history.append({
            "role": "system",
            "content": system_prompt
        })
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history"""
        self.state.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool by name with the given arguments"""
        tool = self.tool_registry.get_tool(tool_name)
        if not tool:
            return f"Error: Tool '{tool_name}' not found"
        
        try:
            result = tool.function(**arguments)
            # Store the result in the agent's state
            self.state.tool_results[tool_name] = result
            return result
        except Exception as e:
            return f"Error executing tool '{tool_name}': {str(e)}"
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate a response"""
        # Add user message to conversation
        self.add_message("user", user_input)
        
        # Get response from LLM with tools
        tools = self.tool_registry.list_tools()
        response = self.llm_client.generate_response(
            self.state.conversation_history,
            tools=tools
        )
        
        # Process tool calls if present
        if response.get("tool_calls"):
            for tool_call in response["tool_calls"]:
                tool_name = tool_call["name"]
                arguments = tool_call["arguments"]
                
                # Add the tool call to the conversation
                self.add_message("assistant", None, tool_call)
                
                # Execute the tool
                result = self.execute_tool(tool_name, arguments)
                
                # Add the tool result to the conversation
                self.add_message("tool", str(result))
            
            # Get final response from LLM after tool execution
            final_response = self.llm_client.generate_response(
                self.state.conversation_history
            )
            
            # Add assistant's final response to conversation
            self.add_message("assistant", final_response["content"])
            return final_response["content"]
        else:
            # No tool calls, just add the response to conversation
            self.add_message("assistant", response["content"])
            return response["content"]

# ===================== EXAMPLE USAGE =====================

# Define some example tools
def search_web(query: str) -> str:
    """Simulate web search"""
    return f"Results for '{query}': [Simulated web search results]"

def calculate(expression: str) -> str:
    """Calculate mathematical expression"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"

def get_weather(location: str, unit: str = "celsius") -> str:
    """Get weather information for a location"""
    return f"Weather in {location}: 22°{unit}, Partly Cloudy [Simulated]"

# Example usage
if __name__ == "__main__":
    # Create tool registry and register tools
    registry = ToolRegistry()
    registry.register_tool(Tool(
        name="search_web",
        description="Search the web for information",
        function=search_web
    ))
    registry.register_tool(Tool(
        name="calculate",
        description="Calculate mathematical expressions",
        function=calculate
    ))
    registry.register_tool(Tool(
        name="get_weather",
        description="Get weather information for a location",
        function=get_weather
    ))
    
    # Create LLM client
    llm = LLMClient(model="gpt-4")  # or gpt-3.5-turbo, etc.
    
    # Create agent
    agent = Agent(
        name="Assistant",
        system_prompt="You are a helpful assistant with access to tools. Use them when appropriate.",
        llm_client=llm,
        tool_registry=registry
    )
    
    # Run a simple conversation
    print("Agent: Hello! I'm your AI assistant. I can help you with various tasks.")
    print("Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        
        response = agent.process_input(user_input)
        print(f"Agent: {response}")
