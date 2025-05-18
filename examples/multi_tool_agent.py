"""
Example demonstrating multiple tools and custom tools.
"""

# TODO:
# Implement a custom tool and integrate

import logging
import sys
import os
import json
from typing import Dict, Any, Optional

# Add the parent directory to sys.path to allow importing the package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openagents.core.agent import Agent
from openagents.llm.ollama_me import OllamaLLM
from openagents.tools.registry import ToolRegistry
from openagents.tools.general import GeneralTools
from openagents.tools.base import Tool


# Define custom tools
def search_database(query: str, database: str = "main") -> str:
    """Search a database for information
    
    Args:
        query: Search query
        database: Database to search
        
    Returns:
        Search results
    """
    # This is a simulated database search
    databases = {
        "main": {
            "users": ["alice", "bob", "charlie"],
            "products": ["widget", "gadget", "doodad"]
        },
        "archive": {
            "users": ["david", "eve", "frank"],
            "products": ["thingamajig", "whatchamacallit", "doohickey"]
        }
    }
    
    if database not in databases:
        return f"Error: Database '{database}' not found"
    
    db_content = databases[database]
    
    # Simple "search" by checking if query is in any values
    results = {}
    for category, items in db_content.items():
        matches = [item for item in items if query.lower() in item.lower()]
        if matches:
            results[category] = matches
    
    if not results:
        return f"No results found for '{query}' in database '{database}'"
    
    return json.dumps(results, indent=2)


def send_notification(user: str, message: str, priority: str = "normal") -> str:
    """Send a notification to a user
    
    Args:
        user: User to send notification to
        message: Notification message
        priority: Priority level (low, normal, high)
        
    Returns:
        Status message
    """
    valid_priorities = ["low", "normal", "high"]
    if priority.lower() not in valid_priorities:
        return f"Error: Invalid priority '{priority}'. Must be one of {valid_priorities}"
    
    # This is a simulated notification
    return f"Notification sent to {user} with {priority} priority: {message}"


def main():
    """Run a multi-tool example of the OpenAgents framework"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create LLM client
    llm = OllamaLLM(
        model="llama3.2"
    )  # Use a model available in your Ollama installation
    
    # Create tool registry and register tools
    registry = ToolRegistry()
    
    # Register general tools
    registry.register_provider(GeneralTools())
    
    # Register custom tools
    registry.register_tool(Tool(
        name="search_database",
        description="Search a database for information",
        function=search_database
    ))
    
    registry.register_tool(Tool(
        name="send_notification",
        description="Send a notification to a user",
        function=send_notification
    ))
    
    # Create agent with specialized system prompt
    agent = Agent(
        name="DatabaseAssistant",
        system_prompt=(
            "You are a database assistant that helps users interact with databases and send notifications. "
            "Use the search_database tool to look up information. "
            "Use the send_notification tool to send messages to users. "
            "You also have access to general tools like calculator and time functions. "
            "Always use the most appropriate tool for the job."
        ),
        llm=llm,
        tool_registry=registry,
        verbose=True
    )
    
    print(f"\n{agent.name}: Hello! I'm your database assistant. I can help you search databases and send notifications.")
    print("Type 'exit' to end the conversation.\n")
    
    # List available tools
    tools = registry.get_tool_names()
    print(f"Available tools: {', '.join(tools)}\n")
    
    # Main conversation loop
    while True:
        # Get user input
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print(f"\n{agent.name}: Goodbye! Have a great day!")
            break
        
        # Process the input and get a response
        try:
            response = agent.process_input(user_input)
            print(f"\n{agent.name}: {response}\n")
        except Exception as e:
            logging.error(f"Error processing input: {e}")
            print(f"\n{agent.name}: I encountered an error while processing your request. Please try again.\n")


if __name__ == "__main__":
    main()
